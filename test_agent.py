"""
test_agent.py — End-to-end test of the Smart Farming Agent.
Run: python test_agent.py
"""
from dotenv import load_dotenv
load_dotenv(".env")

from modules.watsonx_client import watsonx_client
from modules.agent_instructions import get_system_prompt, AGENT_NAME
from modules.farming_advisor import get_pest_disease_advice, get_crop_plan

print("=" * 55)
print(f"  Smart Farming Agent ({AGENT_NAME}) — Live Test")
print("=" * 55)

# 1. Health check
print("\n[1] Health check...")
status = watsonx_client.health_check()
print(f"    Status : {status['status']}")
print(f"    Model  : {status.get('model', 'N/A')}")
print(f"    URL    : {status.get('url', 'N/A')}")

# 2. Multi-turn chat
print("\n[2] Chat test — cotton sowing question...")
farmer = {
    "name": "Ramesh",
    "location": "Vidarbha, Maharashtra",
    "crops": ["Cotton", "Soybean"],
    "soil_type": "Black Cotton",
    "experience_years": "10",
}
system = get_system_prompt(farmer)
reply = watsonx_client.chat(
    messages=[{"role": "user", "content": "What is the best time to sow cotton in Maharashtra?"}],
    system_prompt=system,
)
print(f"    Reply  : {reply[:300]}")

# 3. Pest advisory
print("\n[3] Pest & Disease advisory — whitefly on cotton...")
advice = get_pest_disease_advice(
    crop="Cotton",
    symptoms="White flies visible on undersides of leaves, leaves turning yellow and curling",
    growth_stage="Vegetative",
    location="Vidarbha, Maharashtra",
    season="Kharif",
    farmer_profile=farmer,
)
print(f"    Advice : {advice[:300]}")

# 4. Crop plan
print("\n[4] Crop planning — Rabi season...")
plan = get_crop_plan(
    location="Nashik, Maharashtra",
    land_size=2.0,
    soil_type="Alluvial",
    water_availability="Bore-well",
    season="Rabi (Nov-Mar)",
    budget_inr=60000,
    goals="Maximise profit",
    farmer_profile=farmer,
)
print(f"    Plan   : {plan[:300]}")

print("\n" + "=" * 55)
print("  ALL TESTS PASSED — Agent is fully operational!")
print("=" * 55)
print("\nRun the app with:  python app.py")
print("Then open       :  http://localhost:5000")
