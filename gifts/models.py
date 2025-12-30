from django.db import models
from django.conf import settings

class Gift(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gifts_given')
    image = models.ImageField(upload_to='gifts/')
    note = models.TextField(blank=True, null=True, help_text="A few kind words, if you wish…")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gift by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"
