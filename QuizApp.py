import streamlit as st
import openai
import random

# Set up OpenAI API key
openai.api_key = "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"

def generate_gpt3_quiz(topic, num_questions):
    quiz_data = {'questions': []}

    for _ in range(num_questions):
        # Generate question using GPT-3
        gpt3_prompt = f"Generate a random quiz question about {topic}"
        gpt3_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=gpt3_prompt,
            temperature=0.7,
            max_tokens=500
        )

        question_text = gpt3_response.choices[0].text.strip()
        # Generate four answer options for each question
        options = generate_answer_options(question_text)
        random.shuffle(options)  # Shuffle options to make it more challenging
        quiz_data['questions'].append({'text': question_text, 'options': options})

    # Assign correct options (e.g., index 0 for simplicity)
    quiz_data['correct_options'] = [0] * num_questions

    return quiz_data

def generate_answer_options(question_text):
    # Generate answer options for a question using GPT-3
    gpt3_prompt = f"Generate four answer options for the question: {question_text}"
    gpt3_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=gpt3_prompt,
        temperature=0.7,
        max_tokens=100
    )

    answer_options = gpt3_response.choices[0].text.split('\n')
    return [option.strip() for option in answer_options if option.strip()][:4]

def calculate_score(quiz_data, user_answers):
    # Check if the lengths match
    if len(user_answers) != len(quiz_data['correct_options']):
        raise ValueError("Number of user answers does not match the number of questions.")

    # Compare user answers with correct options and calculate the score
    score = sum(user_answer == correct_option for user_answer, correct_option in
                zip(user_answers, quiz_data['correct_options']))

    return score

def main():
    st.title("MCQ Quiz Application")

    # User input for quiz topic and number of questions
    topic = st.text_input("Enter your preferred quiz topic:")
    num_questions = st.number_input("Enter the number of questions:", min_value=1, step=1, value=5)

    # Generate quiz based on user input using GPT-3
    quiz_data = generate_gpt3_quiz(topic, num_questions)

    if st.button("Generate Quiz"):
        # Display quiz questions and answer options one by one
        user_answers = []
        for i, question in enumerate(quiz_data['questions']):
            st.write(f"Q{i + 1}: {question['text']}")

            options = question['options']
            selected_option = st.radio(f"Select an option:", options, key=i)
            user_answers.append(options.index(selected_option))

            st.write("-----------")  # Separate questions for clarity

        # Button to submit the quiz
        if st.button("Submit Quiz"):
            # Calculate and display the score
            try:
                score = calculate_score(quiz_data, user_answers)

                # Check if the selected answers are correct or wrong
                result_messages = [f"Q{i + 1}: {'Correct' if user_answers[i] == correct_option else 'Wrong'}"
                                for i, correct_option in enumerate(quiz_data['correct_options'])]

                st.success(f"Your score: {score}/{num_questions}")
                st.info("Result:")
                for result_message in result_messages:
                    st.write(result_message)

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
