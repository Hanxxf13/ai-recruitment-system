// ─── CONFIG ───────────────────────────────────────────────────────────────────
const API_URL = window.API_URL || 'http://localhost:8000';

// ─── SESSION ──────────────────────────────────────────────────────────────────
const session = {
  get: () => JSON.parse(localStorage.getItem('nukhba_user') || 'null'),
  set: (u) => localStorage.setItem('nukhba_user', JSON.stringify(u)),
  clear: () => localStorage.removeItem('nukhba_user'),
};

// ─── TOAST ────────────────────────────────────────────────────────────────────
function showToast(msg, type = 'info', duration = 4000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = msg;
  container.appendChild(t);
  setTimeout(() => t.remove(), duration);
}

// ─── API HELPER ───────────────────────────────────────────────────────────────
async function api(method, path, body = null, params = null) {
  let url = `${API_URL}${path}`;
  if (params) url += '?' + new URLSearchParams(params).toString();
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  try {
    const res = await fetch(url, opts);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
    return data;
  } catch (err) {
    throw err;
  }
}

// ─── OTP COUNTDOWN ────────────────────────────────────────────────────────────
function startOtpCountdown(seconds, onExpire) {
  const timerEl = document.getElementById('otp-timer');
  const bannerEl = document.getElementById('otp-active');
  const expiredEl = document.getElementById('otp-expired');
  const verifyBtn = document.getElementById('btn-verify');
  const resendBtn = document.getElementById('btn-resend');
  if (!timerEl) return;

  let remaining = seconds;
  const interval = setInterval(() => {
    remaining--;
    if (remaining <= 0) {
      clearInterval(interval);
      if (bannerEl) bannerEl.classList.add('hidden');
      if (expiredEl) expiredEl.classList.remove('hidden');
      if (verifyBtn) verifyBtn.disabled = true;
      if (resendBtn) resendBtn.disabled = false;
      if (onExpire) onExpire();
    } else {
      timerEl.textContent = remaining + 's';
      if (remaining <= 10) timerEl.style.color = '#e53e3e';
    }
  }, 1000);
  timerEl.textContent = remaining + 's';
  return interval;
}

// ─── BTN LOADING STATE ────────────────────────────────────────────────────────
function setLoading(btn, loading) {
  if (loading) {
    btn.dataset.orig = btn.innerHTML;
    btn.innerHTML = '<span class="spinner"></span>';
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.orig || btn.innerHTML;
    btn.disabled = false;
  }
}

// ─── GUARD: redirect if not logged in ────────────────────────────────────────
function requireAuth(role = null) {
  const user = session.get();
  if (!user) { window.location.href = '/index.html'; return null; }
  if (role && user.role !== role) {
    showToast('Access denied — wrong role', 'error');
    setTimeout(() => window.location.href = '/index.html', 1500);
    return null;
  }
  return user;
}

// ─── RENDER USER AVATAR ──────────────────────────────────────────────────────
function renderTopbar() {
  const user = session.get();
  const el = document.getElementById('topbar-user');
  if (!el || !user) return;
  el.innerHTML = `
    <span style="color:var(--text-dim);font-size:.85rem">${user.role}</span>
    <div class="avatar">${user.name.charAt(0).toUpperCase()}</div>
    <button class="btn btn-ghost" style="width:auto;padding:8px 16px" onclick="logout()">Logout</button>
  `;
}

function logout() {
  session.clear();
  window.location.href = '/index.html';
}
