from enum import Enum
from dataclasses import dataclass

@dataclass
class TechStack:
    language: str
    script: str

class Framework(Enum):
    FLASK = TechStack("python", "flask.py")
    FAST_API = TechStack("python", "fastapi.py")
    REACT_JS = TechStack('javascript', 'react-js.py')
    REACT_TS = TechStack('typescript', 'react-ts.py')
    ANGULAR = TechStack('typescript', 'angular-ts.py')
    VUE = TechStack('javascript', 'vue.py')

    @classmethod
    def get_framework(cls, name):
        """Retreives the given framework from the Framework Enum"""
        try:
            name = name.replace('-', '_')
            framework = cls[name.upper()].value
            return framework.language, framework.script
        except KeyError:
            return None
