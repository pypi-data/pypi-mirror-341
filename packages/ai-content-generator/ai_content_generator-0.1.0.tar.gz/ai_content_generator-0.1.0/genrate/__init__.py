import google.generativeai as genai

genai.configure(api_key="AIzaSyAvyLEzkIaibw5BFF4ZCISLljZNbLKd2Cg")  # For safety, use environment variable in production

model = genai.GenerativeModel("gemini-2.0-flash")

class GenerateContentWithAI:
    def __init__(self, prompt):
        res = model.generate_content(prompt)
        print(res.text)
