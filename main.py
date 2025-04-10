import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, db, messaging
from typing import List, Dict, Optional
import asyncio
import threading
import os
from datetime import datetime

# Import models and routes
from models import NotificationBase, DeviceRegistration, NotificationResponse
from routes import notification_router
from middleware import auth_middleware
from services.notification_service import NotificationService

# Initialize FastAPI app
app = FastAPI(
    title="Push Notification Service",
    description="API for managing device registrations and sending push notifications",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase
try:
    cred = credentials.Certificate('GPSD Google Firebase.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('FIREBASE_DATABASE_URL', 'https://gpsd-notification-service-default-rtdb.europe-west1.firebasedatabase.app/')
    })
    print("Firebase initialized successfully")
except Exception as e:
    print(f"Error initializing Firebase: {str(e)}")
    raise

# Create notification service instance
notification_service = NotificationService()

# Include routers
app.include_router(notification_router, prefix="/api", tags=["notifications"])

# Function to listen for new notifications
def listen_for_notifications():
    def on_notification_added(event):
        notification = event.data
        if notification and notification.get('status') == 'pending':
            user_id = notification.get('user_id')
            title = notification.get('title')
            message = notification.get('message')
            
            # Create a new event loop for the async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Send the notification
            success = loop.run_until_complete(notification_service.send_push_notification(user_id, title, message))
            
            # Update notification status
            if success:
                # Get the key of the notification
                notification_key = event.path.split('/')[-1]
                ref = db.reference(f'notifications/{notification_key}')
                ref.update({
                    'status': 'sent',
                    'sent_at': datetime.now().isoformat()
                })
            else:
                notification_key = event.path.split('/')[-1]
                ref = db.reference(f'notifications/{notification_key}')
                ref.update({
                    'status': 'failed',
                    'error_at': datetime.now().isoformat()
                })
            
            loop.close()
    
    # Listen for new notifications
    ref = db.reference('notifications')
    ref.listen(on_notification_added)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to Push Notification Service API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    try:
        # Check Firebase connection
        db.reference('/').get()
        return {
            "status": "healthy",
            "firebase": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Direct notification endpoint
@app.post("/notify/send_push", response_model=Dict[str, str], tags=["notifications"])
async def send_push(notification: NotificationBase):
    try:
        # Send the push notification
        success = await notification_service.send_push_notification(
            notification.user_id, 
            notification.title, 
            notification.message
        )
        
        if success:
            return {"status": "success", "message": "Push notification sent successfully"}
        else:
            return {"status": "failed", "message": "Failed to send push notification"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Start the notification listener in a separate thread when the app starts
@app.on_event("startup")
async def startup_event():
    # Start the notification listener in a separate thread
    notification_listener = threading.Thread(target=listen_for_notifications, daemon=True)
    notification_listener.start()
    print("Notification listener started")

# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
