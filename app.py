"""
app.py — Smart Farming Advice Agent
Flask application entry point with all API routes.
"""

import json
import logging
import os
import sys

from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS

# Ensure project root is on sys.path when running from subdirectory
sys.path.insert(0, os.path.dirname(__file__))

from config import active_config
from modules.agent_instructions import (
    AGENT_NAME,
    EXPERTISE_DOMAINS,
    INDIAN_AGRICULTURE_CONTEXT,
    RESPONSE_FORMAT,
    SAFETY_RULES,
    TONE_GUIDELINES,
    get_system_prompt,
)
from modules.farming_advisor import (
    analyse_soil,
    estimate_costs,
    get_crop_plan,
    get_fertilizer_plan,
    get_government_schemes,
    get_irrigation_schedule,
    get_pest_disease_advice,
    get_sustainable_practices,
    get_weather_advisory,
)
from modules.watsonx_client import watsonx_client

# ------------------------------------------------------------------ #
#  Logging                                                             #
# ------------------------------------------------------------------ #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------ #
#  Flask app                                                           #
# ------------------------------------------------------------------ #
app = Flask(__name__)
app.secret_key = active_config.SECRET_KEY
CORS(app)

# ------------------------------------------------------------------ #
#  In-memory session store (replace with Redis/DB for production)     #
# ------------------------------------------------------------------ #
# farmer_profiles: { session_id -> {name, location, land_size, ...} }
farmer_profiles: dict[str, dict] = {}

# chat_histories:  { session_id -> [ {role, content}, ... ] }
chat_histories: dict[str, list[dict]] = {}

MAX_HISTORY = 20  # max turns kept per session


# ================================================================== #
#  PAGE ROUTES                                                         #
# ================================================================== #

@app.route("/")
def index():
    """Landing / chatbot page."""
    return render_template("index.html", agent_name=AGENT_NAME, app_name=active_config.APP_NAME)


@app.route("/dashboard")
def dashboard():
    """Crop advisory dashboard."""
    return render_template("dashboard.html", agent_name=AGENT_NAME, app_name=active_config.APP_NAME)


@app.route("/profile")
def profile():
    """Farmer profile management page."""
    return render_template("profile.html", agent_name=AGENT_NAME, app_name=active_config.APP_NAME)


@app.route("/agent-settings")
def agent_settings():
    """Editable agent instructions page."""
    return render_template(
        "agent_settings.html",
        agent_name=AGENT_NAME,
        app_name=active_config.APP_NAME,
        persona=_get_section("AGENT_PERSONA"),
        expertise=EXPERTISE_DOMAINS,
        tone=TONE_GUIDELINES,
        indian_context=INDIAN_AGRICULTURE_CONTEXT,
        safety=SAFETY_RULES,
        response_format=RESPONSE_FORMAT,
    )


# ================================================================== #
#  API — Health                                                        #
# ================================================================== #

@app.route("/api/health")
def health():
    """Health-check endpoint."""
    status = watsonx_client.health_check()
    return jsonify(
        {
            "app": active_config.APP_NAME,
            "version": active_config.APP_VERSION,
            "watsonx": status,
        }
    )


# ================================================================== #
#  API — Farmer Profile                                                #
# ================================================================== #

@app.route("/api/profile", methods=["GET"])
def get_profile():
    sid = _get_session_id()
    profile = farmer_profiles.get(sid, {})
    return jsonify({"success": True, "profile": profile})


@app.route("/api/profile", methods=["POST"])
def save_profile():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profiles[sid] = data
    logger.info("Profile saved for session %s", sid)
    return jsonify({"success": True, "message": "Profile saved successfully."})


@app.route("/api/profile", methods=["DELETE"])
def delete_profile():
    sid = _get_session_id()
    farmer_profiles.pop(sid, None)
    chat_histories.pop(sid, None)
    return jsonify({"success": True, "message": "Profile and chat history cleared."})


# ================================================================== #
#  API — Chatbot                                                       #
# ================================================================== #

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Multi-turn chatbot endpoint.
    Body: { "message": str, "reset": bool (optional) }
    """
    sid = _get_session_id()
    data = request.get_json(force=True) or {}

    if data.get("reset"):
        chat_histories[sid] = []
        return jsonify({"success": True, "message": "Conversation reset."})

    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"success": False, "error": "Empty message."}), 400

    history = chat_histories.setdefault(sid, [])
    history.append({"role": "user", "content": user_message})

    # Keep only last MAX_HISTORY messages to stay within token limits
    if len(history) > MAX_HISTORY:
        history[:] = history[-MAX_HISTORY:]

    farmer_profile = farmer_profiles.get(sid)
    system_prompt = get_system_prompt(farmer_profile)

    try:
        reply = watsonx_client.chat(messages=history, system_prompt=system_prompt)
        history.append({"role": "assistant", "content": reply})
        return jsonify({"success": True, "reply": reply, "history_length": len(history)})
    except Exception as exc:
        logger.error("Chat error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


@app.route("/api/chat/history", methods=["GET"])
def chat_history():
    sid = _get_session_id()
    return jsonify({"success": True, "history": chat_histories.get(sid, [])})


# ================================================================== #
#  API — Soil Analysis                                                 #
# ================================================================== #

@app.route("/api/soil/analyse", methods=["POST"])
def soil_analyse():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = analyse_soil(soil_data=data, farmer_profile=farmer_profile)
        return jsonify({"success": True, "analysis": result})
    except Exception as exc:
        logger.error("Soil analysis error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Irrigation                                                    #
# ================================================================== #

@app.route("/api/irrigation/schedule", methods=["POST"])
def irrigation_schedule():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = get_irrigation_schedule(
            crop=data.get("crop", "wheat"),
            growth_stage=data.get("growth_stage", "vegetative"),
            soil_type=data.get("soil_type", "loamy"),
            weather=data.get("weather", "dry"),
            area_hectares=float(data.get("area_hectares", 1)),
            irrigation_method=data.get("irrigation_method", "drip"),
            farmer_profile=farmer_profile,
        )
        return jsonify({"success": True, "schedule": result})
    except Exception as exc:
        logger.error("Irrigation error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Fertilizer                                                    #
# ================================================================== #

@app.route("/api/fertilizer/plan", methods=["POST"])
def fertilizer_plan():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = get_fertilizer_plan(
            crop=data.get("crop", "wheat"),
            area_hectares=float(data.get("area_hectares", 1)),
            soil_data=data.get("soil_data", {}),
            growth_stage=data.get("growth_stage", "sowing"),
            farmer_profile=farmer_profile,
        )
        return jsonify({"success": True, "plan": result})
    except Exception as exc:
        logger.error("Fertilizer error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Pest & Disease                                                #
# ================================================================== #

@app.route("/api/pest/advice", methods=["POST"])
def pest_advice():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = get_pest_disease_advice(
            crop=data.get("crop", "rice"),
            symptoms=data.get("symptoms", "yellowing leaves"),
            growth_stage=data.get("growth_stage", "vegetative"),
            location=data.get("location", "India"),
            season=data.get("season", "Kharif"),
            farmer_profile=farmer_profile,
        )
        return jsonify({"success": True, "advice": result})
    except Exception as exc:
        logger.error("Pest advice error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Weather Advisory                                              #
# ================================================================== #

@app.route("/api/weather/advisory", methods=["POST"])
def weather_advisory():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = get_weather_advisory(
            weather_data=data.get("weather_data", {}),
            crop=data.get("crop", "wheat"),
            growth_stage=data.get("growth_stage", "vegetative"),
            farmer_profile=farmer_profile,
        )
        return jsonify({"success": True, "advisory": result})
    except Exception as exc:
        logger.error("Weather advisory error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Crop Planning                                                 #
# ================================================================== #

@app.route("/api/crop/plan", methods=["POST"])
def crop_plan():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = get_crop_plan(
            location=data.get("location", "India"),
            land_size=float(data.get("land_size", 1)),
            soil_type=data.get("soil_type", "loamy"),
            water_availability=data.get("water_availability", "canal"),
            season=data.get("season", "Kharif"),
            budget_inr=float(data.get("budget_inr", 50000)),
            goals=data.get("goals", "maximize yield"),
            farmer_profile=farmer_profile,
        )
        return jsonify({"success": True, "plan": result})
    except Exception as exc:
        logger.error("Crop plan error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Government Schemes                                            #
# ================================================================== #

@app.route("/api/schemes", methods=["POST"])
def government_schemes():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = get_government_schemes(
            state=data.get("state", "Maharashtra"),
            crop=data.get("crop", "cotton"),
            farmer_category=data.get("farmer_category", "small"),
            land_size=float(data.get("land_size", 1)),
            farmer_profile=farmer_profile,
        )
        return jsonify({"success": True, "schemes": result})
    except Exception as exc:
        logger.error("Schemes error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Cost Estimation                                               #
# ================================================================== #

@app.route("/api/cost/estimate", methods=["POST"])
def cost_estimate():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = estimate_costs(
            crop=data.get("crop", "wheat"),
            area_hectares=float(data.get("area_hectares", 1)),
            input_costs=data.get("input_costs", {}),
            expected_yield_qtl=float(data.get("expected_yield_qtl", 30)),
            msp_or_market_price=float(data.get("msp_or_market_price", 2000)),
            farmer_profile=farmer_profile,
        )
        return jsonify({"success": True, "estimate": result})
    except Exception as exc:
        logger.error("Cost estimate error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Sustainable Practices                                         #
# ================================================================== #

@app.route("/api/sustainable", methods=["POST"])
def sustainable_practices():
    sid = _get_session_id()
    data = request.get_json(force=True) or {}
    farmer_profile = farmer_profiles.get(sid)

    try:
        result = get_sustainable_practices(
            farming_type=data.get("farming_type", "conventional"),
            crop=data.get("crop", "rice"),
            location=data.get("location", "India"),
            challenges=data.get("challenges", "pest pressure, water scarcity"),
            farmer_profile=farmer_profile,
        )
        return jsonify({"success": True, "practices": result})
    except Exception as exc:
        logger.error("Sustainable practices error: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 500


# ================================================================== #
#  API — Agent Settings (read/preview)                                 #
# ================================================================== #

@app.route("/api/agent/settings", methods=["GET"])
def get_agent_settings():
    """Return current agent instruction sections as JSON."""
    from modules.agent_instructions import (
        AGENT_NAME as name,
        AGENT_PERSONA,
    )
    return jsonify(
        {
            "success": True,
            "settings": {
                "agent_name": name,
                "persona": AGENT_PERSONA,
                "expertise_domains": EXPERTISE_DOMAINS,
                "tone_guidelines": TONE_GUIDELINES,
                "indian_context": INDIAN_AGRICULTURE_CONTEXT,
                "safety_rules": SAFETY_RULES,
                "response_format": RESPONSE_FORMAT,
            },
        }
    )


# ================================================================== #
#  Private helpers                                                     #
# ================================================================== #

def _get_session_id() -> str:
    """Return or create a persistent session ID."""
    if "sid" not in session:
        import uuid
        session["sid"] = str(uuid.uuid4())
    return session["sid"]


def _get_section(name: str) -> str:
    """Safely retrieve a module-level string from agent_instructions."""
    import modules.agent_instructions as ai
    return getattr(ai, name, "")


# ================================================================== #
#  Main                                                                #
# ================================================================== #

if __name__ == "__main__":
    logger.info(
        "Starting %s v%s on %s:%s",
        active_config.APP_NAME,
        active_config.APP_VERSION,
        active_config.HOST,
        active_config.PORT,
    )
    app.run(
        host=active_config.HOST,
        port=active_config.PORT,
        debug=active_config.DEBUG,
    )
