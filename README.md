# TalentSpark AI - Intelligent Recruitment System ✨

TalentSpark AI is an end-to-end recruitment platform that leverages FastAPI (backend) and Streamlit (frontend) to streamline hiring with AI-powered candidate screening and a premium user experience.

## ✨ Features
- **Premium UI**: Glassmorphism design and high-end aesthetics.
- **AI Matching**: Automated fit-score calculation based on resume and job requirements.
- **HR Command Center**: Manage job listings and review AI-screened applicants.
- **Candidate Portal**: Browse opportunities and track application statuses.

## 🚀 Local Setup

### 1. Prerequisites
- Python 3.12+ (Tested on 3.14.3)
- Virtual Environment recommended

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Run the System
You need **two** terminal windows:

**Terminal 1 (Backend):**
```bash
python -m uvicorn backend.main:app --port 8000 --reload
```

**Terminal 2 (Frontend):**
```bash
streamlit run frontend/app.py
```

## 🌍 Deployment (Railway / Render)

I have optimized the project for cloud hosting:
1. **Dynamic API URL**: The frontend now looks for an `API_URL` environment variable.
2. **Procfile**: Added a `Procfile` to tell hosting services how to run your apps.

### Hosting the Backend (Railway/Render)
- **Repo**: Use your GitHub repository.
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Hosting the Frontend (Streamlit Cloud)
- **App File**: `frontend/app.py`
- **Environment Variable**: Add `API_URL` set to your live Backend URL.

---
Created with ✨ by TalentSpark Team.
