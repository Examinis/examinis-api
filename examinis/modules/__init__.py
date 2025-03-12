import importlib
import logging
import os
from typing import List

from fastapi import Depends, FastAPI

from examinis.core.security import get_current_user


def __get_named_modules() -> List[str]:
    """Get named modules in the current directory."""
    excluded = {'__pycache__', '__init__.py'}
    modules_path = os.path.abspath(os.path.dirname(__file__))
    return [
        module for module in os.listdir(modules_path) if module not in excluded
    ]


def include_routers(app: FastAPI):
    """Include routers from all modules."""
    authentication = [Depends(get_current_user)]
    excluded_modules = {'auth', 'user'}

    for module in __get_named_modules():
        try:
            module_name = f'examinis.modules.{module}.views'
            mod = importlib.import_module(module_name)

            if hasattr(mod, 'router'):
                if module in excluded_modules:
                    app.include_router(mod.router)
                else:
                    app.include_router(mod.router, dependencies=authentication)
            else:
                logging.warning(
                    f"Module '{module}' does not have a 'router'. Skipping."
                )

        except ImportError as e:
            logging.error(f"Failed to import module '{module}': {e}")
        except Exception as e:
            logging.error(
                f"An error occurred while including module '{module}': {e}"
            )
