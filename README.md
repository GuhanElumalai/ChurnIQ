# BizNexus AI — Unique Starter (v1)

An opinionated, modular Streamlit scaffold for your **AI-driven business analytics** platform:
- **CLV** (starter: RFM + simple CLV proxy; upgrade-ready to BG/NBD + Gamma-Gamma)
- **Churn** (starter: feature engineering + baseline model; upgrade-ready to XGBoost)
- **Sales Forecasting** (starter: rolling-average forecast; upgrade-ready to ARIMA/Prophet)
- **AI Assistant** (starter: rule-based; upgrade-ready to Gemini)
- **Email Alerts** (SMTP)
- **Firebase Auth (optional)** or **Local Demo Mode** (auto-fallback)

> Designed to run **even without secrets** in a safe *Demo Mode*, so you can iterate quickly and wire real services later.

## Quickstart

```bash
# 1) Create venv
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Run
streamlit run app.py
```

Open http://localhost:8501

---

## Configuration

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in values.
If secrets are missing, the app runs in **Demo Mode** (no external services required).

### Firebase
```toml
[firebase.config]
apiKey = "YOUR_API_KEY"
authDomain = "YOUR_PROJECT_ID.firebaseapp.com"
projectId = "YOUR_PROJECT_ID"
storageBucket = "YOUR_PROJECT_ID.appspot.com"
messagingSenderId = "YOUR_SENDER_ID"
appId = "YOUR_APP_ID"
```

### Gemini
```toml
[gemini]
api_key = "YOUR_GEMINI_API_KEY"
```

### SMTP
```toml
[email]
sender_email = "your-email@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 465
smtp_username = "your-email@gmail.com"
smtp_password = "your-app-password"
use_ssl = true
```

> ⚠️ **Note:** In TOML, section names **must not contain spaces**. Keep them like `[firebase.config]`, `[gemini]`, `[email]` to avoid parsing errors.

---

## Project Structure

```
biznexus-ai/
├── app.py
├── pages/
│   ├── 01_Home.py
│   ├── 02_Authentication.py
│   ├── 03_Upload.py
│   ├── 04_CLV.py
│   ├── 05_Churn.py
│   ├── 06_Forecast.py
│   └── 07_Assistant.py
├── src/
│   ├── auth/firebase_auth.py
│   ├── assistant/gemini_client.py
│   ├── data_processing/loaders.py
│   ├── models/clv.py
│   ├── models/churn.py
│   ├── models/forecast.py
│   ├── firebase/client.py
│   └── utils/{theme.py, emailer.py, state.py}
├── assets/
│   ├── css/style.css
│   └── sample/customers.csv
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── requirements.txt
└── README.md
```

---

## Step-by-step roadmap (we'll follow this)
1. ✅ **Scaffold & theming** (this starter)
2. **Data model & validators** (strict schema + helpful error messages)
3. **CLV module (baseline)** (RFM + simple CLV proxy)
4. **Churn module (baseline)** (quick features + baseline model)
5. **Forecasting (baseline)** (rolling average + interactive what-ifs)
6. **AI Assistant (demo)** (rule-based + prompt harness)
7. **Firebase Auth** (switch from Demo Mode to real auth)
8. **Alerts** (SMTP triggers for risk conditions)
9. **Hardening & UX polish** (loading states, caching, tests)

---

## License
MIT (for your convenience)
