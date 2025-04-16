from typing import Dict, List, Union, Optional

class ToolResult:
    """Result of a tool call."""

    def __init__(self, data: Optional[Union[Dict, List]] = None, error: Optional[str] = None):
        self.data = data
        self.error = error

    def to_response(self) -> Dict:
        if self.error:
            return {
                "error": self.error
            }

        return self.data
