import requests
import threading
import time

stop_spinner = False

#Define role
role = """
    You are a helpful IT support Assistant.
    You provide clear, professional, and concise technical support answers
    When explaining technical concepts, use simple language and step-by-step instructions.
"""

def spinner():
    while not stop_spinner:
        for char in "|/-\\":
            print(f"\rAgent is Thinking... {char}", end="", flush=True)
            time.sleep(0.1)
            if stop_spinner:
                break

#Ask the user to enter the prompt
user_prompt = input("Enter your prompt: ")
full_prompt = f"{role}\n\nUser: {user_prompt}\nAssistant: "

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
    print("\nSupport Response: ")
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