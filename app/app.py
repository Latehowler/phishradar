from flask import Flask, render_template, request, jsonify
import pickle
import re
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ── ML Models ──
vector = pickle.load(open("vectorizer.pkl", 'rb'))
model  = pickle.load(open("phishing.pkl", 'rb'))

DB_PATH = "reports.db"

VALID_THREAT_TYPES = {"phishing", "malware", "scam", "spoofing", "ransomware", "other"}
VALID_SEVERITIES   = {"low", "medium", "high", "critical"}


# ─────────────────────────────────────────
#  DATABASE
# ─────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                url          TEXT    NOT NULL,
                email        TEXT,
                threat_type  TEXT    NOT NULL,
                severity     TEXT    NOT NULL,
                details      TEXT,
                ml_result    TEXT,
                ml_confidence REAL,
                status       TEXT    DEFAULT 'pending',
                submitted_at TEXT    NOT NULL
            )
        """)
        conn.commit()


# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────

def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(re.match(pattern, url))


def is_valid_email(email: str) -> bool:
    if not email:
        return True
    return bool(re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email.strip()))


def run_ml_scan(url: str) -> dict:
    if not url.startswith("http"):
        url = "http://" + url

    if not is_valid_url(url):
        return {"label": "invalid", "text": "⚠️ Please enter a valid website URL", "css_class": "warn", "confidence": None}

    cleaned = re.sub(r'^https?://(www\.)?', '', url)
    X       = vector.transform([cleaned])
    proba   = model.predict_proba(X)[0]
    classes = model.classes_

    idx        = proba.argmax()
    prediction = classes[idx]
    confidence = round(proba[idx] * 100, 2)

    if prediction == 'bad':
        if confidence > 80:
            return {"label": "danger", "text": f"❌ Phishing detected ({confidence}%)",           "css_class": "danger", "confidence": confidence}
        else:
            return {"label": "warn",   "text": f"⚠️ Suspicious website ({confidence}%)",           "css_class": "warn",   "confidence": confidence}
    elif prediction == 'good':
        if confidence < 60:
            return {"label": "warn",   "text": f"⚠️ Possibly safe but uncertain ({confidence}%)", "css_class": "warn",   "confidence": confidence}
        else:
            return {"label": "safe",   "text": f"✅ Legit website ({confidence}%)",                "css_class": "safe",   "confidence": confidence}

    return {"label": "error", "text": "Something went wrong 🤨", "css_class": "warn", "confidence": None}


# ─────────────────────────────────────────
#  ROUTES — PAGES
# ─────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def index():
    predict = predict_css = scanned_url = None

    if request.method == "POST":
        url    = request.form.get("url", "").strip()
        result = run_ml_scan(url)
        predict     = result["text"]
        predict_css = result["css_class"]
        scanned_url = url

    return render_template("index.html", predict=predict, predict_css=predict_css, scanned_url=scanned_url)


@app.route("/report")
def report_page():
    return render_template("index.html", scroll_to_report=True)


@app.route("/about")
def about():
    return render_template("about.html")


# ─────────────────────────────────────────
#  ADMIN DASHBOARD
# ─────────────────────────────────────────

@app.route("/admin/reports")
def admin_reports():
    # Optional filters from query params: ?threat=phishing&severity=high&status=pending&q=someurl
    threat   = request.args.get("threat", "")
    severity = request.args.get("severity", "")
    status   = request.args.get("status", "")
    search   = request.args.get("q", "").strip()

    query  = "SELECT * FROM reports WHERE 1=1"
    params = []

    if threat:
        query += " AND threat_type = ?"; params.append(threat)
    if severity:
        query += " AND severity = ?";    params.append(severity)
    if status:
        query += " AND status = ?";      params.append(status)
    if search:
        query += " AND url LIKE ?";      params.append(f"%{search}%")

    query += " ORDER BY id DESC"

    with get_db() as conn:
        rows  = conn.execute(query, params).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
        counts = {
            "pending":  conn.execute("SELECT COUNT(*) FROM reports WHERE status='pending'").fetchone()[0],
            "reviewed": conn.execute("SELECT COUNT(*) FROM reports WHERE status='reviewed'").fetchone()[0],
            "danger":   conn.execute("SELECT COUNT(*) FROM reports WHERE ml_result='danger'").fetchone()[0],
        }

    reports = [dict(r) for r in rows]
    return render_template(
        "admin.html",
        reports=reports, total=total, counts=counts,
        filters={"threat": threat, "severity": severity, "status": status, "q": search}
    )


@app.route("/admin/reports/<int:report_id>/status", methods=["POST"])
def update_status(report_id):
    new_status = request.get_json(silent=True).get("status", "")
    if new_status not in {"pending", "reviewed", "dismissed"}:
        return jsonify({"success": False, "error": "Invalid status"}), 400

    with get_db() as conn:
        conn.execute("UPDATE reports SET status = ? WHERE id = ?", (new_status, report_id))
        conn.commit()

    return jsonify({"success": True})


@app.route("/admin/reports/<int:report_id>", methods=["DELETE"])
def delete_report(report_id):
    with get_db() as conn:
        conn.execute("DELETE FROM reports WHERE id = ?", (report_id,))
        conn.commit()
    return jsonify({"success": True})


# ─────────────────────────────────────────
#  API
# ─────────────────────────────────────────

@app.route("/api/scan", methods=["POST"])
def api_scan():
    data = request.get_json(silent=True) or {}
    url  = data.get("url", "").strip()
    if not url:
        return jsonify({"success": False, "error": "URL is required"}), 400
    result = run_ml_scan(url)
    return jsonify({"success": True, **result})


@app.route("/api/report", methods=["POST"])
def submit_report():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON payload"}), 400

    url         = data.get("url", "").strip()
    email       = data.get("email", "").strip()
    threat_type = data.get("threat_type", "").strip().lower()
    severity    = data.get("severity", "").strip().lower()
    details     = data.get("details", "").strip()

    errors = {}
    if not url:
        errors["url"] = "URL is required."
    elif not is_valid_url("http://" + url if not url.startswith("http") else url):
        errors["url"] = "Please enter a valid URL."
    if email and not is_valid_email(email):
        errors["email"] = "Please enter a valid email address."
    if not threat_type or threat_type not in VALID_THREAT_TYPES:
        errors["threat_type"] = "Please select a valid threat type."
    if not severity or severity not in VALID_SEVERITIES:
        errors["severity"] = "Please select a severity level."
    if len(details) > 500:
        errors["details"] = "Details must be 500 characters or fewer."

    if errors:
        return jsonify({"success": False, "errors": errors}), 422

    scan = run_ml_scan(url)

    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO reports
               (url, email, threat_type, severity, details, ml_result, ml_confidence, status, submitted_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)""",
            (url, email or None, threat_type, severity, details or None,
             scan["label"], scan["confidence"], datetime.utcnow().isoformat() + "Z")
        )
        report_id = cursor.lastrowid
        conn.commit()

    print(f"[PhishRadar] Report #{report_id}: {threat_type} | {severity} | {url} | ML={scan['label']}")

    return jsonify({
        "success": True,
        "message": "Report submitted. Our ML engine has scanned the URL.",
        "report_id": report_id,
        "ml_result": scan,
    }), 201


@app.route("/api/reports", methods=["GET"])
def api_reports():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
    return jsonify({"count": len(rows), "reports": [dict(r) for r in rows]})


# ─────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
