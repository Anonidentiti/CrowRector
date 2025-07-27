import argparse
import os
import json
import requests

# ANSI escape codes for colors and styles
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"

def print_banner():
    """
    Prints a hacker-like ASCII art banner spelling "CROWRECTOR".
    """
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
  ______ _______ ______ _______ _______ _______ _______ ______
 |   __ \   _   |   __ \   _   |   _   |   _   |   _   |   __ \
 |      <       |      <       |       |       |       |      <
 |______|___|___|______|___|___|___|___|___|___|___|___|______|
 / ____/|  _____||  ____/|  ____/|  ____/|  ____/|  ____/|  ____/
| (___  | |____  | |____  | |____  | |____  | |____  | |____  | |____
 \____ \ |  ____| |  ____| |  ____| |  ____| |  ____| |  ____| |  ____|
 _____) )| |_____ | |      | |      | |      | |      | |      | |
|______/ |_______||_|      |_|      |_|      |_|      |_|      |_|
{Colors.RESET}{Colors.MAGENTA}{Colors.BOLD}
           Your Command Auditor
{Colors.RESET}
"""
    print(banner)

def get_gemini_api_key():
    """
    Retrieves the Gemini API key from environment variables.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print(f"{Colors.RED}{Colors.BOLD}Error: GEMINI_API_KEY environment variable not found.{Colors.RESET}")
        print(f"{Colors.YELLOW}Please set it in your .zshrc or .bashrc file like this:")
        print(f"export GEMINI_API_KEY='YOUR_API_KEY_HERE'{Colors.RESET}")
        exit(1)
    return api_key

def correct_command(tool, command, reason):
    """
    Sends the command, tool, and reason to the Gemini API for correction/evaluation.
    """
    api_key = get_gemini_api_key()
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Construct the prompt for the Gemini API
    prompt = f"""
    As a command-line expert and cybersecurity analyst, evaluate the following command.
    Consider the 'tool' being used and the 'reason' for the command.
    Provide feedback on its correctness, best practices, potential issues, and suggest a corrected or improved version if necessary.
    Be concise and directly address the command's validity and effectiveness for the stated reason.
    Adopt a tone that is professional yet direct, suitable for a cybersecurity context.

    Tool: {tool}
    Command: {command}
    Reason: {reason}

    Please provide your response in a structured JSON format, including:
    - "evaluation": (e.g., "Optimal", "Acceptable with Caveats", "Suboptimal", "Critical Flaw")
    - "feedback": (Detailed explanation of issues or why it's good, focusing on security implications and efficiency)
    - "suggestions": (Corrected or improved command, if applicable. If no changes, state "N/A")
    - "explanationOfSuggestions": (Why the suggested command is better, or why the original was flawed)
    """

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "evaluation": {"type": "STRING"},
                    "feedback": {"type": "STRING"},
                    "suggestions": {"type": "STRING"},
                    "explanationOfSuggestions": {"type": "STRING"}
                },
                "propertyOrdering": ["evaluation", "feedback", "suggestions", "explanationOfSuggestions"]
            }
        }
    }

    print(f"{Colors.YELLOW}Auditing command...{Colors.RESET}")
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        if result.get('candidates') and result['candidates'][0].get('content') and result['candidates'][0]['content'].get('parts'):
            # The API returns the JSON as a string within the 'text' field
            response_text = result['candidates'][0]['content']['parts'][0]['text']
            try:
                parsed_response = json.loads(response_text)
                
                evaluation = parsed_response.get('evaluation', 'N/A')
                feedback = parsed_response.get('feedback', 'N/A')
                suggestions = parsed_response.get('suggestions', 'N/A')
                explanation = parsed_response.get('explanationOfSuggestions', 'N/A')

                print(f"\n{Colors.BLUE}{Colors.BOLD}--- Command Audit Report ---{Colors.RESET}")
                
                # Color-code the evaluation
                eval_color = Colors.YELLOW
                if "Optimal" in evaluation:
                    eval_color = Colors.GREEN
                elif "Critical Flaw" in evaluation or "Incorrect" in evaluation:
                    eval_color = Colors.RED
                elif "Suboptimal" in evaluation or "Needs Improvement" in evaluation:
                    eval_color = Colors.YELLOW
                elif "Acceptable" in evaluation:
                    eval_color = Colors.BLUE

                print(f"{Colors.BOLD}Evaluation:{Colors.RESET} {eval_color}{evaluation}{Colors.RESET}")
                print(f"{Colors.BOLD}Feedback:{Colors.RESET} {feedback}")
                print(f"{Colors.BOLD}Suggestions:{Colors.RESET} {suggestions}")
                print(f"{Colors.BOLD}Explanation of Suggestions:{Colors.RESET} {explanation}")
                print(f"{Colors.BLUE}{Colors.BOLD}--------------------------{Colors.RESET}")
            except json.JSONDecodeError:
                print(f"{Colors.RED}Error: Could not parse API response as JSON.{Colors.RESET}")
                print(f"{Colors.YELLOW}Raw API Response:{Colors.RESET}", response_text)
        else:
            print(f"{Colors.RED}Error: Unexpected API response structure.{Colors.RESET}")
            print(result)

    except requests.exceptions.HTTPError as e:
        print(f"{Colors.RED}HTTP Error:{Colors.RESET} {e.response.status_code} - {e.response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"{Colors.RED}Connection Error:{Colors.RESET} {e}")
    except requests.exceptions.Timeout as e:
        print(f"{Colors.RED}Timeout Error:{Colors.RESET} {e}")
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}An unexpected error occurred:{Colors.RESET} {e}")

def main():
    print_banner() # Print the banner at the start

    parser = argparse.ArgumentParser(
        description=f"{Colors.MAGENTA}A command auditor tool using the Google Gemini API for cybersecurity command evaluation.{Colors.RESET}"
    )
    parser.add_argument(
        "-t", "--tool", required=True, help=f"{Colors.YELLOW}The name of the tool being used (e.g., hydra, nmap).{Colors.RESET}"
    )
    parser.add_argument(
        "-c", "--command", required=True, help=f"{Colors.YELLOW}The command string to be audited/evaluated.{Colors.RESET}"
    )
    parser.add_argument(
        "-r", "--reason", required=True, help=f"{Colors.YELLOW}The reason or goal for running the command.{Colors.RESET}"
    )

    args = parser.parse_args()

    correct_command(args.tool, args.command, args.reason)

if __name__ == "__main__":
    main()
