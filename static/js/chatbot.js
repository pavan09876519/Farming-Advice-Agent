/**
 * chatbot.js — Chatbot UI logic for the index (chat) page.
 */

'use strict';

(function () {

  const chatMessages   = document.getElementById('chatMessages');
  const chatForm       = document.getElementById('chatForm');
  const chatInput      = document.getElementById('chatInput');
  const sendBtn        = document.getElementById('sendBtn');
  const resetChatBtn   = document.getElementById('resetChatBtn');
  const voiceBtn       = document.getElementById('voiceBtn');
  const typingIndicator = document.getElementById('typingIndicator');
  const statusText     = document.getElementById('statusText');
  const charCount      = document.getElementById('charCount');
  const MAX_CHARS      = 2000;

  // ---- Character counter -------------------------------------------------
  chatInput.addEventListener('input', () => {
    const len = chatInput.value.length;
    charCount.textContent = `${len} / ${MAX_CHARS}`;
    if (len > MAX_CHARS) {
      charCount.classList.add('text-danger');
    } else {
      charCount.classList.remove('text-danger');
    }
  });

  // ---- Enter to send (Shift+Enter = newline) ------------------------------
  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (chatInput.value.trim()) chatForm.requestSubmit();
    }
  });

  // ---- Submit handler ----------------------------------------------------
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message || message.length > MAX_CHARS) return;

    appendUserMessage(message);
    chatInput.value = '';
    charCount.textContent = `0 / ${MAX_CHARS}`;
    setThinking(true);

    try {
      const data = await FarmApp.apiPost('/api/chat', { message });
      setThinking(false);
      if (data.success) {
        appendBotMessage(data.reply);
      } else {
        appendErrorMessage(data.error || 'An error occurred. Please try again.');
      }
    } catch (err) {
      setThinking(false);
      appendErrorMessage(err.message || 'Network error. Check your connection.');
    }
  });

  // ---- Reset chat --------------------------------------------------------
  resetChatBtn.addEventListener('click', async () => {
    if (!confirm('Clear this conversation?')) return;
    try {
      await FarmApp.apiPost('/api/chat', { reset: true });
      chatMessages.innerHTML = '';
      appendBotMessage(
        '**Conversation cleared.** 🌱 How can I help you with your farm today?'
      );
      FarmApp.showToast('Conversation cleared.', 'info');
    } catch (err) {
      FarmApp.showToast('Failed to reset: ' + err.message, 'danger');
    }
  });

  // ---- Quick prompt buttons ----------------------------------------------
  document.querySelectorAll('.quick-prompt').forEach(btn => {
    btn.addEventListener('click', () => {
      chatInput.value = btn.dataset.prompt;
      chatInput.dispatchEvent(new Event('input'));
      chatForm.requestSubmit();
    });
  });

  // ---- Voice input (Web Speech API) -------------------------------------
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;

    voiceBtn.addEventListener('click', () => {
      recognition.start();
      voiceBtn.classList.add('btn-success');
      voiceBtn.classList.remove('btn-outline-secondary');
      FarmApp.showToast('Listening… speak now', 'info');
    });

    recognition.onresult = (event) => {
      chatInput.value = event.results[0][0].transcript;
      chatInput.dispatchEvent(new Event('input'));
      voiceBtn.classList.remove('btn-success');
      voiceBtn.classList.add('btn-outline-secondary');
    };

    recognition.onerror = () => {
      voiceBtn.classList.remove('btn-success');
      voiceBtn.classList.add('btn-outline-secondary');
      FarmApp.showToast('Voice input failed. Try again.', 'warning');
    };
  } else {
    voiceBtn.style.display = 'none';
  }

  // ---- Helpers -----------------------------------------------------------

  function appendUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'd-flex gap-2 mb-3 justify-content-end chat-message';
    div.innerHTML = `
      <div class="chat-bubble user-bubble">
        <p class="mb-0">${escapeHtml(text)}</p>
      </div>
      <div class="avatar-circle bg-secondary text-white" style="width:36px;height:36px;">
        <i class="bi bi-person-fill" style="font-size:.9rem;"></i>
      </div>`;
    chatMessages.appendChild(div);
    scrollToBottom();
  }

  function appendBotMessage(text) {
    const div = document.createElement('div');
    div.className = 'd-flex gap-2 mb-3 chat-message';
    div.innerHTML = `
      <div class="avatar-circle bg-success text-white flex-shrink-0" style="width:36px;height:36px;">
        <i class="bi bi-robot" style="font-size:.9rem;"></i>
      </div>
      <div class="chat-bubble assistant-bubble">
        ${FarmApp.renderMarkdown(text)}
      </div>`;
    chatMessages.appendChild(div);
    scrollToBottom();
  }

  function appendErrorMessage(text) {
    const div = document.createElement('div');
    div.className = 'd-flex gap-2 mb-3 chat-message';
    div.innerHTML = `
      <div class="avatar-circle bg-danger text-white flex-shrink-0" style="width:36px;height:36px;">
        <i class="bi bi-exclamation-triangle" style="font-size:.9rem;"></i>
      </div>
      <div class="chat-bubble assistant-bubble border-danger-subtle">
        <div class="text-danger small">
          <i class="bi bi-exclamation-triangle-fill me-1"></i>
          <strong>Error:</strong> ${escapeHtml(text)}
        </div>
      </div>`;
    chatMessages.appendChild(div);
    scrollToBottom();
  }

  function setThinking(active) {
    if (active) {
      typingIndicator.classList.remove('d-none');
      sendBtn.disabled = true;
      chatInput.disabled = true;
      statusText.textContent = 'Thinking…';
    } else {
      typingIndicator.classList.add('d-none');
      sendBtn.disabled = false;
      chatInput.disabled = false;
      statusText.textContent = 'Ready to help';
      chatInput.focus();
    }
    scrollToBottom();
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function escapeHtml(text) {
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // ---- Load existing history on page load -------------------------------
  (async function loadHistory() {
    try {
      const data = await fetch('/api/chat/history').then(r => r.json());
      if (data.success && data.history.length > 0) {
        // Don't show welcome message if there's existing history
        const welcome = document.getElementById('welcomeMsg');
        if (welcome) welcome.remove();

        data.history.forEach(msg => {
          if (msg.role === 'user') appendUserMessage(msg.content);
          else if (msg.role === 'assistant') appendBotMessage(msg.content);
        });
      }
    } catch (_) {
      // Non-critical — history just won't be pre-loaded
    }
  })();

})();
