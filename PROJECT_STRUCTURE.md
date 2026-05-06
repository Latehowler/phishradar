# Project Structure Guide

## Phishing Detection System - Standard Project Layout

```
phishing-detection-system/
│
├── app/                          # Main application package
│   ├── __init__.py              # Package initializer
│   ├── app.py                   # Flask application factory and routes
│   └── models.py                # Database models (User, PhishingReport)
│
├── templates/                    # HTML templates (Jinja2)
│   ├── index.html               # Main detection page
│   ├── about.html               # About page
│   ├── report_phishing.html     # Phishing report form
│   └── error.html               # Error page
│
├── static/                       # Static files (CSS, JS, images)
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript files
│   └── images/                  # Images and icons
│
├── data/                         # Datasets
│   └── phishing_site_urls.csv   # Training dataset
│
├── models/                       # Trained ML models
│   ├── phishing.pkl             # Main Naive Bayes model
│   ├── phishing_mnb.pkl         # Alternative model
│   └── vectorizer.pkl           # TF-IDF vectorizer
│
├── notebooks/                    # Jupyter notebooks
│   └── Phishing website detection system.ipynb
│
├── tests/                        # Unit and integration tests
│   ├── __init__.py
│   ├── test_app.py              # Application tests
│   └── test_models.py           # Model tests
│
├── env/                          # Virtual environment (git-ignored)
│
├── instance/                     # Instance-specific files (git-ignored)
│
├── .github/                      # GitHub configuration
│   ├── ISSUE_TEMPLATE/
│   │   └── bug_report.md
│   ├── CONTRIBUTING.md
│   └── workflows/
│       └── python-app.yml       # CI/CD pipeline
│
├── config.py                     # Application configuration
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── CHANGELOG.md                  # Version history
├── CODE_OF_CONDUCT.md           # Community guidelines
├── LICENSE                       # MIT License
├── .gitignore                    # Git ignore rules
├── .gitattributes               # Git attributes
└── Phishing Detection system.code-workspace  # VS Code workspace config
```

## Running the Application

### Development
```bash
# Activate virtual environment
env\Scripts\activate  # Windows
# or
source env/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py

# Or directly
python -m app.app
```

### Production
```bash
# Set environment
set FLASK_ENV=production  # Windows
# or
export FLASK_ENV=production  # Linux/macOS

python run.py
```

## Key Directories

- **app/**: Core application code with Flask routes and database models
- **templates/**: HTML files rendered by Flask (Jinja2 templates)
- **static/**: Client-side assets (CSS, JavaScript, images)
- **models/**: Trained machine learning models and vectorizers
- **data/**: Datasets and CSV files
- **notebooks/**: Jupyter notebooks for data analysis and model training
- **tests/**: Automated test suite

## Adding New Features

1. Add routes to `app/app.py`
2. Create templates in `templates/`
3. Add styles/scripts in `static/css/` or `static/js/`
4. If database needed, update models in `app/models.py`
5. Write tests in `tests/`
6. Update documentation in `README.md`

## Best Practices

✅ Keep app logic in the `app/` directory
✅ Use templates for HTML rendering
✅ Store configuration in `config.py`
✅ Use environment variables for sensitive data
✅ Write tests for new features
✅ Update documentation and CHANGELOG.md
✅ Keep static files organized (css/, js/, images/)

---

**Last Updated**: May 2026
