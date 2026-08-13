import requests
import threading
import time
import os

stop_spinner = False

# Load IT Policy from file
policy_file_path = os.path.join(os.path.dirname(__file__), 'IT_Policy.txt')
try:
    with open(policy_file_path, 'r') as f:
        it_policy = f.read()
except FileNotFoundError:
    it_policy = "IT Policy file not found."

#Define role
role = """
    You are a helpful IT Policy Desk for CONTOSO CORPORATION.
    You provide clear, professional, and concise technical support answers.
    When explaining technical concepts, use simple language and step-by-step instructions.
    IMPORTANT: You must follow and reference the IT policies provided below when answering questions.
"""

#instructions
instructions = f"""
You must follow CONTOSO CORPORATION IT policies strictly. Here are the official policies:

{it_policy}

Guidelines:
- For password reset requests: Reference the password reset policy process.
- For software installation requests: Reference the software installation approval process.
- For hardware issues: Reference the hardware troubleshooting guide.
- Only recommend approved software or escalate to IT helpdesk for custom software.
- If the prompt is not related to IT assistance or beyond the scope of these policies, reply with "I don't know."
- If you don't know the answer, clearly state that.
- If uncertain, ask the user for clarification.
- Respond in the same language as the user's query.
- If the context is unreadable or of poor quality, inform the user and provide the best possible answer.
- If the answer isn't present in the context but you possess the knowledge, explain this to the user and provide the answer using your own understanding.
- Only include inline citations using [id] (e.g., [1], [2]) when the <source> tag includes an id attribute. Do not cite if the <source> tag does not contain an id attribute.
- Do not use XML tags in your response.

### Task:
Respond to the user query using the provided context, incorporating inline citations in the format [id] **only when the <source> tag includes an explicit id attribute** (e.g., <source id="1">).

### Guidelines:
- If you don't know the answer, clearly state that.
- If uncertain, ask the user for clarification.
- Respond in the same language as the user's query.
- If the context is unreadable or of poor quality, inform the user and provide the best possible answer.
- If the answer isn't present in the context but you possess the knowledge, explain this to the user and provide the answer using your own understanding.
- **Only include inline citations using [id] (e.g., [1], [2]) when the <source> tag includes an id attribute.**
- Do not cite if the <source> tag does not contain an id attribute.
- Do not use XML tags in your response.

Additional Response Rules:
- Keep answers concise and policy-aligned.
- When referencing the IT Policy, cite the section name where relevant.
"""

def spinner():
    while not stop_spinner:
        for char in "|/-\\":
            print(f"\rAgent is Thinking... {char}", end="", flush=True)
            time.sleep(0.1)
            if stop_spinner:
                break

print("==== IT Policy Help Desk Agent ===")
print("Please type in 'Exit' to quit.\n")

while True:

    #Ask the user to enter the prompt
    user_prompt = input("You: ")

    #Exit condition
    if user_prompt.lower() == "exit":
        print("\nGoodBye!")
        break

    full_prompt = f"{role}\n\nRespond in strictly 100 words.\n\nUser: {user_prompt}\nAssistant: "

    #Reset spinner flag
    stop_spinner = False

    #start spinner
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    #Send the prompt to Phi-3 via ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "Phi3",
                "prompt": full_prompt,
                "stream": False
            },
            
            timeout=60
        )
        response.raise_for_status()

        #Stop spinner
        stop_spinner = True
        spinner_thread.join()

        #clear the spinner line
        print("\r" + " " * 40 + "\r", end="")

        #Display response
        print("\n\nHelp Desk Answer: ")
        print(response.json()["response"])

    #Error Handling
    except requests.exceptions.ConnectionError:
        stop_spinner = True
        spinner_thread.join()
        print("\nError: Could not connect to Ollama. Make sure ollama is running.")

    except requests.exceptions.Timeout:
        stop_spinner = True
        spinner_thread.join()
        print("\nError: Request time out.")