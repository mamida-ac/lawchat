from django.shortcuts import render
from django.http import JsonResponse
import requests
import logging

# Configure logging
logger = logging.getLogger(__name__)
def rasahome(request):
    return render(request, "index.html")

def send_message(request):
    if request.method == "POST":
        user_message = request.POST.get("user_message")
        logger.info(f"User message: {user_message}")

        # Rasa server URL
        rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"

        try:
            # Send POST request to Rasa server
            response = requests.post(rasa_server_url, json={"message": user_message})
            response.raise_for_status()  # Raise exception for non-200 status codes

            # Parse JSON response
            bot_response = response.json()
            bot_response_text=""
            # Check if bot response contains text
            if bot_response and isinstance(bot_response, list):
                for message in bot_response:
                    if message.get("text"):
                        bot_response_text += message["text"] + "\n"
            else:
                bot_response_text = "Sorry, I didn't understand that."

            logger.info(f"Bot response: {bot_response_text}")
            #print(bot_response_text)
            return JsonResponse({"bot_response": bot_response_text})

        except requests.RequestException as e:
            # Log error
            logger.error(f"Error sending message to Rasa server: {e}")

            # Return error response
            return JsonResponse({"error": "Error sending message to Rasa server"}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
