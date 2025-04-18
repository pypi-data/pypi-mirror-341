# ConnorsAPI/API.py
import openai

# Set your API key (best to load this from an environment variable or a config file)
openai.api_key = "pypi-AgEIcHlwaS5vcmcCJGUwM2E5ODljLTU3YTctNDk0ZC1iNDYzLWFjMmRkNzZkMjliOAACKlszLCIyZWU5ZjA3ZC0yMTUzLTQ2YmEtYTA4Zi01N2EwMTY4N2Y0ODQiXQAABiCcWyHcC-IHmrwqZn3qxWROcbMqdDyFEY6ad8cqVUvo0g"  # Replace this with your real API key

def ask_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"].strip()
