import os
from typing import List


def get_named_modules() -> List[str]:
    """Get named modules in the current directory."""
    excluded = {'__pycache__', '__init__.py'}
    modules_path = os.path.abspath(os.path.dirname(__file__))
    return [
        module for module in os.listdir(modules_path) if module not in excluded
    ]


__all__: List[str] = get_named_modules()
