import os
import textwrap

def create(app_name: str) -> None:
    """
    Sets up a basic FastAPI backend project structure with essential files and configurations.

    This function creates a directory structure for the backend using the 
    specified application name.
    It includes the following components:
    
    - `backend/app/main.py`: Contains the FastAPI application.
    - `backend/config.py`: Provides environment-specific configurations.
    - `backend/requirements.txt`: Lists necessary Python packages for the project.

    Args:
        app_name (str): The name of the application, used to create the project directory.

    Example:
        create_fastapi_project("my_fastapi_project")
    """
    backend_dir = os.path.join(app_name, "backend")
    os.makedirs(os.path.join(backend_dir, "app"), exist_ok=True)

    with open(os.path.join(backend_dir, "app", "main.py"), 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(
            """
            from fastapi import FastAPI

            app = FastAPI()

            @app.get("/")
            async def read_root():
                return {"Hello": "World"}

            @app.get("/items/{item_id}")
            async def read_item(item_id: int, q: str = None):
                return {"item_id": item_id, "q": q}
            """.lstrip('\n'))
        )

    with open(os.path.join(backend_dir, "config.py"), 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(
            """
            from pydantic import BaseSettings

            class Settings(BaseSettings):
                app_name: str = "FastAPI Application"
                admin_email: str = "admin@example.com"
                items_per_user: int = 50

            settings = Settings()
            """.lstrip('\n'))
        )

    with open(os.path.join(backend_dir, "requirements.txt"), 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(
            """
            fastapi
            uvicorn
            pydantic
            python-dotenv
            fastapi[standard]

            """.lstrip('\n'))
        )

