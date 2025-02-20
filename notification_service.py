from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, db
from typing import Dict, Optional

# Initialize FastAPI
app = FastAPI()

# Firebase initialization
cred = credentials.Certificate('/content/GPSD Google Firebase.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://gpsd-notification-service-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Data Models
class NotificationBase(BaseModel):
    user_id: int
    message: str
    title: str
    device_type: str = "android"

class DeviceRegistration(BaseModel):
    user_id: int
    token: str
    device_info: Dict[str, str]

# Routes
@app.post("/notify/register")
async def register_device(registration: DeviceRegistration):
    try:
        ref = db.reference('devices')
        ref.child(str(registration.user_id)).set({
            'token': registration.token,
            'device_info': registration.device_info
        })
        return {"status": "success", "message": "Device registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/notify/send")
async def send_notification(notification: NotificationBase):
    try:
        # Save notification to Firebase
        ref = db.reference('notifications')
        notification_data = {
            'user_id': notification.user_id,
            'message': notification.message,
            'title': notification.title,
            'status': 'pending',
            'timestamp': {'.sv': 'timestamp'}
        }
        ref.push().set(notification_data)
        return {"status": "success", "message": "Notification queued successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notifications/{user_id}")
async def get_user_notifications(user_id: int):
    try:
        ref = db.reference('notifications')
        notifications = ref.order_by_child('user_id').equal_to(user_id).get()
        return {"notifications": notifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Enable nested event loops
nest_asyncio.apply()

# Run the FastAPI application
def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Start the server in a separate thread
server = Thread(target=run_server)
server.start()

{
  "rules": {
    "notifications": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "devices": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}

import requests

# Register a device
device_data = {
    "user_id": 1,
    "token": "fcm_token_here",
    "device_info": {
        "device_type": "Android",
        "ip": "127.0.0.1"
    }
}
response = requests.post("http://localhost:8000/notify/register", json=device_data)
print(response.json())

# Send a notification
notification_data = {
    "user_id": 96,
    "message": "Test Notification",
    "title": "Test",
    "device_type": "Android"
}
response = requests.post("http://localhost:8000/notify/send", json=notification_data)
print(response.json())
