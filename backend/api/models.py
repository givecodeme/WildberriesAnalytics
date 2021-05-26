from django.db import models


class Todos(models.Model):
    title = models.CharField(max_length=250)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("todos")
        verbose_name_plural = ("todoss")

    def __str__(self):
        return self.title
