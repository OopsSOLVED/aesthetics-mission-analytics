<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Prophet-1.1+-0078D4?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<h1 align="center">🏠 AESTHETICS MISSION Analytics Dashboard</h1>

<p align="center">
  <strong>A production-ready business analytics platform for interior designing companies</strong><br>
  <em>Real-time KPIs · Interactive Maps · Revenue Forecasting · AI Design Generation</em>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-screenshots">Screenshots</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-api-reference">API</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## 📖 Overview

**AESTHETICS MISSION Analytics Dashboard** is a comprehensive, enterprise-grade business intelligence platform purpose-built for interior designing companies operating in Kerala, India. The dashboard transforms raw lead data into actionable insights through interactive visualizations, geospatial mapping, predictive forecasting, and AI-powered design generation.

### Who is this for?

| Role | Use Case |
|------|----------|
| **Business Managers** | Track KPIs, monitor team performance, forecast revenue |
| **Sales Teams** | Analyze lead sources, conversion funnels, city-wise performance |
| **Marketing Teams** | Identify high-ROI channels, optimize ad spend allocation |
| **Designers** | Generate AI-powered interior design concepts for client pitches |

---

## ✨ Features

### 📊 Business Intelligence Dashboard
- **9 Real-time KPI Cards** — Total leads, revenue, conversion rate, top performers
- **Interactive Plotly Charts** — Revenue by source, department distribution, lead stage breakdown
- **Monthly Revenue Trends** — Dual-axis chart with revenue overlay on lead count
- **Team Performance Heatmap** — Person × Month revenue matrix with custom color scale

### 🗺️ Geospatial Analytics
- **Folium Interactive Map** — Customer locations across 10 Kerala cities
- **Marker Clustering** — Auto-grouped markers with color-coded lead stages
- **Revenue Heatmap Overlay** — Geographic revenue density visualization
- **Multi-filter Support** — Filter by lead stage and business type simultaneously

### 🔮 Predictive Forecasting
- **Prophet-powered Revenue Forecasting** — 5-month revenue predictions with confidence intervals
- **Automated Business Insights** — AI-generated growth analysis and strategic recommendations
- **Actionable Manager Summaries** — Training opportunities, budget allocation suggestions
- **Quick Action Items** — Prioritized monthly tasks for the management team

### 🎨 AI Interior Design Generator
- **Pollinations.ai Integration** — Free, no API key required, instant image generation
- **8 Style Presets** — Modern, Traditional Kerala, Minimalist, Luxury, Scandinavian, etc.
- **8 Room Types** — Living Room, Kitchen, Bedroom, Pooja Room, and more
- **Batch Generation** — Generate up to 4 design concepts at once with download support

### 🔐 Authentication System
- **Dual-mode Authentication** — `streamlit-authenticator` with automatic fallback
- **Session Management** — Persistent login state with cookie support
- **Demo Credentials** — Quick access for demonstration purposes

### 🔍 Data Explorer
- **Searchable Data Table** — Full-text search across all columns
- **Statistical Summary** — Descriptive statistics and column type analysis
- **Data Quality Dashboard** — Null percentage visualization, duplicate detection, phone validation

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/OopsSOLVED/aesthetics-mission-analytics.git
cd aesthetics-mission-analytics

# 2. Create a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py
```

The dashboard will open at **http://localhost:8501**

### Demo Login

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `aesthetics123` |

### Using Your Own Data

1. Prepare a CSV or Excel file with the [required columns](#-data-schema)
2. Login to the dashboard
3. Use the **📁 Data Upload** section in the sidebar
4. Alternatively, use the built-in sample data (500 records)

---

## 📐 Architecture

```
aesthetics-mission-analytics/
├── app.py                      # Main application (1526 lines)
│   ├── GLOBAL_CSS              # Custom CSS design system
│   ├── Authentication          # Login flow with dual-mode auth
│   ├── Sidebar                 # Navigation, upload, preferences
│   ├── KPI Section             # Metric cards and sub-KPIs
│   ├── Charts Section          # Interactive Plotly visualizations
│   ├── Map Section             # Folium geospatial analytics
│   ├── Forecasting Section     # Prophet-based predictions
│   ├── AI Designer Section     # Pollinations.ai integration
│   └── Data Explorer           # Data table, stats, quality
├── generate_sample_data.py     # Realistic demo dataset generator
├── sample_leads_data.csv       # Pre-generated sample dataset (500 records)
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml             # Streamlit theme & server config
├── docs/
│   └── ARCHITECTURE.md         # Detailed architecture documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
└── .gitignore                  # Git ignore rules
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.30+ | Interactive web UI framework |
| **Visualization** | Plotly 5.18+ | Interactive charts and graphs |
| **Geospatial** | Folium 0.15+ | Interactive maps with marker clusters |
| **Forecasting** | Prophet 1.1+ | Time-series revenue prediction |
| **AI Generation** | Pollinations.ai | Free AI image generation API |
| **Authentication** | streamlit-authenticator | Session-based login with cookies |
| **Data Processing** | Pandas 2.0+ / NumPy | Data manipulation and analysis |
| **Styling** | Custom CSS | Glassmorphism dark theme with animations |

---

## 📋 Data Schema

The dashboard expects the following columns in your dataset:

| Column | Type | Description |
|--------|------|-------------|
| `sl_no` | Integer | Serial number |
| `date` | Date | Lead date (YYYY-MM-DD) |
| `source_of_leads` | String | Lead acquisition channel |
| `department` | String | Service department |
| `alloted_person` | String | Assigned team member |
| `contact_no` | String | Customer phone number |
| `customer_name` | String | Customer full name |
| `customer_business_name` | String | Business name (optional) |
| `business_type` | String | Individual / Corporate / Builder / etc. |
| `latitude` | Float | Customer location latitude |
| `longitude` | Float | Customer location longitude |
| `city` | String | Customer city |
| `work_requirement` | String | Type of interior work requested |
| `year` | Integer | Lead year |
| `month` | Integer | Lead month (1-12) |
| `phone_valid` | Boolean | Phone number validation status |
| `is_duplicate_lead` | Boolean | Duplicate lead flag |
| `stage_clean_norm` | String | Normalized lead stage |
| `final_lead_stage` | String | Final outcome (Won/Lost/Follow-up/etc.) |
| `Revenue` | Float | Revenue amount in INR (₹) |

---

## ⚙️ Configuration

### Streamlit Theme (`.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#0f0f23"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#e0e0ff"
font = "sans serif"
```

### Authentication

Default credentials are defined in `app.py`. For production, update:

```python
VALID_USERNAME = "your_username"
VALID_PASSWORD = "your_secure_password"
VALID_NAME = "Your Name"
```

> ⚠️ **Security Note**: For production deployments, use environment variables or Streamlit secrets management instead of hardcoded credentials.

---

## 🧪 Generate Sample Data

To regenerate the sample dataset:

```bash
python generate_sample_data.py
```

This creates `sample_leads_data.csv` with 500 realistic records including:
- 10 Kerala cities with real coordinates
- 10 lead sources with weighted probability distributions
- 5 service departments
- 7 lead stages with revenue correlation
- Realistic Indian names and business names

---

## 🚢 Deployment

### Streamlit Community Cloud (Free)

1. Push this repository to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set `app.py` as the main file
5. Deploy!

### Docker (Self-hosted)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t aesthetics-mission .
docker run -p 8501:8501 aesthetics-mission
```

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on the process for submitting pull requests.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Akash Helel**

- GitHub: [@OopsSOLVED](https://github.com/OopsSOLVED)
- Email: akash666helel@gmail.com

---

<p align="center">
  <strong>Built with ❤️ for Interior Excellence</strong><br>
  <em>© 2025 AESTHETICS MISSION Interior Designing Company</em>
</p>
