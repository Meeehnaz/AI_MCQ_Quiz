Submitted to PwC for assessment.

# AI_MCQ_Quiz

## Project Title: MCQ Quiz Application

### Overview

This project is a Multiple-Choice Question (MCQ) Quiz Application built with Streamlit and powered by OpenAI's GPT-3 for question generation. Users can input a preferred quiz topic and the number of questions they want, and the application generates a quiz with random questions and answer options.

### Features

- **Dynamic Question Generation**: The application uses the OpenAI GPT-3 model to dynamically generate quiz questions based on the user-provided topic.
- **Randomized Answer Options**: Answer options for each question are also generated dynamically and shuffled to provide a challenging experience.
- **User Interaction**: Users can interact with the application by selecting answers for each question and submitting the quiz.
- **Score Calculation**: The application calculates and displays the user's score based on the submitted answers.

### Prerequisites

Make sure you have the required dependencies installed. You can install them using the following command:

```bash
pip install streamlit openai
```

### Getting Started

1. Set up your OpenAI API key

2. Run the application:

```bash
streamlit run QuizApp.py
```

### Usage

1. Enter your preferred quiz topic in the provided text input.
2. Choose the number of questions you want.
3. Click the "Generate Quiz" button to generate the quiz.
4. Answer each question by selecting the appropriate radio button.
5. Click the "Submit Quiz" button to see your score and review correct/wrong answers.

### Acknowledgments

- [Streamlit](https://streamlit.io/)
- [OpenAI](https://www.openai.com/)

