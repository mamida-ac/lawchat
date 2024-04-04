import json
import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re

class ActionGetSectionDescription(Action):
    def name(self) -> Text:
        return "action_get_section_description"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            ipc_file_path = os.path.join(
                "C:\\",
                "Users",
                "mamid",
                "AppData",
                "Local",
                "Programs",
                "Python",
                "Python310",
                "chatbot",
                "actions",
                "ipc.json"
            )
            with open(ipc_file_path, "r", encoding="utf-8") as file:
                ipc_data = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: 'ipc.json' file not found.")
            return []
        except Exception as e:
            dispatcher.utter_message(text=f"Error loading 'ipc.json' file: {e}")
            return []

        section_number = next(tracker.get_latest_entity_values("section"), None)
        if section_number is not None:
            section_number = int(section_number)
            section_data = next(
                (
                    section
                    for section in ipc_data
                    if section.get("Section") == section_number
                ),
                None,
            )
            if section_data:
                section_desc = section_data.get("section_desc")
                dispatcher.utter_message(text=section_desc)
            else:
                dispatcher.utter_message(text="Section not found.")
        else:
            dispatcher.utter_message(text="Please provide a valid section number.")

        return []


class ActionGetSectionNumber(Action):
    def name(self) -> Text:
        return "action_get_section_number"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            ipc_file_path = os.path.join(
                "C:\\",
                "Users",
                "mamid",
                "AppData",
                "Local",
                "Programs",
                "Python",
                "Python310",
                "chatbot",
                "actions",
                "ipc.json"
            )
            with open(ipc_file_path, "r", encoding="utf-8") as file:
                ipc_data = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: 'ipc.json' file not found.")
            return []
        except Exception as e:
            dispatcher.utter_message(text=f"Error loading 'ipc.json' file: {e}")
            return []

        section_desc = next(tracker.get_latest_entity_values("section_desc"), None)
        if section_desc is not None:
            # Preprocess input text
            section_desc_cleaned = preprocess_text(section_desc)

            # Check for matches in JSON data
            matched_sections = []
            for section_data in ipc_data:
                if preprocess_text(section_data.get("section_desc")) == section_desc_cleaned:
                    matched_sections.append(section_data.get("Section"))

            if matched_sections:
                dispatcher.utter_message(text=f"The section number: {', '.join(map(str, matched_sections))}")
            else:
                dispatcher.utter_message(text=f"Section number not found for the provided description: {section_desc}")
        else:
            dispatcher.utter_message(text="Please provide a valid section description.")

        return []


class ActionGetSectionNumberByTitle(Action):
    def name(self) -> Text:
        return "action_get_section_number_by_title"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            ipc_file_path = os.path.join(
                "C:\\",
                "Users",
                "mamid",
                "AppData",
                "Local",
                "Programs",
                "Python",
                "Python310",
                "chatbot",
                "actions",
                "ipc.json"
            )
            with open(ipc_file_path, "r", encoding="utf-8") as file:
                ipc_data = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: 'ipc.json' file not found.")
            return []
        except Exception as e:
            dispatcher.utter_message(text=f"Error loading 'ipc.json' file: {e}")
            return []

        section_title = next(tracker.get_latest_entity_values("section_title"), None)
        if section_title is not None:
            section_title_cleaned = preprocess_text(section_title)
            matched_sections = []
            for section_data in ipc_data:
                if preprocess_text(section_data.get("section_title")) == section_title_cleaned:
                    matched_sections.append(section_data.get("Section"))

            if matched_sections:
                dispatcher.utter_message(text=f"The section number: {', '.join(map(str, matched_sections))}")
            else:
                dispatcher.utter_message(text=f"Section number not found for the provided title: {section_title}")
        else:
            dispatcher.utter_message(text="Please provide a valid section title.")

        return []



class ActionGetChapterDetails(Action):
    def name(self) -> Text:
        return "action_get_chapter_details"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            ipc_file_path = os.path.join(
                "C:\\",
                "Users",
                "mamid",
                "AppData",
                "Local",
                "Programs",
                "Python",
                "Python310",
                "chatbot",
                "actions",
                "ipc.json"
            )
            with open(ipc_file_path, "r", encoding="utf-8") as file:
                ipc_data = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: 'ipc.json' file not found.")
            return []
        except Exception as e:
            dispatcher.utter_message(text=f"Error loading 'ipc.json' file: {e}")
            return []

        chapter_number = next(tracker.get_latest_entity_values("chapter"), None)
        if chapter_number is not None:
            chapter_number = int(chapter_number)
            chapter_data = [
                section for section in ipc_data if section.get("chapter") == chapter_number
            ]
            if chapter_data:
                chapter_title = chapter_data[0].get("chapter_title")
                message = f"Details of Chapter {chapter_number} - {chapter_title}:\n"
                for section in chapter_data:
                    message += f"Section {section.get('Section')}: {section.get('section_title')} - {section.get('section_desc')}\n"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text=f"No sections found for Chapter {chapter_number}.")
        else:
            dispatcher.utter_message(text="Please provide a valid chapter number.")

        return []
class ActionGetSectionNumberByDescription(Action):
    def name(self) -> Text:
        return "action_get_section_number_by_description"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            ipc_file_path = os.path.join(
                "C:\\",
                "Users",
                "mamid",
                "AppData",
                "Local",
                "Programs",
                "Python",
                "Python310",
                "chatbot",
                "actions",
                "ipc.json"
            )
            with open(ipc_file_path, "r", encoding="utf-8") as file:
                ipc_data = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: 'ipc.json' file not found.")
            return []
        except Exception as e:
            dispatcher.utter_message(text=f"Error loading 'ipc.json' file: {e}")
            return []

        section_desc = next(tracker.get_latest_entity_values("section_desc"), None)
        if section_desc is not None:
            # Preprocess input text
            section_desc_cleaned = preprocess_text(section_desc)

            # Check for matches in JSON data
            matched_sections = []
            for section_data in ipc_data:
                if preprocess_text(section_data.get("section_desc")) == section_desc_cleaned:
                    matched_sections.append(section_data.get("Section"))

            if matched_sections:
                dispatcher.utter_message(text=f"The section number: {', '.join(map(str, matched_sections))}")
            else:
                dispatcher.utter_message(text=f"Section number not found for the provided description: {section_desc}")
        else:
            dispatcher.utter_message(text="Please provide a valid section description.")

        return []


class ActionGetSectionNumberAndTitleByDescription(Action):
    def name(self) -> Text:
        return "action_get_section_number_and_title_by_description"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            ipc_file_path = os.path.join(
                "C:\\",
                "Users",
                "mamid",
                "AppData",
                "Local",
                "Programs",
                "Python",
                "Python310",
                "chatbot",
                "actions",
                "ipc.json"
            )
            with open(ipc_file_path, "r", encoding="utf-8") as file:
                ipc_data = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="Error: 'ipc.json' file not found.")
            return []
        except Exception as e:
            dispatcher.utter_message(text=f"Error loading 'ipc.json' file: {e}")
            return []

        section_desc = next(tracker.get_latest_entity_values("section_desc"), None)
        if section_desc is not None:
            # Preprocess input text
            section_desc_cleaned = preprocess_text(section_desc)

            # Check for matches in JSON data
            matched_sections = []
            for section_data in ipc_data:
                if preprocess_text(section_data.get("section_desc")) == section_desc_cleaned:
                    matched_sections.append(section_data)

            if matched_sections:
                response = ""
                for section in matched_sections:
                    response += f"Section number: {section.get('Section')}, Title: {section.get('section_title')}\n"
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"Section number and title not found for the provided description: {section_desc}")
        else:
            dispatcher.utter_message(text="Please provide a valid section description.")

        return []




            # Check for matches in JSON data



def preprocess_text(text: str) -> str:
    # Convert text to lowercase
    text = text.lower()
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
