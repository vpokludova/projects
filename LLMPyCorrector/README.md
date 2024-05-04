# LLM Based Python Corrector Application

## Overview

The LLM based Python Corrector Application is a command-line tool designed to assist developers in debugging and correcting Python scripts. This tool leverages the OpenAI API to suggest fixes for errors in Python code, enhancing the efficiency of debugging processes by maintaining an interactive dialogue with a Language Learning Model (LLM) to ensure contextual accuracy and relevance of corrections.

## Features

- **Interactive Python Code Correction:** Utilizes OpenAI's powerful LLM to suggest corrections for Python code dynamically.
- **Real-time Error Analysis and Execution:** Validates fixes through immediate execution of corrected code to ensure error resolution.
- **Conversation History Management:** Maintains a history of the interaction to improve correction suggestions over time.
- **Python File Handling:** Provides a simple command-line interface for loading, analyzing, and debugging Python scripts.

## Usage

The application operates through a command-line interface where users provide the path to the Python script that needs debugging. Below are the steps to use the application:

- **Start the Application:** Run the application from the command line or through a Kotlin-compatible IDE like IntelliJ IDEA. Ensure your system has access to a valid OpenAI API key.
- **Input the Python File Path:** Enter the full path to your Python script when prompted. The application checks for file existence and proper format (`.py` extension).
- **Review Corrections:** After processing, the application will execute the script, identify any errors, and obtain corrections from the OpenAI API. This will repeat until the Python code runs without errors.

## Example Session

```bash
Welcome to the LLM based Python Corrector Application!
Please provide a Python filepath:
src/main/resources/Factorial.py

Error found, consulting LLM for fixes...
LLM Suggestion:
def factorial(n):
if n == 0:
return 1
else:
return n * factorial(n - 1)
    
if __name__ == "__main__":
num = 5
print(f"The factorial of {num} is: {factorial(num)}")

Python code executed successfully!
```

## Technical Approach

**Interaction with OpenAI API**

The application integrates with the OpenAI API to fetch intelligent code corrections. It forms a continuous conversation with the API, building upon previous interactions to enhance the context and accuracy of suggestions. This process involves:

- Sending Python code segments along with error messages that were thrown during execution.
- Receiving suggestions that are contextually aware due to the ongoing dialogue maintained by the application.
- Applying corrections and retesting the code iteratively until all errors are resolved.

**Error Handling and Process Flow**
Upon initiating the application, users are prompted to input the path of a Python file. The application then attempts to execute the Python code. If errors are detected, these are sent to the OpenAI API, which returns suggestions based on the current and past context of the code provided. This iterative process helps refine the corrections until the code runs without errors.


