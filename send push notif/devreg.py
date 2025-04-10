import requests

# Backend API URL
BASE_URL = "http://localhost:8000"

def register_device(user_id, fcm_token, device_info):
    """
    Registers the device with the backend service.
    :param user_id: User ID
    :param fcm_token: FCM Token from the Android app
    :param device_info: Additional device info (e.g., model, OS version)
    """
    payload = {
        "user_id": user_id,
        "token": fcm_token,
        "device_info": device_info
    }
    
    response = requests.post(f"{BASE_URL}/notify/register", json=payload)
    
    if response.status_code == 200:
        print("Device registered successfully:", response.json())
    else:
        print("Failed to register device:", response.text)

# Example usage
user_id = 1
fcm_token = "your_fcm_token_here"
device_info = {
    "device_type": "Android",
    "model": "Pixel 6",
    "os_version": "Android 15"
}

register_device(user_id, fcm_token, device_info)
