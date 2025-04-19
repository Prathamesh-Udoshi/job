import requests

OPENROUTER_API_KEY = "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"  # Replace with your key

def start_mock_interview(answers):
    questions = [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why should we hire you?"
    ]

    prompt = "You're an interview coach. Provide detailed feedback and suggest better answers:\n\n"
    for i, (key, answer) in enumerate(answers.items()):
        prompt += f"Q{i+1}: {questions[i]}\nUser's Answer: {answer}\n\n"

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
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_answers(answers):
    # Example implementation of analyzing answers
    feedback = []
    for question, answer in answers.items():
        feedback.append(f"Your response to '{question}' was insightful.")
    return "\n".join(feedback)