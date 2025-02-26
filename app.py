from flask import Flask, render_template, request, jsonify
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# CHANGE WITH YOUR REAL API KEY! (will not work without one)
openai.api_key = os.getenv("REPLACE_WITH_YOUR_API")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-affirmation', methods=['POST'])
def generate_affirmation():
    # Get form data
    data = request.json
    name = data.get('name', '')
    focus_area = data.get('focus_area', '')
    
    # Validate inputs
    if not name or not focus_area:
        return jsonify({"error": "Please provide both name and focus area"}), 400
    
    try:
        # Generate affirmation using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a positive, empowering assistant that creates personalized affirmations."
                },
                {
                    "role": "user", 
                    "content": f"Create a short, powerful daily affirmation for {name} focused on their {focus_area}. Make it personal, positive, and actionable. Keep it under 100 characters if possible."
                }
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        # Extract the affirmation from the response
        affirmation = response.choices[0].message.content.strip()
        
        return jsonify({"affirmation": affirmation})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
