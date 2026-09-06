/**
 * profile.js — Farmer Profile page logic.
 */

'use strict';

(function () {

  const { apiPost, showToast } = FarmApp;

  // ---- Farm plots -------------------------------------------------------
  let plotCount = 0;

  document.getElementById('addPlotBtn').addEventListener('click', () => {
    plotCount++;
    const container = document.getElementById('farmPlots');
    const div = document.createElement('div');
    div.className = 'plot-card';
    div.dataset.plotId = plotCount;
    div.innerHTML = `
      <div class="d-flex justify-content-between align-items-center mb-2">
        <strong class="small text-success">Plot ${plotCount}</strong>
        <button type="button" class="btn btn-outline-danger btn-sm btn-remove"
          onclick="removePlot(${plotCount})">
          <i class="bi bi-trash"></i>
        </button>
      </div>
      <div class="row g-2">
        <div class="col-md-4">
          <label class="form-label small">Plot Name</label>
          <input type="text" class="form-control form-control-sm plot-name" placeholder="e.g. North Field" />
        </div>
        <div class="col-md-4">
          <label class="form-label small">Area (hectares)</label>
          <input type="number" class="form-control form-control-sm plot-area" step="0.1" placeholder="e.g. 1.5" />
        </div>
        <div class="col-md-4">
          <label class="form-label small">Crop</label>
          <input type="text" class="form-control form-control-sm plot-crop" placeholder="e.g. Cotton" />
        </div>
        <div class="col-md-4">
          <label class="form-label small">Soil Type</label>
          <input type="text" class="form-control form-control-sm plot-soil" placeholder="e.g. Black Cotton" />
        </div>
        <div class="col-md-4">
          <label class="form-label small">Irrigation</label>
          <select class="form-select form-select-sm plot-irrigation">
            <option>Drip</option><option>Sprinkler</option>
            <option>Canal</option><option>Bore-well</option>
            <option>Rain-fed</option>
          </select>
        </div>
        <div class="col-md-4">
          <label class="form-label small">Survey / Khasra No.</label>
          <input type="text" class="form-control form-control-sm plot-survey" placeholder="Optional" />
        </div>
      </div>`;
    container.appendChild(div);
  });

  window.removePlot = function (id) {
    document.querySelector(`[data-plot-id="${id}"]`)?.remove();
  };

  // ---- Family members ---------------------------------------------------
  let memberCount = 0;

  document.getElementById('addMemberBtn').addEventListener('click', () => {
    memberCount++;
    const container = document.getElementById('familyMembers');
    const div = document.createElement('div');
    div.className = 'member-card';
    div.dataset.memberId = memberCount;
    div.innerHTML = `
      <div class="d-flex justify-content-between align-items-center mb-2">
        <strong class="small text-success">Member ${memberCount}</strong>
        <button type="button" class="btn btn-outline-danger btn-sm"
          onclick="removeMember(${memberCount})">
          <i class="bi bi-trash"></i>
        </button>
      </div>
      <div class="row g-2">
        <div class="col-md-4">
          <label class="form-label small">Name</label>
          <input type="text" class="form-control form-control-sm member-name" placeholder="e.g. Sunita Patil" />
        </div>
        <div class="col-md-4">
          <label class="form-label small">Relation</label>
          <select class="form-select form-select-sm member-relation">
            <option>Spouse</option><option>Son</option><option>Daughter</option>
            <option>Father</option><option>Mother</option><option>Brother</option>
            <option>Sister</option><option>Farm Worker</option><option>Other</option>
          </select>
        </div>
        <div class="col-md-4">
          <label class="form-label small">Role on Farm</label>
          <input type="text" class="form-control form-control-sm member-role" placeholder="e.g. Irrigation" />
        </div>
      </div>`;
    container.appendChild(div);
  });

  window.removeMember = function (id) {
    document.querySelector(`[data-member-id="${id}"]`)?.remove();
  };

  // ---- Collect profile data from form -----------------------------------
  function collectProfile() {
    const cropsRaw = document.getElementById('pCrops').value;
    const crops = cropsRaw
      ? cropsRaw.split(',').map(c => c.trim()).filter(Boolean)
      : [];

    // Collect plots
    const plots = [];
    document.querySelectorAll('#farmPlots .plot-card').forEach(card => {
      plots.push({
        name:       card.querySelector('.plot-name').value,
        area:       card.querySelector('.plot-area').value,
        crop:       card.querySelector('.plot-crop').value,
        soil_type:  card.querySelector('.plot-soil').value,
        irrigation: card.querySelector('.plot-irrigation').value,
        survey_no:  card.querySelector('.plot-survey').value,
      });
    });

    // Collect family members
    const family = [];
    document.querySelectorAll('#familyMembers .member-card').forEach(card => {
      family.push({
        name:     card.querySelector('.member-name').value,
        relation: card.querySelector('.member-relation').value,
        role:     card.querySelector('.member-role').value,
      });
    });

    return {
      name:           document.getElementById('pName').value.trim(),
      phone:          document.getElementById('pPhone').value.trim(),
      village:        document.getElementById('pVillage').value.trim(),
      district:       document.getElementById('pDistrict').value.trim(),
      state:          document.getElementById('pState').value,
      location:       [
        document.getElementById('pDistrict').value.trim(),
        document.getElementById('pState').value,
      ].filter(Boolean).join(', '),
      experience_years: document.getElementById('pExperience').value,
      language:       document.getElementById('pLanguage').value,
      farmer_category: document.getElementById('pCategory').value,
      land_size:      document.getElementById('pLandSize').value,
      soil_type:      document.getElementById('pSoilType').value,
      irrigation_type: document.getElementById('pIrrigationType').value,
      farming_type:   document.getElementById('pFarmingType').value,
      crops,
      farm_plots:     plots,
      family_members: family,
      goal:           document.getElementById('pGoal').value,
      budget:         document.getElementById('pBudget').value,
      notes:          document.getElementById('pNotes').value.trim(),
    };
  }

  // ---- Populate form from saved data ------------------------------------
  function populateForm(p) {
    if (!p || !Object.keys(p).length) return;

    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el && val !== undefined && val !== null) el.value = val;
    };

    set('pName', p.name);
    set('pPhone', p.phone);
    set('pVillage', p.village);
    set('pDistrict', p.district);
    set('pState', p.state);
    set('pExperience', p.experience_years);
    set('pLanguage', p.language);
    set('pCategory', p.farmer_category);
    set('pLandSize', p.land_size);
    set('pSoilType', p.soil_type);
    set('pIrrigationType', p.irrigation_type);
    set('pFarmingType', p.farming_type);
    set('pCrops', (p.crops || []).join(', '));
    set('pGoal', p.goal);
    set('pBudget', p.budget);
    set('pNotes', p.notes);

    // Plots
    (p.farm_plots || []).forEach(() => {
      document.getElementById('addPlotBtn').click();
    });
    document.querySelectorAll('#farmPlots .plot-card').forEach((card, i) => {
      const plot = p.farm_plots[i];
      if (!plot) return;
      card.querySelector('.plot-name').value      = plot.name || '';
      card.querySelector('.plot-area').value      = plot.area || '';
      card.querySelector('.plot-crop').value      = plot.crop || '';
      card.querySelector('.plot-soil').value      = plot.soil_type || '';
      card.querySelector('.plot-irrigation').value = plot.irrigation || '';
      card.querySelector('.plot-survey').value    = plot.survey_no || '';
    });

    // Members
    (p.family_members || []).forEach(() => {
      document.getElementById('addMemberBtn').click();
    });
    document.querySelectorAll('#familyMembers .member-card').forEach((card, i) => {
      const m = p.family_members[i];
      if (!m) return;
      card.querySelector('.member-name').value     = m.name || '';
      card.querySelector('.member-relation').value = m.relation || '';
      card.querySelector('.member-role').value     = m.role || '';
    });

    updateSummary(p);
  }

  // ---- Profile summary card ---------------------------------------------
  function updateSummary(p) {
    const el = document.getElementById('profileSummary');
    if (!p || !p.name) {
      el.innerHTML = '<p class="text-muted small">No profile saved yet.</p>';
      return;
    }
    el.innerHTML = `
      <div class="d-flex align-items-center gap-3 mb-3">
        <div class="avatar-circle bg-success text-white" style="width:52px;height:52px;font-size:1.4rem;">
          <i class="bi bi-person-fill"></i>
        </div>
        <div>
          <div class="fw-bold fs-6">${p.name || '—'}</div>
          <div class="text-muted small">${p.location || p.state || '—'}</div>
          <div class="small">${p.farmer_category || ''}</div>
        </div>
      </div>
      <table class="table table-sm table-borderless mb-0 small">
        <tr><td class="text-muted">Land Size</td><td class="fw-semibold">${p.land_size || '—'} ha</td></tr>
        <tr><td class="text-muted">Soil Type</td><td class="fw-semibold">${p.soil_type || '—'}</td></tr>
        <tr><td class="text-muted">Irrigation</td><td class="fw-semibold">${p.irrigation_type || '—'}</td></tr>
        <tr><td class="text-muted">Farming Type</td><td class="fw-semibold">${p.farming_type || '—'}</td></tr>
        <tr><td class="text-muted">Experience</td><td class="fw-semibold">${p.experience_years || '—'} years</td></tr>
        <tr><td class="text-muted">Crops</td><td class="fw-semibold">${(p.crops || []).join(', ') || '—'}</td></tr>
        <tr><td class="text-muted">Farm Plots</td><td class="fw-semibold">${(p.farm_plots || []).length}</td></tr>
        <tr><td class="text-muted">Family / Team</td><td class="fw-semibold">${(p.family_members || []).length} member(s)</td></tr>
        <tr><td class="text-muted">Goal</td><td class="fw-semibold">${p.goal || '—'}</td></tr>
      </table>
      <div class="mt-2">
        <a href="/" class="btn btn-success btn-sm w-100">
          <i class="bi bi-chat-dots me-1"></i> Get Personalised Advice
        </a>
      </div>`;
  }

  // ---- Save profile -----------------------------------------------------
  async function saveProfile() {
    const profile = collectProfile();
    if (!profile.name) {
      showToast('Please enter your name.', 'warning'); return;
    }
    try {
      const data = await apiPost('/api/profile', profile);
      if (data.success) {
        showToast('Profile saved! Advice is now personalised.', 'success');
        updateSummary(profile);
        document.getElementById('profileAlert').className =
          'alert alert-success d-flex align-items-center gap-2';
        document.getElementById('profileAlert').innerHTML =
          '<i class="bi bi-check-circle-fill"></i> Profile saved successfully!';
        setTimeout(() => {
          document.getElementById('profileAlert').className = 'd-none';
        }, 3000);
      } else {
        showToast('Failed to save: ' + data.error, 'danger');
      }
    } catch (e) {
      showToast('Error: ' + e.message, 'danger');
    }
  }

  document.getElementById('saveProfileBtn').addEventListener('click', saveProfile);
  document.getElementById('saveProfileBtn2').addEventListener('click', saveProfile);

  // ---- Clear profile ----------------------------------------------------
  document.getElementById('clearProfileBtn').addEventListener('click', async () => {
    if (!confirm('Clear all profile data and chat history?')) return;
    try {
      const res = await fetch('/api/profile', { method: 'DELETE' });
      const data = await res.json();
      if (data.success) {
        showToast('Profile cleared.', 'info');
        document.querySelectorAll('#farmPlots .plot-card').forEach(c => c.remove());
        document.querySelectorAll('#familyMembers .member-card').forEach(c => c.remove());
        document.getElementById('profileSummary').innerHTML =
          '<p class="text-muted small">No profile saved yet.</p>';
        // Clear text inputs
        document.querySelectorAll('#pName,#pPhone,#pVillage,#pDistrict,#pLandSize,#pCrops,#pBudget,#pNotes,#pExperience')
          .forEach(el => { el.value = ''; });
      }
    } catch (e) {
      showToast('Error: ' + e.message, 'danger');
    }
  });

  // ---- Load existing profile on page load --------------------------------
  (async function loadProfile() {
    try {
      const res = await fetch('/api/profile');
      const data = await res.json();
      if (data.success && data.profile && Object.keys(data.profile).length > 0) {
        populateForm(data.profile);
      }
    } catch (_) {
      // Non-critical
    }
  })();

})();
