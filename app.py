from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-r1-0528:free"

def call_llm(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://prompt-injection-zuag.onrender.com",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)

    # Add debug
    print("Response status:", res.status_code)
    print("Response JSON:", res.text)

    res.raise_for_status()  # raises error if request fails
    return res.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        prompt = request.form.get("prompt")
        response = call_llm(prompt)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
