"""
ReqDev package for generating requirements.txt from Python code without a virtual environment.

Features:
- Extracts imports from Python files and Jupyter notebooks
- Maps import names to PyPI package names
- Filters out standard library modules and local project modules
- Detects implicit dependencies like pymysql
- Generates requirements.txt with optional version pinning
"""

__version__ = '0.1.3'
