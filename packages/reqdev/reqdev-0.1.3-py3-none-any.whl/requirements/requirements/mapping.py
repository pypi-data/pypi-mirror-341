"""
Module for mapping Python import names to PyPI package names.
"""

# This is a database of known mappings from import name to PyPI package name
# Many Python packages have different import names than their PyPI names
IMPORT_TO_PKG = {
    # Standard libraries that shouldn't be included
    "os": None,
    "sys": None,
    "datetime": None,
    "json": None,
    "re": None,
    "math": None,
    "random": None,
    "time": None,
    "collections": None,
    "itertools": None,
    "functools": None,
    "typing": None,
    "pathlib": None,
    "logging": None,
    "argparse": None,
    "multiprocessing": None,
    "threading": None,
    "subprocess": None,
    "io": None,
    "csv": None,
    "uuid": None,
    "hashlib": None,
    "inspect": None,
    "importlib": None,
    "unittest": None,
    "pickle": None,
    "tempfile": None,
    "shutil": None,
    "pprint": None,
    "urllib": None,
    "urllib3": "urllib3",  # External package with same name
    "http": None,
    "email": None,
    "smtplib": None,
    "configparser": None,
    "xml": None,
    "html": None,
    "ast": None,
    "glob": None,
    "ctypes": None,
    "webbrowser": None,
    "getpass": None,
    "platform": None,
    "socket": None,
    "base64": None,
    "copy": None,
    "venv": None,
    "zipfile": None,
    "calendar": None,
    "textwrap": None,
    "string": None,
    "fnmatch": None,
    "queue": None,
    "tkinter": None,
    "asyncio": None,
    "dataclasses": None,
    "contextlib": None,
    "warnings": None,
    "traceback": None,
    "abc": None,
    
    # Common import name != package name mappings
    "cv2": "opencv-python",
    "sklearn": "scikit-learn",
    "PIL": "pillow",
    "bs4": "beautifulsoup4",
    "yaml": "pyyaml",
    "nx": "networkx",
    "np": "numpy",
    "pd": "pandas",
    "plt": "matplotlib",
    "mpl": "matplotlib",
    "tf": "tensorflow",
    "wx": "wxpython",
    "mx": "mxnet",
    "tk": "tkinter",
    "skimage": "scikit-image",
    "cairo": "pycairo",
    "boto3": "boto3",
    "flask_restful": "flask-restful",
    "flask_sqlalchemy": "flask-sqlalchemy",
    "flask_migrate": "flask-migrate",
    "flask_login": "flask-login",
    "flask_wtf": "flask-wtf",
    "flask_cors": "flask-cors",
    "flask_jwt": "flask-jwt",
    "flask_jwt_extended": "flask-jwt-extended",
    "flask_socketio": "flask-socketio",
    "flask_admin": "flask-admin",
    "flask_mail": "flask-mail",
    "flask_caching": "flask-caching",
    "flask_babel": "flask-babel",
    "flask_assets": "flask-assets",
    "django_filters": "django-filter",
    "django_extensions": "django-extensions",
    "django_rest_framework": "djangorestframework",
    "rest_framework": "djangorestframework",
    "sqlalchemy": "sqlalchemy",
    "django": "django",
    "requests": "requests",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "pandas": "pandas",
    "tensorflow": "tensorflow",
    "torch": "torch",
    "scipy": "scipy",
    "pytest": "pytest",
    "flask": "flask",
    "pygame": "pygame",
    "nltk": "nltk",
    "sympy": "sympy",
    "plotly": "plotly",
    "dash": "dash",
    "fastapi": "fastapi",
    "pydantic": "pydantic",
    "streamlit": "streamlit",
    "uvicorn": "uvicorn",
    "aiohttp": "aiohttp",
    "rich": "rich",
    "tqdm": "tqdm",
    "kivy": "kivy",
    "scrapy": "scrapy",
    "psycopg2": "psycopg2-binary",
    "mysqlclient": "mysqlclient",
    "psutil": "psutil",
    "ldap": "python-ldap",
    "dateutil": "python-dateutil",
    "gensim": "gensim",
    "spacy": "spacy",
    "docx": "python-docx",
    "dotenv": "python-dotenv",
    "tabulate": "tabulate",
    "click": "click",
    "typer": "typer",
    "pptx": "python-pptx",
    "openai": "openai",
    "langchain": "langchain",
    "huggingface_hub": "huggingface-hub",
    "transformers": "transformers",
    "jax": "jax",
    "keras": "keras",
    "openpyxl": "openpyxl",
    "xlrd": "xlrd",
    "xlsxwriter": "xlsxwriter",
    "pdfplumber": "pdfplumber",
    "pypdf": "pypdf",
    "reportlab": "reportlab",
    "httpx": "httpx",
    "dask": "dask",
    "graphene": "graphene",
    "elasticsearch": "elasticsearch",
    "celery": "celery",
    "redis": "redis",
    "docker": "docker",
    "boto": "boto",
    "awscli": "awscli",
    "azure": "azure",
    "google": "google-api-python-client",
    "googleapiclient": "google-api-python-client",
    "airflow": "apache-airflow",
    "pyarrow": "pyarrow",
    "sqlmodel": "sqlmodel",
    "pinecone": "pinecone-client",
    "chromadb": "chromadb",
    "qdrant_client": "qdrant-client",
    "sentence_transformers": "sentence-transformers",
    "gradio": "gradio",
    "datasets": "datasets",
    "pillow": "pillow",
    "pysql": "pysql",
    "mysql": "pymysql",
    "sqlite3": "pysqlite3",
    "pg": "psycopg2-binary",
    "connection": "sqlalchemy",
}

def get_package_name(import_name):
    """
    Get the PyPI package name for a given import name.
    
    Args:
        import_name (str): The import name used in Python code
        
    Returns:
        str: The PyPI package name or None if it's a standard library
    """
    # Check if it's a direct match in our mapping
    if import_name in IMPORT_TO_PKG:
        return IMPORT_TO_PKG[import_name]
    
    # Check if it's a submodule of a known package
    for known_import, package in IMPORT_TO_PKG.items():
        if import_name.startswith(f"{known_import}.") and package is not None:
            return package
    
    # Default: use the import name as the package name
    # This works for many packages where import name == package name
    return import_name

def is_std_lib(import_name):
    """
    Check if an import name belongs to the Python standard library.
    
    Args:
        import_name (str): The import name
        
    Returns:
        bool: True if it's a standard library module
    """
    return import_name in IMPORT_TO_PKG and IMPORT_TO_PKG[import_name] is None

# Additional utility functions can be added here
def search_pypi_for_package(import_name):
    """
    Search PyPI for a package matching the import name.
    This is a placeholder for a future implementation using PyPI API.
    
    Args:
        import_name (str): The import name to search for
        
    Returns:
        str: The best matching package name or None if no match
    """
    # Placeholder for future implementation
    # Could use requests to query PyPI API
    return None
