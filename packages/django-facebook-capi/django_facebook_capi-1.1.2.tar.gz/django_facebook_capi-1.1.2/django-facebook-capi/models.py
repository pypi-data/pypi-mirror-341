from django.db import models

class FacebookEventLog(models.Model):
    EVENT_CHOICES = [
        ('PageView', 'PageView'),
        ('ViewContent', 'ViewContent'),
        ('Lead', 'Lead'),
        ('AddToCart', 'AddToCart'),
        ('InitiateCheckout', 'InitiateCheckout'),
        ('Purchase', 'Purchase'),
        ('CustomEvent', 'CustomEvent'),
    ]

    event_name = models.CharField(max_length=50, choices=EVENT_CHOICES)
    status_code = models.PositiveIntegerField()
    response_text = models.TextField()
    source_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.event_name} - {self.status_code} @ {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
