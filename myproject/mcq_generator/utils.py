# import json
# import random

# def load_ipc_data():
#     with open("mcq_generator/ipc.json", "r", encoding="utf-8") as file:
#         return json.load(file)

# ipc_data = load_ipc_data()

# def generate_section_mcq(chapter, taken_mcqs):
#     sections = [section for section in ipc_data if section["chapter"] == int(chapter)]
#     remaining_sections = [section for section in sections if section["Section"] not in taken_mcqs]
#     if not remaining_sections:
#         return None, None, None
    
#     section = random.choice(remaining_sections)
#     question = section['section_title']
#     correct_option = str(section['Section'])
    
#     other_options = []
#     while len(other_options) < 3:
#         other_section = random.choice(sections)
#         if other_section['Section'] != section['Section'] and str(other_section['Section']) not in other_options:
#             other_options.append(str(other_section['Section']))
    
#     options = [correct_option] + other_options
#     random.shuffle(options)
#     return question, options, correct_option

# def generate_mcqs(chapter, mcq_type, taken_mcqs):
#     if mcq_type == 'section':
#         return generate_section_mcq(chapter, taken_mcqs)
#     else:
#         return None, None, None

# def validate_answer(user_answer, correct_answer):
#     return user_answer == correct_answer

