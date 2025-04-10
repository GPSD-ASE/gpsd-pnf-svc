import os
from pydantic import BaseSettings
from typing import Optional, Dict, Any, List

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Push Notification Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Firebase settings
    FIREBASE_CREDENTIALS_PATH: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "GPSD Google Firebase.json")
    FIREBASE_DATABASE_URL: str = os.getenv("FIREBASE_DATABASE_URL", "https://gpsd-notification-service-default-rtdb.europe-west1.firebasedatabase.app/")
    
    # API settings
    API_PREFIX: str = "/api"
    CORS_ORIGINS: List[str] = ["*"]  # Update for production
    
    # FCM settings
    FCM_SERVER_KEY: Optional[str] = os.getenv("FCM_SERVER_KEY")
    FCM_SENDER_ID: Optional[str] = os.getenv("FCM_SENDER_ID")
    
    # Notification settings
    DEFAULT_NOTIFICATION_TTL: int = 86400  # 24 hours in seconds
    MAX_BATCH_SIZE: int = 500  # Maximum number of notifications to process in a batch
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Performance settings
    WORKER_THREADS: int = int(os.getenv("WORKER_THREADS", "4"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings object
settings = Settings()

# Firebase collections
FIREBASE_COLLECTIONS = {
    "devices": "devices",
    "notifications": "notifications",
    "users": "users"
}

# Notification statuses
NOTIFICATION_STATUS = {
    "PENDING": "pending",
    "SENT": "sent",
    "FAILED": "failed",
    "DELIVERED": "delivered",
    "READ": "read"
}

# Device types
DEVICE_TYPES = {
    "ANDROID": "android",
    "IOS": "ios",
    "WEB": "web"
}

# Notification priorities
NOTIFICATION_PRIORITY = {
    "HIGH": "high",
    "NORMAL": "normal",
    "LOW": "low"
}
