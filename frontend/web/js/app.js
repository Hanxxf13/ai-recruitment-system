// ─── API CONFIGURATION ────────────────────────────────────────────────────────
// In production, FastAPI serves the frontend from the same origin,
// so the API is at the same base URL. Locally, it's on port 8000.
const API_URL = (
  window.location.hostname === 'localhost' ||
  window.location.hostname === '127.0.0.1'
) ? 'http://localhost:8000' : window.location.origin;

// ─── SESSION ──────────────────────────────────────────────────────────────────
const session = {
  get:   () => JSON.parse(localStorage.getItem('nukhba_user') || 'null'),
  set:   (u) => localStorage.setItem('nukhba_user', JSON.stringify(u)),
  clear: () => localStorage.removeItem('nukhba_user'),
};

// ─── TOAST ────────────────────────────────────────────────────────────────────
function showToast(msg, type = 'info', duration = 4500) {
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

  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body) opts.body = JSON.stringify(body);

  try {
    const res  = await fetch(url, opts);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
    return data;
  } catch (err) {
    if (err.name === 'TypeError') throw new Error('Cannot reach the server. Please try again.');
    throw err;
  }
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

// ─── TOPBAR USER ──────────────────────────────────────────────────────────────
function renderTopbar() {
  const user = session.get();
  const el   = document.getElementById('topbar-user');
  if (!el || !user) return;
  const avatar = user.avatar_url
    ? `<img src="${user.avatar_url}" style="width:32px;height:32px;border-radius:50%;object-fit:cover;border:2px solid var(--gold)" alt="${user.name}">`
    : `<div class="avatar" title="${user.name}">${user.name.charAt(0).toUpperCase()}</div>`;
  el.innerHTML = `
    <div style="display:flex;align-items:center;gap:10px">
      ${avatar}
      <div style="text-align:right">
        <div style="font-size:.88rem;font-weight:600">${user.name}</div>
        <div style="font-size:.72rem;color:var(--text-muted)">${user.role}</div>
      </div>
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

// ─── GOOGLE SIGN-IN ───────────────────────────────────────────────────────────
let _googleInitialized = false;

async function initGoogleAuth() {
  if (_googleInitialized || typeof google === 'undefined') return;
  try {
    const cfg = await fetch(`${API_URL}/config`).then(r => r.json());
    if (!cfg.google_client_id) return;

    _googleInitialized = true;
    google.accounts.id.initialize({
      client_id: cfg.google_client_id,
      callback:  handleGoogleCredential,
      auto_select: false,
      cancel_on_tap_outside: true,
    });

    // Render button in all containers with class 'google-btn-container'
    document.querySelectorAll('.google-btn-container').forEach(container => {
      google.accounts.id.renderButton(container, {
        theme: 'filled_black',
        size:  'large',
        text:  'continue_with',
        shape: 'rectangular',
        width: container.offsetWidth || 340,
      });
      // Show the or-divider after the button
      const divider = container.nextElementSibling;
      if (divider && divider.classList.contains('or-divider')) {
        divider.style.display = 'flex';
      }
    });
  } catch (e) {
    console.warn('Google auth init skipped:', e.message);
  }
}

async function handleGoogleCredential(response) {
  try {
    // Determine role from active tab if on login page
    const regPanel = document.getElementById('panel-register');
    const role = (regPanel && !regPanel.classList.contains('hidden'))
      ? (document.getElementById('reg-role')?.value || 'Candidate')
      : 'Candidate';

    const user = await api('POST', '/users/google-verify', {
      credential: response.credential,
      role,
    });
    session.set(user);
    showToast(`Welcome, ${user.name}! 💎`, 'success');
    setTimeout(() => redirectByRole(user), 900);
  } catch (e) {
    showToast(e.message || 'Google sign-in failed. Please try again.', 'error');
  }
}

// Load Google GSI and init once ready
window.addEventListener('load', () => {
  const gsiScript = document.querySelector('script[src*="accounts.google.com/gsi"]');
  if (gsiScript) {
    if (typeof google !== 'undefined') {
      initGoogleAuth();
    } else {
      gsiScript.addEventListener('load', initGoogleAuth);
    }
  }
});
