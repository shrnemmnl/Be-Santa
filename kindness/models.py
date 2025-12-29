from django.db import models

class KindnessMessage(models.Model):
    EMOTION_CHOICES = [
        ('kindness', 'Kindness'),
        ('love', 'Love'),
        ('hope', 'Hope'),
    ]

    message_text = models.TextField()
    emotion_type = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    is_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_flagged = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Soft delete functionality

    def __str__(self):
        return f"{self.emotion_type}: {self.message_text[:50]}"
