"""
Flask application factory and routes for Phishing Detection System
"""
import os
import re
import pickle
from flask import Flask, render_template, request
from config import config


def load_models(app):
    """Load ML models and vectorizer from the models directory"""
    models_dir = app.config.get('MODELS_DIR', os.path.join(os.path.dirname(__file__), '..', 'models'))
    
    try:
        vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
        model_path = os.path.join(models_dir, 'phishing.pkl')
        
        with open(vectorizer_path, 'rb') as f:
            vector = pickle.load(f)
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        return vector, model
    except FileNotFoundError as e:
        app.logger.error(f"Model files not found: {e}")
        return None, None


def is_valid_url(url):
    """Validate URL format"""
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None


def create_app(env='development'):
    """Application factory function"""
    app = Flask(__name__, 
                template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    # Load configuration
    app.config.from_object(config[env])
    
    # Load ML models
    app.vector, app.model = load_models(app)
    
    # Register routes
    @app.route("/", methods=['GET', 'POST'])
    def index():
        """Main phishing detection page"""
        if request.method == "POST":
            if not app.model or not app.vector:
                return render_template("index.html", predict="⚠️ Model not available. Please try again later.")
            
            url = request.form.get('url', '').strip()
            
            # Fix missing scheme
            if not url.startswith("http"):
                url = "http://" + url
            
            # Validate URL
            if not is_valid_url(url):
                predict = "⚠️ Please enter a valid website URL (e.g., google.com)"
                return render_template("index.html", predict=predict)
            
            # Clean URL
            cleaned_url = re.sub(r'^https?://(www\.)?', '', url)
            
            try:
                # Vectorize input
                X = app.vector.transform([cleaned_url])
                
                # Model prediction + probability
                proba = app.model.predict_proba(X)[0]
                classes = app.model.classes_
                
                result_index = proba.argmax()
                prediction = classes[result_index]
                confidence = round(proba[result_index] * 100, 2)
                
                # Decision logic
                if prediction == 'bad':
                    if confidence > 80:
                        predict = f"❌ Phishing detected ({confidence}%)"
                    else:
                        predict = f"⚠️ Suspicious website ({confidence}%)"
                elif prediction == 'good':
                    if confidence < 60:
                        predict = f"⚠️ Possibly safe but uncertain ({confidence}%)"
                    else:
                        predict = f"✅ Legit website ({confidence}%)"
                else:
                    predict = "Something went wrong 🤨"
            
            except Exception as e:
                app.logger.error(f"Prediction error: {e}")
                predict = "⚠️ An error occurred during prediction. Please try again."
            
            return render_template("index.html", predict=predict)
        
        return render_template("index.html")
    
    @app.route("/about")
    def about():
        """About page"""
        return render_template("about.html")
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template("error.html", error="Page not found"), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        return render_template("error.html", error="Internal server error"), 500
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get('DEBUG', False))