import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase Admin SDK
cred = credentials.Certificate('GPSD Google Firebase.json')
firebase_admin.initialize_app(cred)

def send_fcm_notification(token, title, body, data=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=data,
        token=token
    )

    try:
        response = messaging.send(message)
        print('Successfully sent message:', response)
        return response
    except Exception as e:
        print('Error sending message:', e)
        return None

# Example usage
device_token = 'YOUR_DEVICE_TOKEN_HERE'
send_fcm_notification(
    device_token,
    'Welcome',
    'Hello from Firebase!',
    {'key1': 'value1', 'key2': 'value2'}
)
