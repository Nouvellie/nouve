#!/usr/bin/env python
# Standard library imports
import os
import sys

# Third-party imports
from config.settings import DEBUG


def main():
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    # Custom runserver port:
    if DEBUG:
        from django.core.management.commands.runserver import Command as runserver
        runserver.default_port = "8000"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
