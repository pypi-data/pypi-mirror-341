import subprocess
from google import genai

def vibe(prompt: str, gemini_api_key: str):
    client = genai.Client(api_key = gemini_api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents="Respond to this only with PYTHON 3.5+ code that can be compiled in the python3 compiler, do not add anything other than code to your answer. The code should run any function necessary and at the end return to the stdout a value requested by the prompt. The code you provide can be a single print statement with the answer. This is the prompt: " + prompt
    )

    lines = response.text.splitlines()
    middle_lines = lines[1:-1]
    result = '\n'.join(middle_lines)
    return subprocess.run(["python", "-c", result ], capture_output=True, text=True).stdout.strip()