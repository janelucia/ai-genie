from django.apps import AppConfig
from .ai_engine.vector_db_service import VectorDatabaseService
import os
from django.conf import settings

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # import app.signals
        try:
            # Initialize the vector DB service (without resetting collection on each startup)
            self.vector_db_service = VectorDatabaseService(reset_collection=False)
            research_dir = settings.RESEARCH_FILES_DIR
            for file in os.listdir(research_dir):
                full_path = os.path.join(research_dir, file)
                if os.path.isfile(full_path):
                    self.vector_db_service.add_file(file)
            print("VectorDatabaseService initialized successfully.")
        except Exception as e:
            print(f"Error initializing VectorDatabaseService: {e}")