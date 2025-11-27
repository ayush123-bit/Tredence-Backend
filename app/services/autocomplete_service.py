import re
from app.schemas import AutocompleteResponse

class AutocompleteService:
    def __init__(self):
        self.python_suggestions = {
            "def ": "def function_name(param):\n    return result",
            "class ": "class ClassName:\n    def __init__(self):\n        self.attribute = value",
            "for ": "for item in items:\n    print(item)",
            "if ": "if condition:\n    # do something\n    pass",
            "elif ": "elif another_condition:\n    # do something else\n    pass",
            "else": "else:\n    # default case\n    pass",
            "import ": "import module_name",
            "from ": "from module import function",
            "while ": "while condition:\n    # loop body\n    pass",
            "try": "try:\n    # code that might raise exception\n    pass\nexcept Exception as e:\n    print(f'Error: {e}')",
            "with ": "with open('file.txt', 'r') as f:\n    content = f.read()",
            "async def ": "async def async_function(param):\n    result = await some_async_call()\n    return result",
            "await ": "await async_function()",
            "lambda": "lambda x: x * 2",
            "return": "return value",
        }
        
        # Variable name suggestions
        self.common_patterns = {
            "print": 'print("Hello, World!")',
            "input": 'user_input = input("Enter value: ")',
            "open": "with open('filename.txt', 'r') as file:\n    content = file.read()",
            "range": "for i in range(10):\n    print(i)",
            "len": "length = len(collection)",
            "list": "my_list = [1, 2, 3, 4, 5]",
            "dict": "my_dict = {'key': 'value'}",
            "str": "text = str(value)",
            "int": "number = int(value)",
        }
    
    def get_suggestion(self, code: str, cursor_position: int, language: str) -> AutocompleteResponse:
        """Generate mocked autocomplete suggestion"""
        
        # Handle empty or very short code
        if not code or len(code.strip()) < 1:
            return AutocompleteResponse(
                suggestion="# Start typing Python code...",
                confidence=0.5
            )
        
        # Get the current line where cursor is
        lines = code[:cursor_position].split('\n')
        current_line = lines[-1] if lines else ""
        current_line_stripped = current_line.strip()
        
        print(f"[Autocomplete] Current line: '{current_line_stripped}'")
        
        # Python language specific suggestions
        if language == "python":
            # Check for exact keyword matches first
            for pattern, suggestion in self.python_suggestions.items():
                if current_line_stripped.endswith(pattern.strip()):
                    print(f"[Autocomplete] Matched pattern: {pattern}")
                    return AutocompleteResponse(
                        suggestion=suggestion,
                        confidence=0.90
                    )
            
            # Check for partial keyword matches
            for pattern, suggestion in self.python_suggestions.items():
                if pattern.strip() in current_line_stripped:
                    print(f"[Autocomplete] Partial match: {pattern}")
                    return AutocompleteResponse(
                        suggestion=suggestion,
                        confidence=0.85
                    )
            
            # Check for common patterns
            for keyword, suggestion in self.common_patterns.items():
                if keyword in current_line.lower():
                    print(f"[Autocomplete] Common pattern: {keyword}")
                    return AutocompleteResponse(
                        suggestion=suggestion,
                        confidence=0.75
                    )
            
            # Variable assignment detection
            if "=" in current_line and "==" not in current_line:
                var_name = current_line.split("=")[0].strip()
                if var_name and not any(kw in var_name for kw in ["def", "class", "if", "for"]):
                    return AutocompleteResponse(
                        suggestion=f"{var_name} = None  # Initialize variable",
                        confidence=0.70
                    )
            
            # Function call detection
            if "(" in current_line and ")" not in current_line:
                return AutocompleteResponse(
                    suggestion="# Add closing parenthesis and arguments",
                    confidence=0.65
                )
            
            # MongoDB-specific suggestions
            if any(word in current_line.lower() for word in ["mongo", "collection", "db."]):
                return AutocompleteResponse(
                    suggestion="result = collection.find_one({'_id': ObjectId(id)})",
                    confidence=0.80
                )
            
            # Database/async patterns
            if "async" in current_line.lower():
                return AutocompleteResponse(
                    suggestion="result = await async_function()\nreturn result",
                    confidence=0.80
                )
            
            # Check last few characters for context
            if current_line_stripped:
                last_word = current_line_stripped.split()[-1] if current_line_stripped.split() else ""
                
                # Suggest based on last word
                if last_word in ["def", "class", "for", "while", "if", "elif"]:
                    return AutocompleteResponse(
                        suggestion=self.python_suggestions.get(last_word + " ", "# Complete statement"),
                        confidence=0.85
                    )
        
        # Default fallback - provide contextual hint
        if len(lines) > 1:
            return AutocompleteResponse(
                suggestion="# Continue coding... Try: def, class, for, if, import",
                confidence=0.55
            )
        
        return AutocompleteResponse(
            suggestion="# Type 'def', 'class', 'for', 'if' or 'import' for suggestions",
            confidence=0.50
        )