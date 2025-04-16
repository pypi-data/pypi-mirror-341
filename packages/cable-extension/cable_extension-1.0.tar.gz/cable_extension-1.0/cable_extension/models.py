from django.db import models
from dcim.models import Cable

class CableExtension(models.Model):
    cable = models.OneToOneField(
        Cable,
        on_delete=models.CASCADE,
        related_name='extension'
    )
    cable_length = models.PositiveIntegerField(blank=True, null=True,
                                            help_text="Cable length in meters")
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Extension for cable {self.cable.id}"
