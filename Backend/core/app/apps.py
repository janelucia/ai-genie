from django.apps import AppConfig
from .ai_engine.vector_db_service import VectorDatabaseService

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        try:
            # Initialize the vector DB service (without resetting collection on each startup)
            self.vector_db_service = VectorDatabaseService(reset_collection=False)
            # self.vector_db_service.add_file('rector.pdf')
            # self.vector_db_service.add_file('NumericalMethodsResearchPaper.pdf')
            self.vector_db_service.add_file('The_Role_of_Renewable_Energy_in_Combating_Climate_Change.pdf')
            print(id(self.vector_db_service))
            print("VectorDatabaseService initialized successfully.")
        except Exception as e:
            print(f"Error initializing VectorDatabaseService: {e}")