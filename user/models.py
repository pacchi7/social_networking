from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_profile'
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfile"
        ordering = ["id"]

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'friend_request'
        verbose_name = "Friend Request"
        verbose_name_plural = "FriendRequest"
        ordering = ["id"]


class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends_with', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'friendship'
        verbose_name = "Friendship"
        verbose_name_plural = "Friendships"
        ordering = ["id"]

    # def save(self, *args, **kwargs):
    #     # Ensure that user1 is always less than user2 to avoid duplicates
    #     if self.user1.id > self.user2.id:
    #         self.user1, self.user2 = self.user2, self.user1
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"