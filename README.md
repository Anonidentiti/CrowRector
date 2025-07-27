Crowrecter: Your Command Auditor
Crowrecter is a command-line tool designed to help cybersecurity professionals and enthusiasts audit their commands. It leverages the Google Gemini API to provide real-time feedback, suggestions, and explanations for your terminal commands, ensuring best practices, efficiency, and security.

Features
Intelligent Command Evaluation: Get detailed feedback on your commands, considering the tool, command string, and your stated reason.

Best Practices & Security: Receive suggestions to improve command correctness, adhere to security best practices, and avoid potential pitfalls.

Clear & Concise Reports: Outputs a structured audit report directly in your terminal with color-coded evaluations.

Hacker-like Aesthetic: Features an ASCII art banner and colored output for a visually engaging experience.

Installation
Save the Script:
Save the provided Python code into a file named crowrecter.py.

Install Dependencies:
Crowrecter requires the requests Python library. If you don't have it, install it using pip:

pip install requests

Set Your Google Gemini API Key:
Crowrecter uses the Google Gemini API to perform its evaluations. You need to set your API key as an environment variable named GEMINI_API_KEY.

Open your shell configuration file (~/.zshrc for Zsh or ~/.bashrc for Bash) and add the following line:

export GEMINI_API_KEY='YOUR_ACTUAL_GEMINI_API_KEY_HERE'

Replace YOUR_ACTUAL_GEMINI_API_KEY_HERE with your actual Gemini API key.

After adding the line, save the file and apply the changes by sourcing your shell configuration:

source ~/.zshrc  # Or source ~/.bashrc

Usage
Run crowrecter.py from your terminal, providing the tool, command, and reason using the -t, -c, and -r flags, respectively.

python crowrecter.py -t <tool_name> -c "<command_string>" -r "<reason_for_command>"

Examples
Auditing a Hydra Command for Brute-Force Login:

python crowrecter.py -t hydra -c "hydra -l man -p man -u http://Google.com/login" -r "bruteforce login"

Auditing an Nmap Scan for Service Versions:

python crowrecter.py -t nmap -c "nmap -sV 192.168.1.1" -r "scan for open ports and service versions"

Auditing a curl Command for Web Content Retrieval:

python crowrecter.py -t curl -c "curl example.com" -r "retrieve content from example.com"

Output
Crowrecter will provide a detailed audit report, including:

Evaluation: A high-level assessment (e.g., Optimal, Suboptimal, Critical Flaw).

Feedback: A detailed explanation of the command's pros, cons, and potential security implications.

Suggestions: An improved or corrected version of the command, if applicable.

Explanation of Suggestions: The rationale behind the suggested changes.

The output will be color-coded for readability and quick assessment.
