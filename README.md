# 🛡️ CyberShield AI — Personal Cybersecurity Assistant

> **Detect Threats. Protect Your Digital World.**

CyberShield AI is a modern, interactive cybersecurity web application designed for students, everyday internet users, and beginner cybersecurity learners. It helps identify suspicious URLs, phishing emails, scam messages, and weak passwords — all explained in simple English.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?style=flat-square&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Testing](#-testing)
- [Optional AI Integration](#-optional-ai-integration)
- [Security Considerations](#-security-considerations)
- [Contributing](#-contributing)

---

## ✨ Features

### Core Tools
- **🔗 URL Risk Analyzer** — Analyze suspicious URLs for phishing indicators, brand impersonation, and deceptive patterns
- **📧 Phishing Email Detector** — Identify phishing attempts in emails with detailed risk breakdowns
- **💬 Scam Message Analyzer** — Detect scam patterns in SMS, WhatsApp messages, and job offers (with Indian context support)
- **🔑 Password Security Analyzer** — Test password strength entirely in-browser (never transmitted to server)
- **📊 Personal Security Score** — Assess your cybersecurity habits with a personalized questionnaire

### Education & Resources
- **📚 Cybersecurity Education Center** — 10 beginner-friendly topics with quizzes and progress tracking
- **📖 Security Glossary** — Searchable glossary of cybersecurity terms
- **💡 Security Tips** — Practical recommendations for everyday online safety

### Application Features
- **📈 Interactive Dashboard** — Real-time statistics, activity charts, and quick actions
- **📋 Scan History** — View, filter, sort, and manage past analyses
- **🌗 Dark/Light Theme** — Toggle between dark (default) and light themes
- **📱 Fully Responsive** — Works on desktop, tablet, and mobile devices
- **♿ Accessible** — Keyboard navigation, screen reader support, and focus indicators

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript (ES6+) |
| **Backend** | Python Flask |
| **Database** | SQLite |
| **Charts** | Chart.js 4 |
| **Icons** | Lucide Icons |
| **Fonts** | Inter, JetBrains Mono |

> **Note:** No Node.js or npm required! The frontend uses CDN imports and is served directly by Flask.

---

## 📸 Screenshots

The application features a premium cybersecurity dashboard with:
- 🌑 Dark navy/black theme with neon cyan accents
- 🔲 Glassmorphism cards with glowing borders
- 📊 Interactive charts and score visualizations
- ✨ Smooth animations and micro-interactions

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **pip** (Python package manager)
- **Windows 11** (also works on Windows 10, macOS, Linux)

### Step-by-Step Setup (Windows 11)

1. **Open PowerShell or Command Prompt**

2. **Navigate to the project folder:**
   ```powershell
   cd C:\Users\HITESH\OneDrive\Desktop\PROJECT_ANTY\cybershield-ai
   ```

3. **Create a virtual environment (recommended):**
   ```powershell
   python -m venv venv
   ```

4. **Activate the virtual environment:**
   ```powershell
   # PowerShell
   .\venv\Scripts\Activate.ps1

   # Command Prompt
   .\venv\Scripts\activate.bat
   ```

5. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

6. **Set up environment configuration:**
   ```powershell
   copy .env.example .env
   ```
   Edit `.env` if you want to customize settings.

7. **Run the application:**
   ```powershell
   cd backend
   python app.py
   ```

8. **Open your browser:**
   ```
   http://localhost:5000
   ```

---

## ▶️ Running the Application

### Quick Start
```powershell
# From the cybershield-ai directory:
cd backend
python app.py
```

The application will start at `http://localhost:5000`.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_DEBUG` | `true` | Enable debug mode |
| `PORT` | `5000` | Server port |
| `SECRET_KEY` | `dev-secret-key...` | Flask secret key (change in production) |
| `OPENAI_API_KEY` | *(empty)* | Optional: Enable AI-enhanced analysis |

---

## 📁 Project Structure

```
cybershield-ai/
├── backend/
│   ├── app.py                    # Flask application entry point
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py                 # SQLite database operations
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── scan_routes.py        # URL, email, message scan endpoints
│   │   ├── history_routes.py     # Scan history CRUD endpoints
│   │   └── education_routes.py   # Education content endpoints
│   └── services/
│       ├── __init__.py
│       ├── url_analyzer.py       # URL risk analysis engine
│       ├── email_analyzer.py     # Phishing email detection engine
│       ├── message_analyzer.py   # Scam message analysis engine
│       └── score_calculator.py   # Security score calculator
├── frontend/
│   ├── index.html                # Main SPA shell
│   ├── css/
│   │   ├── variables.css         # Design system variables
│   │   ├── base.css              # Reset and base styles
│   │   ├── layout.css            # Sidebar and layout
│   │   ├── components.css        # Reusable UI components
│   │   ├── pages.css             # Page-specific styles
│   │   ├── animations.css        # Animations and transitions
│   │   └── responsive.css        # Mobile responsiveness
│   └── js/
│       ├── utils.js              # Utility functions
│       ├── api.js                # API client
│       ├── router.js             # Client-side router
│       ├── components.js         # Shared UI components
│       ├── app.js                # Application entry point
│       └── pages/
│           ├── dashboard.js      # Dashboard page
│           ├── url-scanner.js    # URL scanner page
│           ├── phishing-detector.js  # Phishing detector page
│           ├── scam-analyzer.js  # Scam analyzer page
│           ├── password-security.js  # Password analyzer page
│           ├── security-score.js # Security score page
│           ├── education.js      # Education center page
│           ├── scan-history.js   # Scan history page
│           └── settings.js       # Settings page
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment configuration template
└── README.md                     # This file
```

---

## 🔌 API Endpoints

### Health & Status
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | System health check |
| `GET` | `/api/dashboard-stats` | Dashboard statistics |

### Analysis Tools
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/scan-url` | Analyze a URL for risks |
| `POST` | `/api/analyze-email` | Detect phishing in emails |
| `POST` | `/api/analyze-message` | Analyze scam messages |
| `POST` | `/api/security-score` | Calculate security habits score |

### Scan History
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/history` | Get scan history (filterable) |
| `DELETE` | `/api/history/<id>` | Delete a specific record |
| `DELETE` | `/api/history` | Clear all history |

### Education
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/education/topics` | List education topics |
| `GET` | `/api/education/topics/<id>` | Get topic details with quiz |
| `GET` | `/api/glossary` | Get cybersecurity glossary |

### Example API Usage

```bash
# Health check
curl http://localhost:5000/api/health

# Scan a URL
curl -X POST http://localhost:5000/api/scan-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://g00gle-security.suspicious-site.com/verify"}'

# Analyze a suspicious email
curl -X POST http://localhost:5000/api/analyze-email \
  -H "Content-Type: application/json" \
  -d '{"subject": "Urgent: Verify Your Account", "sender": "security@bank-verify.xyz", "body": "Your account will be suspended. Click here to verify immediately."}'

# Analyze a scam message
curl -X POST http://localhost:5000/api/analyze-message \
  -H "Content-Type: application/json" \
  -d '{"message": "Congratulations! You won ₹50,000. Pay ₹499 processing fees to claim.", "type": "sms"}'
```

---

## 🧪 Testing

### Manual Testing Checklist

1. **Navigation:** Click all sidebar links — each should load the corresponding page
2. **URL Scanner:**
   - Test with a normal URL: `https://www.google.com`
   - Test with a suspicious URL: `http://192.168.1.1/login.php?user=admin`
   - Test with empty input (should show validation error)
   - Test with invalid format (should show format error)
3. **Phishing Detector:**
   - Click each example button to populate test data
   - Submit analysis and verify results
   - Test with empty fields (validation)
4. **Scam Analyzer:**
   - Click each example button (Fake Prize, Fake Job, UPI Scam, Investment Scam)
   - Verify risk detection and scores
5. **Password Security:**
   - Type `password` — should show Very Weak
   - Type `MyP@ssw0rd123!` — should show Strong
   - Verify password is NEVER sent to server (check Network tab)
6. **Security Score:**
   - Complete the questionnaire
   - Verify score calculation
7. **Education:**
   - Browse topics, open topic details
   - Complete a quiz
8. **Scan History:**
   - After performing scans, verify history entries
   - Test filter and delete functionality
9. **Theme Toggle:** Switch between dark and light modes
10. **Responsive:** Test on mobile viewport (F12 → device toolbar)

### API Testing

```powershell
# Test health endpoint
Invoke-RestMethod -Uri http://localhost:5000/api/health

# Test URL scan
Invoke-RestMethod -Uri http://localhost:5000/api/scan-url -Method POST -ContentType "application/json" -Body '{"url":"http://suspicious-link.xyz/login"}'
```

---

## 🤖 Optional AI Integration

CyberShield AI works fully with **rule-based analysis** out of the box. For enhanced analysis, you can optionally configure an AI API:

### Setup (Optional)

1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Add it to your `.env` file:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
3. Restart the application

### How It Works

- **Without API key:** All analysis uses comprehensive rule-based pattern matching (fully functional)
- **With API key:** Enhanced analysis using AI for complex phishing and scam detection

> ⚠️ **Note:** The rule-based mode is comprehensive and sufficient for most use cases. AI integration is optional and requires a paid API key.

---

## 🔒 Security Considerations

### What CyberShield AI Does Right
- ✅ **Passwords never leave the browser** — analyzed entirely client-side
- ✅ **No URL fetching** — URLs are analyzed by pattern only, never visited
- ✅ **Parameterized SQL queries** — prevents SQL injection
- ✅ **Input validation** — all user inputs are validated and sanitized
- ✅ **Rate limiting** — prevents abuse of API endpoints
- ✅ **No sensitive data storage** — passwords, full emails, and messages are NOT stored
- ✅ **HTML sanitization** — prevents XSS attacks
- ✅ **CORS configured** — restricts API access to allowed origins
- ✅ **Environment variables** — secrets are never hardcoded

### Important Disclaimers
- ⚠️ This is an **educational tool** — not a replacement for professional security software
- ⚠️ URL analysis is **heuristic-based** — it cannot guarantee a URL is safe or malicious
- ⚠️ Phishing detection uses **pattern matching** — sophisticated attacks may not be detected
- ⚠️ Security scores are **educational assessments** — not professional security audits
- ⚠️ Always use dedicated antivirus/anti-malware software for real protection

---

## 📝 License

This project is for educational purposes. Built as a cybersecurity learning tool.

---

## 🙏 Credits

- **Lucide Icons** — Beautiful open-source icons
- **Chart.js** — Simple yet flexible JavaScript charting
- **Inter Font** — Modern sans-serif typeface
- **Flask** — Lightweight Python web framework

---

<div align="center">

**🛡️ CyberShield AI — Empowering everyone to stay safe online.**

*Built with ❤️ for cybersecurity education*

</div>
