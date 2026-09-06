/**
 * dashboard.js — Advisory Dashboard tab logic.
 */

'use strict';

(function () {

  const { apiPost, showLoading, showError, renderResult, showToast } = FarmApp;

  // ---- Soil Analysis -------------------------------------------------
  document.getElementById('analyseSoilBtn').addEventListener('click', async () => {
    const body = {
      ph:             document.getElementById('soilPh').value,
      nitrogen:       document.getElementById('soilN').value,
      phosphorus:     document.getElementById('soilP').value,
      potassium:      document.getElementById('soilK').value,
      organic_matter: document.getElementById('soilOM').value,
      texture:        document.getElementById('soilTexture').value,
      location:       document.getElementById('soilLocation').value,
      current_crop:   document.getElementById('soilCrop').value,
    };
    if (!body.ph && !body.nitrogen) {
      showToast('Please enter at least pH and Nitrogen values.', 'warning'); return;
    }
    showLoading('soilResult');
    try {
      const data = await apiPost('/api/soil/analyse', body);
      if (data.success) renderResult('soilResult', data.analysis);
      else showError('soilResult', data.error);
    } catch (e) { showError('soilResult', e.message); }
  });

  // ---- Irrigation Schedule -------------------------------------------
  document.getElementById('getIrrigationBtn').addEventListener('click', async () => {
    const body = {
      crop:             document.getElementById('irrCrop').value || 'wheat',
      growth_stage:     document.getElementById('irrStage').value,
      soil_type:        document.getElementById('irrSoil').value,
      weather:          document.getElementById('irrWeather').value,
      area_hectares:    parseFloat(document.getElementById('irrArea').value) || 1,
      irrigation_method: document.getElementById('irrMethod').value,
    };
    showLoading('irrigationResult');
    try {
      const data = await apiPost('/api/irrigation/schedule', body);
      if (data.success) renderResult('irrigationResult', data.schedule);
      else showError('irrigationResult', data.error);
    } catch (e) { showError('irrigationResult', e.message); }
  });

  // ---- Fertilizer Plan -----------------------------------------------
  document.getElementById('getFertilizerBtn').addEventListener('click', async () => {
    const body = {
      crop:          document.getElementById('fertCrop').value || 'wheat',
      area_hectares: parseFloat(document.getElementById('fertArea').value) || 1,
      growth_stage:  document.getElementById('fertStage').value,
      soil_data: {
        nitrogen:   document.getElementById('fertN').value,
        phosphorus: document.getElementById('fertP').value,
        potassium:  document.getElementById('fertK').value,
      },
    };
    showLoading('fertilizerResult');
    try {
      const data = await apiPost('/api/fertilizer/plan', body);
      if (data.success) renderResult('fertilizerResult', data.plan);
      else showError('fertilizerResult', data.error);
    } catch (e) { showError('fertilizerResult', e.message); }
  });

  // ---- Pest & Disease ------------------------------------------------
  document.getElementById('getPestAdviceBtn').addEventListener('click', async () => {
    const symptoms = document.getElementById('pestSymptoms').value.trim();
    if (!symptoms) { showToast('Please describe the symptoms you observed.', 'warning'); return; }
    const body = {
      crop:         document.getElementById('pestCrop').value || 'rice',
      growth_stage: document.getElementById('pestStage').value,
      season:       document.getElementById('pestSeason').value,
      location:     document.getElementById('pestLocation').value || 'India',
      symptoms,
    };
    showLoading('pestResult');
    try {
      const data = await apiPost('/api/pest/advice', body);
      if (data.success) renderResult('pestResult', data.advice);
      else showError('pestResult', data.error);
    } catch (e) { showError('pestResult', e.message); }
  });

  // ---- Weather Advisory ----------------------------------------------
  document.getElementById('getWeatherAdvBtn').addEventListener('click', async () => {
    const body = {
      crop:         document.getElementById('wxCrop').value || 'wheat',
      growth_stage: document.getElementById('wxStage').value,
      weather_data: {
        condition:         document.getElementById('wxCondition').value,
        temp_max:          document.getElementById('wxTempMax').value,
        temp_min:          document.getElementById('wxTempMin').value,
        humidity:          document.getElementById('wxHumidity').value,
        rainfall_forecast: document.getElementById('wxRainfall').value,
        wind_speed:        document.getElementById('wxWind').value,
      },
    };
    showLoading('weatherResult');
    try {
      const data = await apiPost('/api/weather/advisory', body);
      if (data.success) renderResult('weatherResult', data.advisory);
      else showError('weatherResult', data.error);
    } catch (e) { showError('weatherResult', e.message); }
  });

  // ---- Crop Plan -----------------------------------------------------
  document.getElementById('getCropPlanBtn').addEventListener('click', async () => {
    const body = {
      location:          document.getElementById('cpLocation').value || 'India',
      land_size:         parseFloat(document.getElementById('cpLand').value) || 1,
      soil_type:         document.getElementById('cpSoil').value,
      water_availability: document.getElementById('cpWater').value,
      season:            document.getElementById('cpSeason').value,
      budget_inr:        parseFloat(document.getElementById('cpBudget').value) || 50000,
      goals:             document.getElementById('cpGoals').value,
    };
    showLoading('cropPlanResult');
    try {
      const data = await apiPost('/api/crop/plan', body);
      if (data.success) renderResult('cropPlanResult', data.plan);
      else showError('cropPlanResult', data.error);
    } catch (e) { showError('cropPlanResult', e.message); }
  });

  // ---- Government Schemes --------------------------------------------
  document.getElementById('getSchemesBtn').addEventListener('click', async () => {
    const catVal = document.getElementById('schCategory').value;
    const category = catVal.split(' ')[0].toLowerCase(); // marginal / small / etc.
    const body = {
      state:            document.getElementById('schState').value,
      crop:             document.getElementById('schCrop').value || 'rice',
      farmer_category:  category,
      land_size:        parseFloat(document.getElementById('schLand').value) || 1,
    };
    showLoading('schemesResult');
    try {
      const data = await apiPost('/api/schemes', body);
      if (data.success) renderResult('schemesResult', data.schemes);
      else showError('schemesResult', data.error);
    } catch (e) { showError('schemesResult', e.message); }
  });

  // ---- Cost Estimation -----------------------------------------------
  document.getElementById('getCostEstBtn').addEventListener('click', async () => {
    const body = {
      crop:                 document.getElementById('costCrop').value || 'wheat',
      area_hectares:        parseFloat(document.getElementById('costArea').value) || 1,
      expected_yield_qtl:   parseFloat(document.getElementById('costYield').value) || 30,
      msp_or_market_price:  parseFloat(document.getElementById('costPrice').value) || 2000,
      input_costs: {
        seeds:      parseFloat(document.getElementById('costSeeds').value) || 0,
        fertilizers: parseFloat(document.getElementById('costFert').value) || 0,
        pesticides:  parseFloat(document.getElementById('costPest').value) || 0,
        labour:      parseFloat(document.getElementById('costLabour').value) || 0,
        irrigation:  parseFloat(document.getElementById('costIrrigation').value) || 0,
        machinery:   parseFloat(document.getElementById('costMachinery').value) || 0,
        other:       parseFloat(document.getElementById('costOther').value) || 0,
      },
    };
    showLoading('costResult');
    try {
      const data = await apiPost('/api/cost/estimate', body);
      if (data.success) renderResult('costResult', data.estimate);
      else showError('costResult', data.error);
    } catch (e) { showError('costResult', e.message); }
  });

  // ---- Sustainable Practices -----------------------------------------
  document.getElementById('getSustainBtn').addEventListener('click', async () => {
    const body = {
      farming_type: document.getElementById('sustFarmType').value,
      crop:         document.getElementById('sustCrop').value || 'rice',
      location:     document.getElementById('sustLocation').value || 'India',
      challenges:   document.getElementById('sustChallenges').value || 'high input costs',
    };
    showLoading('sustainResult');
    try {
      const data = await apiPost('/api/sustainable', body);
      if (data.success) renderResult('sustainResult', data.practices);
      else showError('sustainResult', data.error);
    } catch (e) { showError('sustainResult', e.message); }
  });

})();
