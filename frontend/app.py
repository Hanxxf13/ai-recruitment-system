import streamlit as st
import requests
import pandas as pd
import time

# ─── CONFIG ───────────────────────────────────────────────────────────────────
try:
    API_URL = st.secrets["API_URL"]
except Exception:
    API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="نخبة | Nukhba Elite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;700;900&family=Amiri:wght@400;700&display=swap');

/* ─── Variables ─── */
:root {
  --gold:      #C9A84C;
  --gold-lt:   #E4C46A;
  --gold-dk:   #8B6914;
  --gold-glow: rgba(201,168,76,0.18);
  --obsidian:  #080809;
  --dark:      #0f0f10;
  --card:      #141416;
  --border:    rgba(201,168,76,0.18);
  --text:      #eaeaea;
  --dim:       #888;
}

/* ─── Base ─── */
html, body, [class*="css"] {
  font-family: 'Inter', sans-serif !important;
  color: var(--text) !important;
}

.stApp {
  background: radial-gradient(ellipse at top left, #0d0c0a 0%, #080809 60%, #060508 100%) !important;
}

/* ─── Hide Streamlit chrome ─── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── Remove white top padding ─── */
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* ─── Sidebar ─── */
[data-testid="stSidebar"] {
  background: #0a0a0b !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label { color: var(--dim) !important; }

/* ─── Headings ─── */
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

/* ─── Metric cards ─── */
[data-testid="metric-container"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  padding: 18px !important;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: var(--gold) !important;
  font-weight: 900 !important;
  font-size: 2rem !important;
}
[data-testid="metric-container"] label {
  color: var(--dim) !important;
  font-size: 0.78rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
}

/* ─── Inputs ─── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px var(--gold-glow) !important;
}

/* ─── Buttons ─── */
.stButton > button {
  background: linear-gradient(135deg, var(--gold-dk) 0%, var(--gold) 60%, var(--gold-lt) 100%) !important;
  color: #000 !important;
  font-weight: 800 !important;
  font-family: 'Inter', sans-serif !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.6rem 1.5rem !important;
  letter-spacing: 0.5px !important;
  transition: all 0.25s !important;
  box-shadow: 0 4px 16px var(--gold-glow) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px var(--gold-glow) !important;
}

/* ─── Tabs ─── */
.stTabs {
  margin-top: 0 !important;
}
.stTabs [data-baseweb="tab-list"] {
  background: #111112 !important;
  border-radius: 12px !important;
  padding: 4px !important;
  border: 1px solid rgba(255,255,255,0.06) !important;
  gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 9px !important;
  color: var(--dim) !important;
  font-weight: 600 !important;
  font-family: 'Inter', sans-serif !important;
  padding: 6px 14px !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--gold-dk), var(--gold)) !important;
  color: #000 !important;
}

/* ─── Dataframe ─── */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 12px !important; }
.stDataFrame thead th {
  background: var(--card) !important;
  color: var(--gold) !important;
  font-size: 0.78rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
}

/* ─── Reduce default Streamlit spacing ─── */
[data-testid="stVerticalBlock"] > div {
  gap: 0.8rem !important;
}
div.stButton > button {
  margin-top: 10px !important;
}

/* ─── Alerts ─── */
.stSuccess { background: rgba(56,161,105,0.1) !important; border-color: #38a169 !important; }
.stError   { background: rgba(229,62,62,0.1)  !important; border-color: #e53e3e !important; }
.stWarning { background: rgba(201,168,76,0.08) !important; border-color: var(--gold) !important; }

/* ─── Login card ─── */
.login-card {
  background: #111113;
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 32px 40px 24px;
  box-shadow: 0 24px 60px rgba(0,0,0,0.6);
}
.hero-arabic {
  font-family: 'Amiri', serif;
  font-size: 4.5rem;
  color: var(--gold);
  line-height: 1;
  text-shadow: 0 0 40px rgba(201,168,76,0.3);
}
.hero-tagline {
  font-family: 'Inter', sans-serif;
  font-size: 0.75rem;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--dim);
  margin: 8px 0 28px;
}
.hero-headline {
  font-family: 'Playfair Display', serif;
  font-size: 2.2rem;
  font-weight: 700;
  line-height: 1.25;
  color: var(--text);
}
.hero-sub {
  font-size: 0.95rem;
  color: var(--dim);
  margin-top: 12px;
  line-height: 1.6;
}
.feature-pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 28px;
}
.feature-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 100px;
  font-size: 0.78rem;
  color: var(--dim);
}
.dot { display:inline-block; width:6px; height:6px; border-radius:50%; background:var(--gold); }

/* ─── Stat card ─── */
.stat-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px 20px;
  position: relative;
  overflow: hidden;
  height: 100%;
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(to right, var(--gold), transparent);
}
.stat-num   { font-size: 2rem; font-weight: 900; color: var(--gold); line-height: 1; }
.stat-label { font-size: 0.75rem; color: var(--dim); margin-top: 6px; text-transform: uppercase; letter-spacing: 0.8px; }
.stat-icon  { font-size: 1.6rem; margin-bottom: 10px; }

/* ─── Job card ─── */
.job-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 22px 20px;
  transition: border-color 0.25s;
  height: 100%;
}
.job-card:hover { border-color: rgba(201,168,76,0.5); }
.job-title { font-size: 1rem; font-weight: 700; margin-bottom: 8px; }
.job-reqs  { font-size: 0.78rem; color: var(--gold-dk); font-weight: 600; margin: 10px 0; }

/* ─── Score ring ─── */
.score-ring {
  width: 80px; height: 80px;
  border-radius: 50%;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  border: 3px solid var(--gold);
  box-shadow: 0 0 18px var(--gold-glow);
  margin: 0 auto 12px;
}
.score-ring .snum { font-size: 1.6rem; font-weight: 900; color: var(--gold); line-height:1; }
.score-ring .slbl { font-size: 0.6rem; color: var(--dim); text-transform: uppercase; letter-spacing:.5px; }

/* ─── Divider ─── */
.gold-divider {
  height: 1px;
  background: linear-gradient(to right, transparent, var(--gold), transparent);
  margin: 12px 0;
  opacity: 0.3;
}

/* ─── Status badge ─── */
.badge-green { background: rgba(56,161,105,0.15); color: #68d391; border-radius: 20px; padding: 2px 10px; font-size: .75rem; font-weight:700; }
.badge-gold  { background: rgba(201,168,76,0.15);  color: var(--gold-lt); border-radius: 20px; padding: 2px 10px; font-size: .75rem; font-weight:700; }
.badge-red   { background: rgba(229,62,62,0.15);   color: #fc8181; border-radius: 20px; padding: 2px 10px; font-size: .75rem; font-weight:700; }
</style>
""", unsafe_allow_html=True)


# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "user"    not in st.session_state: st.session_state.user    = None
if "section" not in st.session_state: st.session_state.section = "overview"


# ─── API HELPERS ──────────────────────────────────────────────────────────────
def call(method, path, **kwargs):
    try:
        r = requests.request(method, f"{API_URL}{path}", timeout=8, **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot reach the backend. Is it running on port 8000?")
        return None
    except Exception as e:
        detail = ""
        try: detail = e.response.json().get("detail","")
        except: pass
        st.error(f"API error: {detail or str(e)}")
        return None


# ──────────────────────────────────────────────────────────────────────────────
# AUTH PAGE
# ──────────────────────────────────────────────────────────────────────────────
def show_auth():
    left, pad, right = st.columns([1.3, 0.15, 1])

    with left:
        st.markdown("""
        <div style="margin-top:60px">
          <div class="hero-arabic">نخبة</div>
          <div class="hero-tagline">Elite • Selection • Intelligence</div>
          <div class="hero-headline">Where Elite Talent<br>Meets Visionary Teams.</div>
          <p class="hero-sub">
            The most sophisticated AI-powered recruitment platform.<br>
            Secure access for distinguished professionals.
          </p>
          <div class="feature-pill-row">
            <span class="feature-pill"><span class="dot"></span>AI Screening</span>
            <span class="feature-pill"><span class="dot"></span>Smart Matching</span>
            <span class="feature-pill"><span class="dot"></span>Instant Analytics</span>
            <span class="feature-pill"><span class="dot"></span>Elite Pool</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        tab_login, tab_reg = st.tabs(["  🔐  Sign In  ", "  ✨  Create Account  "])

        # ── Sign In ──
        with tab_login:
            email = st.text_input("Email Address", placeholder="you@example.com", key="li_email")
            pwd   = st.text_input("Password",       placeholder="••••••••",        type="password", key="li_pwd")

            if st.button("Sign In →", use_container_width=True, key="btn_login"):
                if not email or not pwd:
                    st.warning("Please fill in all fields.")
                else:
                    with st.spinner("Authenticating…"):
                        res = call("POST", "/users/login",
                                   json={"name":"","email":email,"password":pwd,"role":""})
                    if res:
                        st.session_state.user = res
                        st.success(f"Welcome back, **{res['name']}** 💎")
                        time.sleep(0.7)
                        st.rerun()

            st.markdown("""
            <div style="text-align:center;margin-top:16px;padding:10px;background:rgba(201,168,76,0.04);
                        border:1px dashed rgba(201,168,76,0.2);border-radius:10px;font-size:.78rem;color:#555">
              Demo: <span style="color:#C9A84C">hr@example.com</span> /
              <span style="color:#C9A84C">password123</span>
            </div>
            """, unsafe_allow_html=True)

        # ── Register ──
        with tab_reg:
            c1, c2 = st.columns(2)
            with c1: reg_name = st.text_input("Full Name",    placeholder="Jane Doe",    key="rn")
            with c2: reg_role = st.selectbox("Role", ["Candidate","HR","Admin"],          key="rr")
            reg_email = st.text_input("Email Address",  placeholder="jane@example.com",  key="re")
            reg_pwd   = st.text_input("Password",       placeholder="Create a strong password", type="password", key="rp")

            if st.button("✨ Join the Elite", use_container_width=True, key="btn_reg"):
                if not reg_name or not reg_email or not reg_pwd:
                    st.warning("Please fill all fields.")
                elif len(reg_pwd) < 6:
                    st.warning("Password must be at least 6 characters.")
                else:
                    with st.spinner("Creating your elite account…"):
                        res = call("POST", "/users/register",
                                   json={"name":reg_name,"email":reg_email,
                                         "password":reg_pwd,"role":reg_role})
                    if res:
                        st.session_state.user = res
                        st.success("🎉 Account created! Welcome to Nukhba.")
                        time.sleep(0.8)
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# SHARED SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
def render_sidebar(user):
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:8px 0 20px">
          <div style="font-family:'Amiri',serif;font-size:2rem;color:#C9A84C">نخبة</div>
          <div style="font-size:.65rem;letter-spacing:3px;color:#555;text-transform:uppercase">Elite Selection</div>
        </div>
        <div style="background:#141416;border:1px solid rgba(201,168,76,.18);border-radius:12px;padding:14px 16px;margin-bottom:20px">
          <div style="display:flex;align-items:center;gap:12px">
            <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#C9A84C,#8B6914);
                        display:flex;align-items:center;justify-content:center;font-weight:900;color:#000;font-size:.9rem">
              {user['name'][0].upper()}
            </div>
            <div>
              <div style="font-weight:700;font-size:.9rem">{user['name']}</div>
              <div style="font-size:.72rem;color:#888">{user['role']}</div>
            </div>
          </div>
        </div>
        <div class="gold-divider"></div>
        """, unsafe_allow_html=True)

        if user['role'] in ('HR','Admin'):
            nav = {
                "📊  Overview":     "overview",
                "💼  Job Postings": "jobs",
                "📋  Applications": "applications",
                "➕  Post New Job": "post_job",
            }
        else:
            nav = {
                "🔍  Discover Jobs":     "discover",
                "📋  My Applications":   "my_apps",
                "👤  My Profile":        "profile",
            }

        for label, key in nav.items():
            active = st.session_state.section == key
            if st.button(
                label,
                use_container_width=True,
                key=f"nav_{key}",
                type="primary" if active else "secondary",
            ):
                st.session_state.section = key
                st.rerun()

        st.markdown("<div class='gold-divider' style='margin-top:auto'></div>", unsafe_allow_html=True)
        if st.button("🚪  Logout", use_container_width=True):
            st.session_state.user    = None
            st.session_state.section = "overview"
            st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# HR DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────
def show_hr_dashboard(user):
    render_sidebar(user)
    sec = st.session_state.section

    # ── Load data ──
    @st.cache_data(ttl=30, show_spinner=False)
    def load_jobs(): return call("GET", "/jobs") or []
    @st.cache_data(ttl=30, show_spinner=False)
    def load_apps(job_id): return call("GET", f"/applications/{job_id}") or []

    jobs = load_jobs()
    all_apps = []
    for j in jobs:
        apps = load_apps(j['id'])
        for a in apps: a['_job_title'] = j['title']
        all_apps.extend(apps)

    # ────────────────── OVERVIEW ──────────────────
    if sec == "overview":
        st.markdown("<h1 style='font-size:1.9rem'>HR Command Center</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;margin-bottom:24px'>Monitor your elite talent pipeline.</p>",
                    unsafe_allow_html=True)

        c1,c2,c3,c4 = st.columns(4)
        open_jobs = sum(1 for j in jobs if j.get('status')=='Open')
        scores = [a['ai_score'] for a in all_apps if a.get('ai_score') is not None]
        shortlisted = sum(1 for a in all_apps if a.get('status') in ('Shortlisted','Screened'))

        c1.metric("💼 Active Jobs",     open_jobs)
        c2.metric("📋 Applications",    len(all_apps))
        c3.metric("🤖 Avg AI Score",    f"{sum(scores)/len(scores):.1f}%" if scores else "—")
        c4.metric("✅ Shortlisted",     shortlisted)

        st.markdown("<div class='gold-divider' style='margin:20px 0'></div>", unsafe_allow_html=True)
        st.markdown("#### Recent Applications")

        if all_apps:
            recent = all_apps[-8:][::-1]
            df = pd.DataFrame([{
                "Job":       a.get('_job_title','—'),
                "Score":     f"{a['ai_score']:.1f}%" if a.get('ai_score') is not None else '—',
                "Status":    a.get('status','—'),
                "Feedback":  (a.get('ai_feedback') or '')[:70] + '…',
            } for a in recent])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No applications yet. Post a job to get started.")

    # ────────────────── JOB POSTINGS ──────────────────
    elif sec == "jobs":
        st.markdown("<h1 style='font-size:1.9rem'>Job Postings</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;margin-bottom:24px'>All active & closed positions.</p>",
                    unsafe_allow_html=True)

        if not jobs:
            st.info("No jobs posted yet.")
        else:
            cols = st.columns(2)
            for i, j in enumerate(jobs):
                with cols[i % 2]:
                    status_color = "#68d391" if j.get('status')=='Open' else "#888"
                    st.markdown(f"""
                    <div class="job-card">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div class="job-title">{j['title']}</div>
                        <span style="color:{status_color};font-size:.78rem;font-weight:700">{j.get('status','—')}</span>
                      </div>
                      <p style="font-size:.85rem;color:#888;line-height:1.6;margin:8px 0">{j['description']}</p>
                      <div class="job-reqs">🔑 {j['requirements']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ────────────────── ALL APPLICATIONS ──────────────────
    elif sec == "applications":
        st.markdown("<h1 style='font-size:1.9rem'>All Applications</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;margin-bottom:24px'>AI-screened submissions.</p>",
                    unsafe_allow_html=True)

        if not all_apps:
            st.info("No applications yet.")
        else:
            for a in reversed(all_apps[-20:]):
                score = a.get('ai_score')
                score_color = ("#68d391" if score and score>=75 else
                               "#C9A84C" if score and score>=50 else "#fc8181")
                with st.expander(f"**{a.get('_job_title','Job')}** — Score: {f'{score:.0f}%' if score else '—'}"):
                    lcol, rcol = st.columns([2,1])
                    with lcol:
                        st.caption("AI Feedback")
                        st.write(a.get('ai_feedback','—'))
                        st.caption("Resume Extract")
                        st.text(str(a.get('resume_text',''))[:400] + '…')
                    with rcol:
                        if score is not None:
                            st.markdown(f"""
                            <div class="score-ring" style="border-color:{score_color};box-shadow:0 0 18px {score_color}44">
                              <div class="snum" style="color:{score_color}">{score:.0f}</div>
                              <div class="slbl">% fit</div>
                            </div>""", unsafe_allow_html=True)
                        new_status = st.selectbox(
                            "Update Status",
                            ["Screened","Shortlisted","Interview","Rejected","Hired"],
                            index=["Screened","Shortlisted","Interview","Rejected","Hired"].index(
                                a.get('status','Screened')
                            ) if a.get('status') in ["Screened","Shortlisted","Interview","Rejected","Hired"] else 0,
                            key=f"status_{a['id']}"
                        )
                        if st.button("💾 Save", key=f"save_{a['id']}"):
                            r = call("PUT", f"/applications/{a['id']}/status",
                                     params={"status": new_status})
                            if r is not None:
                                st.success("Status updated!")
                                st.cache_data.clear()

    # ────────────────── POST JOB ──────────────────
    elif sec == "post_job":
        st.markdown("<h1 style='font-size:1.9rem'>Post a New Job</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;margin-bottom:24px'>AI will auto-match elite candidates.</p>",
                    unsafe_allow_html=True)

        with st.form("post_job_form", clear_on_submit=True):
            title = st.text_input("Job Title", placeholder="e.g. Senior Software Engineer")
            desc  = st.text_area("Description", placeholder="Describe the role and responsibilities…")
            reqs  = st.text_area("Key Requirements (comma separated)",
                                  placeholder="Python, FastAPI, 3+ years experience…", height=100)
            submitted = st.form_submit_button("🚀 Post Job", use_container_width=True)

        if submitted:
            if not title or not desc or not reqs:
                st.warning("Please fill all fields.")
            else:
                with st.spinner("Posting job…"):
                    r = call("POST", f"/jobs?hr_id={user['id']}",
                             json={"title":title,"description":desc,"requirements":reqs})
                if r:
                    st.success(f"✅ **{title}** posted successfully!")
                    st.cache_data.clear()
                    time.sleep(0.8)
                    st.session_state.section = "jobs"
                    st.rerun()


# ──────────────────────────────────────────────────────────────────────────────
# CANDIDATE PORTAL
# ──────────────────────────────────────────────────────────────────────────────
def show_candidate_portal(user):
    render_sidebar(user)
    sec = st.session_state.section

    @st.cache_data(ttl=30, show_spinner=False)
    def load_jobs(): return call("GET", "/jobs") or []
    @st.cache_data(ttl=30, show_spinner=False)
    def load_my_apps(uid): return call("GET", f"/applications/candidate/{uid}") or []

    jobs   = load_jobs()
    my_apps = load_my_apps(user['id'])
    applied_ids = {a['job_id'] for a in my_apps}

    # ────────────────── DISCOVER ──────────────────
    if sec == "discover":
        st.markdown("<h1 style='font-size:1.9rem'>Discover Elite Opportunities</h1>",
                    unsafe_allow_html=True)
        st.markdown("<p style='color:#888;margin-bottom:24px'>AI-curated positions for top talent.</p>",
                    unsafe_allow_html=True)

        if not jobs:
            st.info("No open positions right now. Check back soon!")
        else:
            cols = st.columns(2)
            for i, j in enumerate(jobs):
                with cols[i % 2]:
                    is_applied = j['id'] in applied_ids
                    st.markdown(f"""
                    <div class="job-card" style="margin-bottom:4px">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div class="job-title">{j['title']}</div>
                        <span style="color:#68d391;font-size:.78rem;font-weight:700">{j.get('status','Open')}</span>
                      </div>
                      <p style="font-size:.85rem;color:#888;line-height:1.6;margin:8px 0">{j['description']}</p>
                      <div class="job-reqs">🔑 {j['requirements']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if is_applied:
                        st.button("✓ Already Applied", key=f"ap_{j['id']}", disabled=True,
                                  use_container_width=True)
                    else:
                        if st.button(f"Apply Now →", key=f"ap_{j['id']}", use_container_width=True):
                            st.session_state[f"apply_job"] = j
                            st.session_state.section = "apply_flow"
                            st.rerun()
                    st.write("")

    # ────────────────── APPLY FLOW ──────────────────
    elif sec == "apply_flow":
        job = st.session_state.get("apply_job", {})
        if not job:
            st.session_state.section = "discover"; st.rerun()

        st.markdown(f"<h1 style='font-size:1.9rem'>Apply for {job.get('title','Position')}</h1>",
                    unsafe_allow_html=True)
        st.markdown("<p style='color:#888;margin-bottom:20px'>Our AI will evaluate your fit instantly.</p>",
                    unsafe_allow_html=True)

        with st.form("apply_form"):
            resume = st.text_area(
                "Resume / Experience Summary",
                placeholder="Paste your resume or describe your skills and experience in detail…",
                height=220,
            )
            submitted = st.form_submit_button("🚀 Submit & Get AI Score", use_container_width=True)

        if submitted:
            if not resume.strip():
                st.warning("Please enter your resume or experience summary.")
            else:
                with st.spinner("Submitting and running AI evaluation…"):
                    res = call("POST", f"/applications?candidate_id={user['id']}",
                               json={"job_id": job['id'], "resume_text": resume})
                if res:
                    score = res.get('ai_score')
                    score_color = ("#68d391" if score and score>=75 else
                                   "#C9A84C" if score and score>=50 else "#fc8181")
                    st.markdown(f"""
                    <div style="text-align:center;margin:20px 0">
                      <div class="score-ring" style="border-color:{score_color};box-shadow:0 0 24px {score_color}44;margin:0 auto 16px">
                        <div class="snum" style="color:{score_color}">{f'{score:.0f}' if score else '—'}</div>
                        <div class="slbl">% fit</div>
                      </div>
                      <h3 style="color:{score_color}">Your AI Fit Score</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info(res.get('ai_feedback','No feedback.'))
                    st.success("✅ Application submitted!")
                    st.cache_data.clear()
                    if st.button("← Back to Jobs"):
                        st.session_state.section = "discover"; st.rerun()

    # ────────────────── MY APPLICATIONS ──────────────────
    elif sec == "my_apps":
        st.markdown("<h1 style='font-size:1.9rem'>My Applications</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#888;margin-bottom:24px'>Track your submissions and AI scores.</p>",
                    unsafe_allow_html=True)

        if not my_apps:
            st.info("You haven't applied to any positions yet.")
            if st.button("Browse Jobs"):
                st.session_state.section = "discover"; st.rerun()
        else:
            job_map = {j['id']: j for j in jobs}
            for a in my_apps:
                job = job_map.get(a['job_id'],{})
                score = a.get('ai_score')
                score_color = ("#68d391" if score and score>=75 else
                               "#C9A84C" if score and score>=50 else "#fc8181")
                with st.expander(f"**{job.get('title','Position')}** — {a.get('status','—')}"):
                    l, r = st.columns([3,1])
                    with l:
                        st.write(f"**AI Feedback:** {a.get('ai_feedback','—')}")
                    with r:
                        if score is not None:
                            st.markdown(f"""
                            <div class="score-ring" style="border-color:{score_color};box-shadow:0 0 14px {score_color}33">
                              <div class="snum" style="color:{score_color}">{score:.0f}</div>
                              <div class="slbl">% fit</div>
                            </div>""", unsafe_allow_html=True)

    # ────────────────── PROFILE ──────────────────
    elif sec == "profile":
        st.markdown("<h1 style='font-size:1.9rem'>My Profile</h1>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#141416;border:1px solid rgba(201,168,76,.18);border-radius:16px;padding:28px;max-width:500px;margin-top:8px">
          <div style="display:flex;align-items:center;gap:18px;margin-bottom:20px">
            <div style="width:56px;height:56px;border-radius:50%;
                        background:linear-gradient(135deg,#C9A84C,#8B6914);
                        display:flex;align-items:center;justify-content:center;
                        font-weight:900;color:#000;font-size:1.4rem">
              {user['name'][0].upper()}
            </div>
            <div>
              <div style="font-size:1.15rem;font-weight:700">{user['name']}</div>
              <div style="font-size:.82rem;color:#888">{user['email']}</div>
              <span style="background:rgba(201,168,76,.15);color:#E4C46A;
                           border-radius:20px;padding:2px 10px;font-size:.72rem;font-weight:700">
                {user['role']}
              </span>
            </div>
          </div>
          <div class="gold-divider"></div>
          <p style="font-size:.88rem;color:#888;line-height:1.6;margin-top:14px">
            You are a valued member of the <strong style="color:#C9A84C">Nukhba Elite</strong> talent network.
            Apply to exceptional opportunities and track your AI-driven journey.
          </p>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# MAIN ROUTER
# ──────────────────────────────────────────────────────────────────────────────
u = st.session_state.user

if u is None:
    show_auth()
elif u.get('role') in ('HR', 'Admin'):
    show_hr_dashboard(u)
else:
    show_candidate_portal(u)
