# gpsd-pnf-svc
Notification Service Management

This is a Notification Service Management system that handles device registration and notification delivery. The service allows:
1. Registering devices with user IDs and device tokens
2. Sending notifications to registered users
3. Retrieving notifications for specific users

The service is built using:
- **FastAPI**: A modern, high-performance web framework for building APIs with Python
- 
- **Firebase Admin SDK**: Used for database operations and potentially notification delivery
- 
- **Uvicorn**: ASGI server for running the FastAPI application
- 
- **Pydantic**: For data validation and settings management
- 
- **Firebase Realtime Database**: For storing device registrations and notifications

This follows an  architecture of RESTful API design pattern with endpoints for device registration, notification sending, and notification retrieval

**Firebase Integration**: The service uses Firebase for both authentication and data storage, with security rules defined for read/write access

**Asynchronous API Design**: The endpoints are implemented as async functions, allowing for non-blocking I/O operations

**Notification Queueing**: Notifications are stored with a 'pending' status, suggesting a queue-based approach for processing

**Server Threading**: The application runs the FastAPI server in a separate thread, allowing for other operations to run concurrently

**Timestamp Server Value**: Uses Firebase's server timestamp feature to record when notifications are created


**Repository Pattern**: Abstracting the data storage layer through Firebase references

**Model-View-Controller (MVC)**: Separation of data models (Pydantic classes) from the controller logic (API routes)

**Dependency Injection**: FastAPI's approach to handling dependencies and services

**Data Transfer Objects (DTOs)**: Using Pydantic models to define the structure of incoming and outgoing data

**Error Handling Pattern**: Consistent approach to exception handling and HTTP error responses
