# Smart Farming Advice Agent 🌾

An AI-powered Smart Farming Advice Agent built with **Python Flask** and
**IBM watsonx.ai Granite models**. Provides personalised crop advice,
irrigation schedules, fertilizer plans, pest management, weather guidance,
government scheme information, and more — tailored for Indian agriculture.

---

## Features

| Feature | Description |
|---|---|
| 🤖 AI Chatbot | Multi-turn conversation with KisanMitra, powered by IBM Granite |
| 🌱 Soil Analysis | NPK, pH, organic matter assessment with improvement plan |
| 💧 Irrigation | Week-wise irrigation schedule by crop, stage, and method |
| 🌿 Fertilizer | Complete dose & split schedule (chemical + organic) |
| 🐛 Pest & Disease | IPM-based diagnosis and treatment recommendations |
| 🌦️ Weather Advisory | Weather-based farming actions for any crop stage |
| 📅 Crop Planning | Season-wise crop plan with cost estimates |
| 🏦 Govt Schemes | PM-KISAN, PMFBY, KCC, state schemes, and more |
| 💰 Cost Estimation | Input cost, revenue, and break-even analysis |
| ♻️ Sustainable Farming | Organic, conservation, and natural farming practices |
| 👨‍👩‍👧 Family / Multi-farm | Multiple plots and family member profiles |
| ⚙️ Editable Agent | Customise AI persona, tone, safety rules via `agent_instructions.py` |

---

## Project Structure

```
smart-farming-agent/
├── app.py                         # Flask application & all API routes
├── config.py                      # Centralised configuration (reads .env)
├── requirements.txt               # Python dependencies
├── .env.example                   # Template — copy to .env and fill in
├── .gitignore                     # Prevents secrets from being committed
│
├── modules/
│   ├── __init__.py
│   ├── agent_instructions.py      # ★ Editable AI persona, tone, safety rules
│   ├── watsonx_client.py          # IBM watsonx.ai / Granite model wrapper
│   └── farming_advisor.py         # Domain-specific prompt composers
│
├── templates/
│   ├── base.html                  # Shared layout (navbar, footer)
│   ├── index.html                 # Chatbot page
│   ├── dashboard.html             # Advisory dashboard (9 tabs)
│   ├── profile.html               # Farmer profile & multi-farm management
│   └── agent_settings.html        # View live agent instructions
│
└── static/
    ├── css/
    │   └── main.css               # Custom styles
    └── js/
        ├── main.js                # Shared utilities (toast, markdown, API)
        ├── chatbot.js             # Chat page logic
        ├── dashboard.js           # Dashboard tab logic
        └── profile.js             # Profile page logic
```

---

## Prerequisites

- Python 3.11+
- An **IBM Cloud account** with watsonx.ai enabled
- A **watsonx.ai Project ID** (create at [cloud.ibm.com](https://cloud.ibm.com))
- An **IBM Cloud API key** (create at IAM → API Keys)

---

## Quick Start

### 1. Clone / download the project

```bash
git clone <your-repo-url>
cd smart-farming-agent
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in:

```env
WATSONX_API_KEY=your-ibm-cloud-api-key
WATSONX_PROJECT_ID=your-watsonx-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct
FLASK_SECRET_KEY=a-strong-random-secret
```

> **Never commit `.env` to source control.**

### 5. Run the application

```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## Getting IBM watsonx.ai Credentials

### IBM Cloud API Key
1. Log in to [cloud.ibm.com](https://cloud.ibm.com)
2. Go to **Manage → Access (IAM) → API Keys**
3. Click **Create an IBM Cloud API key**
4. Copy and paste into `WATSONX_API_KEY` in your `.env`

### watsonx.ai Project ID
1. Go to [dataplatform.cloud.ibm.com](https://dataplatform.cloud.ibm.com)
2. Open (or create) a watsonx.ai project
3. Go to **Manage → General** — copy the **Project ID**
4. Paste into `WATSONX_PROJECT_ID` in your `.env`

### Region URL
| Region | URL |
|--------|-----|
| US South (Dallas) | `https://us-south.ml.cloud.ibm.com` |
| EU Germany | `https://eu-de.ml.cloud.ibm.com` |
| Japan (Tokyo) | `https://jp-tok.ml.cloud.ibm.com` |

---

## Customising the AI Agent

Edit `modules/agent_instructions.py` to change:

| Section | What it controls |
|---------|-----------------|
| `AGENT_NAME` | Display name (default: KisanMitra) |
| `AGENT_PERSONA` | AI identity, backstory, language style |
| `EXPERTISE_DOMAINS` | Knowledge areas the AI focuses on |
| `TONE_GUIDELINES` | Communication style and empathy rules |
| `INDIAN_AGRICULTURE_CONTEXT` | Regional units, crop calendars, portals |
| `SAFETY_RULES` | Restricted topics and ethical boundaries |
| `RESPONSE_FORMAT` | Length, structure, and formatting rules |
| `MULTI_FARM_CONTEXT` | Multi-plot and family advice behaviour |

After editing, restart the server — no other files need changes.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check & model status |
| GET | `/api/profile` | Get current farmer profile |
| POST | `/api/profile` | Save farmer profile |
| DELETE | `/api/profile` | Delete profile & chat history |
| POST | `/api/chat` | Multi-turn chat message |
| GET | `/api/chat/history` | Get conversation history |
| POST | `/api/soil/analyse` | Soil analysis & recommendations |
| POST | `/api/irrigation/schedule` | Irrigation schedule |
| POST | `/api/fertilizer/plan` | Fertilizer management plan |
| POST | `/api/pest/advice` | Pest & disease IPM advice |
| POST | `/api/weather/advisory` | Weather-based farming advice |
| POST | `/api/crop/plan` | Seasonal crop planning |
| POST | `/api/schemes` | Government scheme information |
| POST | `/api/cost/estimate` | Cost-benefit analysis |
| POST | `/api/sustainable` | Sustainable farming tips |
| GET | `/api/agent/settings` | Current agent instruction settings |

---

## Production Deployment

### Using Gunicorn (Linux / macOS)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Gunicorn on Windows (via WSL)

Run the above command inside a WSL terminal.

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t smart-farming-agent .
docker run -p 5000:5000 --env-file .env smart-farming-agent
```

### IBM Code Engine (Recommended for IBM stack)

```bash
# Install IBM Cloud CLI + Code Engine plugin
ibmcloud login
ibmcloud ce application create \
  --name smart-farming-agent \
  --image <your-container-registry>/smart-farming-agent \
  --env-from-secret farming-secrets \
  --port 5000
```

### Environment Variables for Production

Set these in your deployment platform:

```
WATSONX_API_KEY=...
WATSONX_PROJECT_ID=...
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct
FLASK_ENV=production
FLASK_SECRET_KEY=<strong-random-key>
MAX_TOKENS=1024
TEMPERATURE=0.7
```

---

## Security Notes

- `.env` is listed in `.gitignore` — never commit it
- `FLASK_SECRET_KEY` should be a long random string in production
- Set `FLASK_DEBUG=false` in production
- Use HTTPS in production (reverse proxy: Nginx or Caddy)
- For scale, replace the in-memory session store with Redis

---

## Farmer Helplines (India)

| Service | Contact |
|---------|---------|
| Kisan Call Centre | 1800-180-1551 (free) |
| PM-KISAN | 155261 / 011-24300606 |
| Crop Insurance (PMFBY) | 1800-200-7710 |
| Soil Health Card | soilhealth.dac.gov.in |
| eNAM Market | enam.gov.in |
| PM-KISAN Portal | pmkisan.gov.in |

---

## License

MIT License — see `LICENSE` for details.

---

*Built with ❤️ for Indian farmers using IBM watsonx.ai + Granite*
