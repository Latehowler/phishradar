from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("phishing.pkl", 'rb'))
import re

def is_valid_url(url):
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        url = request.form['url'].strip()

        # Fix missing scheme
        if not url.startswith("http"):
            url = "http://" + url

        # Validate URL
        if not is_valid_url(url):
            predict = "⚠️ Please enter a valid website URL (e.g. google.com)"
            return render_template("index.html", predict=predict)

        # Clean URL
        cleaned_url = re.sub(r'^https?://(www\.)?', '', url)

        # Vectorize input
        X = vector.transform([cleaned_url])

        # Model prediction + probability
        proba = model.predict_proba(X)[0]
        classes = model.classes_

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

        return render_template("index.html", predict=predict)

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__=="__main__":
    app.run(debug=True)