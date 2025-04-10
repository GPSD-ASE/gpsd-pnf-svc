from firebase_admin import messaging

def send_notification_to_device(fcm_token, title, body):
    """
    Sends a notification to a specific device using FCM.
    :param fcm_token: Device's FCM token
    :param title: Notification title
    :param body: Notification body
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=fcm_token,
    )
    
    try:
        response = messaging.send(message)
        print("Successfully sent message:", response)
        return response
    except Exception as e:
        print("Error sending message:", str(e))
        return None

# Example usage
fcm_token = "your_device_fcm_token_here"
title = "Hello!"
body = "This is a test notification."
send_notification_to_device(fcm_token, title, body)
