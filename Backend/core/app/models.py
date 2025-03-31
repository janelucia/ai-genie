from django.db import models
import os

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Research(models.Model):
    name = models.CharField(max_length=100)
    summary = models.CharField(max_length=255)
    source_file = models.FileField(upload_to='app/research_files/')

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        """Delete the file from storage when the object is deleted"""
        if self.source_file:
            if os.path.isfile(self.source_file.path):
                os.remove(self.source_file.path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Research"
        verbose_name_plural = "Research"

class Researcher(models.Model):
    firstname = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    related_research = models.ManyToManyField(
        Research,
        related_name="researchers",
        blank=True,
    )

    def __str__(self) -> str:
        return (self.firstname + " " + self.surname)
    
class Chat(models.Model):
    created = models.DateTimeField(auto_now_add = True, null = True)
    
    def __str__(self) -> str:
        return str(self.id)

class Message(models.Model):
    content = models.CharField(max_length=2000)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True, null=True)
    ai_response = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return "chat: " + str(self.chat) + " | content: " + str(self.content)