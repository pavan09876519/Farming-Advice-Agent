/**
 * main.js — Shared utilities for Smart Farming Advice Agent
 */

'use strict';

// ---- Toast notifications -----------------------------------------------

function showToast(message, type = 'success') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
  }

  const toastEl = document.createElement('div');
  const iconMap = {
    success: 'bi-check-circle-fill text-success',
    danger:  'bi-exclamation-circle-fill text-danger',
    warning: 'bi-exclamation-triangle-fill text-warning',
    info:    'bi-info-circle-fill text-info',
  };
  const icon = iconMap[type] || iconMap.info;

  toastEl.className = `toast align-items-center border-0 bg-white shadow`;
  toastEl.setAttribute('role', 'alert');
  toastEl.setAttribute('aria-live', 'assertive');
  toastEl.innerHTML = `
    <div class="d-flex align-items-center gap-2 p-3">
      <i class="bi ${icon} fs-5"></i>
      <div class="me-auto small">${message}</div>
      <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
    </div>`;

  container.appendChild(toastEl);
  const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
  toast.show();
  toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

// ---- Markdown renderer -------------------------------------------------

function renderMarkdown(text) {
  if (typeof marked !== 'undefined') {
    return marked.parse(text);
  }
  // Fallback: simple paragraph wrapping
  return '<p>' + text.replace(/\n\n+/g, '</p><p>').replace(/\n/g, '<br>') + '</p>';
}

// ---- Loading spinner helper for result panels --------------------------

function showLoading(panelId) {
  const el = document.getElementById(panelId);
  if (el) {
    el.innerHTML = `
      <div class="panel-loading">
        <div class="spinner-border text-success" role="status"></div>
        <span class="text-muted small">Consulting KisanMitra AI…</span>
      </div>`;
  }
}

function showError(panelId, message) {
  const el = document.getElementById(panelId);
  if (el) {
    el.innerHTML = `
      <div class="alert alert-danger d-flex gap-2 align-items-start mb-0">
        <i class="bi bi-exclamation-triangle-fill flex-shrink-0 mt-1"></i>
        <div><strong>Error:</strong> ${message}</div>
      </div>`;
  }
}

function renderResult(panelId, text) {
  const el = document.getElementById(panelId);
  if (el) el.innerHTML = renderMarkdown(text);
}

// ---- Generic API POST helper -------------------------------------------

async function apiPost(endpoint, body) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ error: response.statusText }));
    throw new Error(err.error || `HTTP ${response.status}`);
  }
  return response.json();
}

// ---- Export to window scope (simple module pattern) --------------------

window.FarmApp = {
  showToast,
  renderMarkdown,
  showLoading,
  showError,
  renderResult,
  apiPost,
};
