from django.db import models

# Create your models here.
class SelectedSite(models.Model):
    sitechoice = models.CharField(max_length = 200)

    def __str__(self):
        return self.sitechoice
