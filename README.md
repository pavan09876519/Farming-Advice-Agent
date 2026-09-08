# Smart Farming Advice Agent 🌾

An AI-powered Smart Farming Advice Agent built with **Python Flask** and **IBM watsonx.ai Granite models**. It provides personalised crop advice, irrigation schedules, fertilizer plans, pest management, weather guidance, government scheme information, cost estimation, and sustainable farming recommendations tailored for Indian agriculture.

---

## 🌟 Features

| Feature                          | Description                                                                      |
| -------------------------------- | -------------------------------------------------------------------------------- |
| 🤖 **AI Chatbot**                | Multi-turn conversation with KisanMitra, powered by IBM Granite                  |
| 🌱 **Soil Analysis**             | NPK, pH, and organic matter assessment with improvement recommendations          |
| 💧 **Irrigation Advisory**       | Week-wise irrigation schedule based on crop, growth stage, and irrigation method |
| 🌿 **Fertilizer Planning**       | Fertilizer dose and split-application schedule with chemical and organic options |
| 🐛 **Pest & Disease Advisory**   | IPM-based pest and disease diagnosis and treatment recommendations               |
| 🌦️ **Weather Advisory**         | Weather-based farming actions for different crop stages                          |
| 📅 **Crop Planning**             | Season-wise crop planning with estimated costs                                   |
| 🏦 **Government Schemes**        | Information about PM-KISAN, PMFBY, KCC, and state-level schemes                  |
| 💰 **Cost Estimation**           | Input cost, revenue estimation, and break-even analysis                          |
| ♻️ **Sustainable Farming**       | Organic, conservation, and natural farming practices                             |
| 👨‍👩‍👧 **Family / Multi-Farm** | Support for multiple farm plots and family member profiles                       |
| ⚙️ **Editable Agent**            | Customise AI persona, tone, safety rules, and response behaviour                 |

---

## 🏗️ Project Architecture

```text
Farmer
   │
   ▼
Web Interface
(HTML / CSS / JavaScript)
   │
   ▼
Flask Backend
(app.py)
   │
   ├── Soil Analysis
   ├── Irrigation Advisory
   ├── Fertilizer Planning
   ├── Pest & Disease Advisory
   ├── Weather Advisory
   ├── Crop Planning
   ├── Government Schemes
   ├── Cost Estimation
   └── Sustainable Farming
          │
          ▼
   Farming Advisor Modules
          │
          ▼
   IBM watsonx.ai
          │
          ▼
   IBM Granite Model
   (ibm/granite-3-3-8b-instruct)
          │
          ▼
 Personalized Farming Advice
          │
          ▼
       Farmer
```

---

## 📁 Project Structure

```text
smart-farming-agent/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── modules/
│   ├── __init__.py
│   ├── agent_instructions.py
│   ├── watsonx_client.py
│   └── farming_advisor.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── profile.html
│   └── agent_settings.html
│
└── static/
    ├── css/
    │   └── main.css
    │
    └── js/
        ├── main.js
        ├── chatbot.js
        ├── dashboard.js
        └── profile.js
```

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive Web UI

### Backend

* Python
* Flask
* REST APIs

### AI

* IBM watsonx.ai
* IBM Granite
* `ibm/granite-3-3-8b-instruct`

### Configuration

* Environment variables
* `.env`
* IBM Cloud API Key
* watsonx.ai Project ID

---

## 📋 Prerequisites

Before running the project, install:

* Python 3.11 or above
* IBM Cloud account
* IBM watsonx.ai access
* watsonx.ai Project ID
* IBM Cloud API Key

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/pavan09876519/Farming-Advice-Agent.git
cd Farming-Advice-Agent
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

```env
WATSONX_API_KEY=your-ibm-cloud-api-key
WATSONX_PROJECT_ID=your-watsonx-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct
FLASK_SECRET_KEY=your-secret-key
```

**Never commit your `.env` file to GitHub.**

### 5. Run the application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

## 🤖 AI Agent — KisanMitra

The project includes an AI farming assistant called **KisanMitra**.

KisanMitra helps farmers with:

* Crop-related questions
* Soil analysis
* Irrigation planning
* Fertilizer recommendations
* Pest and disease management
* Weather-based farming actions
* Crop planning
* Government schemes
* Cost estimation
* Sustainable farming practices

The AI agent can also be customised through:

```text
modules/agent_instructions.py
```

---

## ⚙️ Agent Customization

The following settings can be modified:

| Setting                      | Purpose                             |
| ---------------------------- | ----------------------------------- |
| `AGENT_NAME`                 | Display name of the AI agent        |
| `AGENT_PERSONA`              | AI identity and communication style |
| `EXPERTISE_DOMAINS`          | Agricultural knowledge areas        |
| `TONE_GUIDELINES`            | Communication style                 |
| `INDIAN_AGRICULTURE_CONTEXT` | Indian agricultural context         |
| `SAFETY_RULES`               | Safety and ethical rules            |
| `RESPONSE_FORMAT`            | Response structure                  |
| `MULTI_FARM_CONTEXT`         | Multi-farm and family behaviour     |

After modifying these settings, restart the Flask server.

---

## 🔌 API Reference

| Method | Endpoint                   | Description                         |
| ------ | -------------------------- | ----------------------------------- |
| GET    | `/api/health`              | Health check and model status       |
| GET    | `/api/profile`             | Get farmer profile                  |
| POST   | `/api/profile`             | Save farmer profile                 |
| DELETE | `/api/profile`             | Delete profile and chat history     |
| POST   | `/api/chat`                | Send multi-turn chat message        |
| GET    | `/api/chat/history`        | Get conversation history            |
| POST   | `/api/soil/analyse`        | Soil analysis and recommendations   |
| POST   | `/api/irrigation/schedule` | Generate irrigation schedule        |
| POST   | `/api/fertilizer/plan`     | Generate fertilizer management plan |
| POST   | `/api/pest/advice`         | Pest and disease IPM advice         |
| POST   | `/api/weather/advisory`    | Weather-based farming advice        |
| POST   | `/api/crop/plan`           | Seasonal crop planning              |
| POST   | `/api/schemes`             | Government scheme information       |
| POST   | `/api/cost/estimate`       | Cost-benefit analysis               |
| POST   | `/api/sustainable`         | Sustainable farming recommendations |
| GET    | `/api/agent/settings`      | View current agent settings         |

---

## 🌱 Main Farming Advisory Modules

### Soil Analysis

The system analyses:

* Nitrogen
* Phosphorus
* Potassium
* pH
* Organic matter

It then provides soil improvement recommendations.

### Irrigation Advisory

The system generates irrigation schedules based on:

* Crop
* Growth stage
* Irrigation method
* Water management requirements

### Fertilizer Planning

Provides:

* Fertilizer dosage
* Split application schedule
* Chemical fertilizer options
* Organic fertilizer options

### Pest & Disease Advisory

Provides:

* Pest and disease guidance
* Diagnosis support
* Integrated Pest Management (IPM)
* Treatment recommendations

### Weather Advisory

Provides weather-based farming actions for different crop stages.

### Crop Planning

Provides:

* Seasonal crop recommendations
* Crop planning
* Input planning
* Cost estimation

### Government Schemes

Provides information about:

* PM-KISAN
* PMFBY
* KCC
* State government schemes

### Cost Estimation

Provides:

* Input cost estimation
* Revenue estimation
* Break-even analysis

### Sustainable Farming

Provides recommendations related to:

* Organic farming
* Conservation practices
* Natural farming
* Long-term soil health

---

## ☁️ IBM watsonx.ai Integration

The project uses **IBM watsonx.ai** as the AI platform and **IBM Granite** as the foundation model.

Configured model:

```text
ibm/granite-3-3-8b-instruct
```

watsonx.ai is accessed through the project configuration and IBM Cloud credentials.

---

## 🔐 Security

The project follows basic security practices:

* `.env` is excluded through `.gitignore`
* API keys are stored as environment variables
* Flask secret key is configurable
* Debug mode should be disabled in production
* HTTPS should be used in production
* Redis can be used instead of in-memory sessions for scaling

**Never upload API keys or secret credentials to GitHub.**

---

## 🚀 Production Deployment

The application can be deployed using:

* Gunicorn
* Docker
* IBM Code Engine

### Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

```bash
docker build -t smart-farming-agent .
docker run -p 5000:5000 --env-file .env smart-farming-agent
```

### IBM Code Engine

The application can also be deployed using IBM Cloud Code Engine with the required environment variables and secrets.

---

## 🔮 Future Scope

Possible future improvements include:

* Real-time weather API integration
* Live mandi/market price integration
* Regional-language voice interaction
* Mobile application
* Image-based crop disease detection
* More personalised recommendations
* Integration with additional agricultural data sources
* Advanced RAG-based agricultural knowledge retrieval
* IoT-based soil and field monitoring

---

## 👨‍🌾 Farmer Support

### Kisan Call Centre

```text
1800-180-1551
```

### PM-KISAN

```text
155261
011-24300606
```

### Crop Insurance – PMFBY

```text
1800-200-7710
```

---

## 📌 Important Indian Agriculture Portals

* Soil Health Card
* eNAM
* PM-KISAN
* PMFBY

---

## 📜 License

MIT License

---

## ❤️ Project

**Smart Farming Advice Agent 🌾**

Built for Indian farmers using:

**Python + Flask + IBM watsonx.ai + IBM Granite**

### GitHub Repository

https://github.com/pavan09876519/Farming-Advice-Agent.git
