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

print("==== IT Support Assistant ===")
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
        print("\nSupport Agent: ")
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