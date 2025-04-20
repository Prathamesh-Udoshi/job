import os
import requests

# Use the provided API key directly if environment variable is not set
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "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"

def analyze_answers(answers):
    questions = [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why should we hire you?"
    ]

    prompt = "You're an interview coach. Provide detailed feedback and suggest better answers:\n\n"
    for i, (key, answer) in enumerate(answers.items()):
        prompt += f"Q{i+1}: {questions[i]}\nUser's Answer: {answer}\n\n"

    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY environment variable is not set."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            feedback = result['choices'][0]['message']['content']
            # Replace line breaks with HTML <br> tags for proper rendering
            return feedback.replace("\n", "<br>")
        elif 'error' in result:
            error_message = result['error'].get('message', 'Unknown error')
            return f"API Error: {error_message}"
        else:
            # Return the full response for debugging if 'choices' key is missing or empty
            return f"Unexpected response format: {result}"
    except Exception as e:
        return f"Error: {str(e)}"