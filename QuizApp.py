# Bring in deps
import os
import streamlit as st
from apikey import apikey
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Set up OpenAI API key
os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('MCQ Quiz Generator')

# Prompt for user's preferred quiz topic
quiz_topic = st.text_input('Enter your preferred quiz topic:')

# Prompt templates
question_template = PromptTemplate(
    input_variables=['topic'],
    template='Generate a quiz question about {topic}'
)

# Memory
question_memory = ConversationBufferMemory(input_key='topic', memory_key='quiz_history')

# LLMs
llm = OpenAI(temperature=0.9)
question_chain = LLMChain(llm=llm, prompt=question_template, verbose=True, output_key='question',
                          memory=question_memory)

# Function to generate AI-generated options for a given question
def generate_ai_options(question):
    # Use the OpenAI language model to generate options
    options_prompt = f"Create multiple-choice options for the following question:\n\n{question}\nOptions:"

    # Generate options using the available method in the langchain library
    options = llm(options_prompt)

    # Extract and return the generated options, removing unwanted characters and empty options
    formatted_options = []
    for option in options.split("\n"):
        cleaned_option = option.strip()
        if cleaned_option:
            formatted_options.append(cleaned_option)

    return formatted_options

# Function to generate quiz questions with AI-generated options
def generate_quiz(topic, num_questions):
    questions = []
    for _ in range(num_questions):
        # Generate questions using OpenAI Chat Completion API
        question = question_chain.run(topic)

        # Generate AI-generated options based on the question
        ai_generated_options = generate_ai_options(question)

        # For simplicity, let's assume the correct answer is the first option
        correct_answer = ai_generated_options[0]

        questions.append({"question": question, "options": ai_generated_options, "correct_answer": correct_answer})
    return questions

# Number of questions
num_questions = st.number_input('Enter the number of questions:', min_value=1, step=1)

# Generate quiz questions
if quiz_topic and num_questions > 0:
    quiz_questions = generate_quiz(quiz_topic, num_questions)

    # Display quiz questions and get user answers
    user_answers = []
    for i, q in enumerate(quiz_questions):
        st.subheader(f"Question {i + 1}: {q['question']}")

        # Format options as "1) Option A," "2) Option B," and so on
        formatted_options = [f"{j + 1}) {option}" for j, option in enumerate(q["options"])]
        user_answer = st.radio("Select an answer:", formatted_options, key=f"user_answer_{i}")

        user_answers.append(user_answer.split(') ')[1])

    # Submit quiz and display results
    if st.button("Submit Quiz"):
        score = 0
        st.success("Quiz Results:")
        for i, q in enumerate(quiz_questions):
            st.write(f"Q{i + 1}: {q['question']}")
            st.write(f"Your Answer: {user_answers[i]}")
            st.write(f"Correct Answer: {q['correct_answer']}")
            if user_answers[i] == q["correct_answer"]:
                score += 1
        st.info(f"Your score: {score}/{len(quiz_questions)}")
        st.info("Correct answers:")
        for i, q in enumerate(quiz_questions):
            st.write(f"Q{i + 1}: {q['correct_answer']}")

# Show history
with st.expander('Quiz History'):
    st.info(question_memory.buffer)
