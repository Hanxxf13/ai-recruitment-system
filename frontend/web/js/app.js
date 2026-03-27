// ─── API CONFIGURATION ────────────────────────────────────────────────────────
const API_URL = window.API_URL || (
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://localhost:8000'
    : 'https://nukhba-elite-api.onrender.com'  // Replace with your Render URL
);

// ─── SESSION ──────────────────────────────────────────────────────────────────
const session = {
  get:   () => JSON.parse(localStorage.getItem('nukhba_user') || 'null'),
  set:   (u) => localStorage.setItem('nukhba_user', JSON.stringify(u)),
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
  setTimeout(() => {
    t.style.animation = 'toastOut 0.3s ease forwards';
    setTimeout(() => t.remove(), 300);
  }, duration);
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

  const res  = await fetch(url, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
  return data;
}

// ─── BUTTON LOADING STATE ─────────────────────────────────────────────────────
function setLoading(btn, loading) {
  if (loading) {
    btn.dataset.orig = btn.innerHTML;
    btn.innerHTML    = '<span class="spinner"></span>';
    btn.disabled     = true;
  } else {
    btn.innerHTML = btn.dataset.orig || btn.innerHTML;
    btn.disabled  = false;
  }
}

// ─── AUTH GUARD ───────────────────────────────────────────────────────────────
function requireAuth(role = null) {
  const user = session.get();
  if (!user) {
    window.location.href = '/web/index.html';
    return null;
  }
  if (role && user.role !== role) {
    showToast('Access denied — wrong role', 'error');
    setTimeout(() => window.location.href = '/web/index.html', 1500);
    return null;
  }
  return user;
}

// ─── RENDER TOPBAR USER ───────────────────────────────────────────────────────
function renderTopbar() {
  const user = session.get();
  const el   = document.getElementById('topbar-user');
  if (!el || !user) return;
  el.innerHTML = `
    <span style="color:var(--text-dim);font-size:.82rem;display:none" id="topbar-role">${user.role}</span>
    <div style="text-align:right;display:none" id="topbar-name-wrap">
      <div style="font-size:.88rem;font-weight:600">${user.name}</div>
      <div style="font-size:.72rem;color:var(--text-muted)">${user.role}</div>
    </div>
    <div class="avatar" title="${user.name}" onclick="this.nextElementSibling.classList.toggle('hidden')">
      ${user.name.charAt(0).toUpperCase()}
    </div>
    <button class="btn btn-ghost" style="width:auto;padding:8px 18px;font-size:.82rem" onclick="logout()">
      Logout
    </button>
  `;
}

// ─── LOGOUT ───────────────────────────────────────────────────────────────────
function logout() {
  session.clear();
  window.location.href = '/web/index.html';
}
