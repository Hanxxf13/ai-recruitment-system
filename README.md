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

## 🌍 Deployment
To deploy this project:
1. **GitHub**: Push this repository to GitHub.
2. **Backend**: Host the `backend` folder on **Railway.app** or **Render.com**.
3. **Frontend**: Point **Streamlit Community Cloud** to your `frontend/app.py`.
4. **Environment Variables**: Update `API_URL` in the frontend files to point to your live backend URL.

---
Created with ✨ by TalentSpark Team.
