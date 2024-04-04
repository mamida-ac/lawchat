import json
import random

# Load the JSON data
with open("C:\\Users\\mamid\\AppData\\Local\\Programs\\Python\\Python310\\chatbot - Copy\\rasa\\actions\\ipc.json", "r", encoding="utf-8") as file:
    ipc_data = json.load(file)
def generate_section_mcq(chapter):
    sections = [section for section in ipc_data if section["chapter"] == int(chapter)]
    if not sections:
        return None, None, None
    section = random.choice(sections)
    question = (section['section_title'], section['section_desc'])
    correct_option = section['Section']
    options = [section['Section']]
    for _ in range(3):
        other_section = random.choice(sections)
        while other_section['Section'] == section['Section']:
            other_section = random.choice(sections)
        options.append(other_section['Section'])
    random.shuffle(options)
    return question, options, correct_option

# Function to generate MCQ questions based on description
def generate_description_mcq(chapter):
    sections = [section for section in ipc_data if section["chapter"] == int(chapter)]
    if not sections:
        return None, None, None
    section = random.choice(sections)
    question = section['Section']
    correct_option = section['section_title']
    options = [section['section_title']]
    for _ in range(3):
        other_section = random.choice(sections)
        while other_section['section_desc'] == section['section_desc']:
            other_section = random.choice(sections)
        options.append(other_section['section_title'])
    random.shuffle(options)
    return question, options, correct_option

# Main function to generate MCQ based on user choice
def generate_mcq(chapter, mcq_type):
    if mcq_type == 'section':
        return generate_section_mcq(chapter)
    elif mcq_type == 'description':
        return generate_description_mcq(chapter)
    else:
        return None, None, None

# Function to validate user's answer
def validate_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        return "Correct!"
    else:
        return f"Wrong. Correct answer is: {correct_answer}"

# Get user input for chapter and MCQ type
chapter = input("Enter chapter (e.g., '1', '2', etc.): ")
mcq_type = input("Enter MCQ type (section or description): ")

# Generate MCQ
question, options, answer = generate_mcq(chapter, mcq_type)

if question is not None:
    # Display question and options
    print("Question:", question)
    print("Options:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    # Get user's choice
    user_choice = input("Enter the option number: ")

    # Validate user's answer
    result = validate_answer(options[int(user_choice) - 1], answer)
    print(result)
else:
    print("No data found for the provided chapter. Please enter a valid chapter number.")