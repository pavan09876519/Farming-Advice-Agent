"""
modules/farming_advisor.py

Domain-specific helper that composes structured prompts for different
farming advisory features (soil analysis, irrigation, fertilizer, pest
management, weather, crop planning, government schemes, cost estimation).

Each public function returns a plain-English AI response string by
delegating to the WatsonxClient.
"""

from __future__ import annotations

import logging
from modules.watsonx_client import watsonx_client
from modules.agent_instructions import get_system_prompt

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
#  Internal helper                                                     #
# ------------------------------------------------------------------ #

def _ask(prompt: str, farmer_profile: dict | None = None) -> str:
    """Send a single prompt to the model with appropriate system context."""
    system = get_system_prompt(farmer_profile)
    try:
        return watsonx_client.generate(prompt=prompt, system_prompt=system)
    except Exception as exc:
        logger.error("FarmingAdvisor error: %s", exc)
        return f"⚠️ Advisory service temporarily unavailable. Error: {exc}"


# ------------------------------------------------------------------ #
#  Soil Analysis                                                       #
# ------------------------------------------------------------------ #

def analyse_soil(soil_data: dict, farmer_profile: dict | None = None) -> str:
    """
    Generate soil health analysis and improvement recommendations.

    soil_data keys: ph, nitrogen, phosphorus, potassium, organic_matter,
                    texture, location, current_crop
    """
    ph = soil_data.get("ph", "unknown")
    n = soil_data.get("nitrogen", "unknown")
    p = soil_data.get("phosphorus", "unknown")
    k = soil_data.get("potassium", "unknown")
    om = soil_data.get("organic_matter", "unknown")
    texture = soil_data.get("texture", "unknown")
    location = soil_data.get("location", "India")
    crop = soil_data.get("current_crop", "not specified")

    prompt = f"""
A farmer in {location} has shared the following soil test results for their
field currently growing / planning to grow: {crop}.

Soil Test Report:
- pH: {ph}
- Nitrogen (N): {n} kg/ha
- Phosphorus (P): {p} kg/ha
- Potassium (K): {k} kg/ha
- Organic Matter: {om}%
- Soil Texture: {texture}

Please provide:
1. Soil health assessment (what's good, what needs improvement)
2. pH correction recommendations (if needed)
3. Nutrient deficiency / toxicity analysis
4. Organic matter improvement suggestions
5. Recommended amendments with quantities and timing
6. Long-term soil health improvement plan
"""
    return _ask(prompt, farmer_profile)


# ------------------------------------------------------------------ #
#  Irrigation Recommendations                                          #
# ------------------------------------------------------------------ #

def get_irrigation_schedule(
    crop: str,
    growth_stage: str,
    soil_type: str,
    weather: str,
    area_hectares: float,
    irrigation_method: str,
    farmer_profile: dict | None = None,
) -> str:
    """Generate a week-wise irrigation schedule."""
    prompt = f"""
Create a detailed irrigation schedule for the following farm:

Crop: {crop}
Growth Stage: {growth_stage}
Soil Type: {soil_type}
Current Weather Conditions: {weather}
Farm Area: {area_hectares} hectares
Irrigation Method: {irrigation_method}

Please provide:
1. Weekly irrigation schedule (days and frequency)
2. Water quantity per irrigation (litres/hectare or hours for drip/sprinkler)
3. Critical irrigation stages (when water stress is most harmful)
4. Signs of over/under-watering to watch for
5. Water conservation tips specific to this setup
6. Estimated total water requirement for the season
"""
    return _ask(prompt, farmer_profile)


# ------------------------------------------------------------------ #
#  Fertilizer Plan                                                     #
# ------------------------------------------------------------------ #

def get_fertilizer_plan(
    crop: str,
    area_hectares: float,
    soil_data: dict,
    growth_stage: str,
    farmer_profile: dict | None = None,
) -> str:
    """Generate a complete fertilizer application schedule."""
    ph = soil_data.get("ph", "unknown")
    n = soil_data.get("nitrogen", "moderate")
    p = soil_data.get("phosphorus", "moderate")
    k = soil_data.get("potassium", "moderate")

    prompt = f"""
Prepare a complete fertilizer management plan for:

Crop: {crop}
Farm Area: {area_hectares} hectares
Current Growth Stage: {growth_stage}
Soil pH: {ph}
Soil Nitrogen Level: {n}
Soil Phosphorus Level: {p}
Soil Potassium Level: {k}

Please provide:
1. Basal dose recommendations (at sowing/planting)
2. Top-dressing schedule (splits, timing, quantities)
3. Both chemical fertilizer options (DAP, Urea, MOP etc.) AND
   organic alternatives (FYM, vermicompost, biofertilizers)
4. Micronutrient requirements (Zinc, Boron, etc.)
5. Foliar spray schedule if beneficial
6. Total input cost estimate (₹)
7. Tips to maximise fertilizer use efficiency
"""
    return _ask(prompt, farmer_profile)


# ------------------------------------------------------------------ #
#  Pest & Disease Management                                           #
# ------------------------------------------------------------------ #

def get_pest_disease_advice(
    crop: str,
    symptoms: str,
    growth_stage: str,
    location: str,
    season: str,
    farmer_profile: dict | None = None,
) -> str:
    """Diagnose pest/disease issues and recommend IPM solutions."""
    prompt = f"""
A farmer needs help diagnosing and managing a crop health issue:

Crop: {crop}
Location: {location}
Season: {season}
Growth Stage: {growth_stage}
Observed Symptoms: {symptoms}

Please provide:
1. Likely pest(s) or disease(s) based on the symptoms
2. Confirmation tips (how to verify the diagnosis)
3. Integrated Pest Management (IPM) approach:
   a. Cultural control methods
   b. Biological control options
   c. Chemical control (CIB&RC approved products only, with dosage and PHI)
4. Preventive measures for the rest of the season
5. Economic threshold level (ETL) guidance
6. When to escalate to a local agriculture officer or KVK
"""
    return _ask(prompt, farmer_profile)


# ------------------------------------------------------------------ #
#  Weather-Based Advisory                                              #
# ------------------------------------------------------------------ #

def get_weather_advisory(
    weather_data: dict,
    crop: str,
    growth_stage: str,
    farmer_profile: dict | None = None,
) -> str:
    """Generate weather-based farming advice."""
    temp_max = weather_data.get("temp_max", "N/A")
    temp_min = weather_data.get("temp_min", "N/A")
    humidity = weather_data.get("humidity", "N/A")
    rainfall_forecast = weather_data.get("rainfall_forecast", "N/A")
    wind_speed = weather_data.get("wind_speed", "N/A")
    condition = weather_data.get("condition", "N/A")

    prompt = f"""
Based on the following weather forecast, advise the farmer on necessary
actions to protect their crop and optimise farm operations.

Crop: {crop}
Growth Stage: {growth_stage}
Weather Forecast:
- Condition: {condition}
- Max Temperature: {temp_max}°C
- Min Temperature: {temp_min}°C
- Humidity: {humidity}%
- Rainfall Forecast: {rainfall_forecast} mm
- Wind Speed: {wind_speed} km/h

Please provide:
1. Weather impact assessment on the crop at this growth stage
2. Immediate actions required (next 24-48 hours)
3. Irrigation adjustment based on rainfall forecast
4. Pest/disease risk assessment given this weather
5. Field operation recommendations (spraying, harvesting, etc.)
6. Any crop protection measures needed (frost, heat stress, lodging)
"""
    return _ask(prompt, farmer_profile)


# ------------------------------------------------------------------ #
#  Crop Planning                                                       #
# ------------------------------------------------------------------ #

def get_crop_plan(
    location: str,
    land_size: float,
    soil_type: str,
    water_availability: str,
    season: str,
    budget_inr: float,
    goals: str,
    farmer_profile: dict | None = None,
) -> str:
    """Generate a seasonal crop plan."""
    prompt = f"""
Help this farmer plan their cropping strategy for the upcoming season.

Location: {location}
Land Available: {land_size} hectares
Soil Type: {soil_type}
Water Availability: {water_availability}
Season: {season}
Budget: ₹{budget_inr:,.0f}
Farmer's Goals: {goals}

Please provide:
1. Top 3-5 recommended crops with reasons (matching conditions and goals)
2. Crop diversification strategy to reduce risk
3. Estimated input costs per crop (₹/hectare)
4. Expected yield range and market value
5. Month-wise activity calendar for the season
6. Government schemes or subsidies applicable
7. Market linkage suggestions (nearest APMC, e-NAM, FPO)
"""
    return _ask(prompt, farmer_profile)


# ------------------------------------------------------------------ #
#  Government Schemes                                                  #
# ------------------------------------------------------------------ #

def get_government_schemes(
    state: str,
    crop: str,
    farmer_category: str,
    land_size: float,
    farmer_profile: dict | None = None,
) -> str:
    """Fetch relevant government scheme information."""
    prompt = f"""
Provide comprehensive information about government agricultural schemes
available to this farmer:

State: {state}
Primary Crop: {crop}
Farmer Category: {farmer_category} (e.g., small/marginal/large)
Land Holding: {land_size} hectares

Please provide:
1. Central Government schemes applicable (PM-KISAN, PMFBY, soil health card, etc.)
2. State-specific schemes for {state}
3. Eligibility criteria for each scheme
4. Benefits and subsidy amounts
5. Application process and required documents
6. Important deadlines or registration windows
7. Contact information (helpline numbers, portals)
8. How to access Kisan Credit Card (KCC)
"""
    return _ask(prompt, farmer_profile)


# ------------------------------------------------------------------ #
#  Cost & Profit Estimation                                            #
# ------------------------------------------------------------------ #

def estimate_costs(
    crop: str,
    area_hectares: float,
    input_costs: dict,
    expected_yield_qtl: float,
    msp_or_market_price: float,
    farmer_profile: dict | None = None,
) -> str:
    """Calculate crop economics and profitability."""
    seeds = input_costs.get("seeds", 0)
    fertilizers = input_costs.get("fertilizers", 0)
    pesticides = input_costs.get("pesticides", 0)
    labour = input_costs.get("labour", 0)
    irrigation = input_costs.get("irrigation", 0)
    machinery = input_costs.get("machinery", 0)
    other = input_costs.get("other", 0)

    total_input = seeds + fertilizers + pesticides + labour + irrigation + machinery + other

    prompt = f"""
Perform a complete cost-benefit analysis for this crop:

Crop: {crop}
Area: {area_hectares} hectares
Expected Yield: {expected_yield_qtl} quintals
Market/MSP Price: ₹{msp_or_market_price}/quintal

Input Costs (₹):
- Seeds: ₹{seeds:,.0f}
- Fertilizers: ₹{fertilizers:,.0f}
- Pesticides: ₹{pesticides:,.0f}
- Labour: ₹{labour:,.0f}
- Irrigation: ₹{irrigation:,.0f}
- Machinery/Equipment: ₹{machinery:,.0f}
- Other: ₹{other:,.0f}
- TOTAL INPUT COST: ₹{total_input:,.0f}

Please provide:
1. Gross revenue calculation
2. Net profit/loss analysis
3. Cost per quintal and per hectare
4. Break-even yield calculation
5. Suggestions to reduce input costs without compromising yield
6. Risk factors that could affect profitability
7. Comparison with crop alternatives (briefly)
"""
    return _ask(prompt, farmer_profile)


# ------------------------------------------------------------------ #
#  Sustainable Farming Practices                                       #
# ------------------------------------------------------------------ #

def get_sustainable_practices(
    farming_type: str,
    crop: str,
    location: str,
    challenges: str,
    farmer_profile: dict | None = None,
) -> str:
    """Recommend sustainable and organic farming practices."""
    prompt = f"""
Recommend sustainable farming practices for this farmer:

Current Farming Type: {farming_type}
Primary Crop: {crop}
Location: {location}
Current Challenges: {challenges}

Please provide:
1. Transition plan toward sustainable/organic practices
2. Soil health improvement techniques (crop rotation, cover crops, green manure)
3. Water conservation methods
4. Natural pest management strategies
5. Carbon footprint reduction tips
6. Organic certification pathway (if interested)
7. Economic benefits of sustainable farming
8. Local success stories or reference models
"""
    return _ask(prompt, farmer_profile)
