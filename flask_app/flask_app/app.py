"""
ClassifyAI - Flask ML Classification Dashboard
Main application entry point
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
import os
import json
from datetime import datetime
import random

# ── App Configuration ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

# ── In-memory "database" (replace with SQLAlchemy in production) ───────────────
USERS = {
    "admin": {
        "password": "admin123",
        "name": "Admin User",
        "role": "admin",
        "email": "admin@classifyai.io",
        "avatar": "A",
    }
}

# Simulated model results matching the notebook's classification models
MODEL_RESULTS = {
    "Logistic Regression":         {"train_acc": 0.9512, "test_acc": 0.9489, "train_f1": 0.1823, "test_f1": 0.1512, "roc_auc": 0.8421, "pr_auc": 0.2341, "train_prec": 0.7143, "test_prec": 0.6667, "train_recall": 0.1023, "test_recall": 0.0889, "train_bal_acc": 0.5495, "test_bal_acc": 0.5427, "category": "linear"},
    "KNN":                         {"train_acc": 0.9701, "test_acc": 0.9412, "train_f1": 0.5614, "test_f1": 0.1923, "roc_auc": 0.7912, "pr_auc": 0.1876, "train_prec": 0.6923, "test_prec": 0.5882, "train_recall": 0.4712, "test_recall": 0.1111, "train_bal_acc": 0.7201, "test_bal_acc": 0.5498, "category": "distance"},
    "SVC":                         {"train_acc": 0.9521, "test_acc": 0.9503, "train_f1": 0.2134, "test_f1": 0.1684, "roc_auc": 0.8634, "pr_auc": 0.2512, "train_prec": 0.7812, "test_prec": 0.7143, "train_recall": 0.1234, "test_recall": 0.1000, "train_bal_acc": 0.5589, "test_bal_acc": 0.5472, "category": "svm"},
    "Decision Tree":               {"train_acc": 1.0000, "test_acc": 0.9321, "train_f1": 1.0000, "test_f1": 0.1923, "roc_auc": 0.7234, "pr_auc": 0.1534, "train_prec": 1.0000, "test_prec": 0.4167, "train_recall": 1.0000, "test_recall": 0.1333, "train_bal_acc": 1.0000, "test_bal_acc": 0.5543, "category": "tree"},
    "Naive Bayes":                 {"train_acc": 0.8934, "test_acc": 0.8923, "train_f1": 0.3241, "test_f1": 0.3012, "roc_auc": 0.8123, "pr_auc": 0.2234, "train_prec": 0.4312, "test_prec": 0.4167, "train_recall": 0.2589, "test_recall": 0.2333, "train_bal_acc": 0.6634, "test_bal_acc": 0.6523, "category": "bayes"},
    "Random Forest":               {"train_acc": 1.0000, "test_acc": 0.9534, "train_f1": 1.0000, "test_f1": 0.2341, "roc_auc": 0.8912, "pr_auc": 0.2867, "train_prec": 1.0000, "test_prec": 0.6923, "train_recall": 1.0000, "test_recall": 0.1444, "train_bal_acc": 1.0000, "test_bal_acc": 0.5684, "category": "ensemble"},
    "Extra Trees":                 {"train_acc": 1.0000, "test_acc": 0.9521, "train_f1": 1.0000, "test_f1": 0.2134, "roc_auc": 0.8789, "pr_auc": 0.2734, "train_prec": 1.0000, "test_prec": 0.7143, "train_recall": 1.0000, "test_recall": 0.1333, "train_bal_acc": 1.0000, "test_bal_acc": 0.5634, "category": "ensemble"},
    "AdaBoost":                    {"train_acc": 0.9534, "test_acc": 0.9489, "train_f1": 0.3012, "test_f1": 0.2134, "roc_auc": 0.8634, "pr_auc": 0.2456, "train_prec": 0.6923, "test_prec": 0.6364, "train_recall": 0.1934, "test_recall": 0.1333, "train_bal_acc": 0.5923, "test_bal_acc": 0.5627, "category": "boosting"},
    "Gradient Boosting":           {"train_acc": 0.9634, "test_acc": 0.9521, "train_f1": 0.4512, "test_f1": 0.2341, "roc_auc": 0.8823, "pr_auc": 0.2712, "train_prec": 0.7812, "test_prec": 0.6667, "train_recall": 0.3212, "test_recall": 0.1556, "train_bal_acc": 0.6523, "test_bal_acc": 0.5723, "category": "boosting"},
    "Hist Gradient Boosting":      {"train_acc": 0.9678, "test_acc": 0.9534, "train_f1": 0.4923, "test_f1": 0.2512, "roc_auc": 0.8912, "pr_auc": 0.2845, "train_prec": 0.8012, "test_prec": 0.6923, "train_recall": 0.3523, "test_recall": 0.1667, "train_bal_acc": 0.6712, "test_bal_acc": 0.5789, "category": "boosting"},
    "XGBoost":                     {"train_acc": 0.9912, "test_acc": 0.9543, "train_f1": 0.8912, "test_f1": 0.2512, "roc_auc": 0.8956, "pr_auc": 0.2912, "train_prec": 0.9234, "test_prec": 0.7143, "train_recall": 0.8612, "test_recall": 0.1667, "train_bal_acc": 0.9298, "test_bal_acc": 0.5789, "category": "boosting"},
    "CatBoost":                    {"train_acc": 0.9689, "test_acc": 0.9543, "train_f1": 0.5234, "test_f1": 0.2612, "roc_auc": 0.8934, "pr_auc": 0.2934, "train_prec": 0.8123, "test_prec": 0.7143, "train_recall": 0.3834, "test_recall": 0.1778, "train_bal_acc": 0.6845, "test_bal_acc": 0.5851, "category": "boosting"},
    "LightGBM":                    {"train_acc": 0.9745, "test_acc": 0.9556, "train_f1": 0.5712, "test_f1": 0.2734, "roc_auc": 0.8967, "pr_auc": 0.2978, "train_prec": 0.8234, "test_prec": 0.7692, "train_recall": 0.4312, "test_recall": 0.1889, "train_bal_acc": 0.7034, "test_bal_acc": 0.5912, "category": "boosting"},
    "Voting Classifier":           {"train_acc": 0.9712, "test_acc": 0.9556, "train_f1": 0.5423, "test_f1": 0.2812, "roc_auc": 0.9012, "pr_auc": 0.3012, "train_prec": 0.8123, "test_prec": 0.7500, "train_recall": 0.4123, "test_recall": 0.2000, "train_bal_acc": 0.6934, "test_bal_acc": 0.5967, "category": "ensemble"},
    "Stacking Classifier":         {"train_acc": 0.9823, "test_acc": 0.9568, "train_f1": 0.7234, "test_f1": 0.2934, "roc_auc": 0.9045, "pr_auc": 0.3145, "train_prec": 0.8812, "test_prec": 0.7692, "train_recall": 0.6112, "test_recall": 0.2111, "train_bal_acc": 0.7989, "test_bal_acc": 0.6012, "category": "ensemble"},
}

# ── Auth helpers ───────────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ── Public Routes ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    """Landing / Home page"""
    return render_template("index.html", active="home")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = USERS.get(username)

        if user and user["password"] == password:
            session["username"] = username
            session["name"] = user["name"]
            session["role"] = user["role"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html", active="login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page"""
    if request.method == "POST":
        username  = request.form.get("username", "").strip()
        email     = request.form.get("email", "").strip()
        name      = request.form.get("name", "").strip()
        password  = request.form.get("password", "")
        confirm   = request.form.get("confirm_password", "")

        if not all([username, email, name, password, confirm]):
            flash("All fields are required.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
        elif username in USERS:
            flash("Username already exists.", "error")
        else:
            USERS[username] = {
                "password": password,
                "name": name,
                "role": "user",
                "email": email,
                "avatar": name[0].upper(),
            }
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("login"))

    return render_template("register.html", active="register")


@app.route("/logout")
def logout():
    """Logout and clear session"""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# ── Protected Routes ───────────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    """Main dashboard with stats overview"""
    best_model  = max(MODEL_RESULTS, key=lambda m: MODEL_RESULTS[m]["roc_auc"])
    best_roc    = MODEL_RESULTS[best_model]["roc_auc"]
    avg_acc     = sum(v["test_acc"] for v in MODEL_RESULTS.values()) / len(MODEL_RESULTS)
    total_models = len(MODEL_RESULTS)

    stats = {
        "total_models":  total_models,
        "best_model":    best_model,
        "best_roc":      f"{best_roc:.4f}",
        "avg_accuracy":  f"{avg_acc:.4f}",
        "dataset":       "Stroke Prediction",
        "features":      10,
        "samples":       5110,
    }
    return render_template("dashboard.html", active="dashboard", stats=stats,
                           results=MODEL_RESULTS)


@app.route("/models")
@login_required
def models():
    """Models comparison table"""
    sort_by = request.args.get("sort", "roc_auc")
    order   = request.args.get("order", "desc")
    search  = request.args.get("search", "").lower()

    filtered = {k: v for k, v in MODEL_RESULTS.items()
                if search in k.lower()} if search else MODEL_RESULTS

    reverse  = (order == "desc")
    sorted_results = dict(
        sorted(filtered.items(),
               key=lambda x: x[1].get(sort_by, 0),
               reverse=reverse)
    )

    return render_template("models.html", active="models",
                           results=sorted_results, sort_by=sort_by,
                           order=order, search=search)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """File upload page"""
    uploaded_file = None
    if request.method == "POST":
        f = request.files.get("dataset")
        if f and f.filename:
            filename     = f.filename
            uploaded_file = {
                "name": filename,
                "size": "—",
                "rows": random.randint(3000, 8000),
                "cols": random.randint(8, 20),
                "time": datetime.now().strftime("%H:%M:%S"),
            }
            flash(f"File '{filename}' uploaded successfully!", "success")
        else:
            flash("No file selected.", "error")
    return render_template("upload.html", active="upload", file=uploaded_file)


# ── REST API ───────────────────────────────────────────────────────────────────
@app.route("/api/models")
@login_required
def api_models():
    """Return all model results as JSON"""
    return jsonify({"status": "ok", "data": MODEL_RESULTS})


@app.route("/api/models/<name>")
@login_required
def api_model_detail(name):
    """Return single model metrics"""
    model = MODEL_RESULTS.get(name)
    if not model:
        return jsonify({"status": "error", "message": "Model not found"}), 404
    return jsonify({"status": "ok", "name": name, "metrics": model})


@app.route("/api/chart/comparison")
@login_required
def api_chart_comparison():
    """JSON for bar chart – ROC-AUC comparison"""
    data = {
        "labels": list(MODEL_RESULTS.keys()),
        "roc_auc": [v["roc_auc"] for v in MODEL_RESULTS.values()],
        "test_acc": [v["test_acc"] for v in MODEL_RESULTS.values()],
        "test_f1":  [v["test_f1"]  for v in MODEL_RESULTS.values()],
    }
    return jsonify(data)


# ── Error Handlers ─────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", code=404,
                           message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", code=500,
                           message="Internal server error"), 500


# ── Context processor – inject current year into all templates ─────────────────
@app.context_processor
def inject_globals():
    return {"year": datetime.now().year}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
