from django.db import models

# Create your models here.
class Subscirber(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=128)

    def __str__(self):
        return ("{} -> {}").format(self.email, self.name)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
