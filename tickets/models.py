import random

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
TICKET_STATUS_CHOICES = [
    (1, 'Active'),
    (2, 'Pending'),
    (3, 'Resolved'),
]

TICKET_PRIORITY_CHOICES = [
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High'),
]

def generate_unique_ticket_id():
    length = 7
    while True:
        ticket_id = ''.join(random.choices('0123456789', k=length))
        if not Ticket.objects.filter(ticket_id=ticket_id).exists():
            return ticket_id

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=7, unique=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.IntegerField(choices=TICKET_STATUS_CHOICES, default=1)
    priority = models.IntegerField(choices=TICKET_PRIORITY_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_tickets')
    engineer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='engineer_tickets', null=True)

    def get_status_display(self):
        return dict(TICKET_STATUS_CHOICES).get(self.status, 'Unknown')
    def get_priority_display(self):
        return dict(TICKET_PRIORITY_CHOICES).get(self.priority, 'Unknown priority')

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = generate_unique_ticket_id()
        super().save(*args, **kwargs)
