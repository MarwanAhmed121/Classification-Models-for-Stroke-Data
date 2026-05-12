# ClassifyAI — Flask ML Classification Dashboard

A production-ready Flask web application for exploring and comparing 15 classification models on the Stroke Prediction dataset.

## Features
- **Home** — animated hero, feature cards, model category overview
- **Dashboard** — stat cards, interactive Chart.js bar/doughnut charts, top-5 table
- **Models** — full sortable/searchable table, train/test toggle, per-model radar chart modal
- **Upload** — drag-and-drop CSV upload with preview
- **Auth** — login, register with password strength meter, session management
- **Dark/Light Mode** — persisted to localStorage
- **REST API** — `/api/models` and `/api/models/<name>` JSON endpoints

## Quick Start

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the development server
python app.py
```

Open **http://localhost:5000** in your browser.

## Demo Login
| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

## Project Structure
```
flask_app/
├── app.py                  # Flask routes, API endpoints, session management
├── requirements.txt
├── templates/
│   ├── base.html           # Layout, navbar, toasts, footer
│   ├── index.html          # Landing page
│   ├── dashboard.html      # Stats + charts
│   ├── models.html         # Full comparison table
│   ├── upload.html         # File upload
│   ├── login.html
│   ├── register.html
│   └── error.html
└── static/
    ├── css/main.css        # Full design system (dark/light, responsive)
    └── js/main.js          # Theme toggle, animations, navbar
```

## API Endpoints
| Endpoint                  | Description                    |
|---------------------------|--------------------------------|
| `GET /api/models`         | All model metrics as JSON      |
| `GET /api/models/<name>`  | Single model metrics           |
| `GET /api/chart/comparison` | Chart data (labels + metrics) |

## Production Notes
- Replace the in-memory `USERS` dict with SQLAlchemy + PostgreSQL
- Set `SECRET_KEY` via environment variable
- Use Gunicorn: `gunicorn -w 4 app:app`
- Serve static files via Nginx
