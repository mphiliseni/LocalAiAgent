import requests
import threading
import time

stop_spinner = False

def spinner():
    while not stop_spinner:
        for char in "|/-\\":
            print(f"\rAgent is Thinking... {char}", end="", flush=True)
            time.sleep(0.1)
            if stop_spinner:
                break
#Ask the user to enter the prompt
user_prompt = input("Enter your prompt: ")

#start spinner
spinner_thread = threading.Thread(target=spinner)
spinner_thread.start()

#Send the prompt to Phi-3 via ollama
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "Phi3",
        "prompt": user_prompt,
        "stream": False
    }
)

#Stop spinner
stop_spinner = True
spinner_thread.join()

#clear the spinner line 
print("\r" + " " * 40 + "\r", end="")

#Display response 
print("\nAgent Response: ")
print(response.json()["response"])