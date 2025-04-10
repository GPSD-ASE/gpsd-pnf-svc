from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class DeviceType(str, Enum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"

class NotificationPriority(str, Enum):
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"
    READ = "read"

class DeviceRegistration(BaseModel):
    user_id: int
    token: str
    device_info: Dict[str, str] = Field(default_factory=dict)
    device_type: DeviceType = DeviceType.ANDROID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 123,
                "token": "fcm_token_string",
                "device_info": {
                    "model": "Pixel 6",
                    "os_version": "Android 12",
                    "app_version": "1.2.3"
                },
                "device_type": "android"
            }
        }

class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    device_type: DeviceType = DeviceType.ANDROID
    priority: NotificationPriority = NotificationPriority.NORMAL
    data: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 123,
                "title": "New Message",
                "message": "You have received a new message",
                "device_type": "android",
                "priority": "high",
                "data": {
                    "message_id": "abc123",
                    "sender": "user456"
                }
            }
        }

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: Optional[str] = None
    status: NotificationStatus = NotificationStatus.PENDING
    created_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": "notification_id_123",
                "user_id": 123,
                "title": "New Message",
                "message": "You have received a new message",
                "device_type": "android",
                "priority": "high",
                "data": {
                    "message_id": "abc123",
                    "sender": "user456"
                },
                "status": "sent",
                "created_at": "2025-04-10T10:30:00",
                "sent_at": "2025-04-10T10:30:05",
                "delivered_at": None,
                "read_at": None,
                "error_message": None
            }
        }

class BatchNotificationRequest(BaseModel):
    notifications: List[NotificationCreate]
    
    @validator('notifications')
    def validate_batch_size(cls, v):
        if len(v) > 500:  # Maximum batch size
            raise ValueError('Batch size cannot exceed 500 notifications')
        return v

class NotificationFilter(BaseModel):
    user_id: Optional[int] = None
    status: Optional[NotificationStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100
    offset: int = 0

class ErrorResponse(BaseModel):
    detail: str
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "User not found or no device registered"
            }
        }

class SuccessResponse(BaseModel):
    status: str
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Notification sent successfully"
            }
        }

class TokenValidationResponse(BaseModel):
    is_valid: bool
    user_id: Optional[int] = None
    device_type: Optional[DeviceType] = None
    
    class Config:
        schema_extra = {
            "example": {
                "is_valid": True,
                "user_id": 123,
                "device_type": "android"
            }
        }
