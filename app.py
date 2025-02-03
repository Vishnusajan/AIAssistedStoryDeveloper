from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import pandas as pd
import os
from constants import openai_key
import openpyxl

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)

# Path to Excel file to store summaries
EXCEL_FILE = "paras.xlsx"

# Initialize Excel file if not exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["paragraph", "summary"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save_paragraph', methods=['POST'])
def save_paragraph():
    data = request.json
    paragraph = data.get("paragraph", "").strip()
    if not paragraph:
        return jsonify({"error": "No paragraph provided"}), 400

    try:
        # Generate summary for the paragraph using OpenAI
        prompt = f"Summarize the following paragraph in maximum 2-3 sentences:\n\n{paragraph}"
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for summarizing text. Provide complete, coherent summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  # Increased from 50 to 150
            temperature=0.7,
            presence_penalty=0.0,
            frequency_penalty=0.0,
        )
        summary = response.choices[0].message.content.strip()

        # Save paragraph and summary to Excel
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame({"paragraph": [paragraph], "summary": [summary]})], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Load summaries from Excel
        df = pd.read_excel(EXCEL_FILE)
        all_summaries = " ".join(df["summary"].tolist())

        # Generate plot suggestion based on summaries
        prompt = f"Here is a summary of the story so far:\n\n{all_summaries}\n\nBased on this, provide a plot suggestion. Keep it short and concise."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for writers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,  # Limit output size for quick responses
        )
        suggestion = response.choices[0].message.content
        return jsonify({'suggestion': suggestion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rerender_summaries', methods=['POST'])
def rerender_summaries():
    try:
        data = request.json
        paragraphs = data.get("paragraphs", [])
        
        df = pd.DataFrame(columns=["paragraph", "summary"])
        df.to_excel(EXCEL_FILE, index=False)
        
        summaries = []
        for paragraph in paragraphs:
            if paragraph.strip():
                prompt = f"Summarize the following paragraph in maximum 2-3 sentences:\n\n{paragraph}"
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for summarizing text. Provide complete, coherent summaries."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,  # Increased from 50 to 150
                    temperature=0.7,
                    presence_penalty=0.0,
                    frequency_penalty=0.0,
                )
                summary = response.choices[0].message.content.strip()
                summaries.append({"paragraph": paragraph, "summary": summary})
        
        df = pd.DataFrame(summaries)
        df.to_excel(EXCEL_FILE, index=False)
        
        return jsonify({"message": "Summaries regenerated successfully", "summaries": summaries})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
