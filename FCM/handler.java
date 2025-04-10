public class MyFirebaseMessagingService extends FirebaseMessagingService {
    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        // Handle FCM messages here
        if (remoteMessage.getNotification() != null) {
            String title = remoteMessage.getNotification().getTitle();
            String body = remoteMessage.getNotification().getBody();
            // Display notification
        }

        if (remoteMessage.getData().size() > 0) {
            // Handle data payload
        }
    }

    @Override
    public void onNewToken(String token) {
        // Send token to your server
    }
}
