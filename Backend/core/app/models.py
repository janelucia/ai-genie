from django.db import models
import os
from .ai_engine.vector_db_service import VectorDatabaseService
from .ai_engine.research_summary_service import summarize_text, extract_keywords

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    img = models.ImageField(upload_to='events_images/', blank=True)
    description = models.CharField(max_length=500)
    contact_email = models.EmailField()
    location = models.CharField(max_length=100, default="AILab")

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        """Delete the file from storage when the object is deleted"""
        if self.img:
            if os.path.isfile(self.img.path):
                os.remove(self.img.path)
        super().delete(*args, **kwargs)

class Research(models.Model):
    name = models.CharField(max_length=100)
    summary = models.CharField(max_length=500, blank=True)
    source_file = models.FileField(upload_to='research_files/')
    keywords = models.CharField(max_length=500, blank=True) # coma separated tags

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # emits signals: generate_summary_and_keywords
        is_new = self.pk is None
        try:
            old_instance = Research.objects.get(pk=self.pk)
            old_file_path = old_instance.source_file.name
        except Research.DoesNotExist:
            old_file_path = None

        super().save(*args, **kwargs)

        vector_db = VectorDatabaseService(reset_collection=False)
        current_file_path = self.source_file.name

        if self.source_file and os.path.isfile(self.source_file.path):
            if is_new:
                vector_db.add_file(current_file_path)
            elif current_file_path != old_file_path:
                vector_db.update_file(current_file_path)

        if (not self.summary or not self.keywords) and vector_db.file_exists(current_file_path):
            text = vector_db.get_file_text(current_file_path)
            updated = False
            if not self.summary:
                self.summary = summarize_text(text)
                updated = True
            if not self.keywords:
                self.keywords = extract_keywords(text)
                updated = True
            if updated:
                print("reached updated")
                super().save(update_fields=["summary", "keywords"])

    def delete(self, *args, **kwargs):
        """Delete the file from storage and vector db when the object is deleted"""
        file_path : str = self.source_file.name
        if self.source_file:
            if os.path.isfile(self.source_file.path):
                os.remove(self.source_file.path)

        # Remove from vector DB
        vector_db = VectorDatabaseService(reset_collection=False)
        vector_db.delete_file(file_path)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Research"
        verbose_name_plural = "Research"

class Researcher(models.Model):
    firstname = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    position = models.CharField(max_length=25)
    short_about = models.CharField(max_length=30)
    about = models.CharField(max_length=500)
    email = models.EmailField(blank=True)
    linkedin = models.CharField(max_length=25, blank=True)
    keywords = models.CharField(max_length=500, blank=True) # coma separated tags
    related_research = models.ManyToManyField(
        Research,
        related_name="researchers_related",
        blank=True,
    )
    img = models.ImageField(upload_to='researchers_images/',blank=True)

    def __str__(self) -> str:
        return (self.firstname + " " + self.surname)
    
    def delete(self, *args, **kwargs):
        """Delete the file from storage when the object is deleted"""
        if self.img:
            if os.path.isfile(self.img.path):
                os.remove(self.img.path)
        super().delete(*args, **kwargs)

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