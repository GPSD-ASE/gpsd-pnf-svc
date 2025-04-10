# Push Notification Service

## Overview

This service provides a robust push notification system for Android mobile applications using Firebase Cloud Messaging (FCM). It handles device registration, notification queueing, and reliable delivery of push notifications to registered devices.

## Functionality

### Core Features

- **Device Registration**: Register Android devices with user IDs and FCM tokens
- **Notification Management**: Queue, send, and track notifications
- **Push Notification Delivery**: Send notifications to registered devices via FCM
- **Status Tracking**: Monitor notification delivery status (pending, sent, failed, delivered, read)
- **Batch Processing**: Support for sending notifications to multiple devices

### API Endpoints

- `POST /notify/register`: Register a device with its FCM token
- `POST /notify/send`: Queue a notification for delivery
- `GET /notifications/{user_id}`: Retrieve all notifications for a specific user
- `POST /notify/send_push`: Directly send push notifications without queueing
- `GET /health`: Service health check endpoint

## Tech Stack

- **FastAPI**: High-performance Python web framework
- **Firebase Admin SDK**: For database operations and FCM integration
- **Firebase Realtime Database**: For storing device registrations and notifications
- **Firebase Cloud Messaging (FCM)**: For delivering push notifications to Android devices
- **Uvicorn**: ASGI server for running the FastAPI application
- **Pydantic**: For data validation and model definitions
- **Docker**: For containerization and deployment
- **Python 3.9**: Programming language

### System Architecture

The service follows a layered architecture:

1. **API Layer**: FastAPI routes that handle HTTP requests
2. **Service Layer**: Business logic for notification processing
3. **Data Layer**: Firebase Realtime Database for persistence
4. **Integration Layer**: Firebase Cloud Messaging for notification delivery

### Notification Flow

1. Client registers device with the service, providing user ID and FCM token
2. Application sends notification request to the service
3. Service stores notification in Firebase with 'pending' status
4. Background listener detects new notifications and processes them
5. Service retrieves the target device's FCM token
6. Notification is sent via FCM to the target device
7. Notification status is updated to 'sent' or 'failed'

## Design Patterns

### Repository Pattern
- Abstracts data storage operations through Firebase references
- Provides a clean interface for database interactions

### Observer Pattern
- Database listeners observe changes to the notification queue
- Triggers notification processing when new entries are detected

### Factory Pattern
- Creates appropriate notification objects based on device type and payload

### Model-View-Controller (MVC)
- **Models**: Pydantic classes define data structures
- **Controllers**: API routes handle request processing
- **Services**: Business logic implementation

### Asynchronous Processing
- Uses async/await for non-blocking I/O operations
- Implements threading for background notification processing

## Implementation Details

### Device Registration
Devices register by providing a unique user ID and FCM token, which are stored in Firebase Realtime Database for later use when sending notifications.

### Notification Queueing
Notifications are queued in Firebase with a 'pending' status, allowing for reliable delivery even if the service experiences temporary issues.

### Background Processing
A dedicated background thread listens for new notifications and processes them asynchronously, ensuring the main application remains responsive.

### Error Handling
Comprehensive error handling ensures that failed notifications are properly logged and their status updated accordingly.

### Security
- Firebase authentication for secure API access
- Input validation using Pydantic models
- Non-root user in Docker container

## Deployment

### Docker
The service is containerized using Docker, making it easy to deploy in any environment that supports containers.

```bash
# Build the Docker image
docker build -t push-notification-service .

# Run the container
docker run -p 8000:8000 push-notification-service
```

### Docker Compose
For more complex deployments, a docker-compose.yaml file is provided:

```bash
docker-compose up -d
```
