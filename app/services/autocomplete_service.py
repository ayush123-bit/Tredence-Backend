import re
from app.schemas import AutocompleteResponse

class AutocompleteService:
    def __init__(self):
        self.python_suggestions = {
            "def ": "def function_name(param):\n    pass",
            "class ": "class ClassName:\n    def __init__(self):\n        pass",
            "for ": "for item in iterable:\n    pass",
            "if ": "if condition:\n    pass",
            "elif ": "elif condition:\n    pass",
            "else:": "else:\n    pass",
            "import ": "import module",
            "from ": "from module import something",
            "while ": "while condition:\n    pass",
            "try:": "try:\n    pass\nexcept Exception as e:\n    pass",
            "with ": "with open('file.txt') as f:\n    content = f.read()",
            "async def ": "async def function_name(param):\n    pass",
            "await ": "await async_function()",
        }
    
    def get_suggestion(self, code: str, cursor_position: int, language: str) -> AutocompleteResponse:
        """Generate mocked autocomplete suggestion"""
        
        # Get the line where cursor is
        lines = code[:cursor_position].split('\n')
        current_line = lines[-1] if lines else ""
        
        # Simple pattern matching for Python
        if language == "python":
            for pattern, suggestion in self.python_suggestions.items():
                if current_line.strip().startswith(pattern.strip()):
                    return AutocompleteResponse(
                        suggestion=suggestion,
                        confidence=0.85
                    )
            
            # Default suggestions based on context
            if "print" in current_line:
                return AutocompleteResponse(
                    suggestion='print("Hello, World!")',
                    confidence=0.75
                )
            
            if "=" in current_line and "(" not in current_line:
                return AutocompleteResponse(
                    suggestion="variable = value",
                    confidence=0.65
                )
            
            # MongoDB-specific suggestions
            if "mongo" in current_line.lower() or "collection" in current_line.lower():
                return AutocompleteResponse(
                    suggestion="collection.find_one({'_id': ObjectId(id)})",
                    confidence=0.80
                )
        
        # Default fallback
        return AutocompleteResponse(
            suggestion="# Continue coding...",
            confidence=0.5
        )