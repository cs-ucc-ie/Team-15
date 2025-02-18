
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import scoped_session
from models import Session, YourTable
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# OpenAI API key
openai.api_key = os.getenv(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)

# session
session = scoped_session(Session)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    # Fetch data from the database
    data = session.query(YourTable).all()
    data_str = '\n'.join([f'{item.id}: {item.name}' for item in data])

    # prompt for OpenAI
    prompt = f"Database contents:\n{data_str}\n\nUser: {user_input}\nAI:"

    # Generate response from OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    ai_message = response.choices[0].text.strip()
    return jsonify({'response': ai_message})

if __name__ == '__main__':
    app.run(debug=True)
