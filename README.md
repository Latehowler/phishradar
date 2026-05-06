# Phishing Detection System

A Flask-based web application that detects phishing websites using machine learning. The system analyzes URLs and classifies them as legitimate or phishing with confidence scores.

## Features

- 🔍 **URL Classification**: Analyzes URLs to detect phishing attempts
- 📊 **Confidence Scoring**: Provides confidence percentages for predictions
- 🎨 **User-Friendly Interface**: Simple web interface for URL submission
- ⚡ **Real-time Detection**: Instant feedback on website legitimacy
- 📈 **ML-Powered**: Uses trained machine learning models for accurate detection

## Tech Stack

- **Backend**: Flask (Python web framework)
- **ML/Data Processing**: scikit-learn, NumPy, Pandas
- **Frontend**: HTML, CSS, Jinja2 templates
- **Database**: SQLAlchemy (optional, for user management)
- **Authentication**: Flask-Login

## Project Structure

```
.
├── app.py                          # Main Flask application
├── models.py                       # Database models
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── Dataset/
│   └── phishing_site_urls.csv     # Training dataset
├── templates/                      # HTML templates
│   ├── index.html                 # Main page
│   ├── about.html                 # About page
│   └── report_phishing.html       # Phishing report page
├── Phishing website detection system.ipynb  # Data analysis notebook
├── phishing.pkl                   # Trained ML model
├── phishing_mnb.pkl              # Alternative ML model
└── vectorizer.pkl                # Text vectorizer
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/phishing-detection-system.git
cd phishing-detection-system
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Application

```bash
# Activate virtual environment (if not already active)
# Windows: env\Scripts\activate
# macOS/Linux: source env/bin/activate

# Start the Flask app
python app.py
```

The application will be available at `http://localhost:5000`

### How to Use

1. Open the web application in your browser
2. Enter a URL you want to check
3. The system will analyze the URL and display:
   - **✅ Legit website**: Safe to visit
   - **⚠️ Suspicious website**: Proceed with caution
   - **❌ Phishing detected**: Likely a phishing attempt

## Model Details

- **Model Type**: Naive Bayes Classifier
- **Training Data**: Phishing website URLs dataset (`Dataset/phishing_site_urls.csv`)
- **Features**: URL text features extracted using TF-IDF vectorization
- **Accuracy**: [Add your model's accuracy metrics]

## Dependencies

- Flask 3.1.3
- scikit-learn 1.8.0
- Pandas 3.0.2
- NumPy 2.4.4
- SQLAlchemy + Flask-SQLAlchemy
- Flask-Login
- Werkzeug 3.1.8

See `requirements.txt` for complete list.

## Configuration

Create a `.env` file in the root directory to configure:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DEBUG=False
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Your Name (@yourprofile)

## Acknowledgments

- Dataset source: [Add if applicable]
- ML framework: scikit-learn
- Web framework: Flask

## Contact

For questions or feedback, please email: your.email@example.com

## Disclaimer

This tool is for educational and security research purposes. Always verify the legitimacy of a website through multiple methods before entering sensitive information.

---

**Last Updated**: May 2026
