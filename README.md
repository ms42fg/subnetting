# Subnetting Quiz: Interactive Learning Tool

## Introduction

The Subnetting Quiz is an interactive Python-based learning tool designed to help networking students and professionals practice and understand IP subnetting concepts. This program offers a hands-on approach to learning subnetting, catering to both beginners and advanced users.

## Features

- **Interactive Quiz Format**: Engage with subnetting problems in a question-and-answer format.
- **Difficulty Levels**: Choose between beginner and advanced modes to match your skill level.
- **Realistic Network Scenarios**: Practice with common private IP ranges used in real-world networking.
- **Step-by-Step Explanations**: Detailed breakdowns of each subnetting step for better understanding.
- **Visual Aids**: Utilizes tables and formatted text to present information clearly.
- **Real-Life Analogies**: Relates subnetting concepts to everyday scenarios for easier comprehension.
- **Customizable Quiz Length**: Select the number of questions you want to attempt.
- **Immediate Feedback**: Get instant feedback on your answers and see the correct solutions.
- **Subnet Details View**: Option to see detailed information about the created subnets.
- **Advanced Topics**: Introduction to concepts like Variable Length Subnet Masking (VLSM) for advanced users.

## Requirements

- Python 3.6 or higher
- Rich library (for enhanced console output)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/ms42fg/subnetting.git
   ```

2. Navigate to the project directory:
   ```
   cd subnetting
   ```

3. Create a virtual environment:
   - On Windows:
     If Python is not in your PATH:
     ```
     c:\Python35\python -m venv c:\path\to\myenv
     ```
     If Python is in your PATH:
     ```
     python -m venv venv
     ```

   - On macOS and Linux:
     ```
     python3 -m venv venv
     ```

4. Activate the virtual environment:

   On Windows:
   
   - Using cmd.exe:
   ```
   venv\Scripts\activate.bat
   ```

   - Using PowerShell:
   ```
   venv\Scripts\Activate.ps1
   ```

   Note: If you encounter a PowerShell execution policy error, run the following command:
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then try activating the virtual environment again.
     
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install rich
   ```

## Usage

1. Ensure you're in the project directory and your virtual environment is activated.

2. Run the script:
   ```
   python main.py
   ```

3. Follow the on-screen prompts to:
   - Choose your difficulty level (beginner or advanced)
   - Select the number of questions you want to attempt
   - Answer the subnetting questions

4. After completing the quiz, you'll receive your score and have the option to provide feedback.

5. When you're done, you can deactivate the virtual environment:
   ```
   deactivate
   ```

## Educational Approach

The Subnetting Quiz employs several strategies to facilitate learning:

1. **Progressive Difficulty**: Starts with basic concepts and gradually introduces more complex ideas.
2. **Interactive Learning**: Engages users through active problem-solving rather than passive reading.
3. **Real-World Context**: Uses practical scenarios to demonstrate the relevance of subnetting skills.
4. **Visual Learning**: Employs tables, color-coding, and formatted text to aid visual learners.
5. **Immediate Feedback**: Provides instant correctness checks and explanations to reinforce learning.
6. **Analogies and Examples**: Relates abstract networking concepts to familiar real-life situations.

## Demo

Here's a screenshot of the Subnetting Quiz in action:

![Subnetting Quiz Demo](/data/demo.png)

This image shows an example of a subnetting question, demonstrating the clear layout, color-coded information, and step-by-step guidance provided by the quiz.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
