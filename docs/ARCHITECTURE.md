# 🏗️ Architecture Documentation

> Detailed technical architecture of the AESTHETICS MISSION Analytics Dashboard

---

## Table of Contents

- [System Overview](#system-overview)
- [Application Flow](#application-flow)
- [Module Architecture](#module-architecture)
- [Data Pipeline](#data-pipeline)
- [Authentication Flow](#authentication-flow)
- [Visualization Engine](#visualization-engine)
- [AI Integration](#ai-integration)
- [Design System](#design-system)
- [Performance Considerations](#performance-considerations)
- [Security](#security)

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Streamlit Frontend (WebSocket connection)                   │   │
│  │  ┌────────────┐ ┌──────────┐ ┌────────────┐ ┌────────────┐ │   │
│  │  │ Dashboard  │ │ Map View │ │ Forecasting│ │ AI Designer│ │   │
│  │  └────────────┘ └──────────┘ └────────────┘ └────────────┘ │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────────┘
                             │ WebSocket
┌────────────────────────────┴────────────────────────────────────────┐
│                     STREAMLIT SERVER (Python)                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  app.py — Single-file Application                            │   │
│  │                                                              │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │   │
│  │  │   Auth      │  │  Data Engine │  │  Visualization     │  │   │
│  │  │   Module    │  │  (Pandas)    │  │  Engine (Plotly)   │  │   │
│  │  └─────────────┘  └──────────────┘  └────────────────────┘  │   │
│  │                                                              │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │   │
│  │  │   Map       │  │  Forecasting │  │  AI Image          │  │   │
│  │  │   (Folium)  │  │  (Prophet)   │  │  (Pollinations)   │  │   │
│  │  └─────────────┘  └──────────────┘  └────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌──────────────┐   ┌─────────────────┐   ┌──────────────────┐
│  CSV/Excel   │   │  Prophet Model  │   │  Pollinations.ai │
│  Data Files  │   │  (In-memory)    │   │  (External API)  │
└──────────────┘   └─────────────────┘   └──────────────────┘
```

---

## Application Flow

```
                    ┌───────────────────┐
                    │    User Opens     │
                    │   localhost:8501  │
                    └────────┬──────────┘
                             │
                    ┌────────▼──────────┐
                    │  Session State    │
                    │  Initialization   │
                    └────────┬──────────┘
                             │
                    ┌────────▼──────────┐
                    │  Authentication   │──── Not Authenticated
                    │  Check            │     │
                    └────────┬──────────┘     ▼
                             │          ┌─────────────┐
                    Authenticated       │ Login Page  │
                             │          └─────────────┘
                    ┌────────▼──────────┐
                    │  Render Sidebar   │
                    │  (Upload/Config)  │
                    └────────┬──────────┘
                             │
                    ┌────────▼──────────┐
                    │  Load & Clean     │
                    │  Data             │
                    └────────┬──────────┘
                             │
           ┌─────────┬──────┴───────┬──────────┬────────────┐
           ▼         ▼             ▼          ▼            ▼
      ┌─────────┐ ┌──────┐ ┌───────────┐ ┌────────┐ ┌──────────┐
      │Dashboard│ │ Map  │ │Forecasting│ │  AI    │ │  Data    │
      │  Tab    │ │ Tab  │ │   Tab     │ │Designer│ │ Explorer │
      └─────────┘ └──────┘ └───────────┘ └────────┘ └──────────┘
```

---

## Module Architecture

### `app.py` — Core Application (1526 lines)

The application follows a **functional architecture** with clearly separated concerns:

| Line Range | Module | Responsibility |
|-----------|--------|---------------|
| 1–32 | **Imports** | All dependency imports |
| 37–42 | **Page Config** | Streamlit page settings |
| 47–389 | **Design System** | Complete CSS with variables, animations, glassmorphism |
| 394–404 | **Visual Layer** | Background gradients and animated orbs |
| 411–549 | **Helper Functions** | `generate_sample_data()`, `clean_data()`, `render_metric_card()`, `plotly_theme()`, `format_inr()` |
| 556–672 | **Authentication** | YAML config, login page, dual-mode auth |
| 679–757 | **Sidebar** | File upload, preferences, info panel |
| 764–807 | **KPI Section** | 4 primary + 5 secondary metric cards |
| 814–948 | **Charts Section** | Bar charts, pie charts, trend lines, heatmap |
| 955–1057 | **Map Section** | Folium map with markers, heatmap, filters |
| 1064–1219 | **Forecasting** | Prophet model, forecast chart, business insights |
| 1226–1348 | **AI Designer** | Pollinations.ai integration, batch generation |
| 1354–1416 | **Data Explorer** | Search, stats, quality dashboard |
| 1423–1526 | **Main Controller** | Application entry point, tab routing |

### `generate_sample_data.py` — Data Generator (103 lines)

Standalone script for generating realistic Kerala-based interior design lead data:

- 30 Kerala first names + 20 surnames for realistic customer names
- 10 business suffixes for company names
- Weighted probability distributions matching real-world patterns
- Revenue correlated with lead stage (Won = ₹50K–₹25L, Lost = ₹0)

---

## Data Pipeline

```
  ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
  │ CSV / Excel  │────▶│  Pandas     │────▶│  Cleaned     │
  │ Upload       │     │  read_csv() │     │  DataFrame   │
  └──────────────┘     └─────────────┘     └──────┬───────┘
                                                  │
  ┌──────────────┐                                │
  │ Sample Data  │────────────────────────────────▶│
  │ Generator    │                                │
  └──────────────┘                                │
                                                  │
                              ┌────────────────────┘
                              ▼
                    ┌──────────────────┐
                    │   clean_data()   │
                    │                  │
                    │  • Fill nulls    │
                    │  • Parse dates   │
                    │  • Revenue→num   │
                    │  • Detect dupes  │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────────┐
              ▼              ▼                  ▼
        ┌──────────┐  ┌───────────┐     ┌────────────┐
        │ Session  │  │ Plotly    │     │ Prophet    │
        │ State    │  │ Charts   │     │ Forecast   │
        │ Cache    │  │          │     │            │
        └──────────┘  └───────────┘     └────────────┘
```

### Data Cleaning Pipeline (`clean_data()`)

| Step | Operation | Details |
|------|-----------|---------|
| 1 | **Null Handling** | Object columns → "Unknown", Numeric columns → 0 |
| 2 | **Date Parsing** | `pd.to_datetime()` with error coercion, extract year/month |
| 3 | **Revenue Normalization** | Cast to numeric, coerce errors to 0 |
| 4 | **Duplicate Detection** | Count via `is_duplicate_lead` boolean column |

---

## Authentication Flow

```
┌─────────────┐
│  User Visit │
└──────┬──────┘
       ▼
┌──────────────────────────────┐
│  Try streamlit-authenticator │
│  (v0.3.x / v0.4.x)          │
└──────┬──────────┬────────────┘
       │ Success  │ ImportError / Exception
       ▼          ▼
┌─────────────┐  ┌─────────────────────┐
│ Cookie-based│  │  Manual Fallback    │
│ Auth with   │  │  st.form() Login    │
│ Hashed PWs  │  │  Plain comparison   │
└──────┬──────┘  └──────────┬──────────┘
       │                    │
       └────────┬───────────┘
                ▼
       ┌─────────────────┐
       │  Session State   │
       │  authentication_ │
       │  status = True   │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │   Dashboard     │
       │   Rendered      │
       └─────────────────┘
```

### Key Design Decisions

- **Dual-mode authentication**: The system tries `streamlit-authenticator` first (supports cookies, password hashing). If it fails (version incompatibility, missing dependency), it falls back to a manual `st.form()` login.
- **Version compatibility**: Handles both v0.3.x (returns tuple) and v0.4.x (sets session state directly) APIs.

---

## Visualization Engine

### Chart Theme System

All charts use the `plotly_theme()` function for consistent styling:

```python
def plotly_theme(fig, title=""):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",     # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",       # Transparent plot area
        font=dict(family="Inter", color="#b8b8d0"),
        # ... grid lines, hover labels, margins
    )
```

### Color Palette

| Variable | Hex | Usage |
|----------|-----|-------|
| `--primary` | `#667eea` | Primary brand color, main gradients |
| `--secondary` | `#764ba2` | Secondary brand color |
| `--accent` | `#f093fb` | Accent highlights, forecast lines |
| `--success` | `#2ecc71` | Positive indicators |
| `--danger` | `#e74c3c` | Negative indicators, alerts |
| `--warning` | `#f39c12` | Warnings, attention items |

### Chart Types

| Chart | Library | Data Aggregation |
|-------|---------|-------------------|
| Revenue by Source | Plotly Bar (H) | `groupby("source_of_leads").sum()` |
| Revenue by Business | Plotly Bar (H) | `groupby("business_type").sum()` |
| Department Distribution | Plotly Donut | `value_counts()` |
| Lead Stage Breakdown | Plotly Donut | `value_counts()` |
| Monthly Revenue Trend | Plotly Dual-axis | `groupby(period).agg()` |
| Team Heatmap | Plotly Heatmap | `pivot_table(person × month)` |
| Forecast | Plotly Scatter+Fill | Prophet model output |

---

## AI Integration

### Pollinations.ai Architecture

```
┌────────────────┐     ┌──────────────────────────────────┐
│  User Input    │     │  Prompt Engineering               │
│                │     │                                    │
│  • Text prompt │────▶│  "{style} {room} interior design, │
│  • Style       │     │   {user_prompt}, professional     │
│  • Room type   │     │   photography, 8k, ultra          │
│  • Count       │     │   realistic..."                   │
└────────────────┘     └────────────┬─────────────────────┘
                                   │
                       ┌───────────▼───────────────┐
                       │  Pollinations.ai API      │
                       │                           │
                       │  GET /prompt/{encoded}    │
                       │  ?width=768               │
                       │  &height=768              │
                       │  &seed={random}           │
                       │  &nologo=true             │
                       └───────────┬───────────────┘
                                   │
                       ┌───────────▼───────────────┐
                       │  Image Bytes Response     │
                       │  (PNG, > 1KB validation)  │
                       └───────────┬───────────────┘
                                   │
                       ┌───────────▼───────────────┐
                       │  st.image() + Download    │
                       └───────────────────────────┘
```

### Key Properties

- **Cost**: Free, no API key required
- **Timeout**: 120 seconds per image
- **Validation**: Response must be > 1000 bytes (filters error pages)
- **Seed System**: Random seed per image ensures variety; same seed = reproducible output

---

## Design System

### CSS Architecture

The design system is implemented as a single `GLOBAL_CSS` string (342 lines) injected via `st.markdown()`:

```
GLOBAL_CSS
├── Google Fonts Import (Inter, Outfit)
├── CSS Custom Properties (:root)
│   ├── Colors (primary, secondary, accent, etc.)
│   ├── Backgrounds (dark-bg, card-bg, glass)
│   └── Gradients (6 predefined gradients)
├── Global Styles (.stApp)
├── Streamlit Overrides
│   ├── Hide MainMenu, footer, header
│   ├── Sidebar gradient background
│   └── Tab styling
├── Component Styles
│   ├── .metric-card (glassmorphism cards)
│   ├── .section-header (gradient text headers)
│   ├── .insight-box (analysis callouts)
│   ├── .strategy-box (green recommendation cards)
│   ├── .warning-box (amber action items)
│   ├── .dashboard-header (hero header)
│   └── .login-container (centered auth form)
├── Animations
│   ├── .orb (floating background spheres)
│   └── @keyframes float (translate + scale)
└── Utility Classes
    ├── .grad-1 through .grad-4
    ├── .map-container
    └── .download-btn
```

### Typography

| Font | Weight | Usage |
|------|--------|-------|
| **Outfit** | 700-800 | Headers, metric values, section titles |
| **Inter** | 300-600 | Body text, labels, UI elements |

---

## Performance Considerations

| Concern | Mitigation |
|---------|------------|
| **Large datasets** | Pandas operations are vectorized; no row-wise loops in charts |
| **Prophet training** | Wrapped in `st.spinner()` for user feedback; runs once per session |
| **Map rendering** | MarkerCluster groups markers to prevent DOM overload |
| **AI image generation** | 120s timeout; progress bar shows generation status |
| **Session state** | Data cached in `st.session_state` to avoid reloading on interactions |
| **CSS injection** | Single `st.markdown()` call for all styles (no per-component injection) |

---

## Security

| Layer | Implementation |
|-------|---------------|
| **Authentication** | Password hashing via `stauth.Hasher`, cookie-based sessions |
| **XSRF** | Disabled in config (typical for internal dashboards) |
| **Data Privacy** | All data processing happens server-side; no data sent to external services except AI prompts |
| **Credentials** | Hardcoded for demo; should use `st.secrets` or env vars in production |
| **API Calls** | Only outbound call is to Pollinations.ai for image generation (user-initiated) |

> ⚠️ **Production Recommendation**: Replace hardcoded credentials with environment variables or Streamlit secrets management. Enable XSRF protection for public-facing deployments.

---

## Dependencies Graph

```
app.py
├── streamlit              — Web framework
├── pandas                 — Data manipulation
├── numpy                  — Numerical operations
├── plotly                 — Interactive charts
│   ├── plotly.express     — High-level API
│   └── plotly.graph_objects — Low-level API
├── folium                 — Map rendering
│   └── streamlit_folium   — Streamlit integration
├── prophet                — Time-series forecasting
├── streamlit_authenticator — Authentication
├── PyYAML                 — Config parsing
├── requests               — HTTP client (AI API)
└── openpyxl               — Excel file support
```

---

*Last updated: April 2025*
