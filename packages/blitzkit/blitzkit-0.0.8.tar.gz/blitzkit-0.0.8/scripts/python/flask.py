""" provides OS-level operations to create directories and files for a flask project """
import os
import textwrap

def create(app_name: str) -> None:
    """
    Sets up a basic Flask backend project structure with essential files and configurations.

    This function creates a directory structure for the backend using the 
        specified application name.
    It includes the following components:
    
    - `backend/app/__init__.py`: Initializes the app module.
    - `backend/app/app.py`: Contains the Flask application factory with CORS and session management.
    - `backend/app/run.py`: Runs the application using the production configuration.
    - `backend/config.py`: Provides environment-specific configurations using `python-decouple`.
    - `backend/requirements.txt`: Lists necessary Python packages for the project.

    Args:
        app_name (str): The name of the application, used to create the project directory.

    Example:
        setup_flask_project("my_project")
    """
    backend_dir = os.path.join(app_name, "backend")
    os.makedirs(os.path.join(backend_dir, "app"), exist_ok=True)

    with open(os.path.join(backend_dir, "app", "__init__.py"), 'w', encoding='utf-8') as f:
        f.write("# Backend init file\n")

    with open(os.path.join(backend_dir, "app", "app.py"), 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(
            """
            from flask import Flask, session
            from flask_session import Session
            from flask_cors import CORS

            def create_app(config):
                app = Flask(__name__)
                app.config.from_object(config)
                CORS(app, supports_credentials=True, automatic_options=True, allow_headers='*')
                Session(app)
                return app
            """.lstrip('\n'))
        )

    with open(os.path.join(backend_dir, "app", "run.py"), 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(
            """
            from app import create_app
            from config import ProdConfig

            if __name__ == '__main__':
                app = create_app(ProdConfig)
                app.run(debug=True)
            """.lstrip('\n'))
        )

    with open(os.path.join(backend_dir, "config.py"), 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(
            """
            from decouple import config

            class Config:
                SECRET_KEY = config('SECRET_KEY')

            class DevConfig(Config):
                pass

            class ProdConfig(Config):
                pass

            class TestConfig(Config):
                pass
            """.lstrip('\n'))
        )


    with open(os.path.join(backend_dir, "requirements.txt"), 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(
            """
            async-timeout==4.0.3
            blinker==1.7.0
            cachelib==0.10.2
            certifi==2023.7.22
            cffi==1.16.0
            charset-normalizer==3.3.2
            click==8.1.7
            colorama==0.4.6
            cryptography==41.0.5
            python-decouple==3.8
            Deprecated==1.2.14
            dnspython==2.4.2
            Flask==2.3.3
            Flask-Cors==4.0.0
            Flask-Session==0.5.0
            idna==3.4
            importlib-metadata==6.9.0
            isort==5.12.0
            itsdangerous==2.1.2
            packaging==23.2
            pycparser==2.21
            pyflakes==3.1.0
            python-dotenv==1.0.0
            requests==2.31.0
            typing_extensions==4.8.0
            urllib3==2.0.7
            Werkzeug==2.3.8
            wrapt==1.16.0
            zipp==3.17.0
            """.lstrip('\n'))
        )
