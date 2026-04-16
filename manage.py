#!/usr/bin/env python
import os
import sys


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(base_dir, 'app'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clublectura.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
