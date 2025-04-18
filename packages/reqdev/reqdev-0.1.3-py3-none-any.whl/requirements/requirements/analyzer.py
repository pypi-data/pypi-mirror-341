"""
Module for analyzing Python files to extract import statements.
"""

import os
import ast
import glob
import sys
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
import logging
import importlib.util
try:
    from tqdm import tqdm
except ImportError:
    # Create a simple fallback if tqdm is not available
    def tqdm(iterable, **kwargs):
        return iterable

from .mapping import get_package_name, is_std_lib

logger = logging.getLogger(__name__)

class ImportAnalyzer:
    """Class to analyze Python files and extract imports."""
    
    def __init__(self, project_path='.', include_notebooks=True):
        """
        Initialize the analyzer.
        
        Args:
            project_path (str): Path to the project to analyze
            include_notebooks (bool): Whether to include Jupyter notebooks
        """
        self.project_path = Path(project_path).resolve()
        self.include_notebooks = include_notebooks
        self.imports = defaultdict(set)  # package -> {modules that use it}
        self.packages = set()  # Set of required packages
        self.local_modules = set()  # Set of local modules to exclude
        
    def _find_local_modules(self):
        """
        Find all local modules in the project to exclude them from requirements.
        
        Returns:
            set: Set of local module names
        """
        local_modules = set()
        python_files = self.find_python_files()
        
        for py_file in python_files:
            # Get the module name from the file path
            rel_path = os.path.relpath(py_file, start=str(self.project_path))
            if rel_path.endswith('.py'):
                # Convert path to module name (e.g., 'dir/file.py' -> 'dir.file')
                module_name = os.path.splitext(rel_path)[0].replace(os.path.sep, '.')
                local_modules.add(module_name.split('.')[0])  # Add the top-level module
                
        return local_modules
    
    def find_python_files(self):
        """
        Find all Python files in the project directory.
        
        Returns:
            list: List of Python file paths
        """
        py_files = []
        
        # Find all .py files
        for py_file in glob.glob(str(self.project_path / "**/*.py"), recursive=True):
            # Skip virtual environments
            if "venv" in py_file or "env" in py_file or "__pycache__" in py_file:
                continue
            py_files.append(py_file)
            
        # Optionally include Jupyter notebooks
        if self.include_notebooks:
            for nb_file in glob.glob(str(self.project_path / "**/*.ipynb"), recursive=True):
                if "venv" in nb_file or "env" in nb_file or ".ipynb_checkpoints" in nb_file:
                    continue
                py_files.append(nb_file)
                
        return py_files
    
    def extract_imports_from_file(self, file_path):
        """
        Extract imports from a Python file.
        
        Args:
            file_path (str): Path to the Python file
            
        Returns:
            list: List of import names
        """
        if file_path.endswith('.ipynb'):
            return self._extract_imports_from_notebook(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
                
            imports = []
            
            for node in ast.walk(tree):
                # Handle standard imports like "import numpy"
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append(name.name.split('.')[0])
                
                # Handle from imports like "from numpy import array"
                elif isinstance(node, ast.ImportFrom):
                    if node.module:  # Ignore relative imports with no module
                        imports.append(node.module.split('.')[0])
                        
            return imports
            
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")
            return []
    
    def _extract_imports_from_notebook(self, nb_path):
        """
        Extract imports from a Jupyter notebook.
        
        Args:
            nb_path (str): Path to the notebook
            
        Returns:
            list: List of import names
        """
        try:
            import json
            with open(nb_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
                
            imports = []
            
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    try:
                        tree = ast.parse(source)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for name in node.names:
                                    imports.append(name.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.append(node.module.split('.')[0])
                    except:
                        # Skip cells that can't be parsed
                        pass
                        
            return imports
            
        except Exception as e:
            logger.warning(f"Failed to parse notebook {nb_path}: {e}")
            return []
    
    def is_local_import(self, import_name):
        """
        Check if an import is a local module.
        
        Args:
            import_name (str): The import name
            
        Returns:
            bool: True if it's a local module
        """
        # Check if it's in our detected local modules
        if import_name in self.local_modules:
            return True
            
        # Check for various local module patterns
        potential_paths = [
            # Direct module or package in the project root
            os.path.join(self.project_path, import_name),
            os.path.join(self.project_path, f"{import_name}.py"),
            os.path.join(self.project_path, import_name, "__init__.py"),
            
            # Common src/app directory patterns
            os.path.join(self.project_path, "src", import_name),
            os.path.join(self.project_path, "src", f"{import_name}.py"),
            os.path.join(self.project_path, "src", import_name, "__init__.py"),
            os.path.join(self.project_path, "app", import_name),
            os.path.join(self.project_path, "app", f"{import_name}.py"),
            os.path.join(self.project_path, "app", import_name, "__init__.py"),
            
            # Check inside 'lib' or 'libs' folder
            os.path.join(self.project_path, "lib", f"{import_name}.py"),
            os.path.join(self.project_path, "libs", f"{import_name}.py"),
        ]
        
        # Check if any of these paths exist
        if any(os.path.exists(p) for p in potential_paths):
            return True
            
        # Try checking import system for local modules
        try:
            # Try to locate the module
            spec = importlib.util.find_spec(import_name)
            if spec and spec.origin:
                # Check if the module's location is within our project path
                # or is not part of site-packages (indicating third-party)
                if str(self.project_path) in spec.origin and 'site-packages' not in spec.origin:
                    return True
        except (ImportError, AttributeError, ValueError):
            pass
            
        return False
            
    def analyze(self):
        """
        Analyze the project and collect all imports.
        
        Returns:
            dict: Dictionary of imports
        """
        python_files = self.find_python_files()
        
        # Find local modules first
        self.local_modules = self._find_local_modules()
        logger.debug(f"Detected local modules: {self.local_modules}")
        
        for file_path in tqdm(python_files, desc="Scanning files", unit="file", ncols=80, bar_format="{l_bar}{bar:30}{r_bar}"):
            imports = self.extract_imports_from_file(file_path)
            for import_name in imports:
                # Skip standard library and local imports
                if is_std_lib(import_name) or self.is_local_import(import_name):
                    continue
                    
                pkg_name = get_package_name(import_name)
                if pkg_name:
                    self.imports[pkg_name].add(os.path.basename(file_path))
                    self.packages.add(pkg_name)
                        
        return self.imports
    
    def add_known_dependencies(self):
        """
        Add known dependencies that might not be directly imported.
        This handles common packages that are dependencies but not directly imported.
        """
        # Find files that might indicate usage of these packages
        files = os.listdir(self.project_path)
        file_contents = []
        
        # Check for .env files and related environment files
        env_files = [f for f in files if f.startswith('.env') or f.endswith('env') or 
                    f in ['.flaskenv', '.djangoenv', '.env.local', '.env.development', 
                         '.env.production', '.env.test', 'env.sample', '.env.example']]
                         
        # Check for dotenv usage in Python files even if .env file not present
        has_dotenv_usage = False
        if not env_files:
            python_files = [f for f in files if f.endswith('.py')][:10]  # Check up to 10 files
            for py_file in python_files:
                try:
                    with open(os.path.join(self.project_path, py_file), 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        if any(pattern in content for pattern in [
                            'load_dotenv', 
                            'dotenv.load_dotenv', 
                            'python-dotenv', 
                            'from dotenv', 
                            'import dotenv', 
                            'os.environ',
                            '.env']):
                            has_dotenv_usage = True
                            logger.debug(f"Found dotenv usage pattern in {py_file}")
                            break
                except Exception as e:
                    logger.debug(f"Error reading {py_file}: {e}")
        
        if env_files or has_dotenv_usage:
            source = env_files[0] if env_files else "usage pattern in code"
            logger.debug(f"Found environment files or usage: {source}")
            if 'python-dotenv' not in self.packages:
                self.packages.add('python-dotenv')
                self.imports['python-dotenv'].add('environment_config')
                logger.info(f"Added python-dotenv due to presence of {source}")
        
        # Check for common SQL indicator files
        sql_indicators = ['.sql', 'db', 'database', 'mysql', 'postgres', 'sqlite']
        has_sql_files = any(any(indicator in f.lower() for indicator in sql_indicators) for f in files)
        
        # For more thorough detection, check Python files for SQL-related content
        if not has_sql_files:
            # Sample a few Python files to look for SQL strings or imports
            python_files = [f for f in files if f.endswith('.py')][:5]  # Check up to 5 files
            for py_file in python_files:
                try:
                    with open(os.path.join(self.project_path, py_file), 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        if any(term in content for term in ['sql', 'database', 'cursor.execute', 'connection', 'query']):
                            has_sql_files = True
                            break
                except:
                    pass
        
        # Get Python version
        python_version = tuple(map(int, sys.version.split()[0].split('.')))
        logger.debug(f"Python version: {python_version}")
        
        # MySQL/SQL-related packages
        if has_sql_files:
            # Add various SQL packages with compatibility checks
            sql_packages = []
            
            # Always include these as they're maintained and compatible
            sql_packages.append('pymysql')
            sql_packages.append('mysql-connector-python')
            sql_packages.append('sqlalchemy')
            
            # Only include pysql for older Python versions as it's not compatible with Python 3.7+
            if python_version < (3, 7):
                sql_packages.append('pysql')  # Known to be incompatible with newer Python
            
            for pkg in sql_packages:
                if pkg not in self.packages:
                    self.packages.add(pkg)
                    self.imports[pkg].add('db_config')
            
        # Check for Django
        if 'django' in self.packages or 'manage.py' in files:
            # Common Django dependencies
            for pkg in ['pillow', 'django-crispy-forms', 'django-extensions']:
                if pkg not in self.packages:
                    self.packages.add(pkg)
                    self.imports[pkg].add('django_app')
                    
        # Check for web frameworks and add common dependencies
        if 'flask' in self.packages:
            # Common Flask dependencies
            for pkg in ['gunicorn', 'flask-wtf', 'flask-login']:
                if pkg not in self.packages:
                    self.packages.add(pkg)
                    self.imports[pkg].add('flask_app')
                    
        # Check for data science packages
        if 'pandas' in self.packages or 'numpy' in self.packages:
            # Common data science dependencies
            if 'matplotlib' not in self.packages:
                self.packages.add('matplotlib')
                self.imports['matplotlib'].add('data_analysis')
                
        # Add more patterns as needed
    
    def get_package_versions(self, install=False, use_latest=True):
        """
        Get the versions of packages either by checking installed versions,
        installing them in a temporary environment, or fetching latest from PyPI.
        
        Args:
            install (bool): Whether to actually install packages to get versions
            use_latest (bool): Whether to fetch latest versions from PyPI instead of installed versions
            
        Returns:
            dict: Dictionary mapping package names to versions
        """
        package_versions = {}
        
        if use_latest:
            try:
                # Try to use pip's index to get latest versions
                import json
                from urllib.request import urlopen
                from urllib.parse import quote
                
                logger.info("Fetching latest compatible versions from PyPI...")
                
                for package in tqdm(list(self.packages), 
                                   desc="Fetching versions from PyPI", 
                                   unit="pkg", 
                                   ncols=80,
                                   bar_format="{l_bar}{bar:30}{r_bar}"):
                    try:
                        # Query PyPI API for the package data
                        url = f"https://pypi.org/pypi/{quote(package)}/json"
                        with urlopen(url, timeout=5) as response:
                            data = json.loads(response.read())
                            
                        # Get the latest version
                        latest_version = data['info']['version']
                        package_versions[package] = latest_version
                        logger.debug(f"Latest version of {package}: {latest_version}")
                        
                    except Exception as e:
                        logger.debug(f"Failed to get latest version for {package}: {e}")
                        # Fall back to installed version if available
                        try:
                            result = subprocess.run(
                                [sys.executable, "-m", "pip", "show", package],
                                capture_output=True,
                                text=True
                            )
                            
                            if result.returncode == 0:
                                for line in result.stdout.split('\n'):
                                    if line.startswith('Version:'):
                                        version = line.split(':', 1)[1].strip()
                                        package_versions[package] = version
                                        logger.debug(f"Using installed version for {package}: {version}")
                                        break
                        except:
                            pass
                
                return package_versions
            except Exception as e:
                logger.warning(f"Error fetching latest versions from PyPI: {e}. Falling back to installed versions.")
                # Fall back to installed versions
                pass
        
        if not install:
            # Try to get versions of already installed packages
            for package in tqdm(list(self.packages), 
                               desc="Checking local versions", 
                               unit="pkg", 
                               ncols=80,
                               bar_format="{l_bar}{bar:30}{r_bar}"):
                try:
                    # Use pip to show package info
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "show", package],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        # Parse the version from the output
                        for line in result.stdout.split('\n'):
                            if line.startswith('Version:'):
                                version = line.split(':', 1)[1].strip()
                                package_versions[package] = version
                                break
                except Exception as e:
                    logger.warning(f"Failed to get version for {package}: {e}")
        else:
            # Create a temporary venv and install packages to get versions
            with tempfile.TemporaryDirectory() as tempdir:
                try:
                    # Create virtual environment
                    venv_path = os.path.join(tempdir, "venv")
                    subprocess.run(
                        [sys.executable, "-m", "venv", venv_path],
                        check=True
                    )
                    
                    # Determine the Python executable in the venv
                    if sys.platform == "win32":
                        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
                    else:
                        python_exe = os.path.join(venv_path, "bin", "python")
                    
                    # Install packages one by one to catch failures
                    for package in tqdm(list(self.packages), 
                                      desc="Installing packages", 
                                      unit="pkg", 
                                      ncols=80,
                                      bar_format="{l_bar}{bar:30}{r_bar}"):
                        try:
                            subprocess.run(
                                [python_exe, "-m", "pip", "install", package],
                                capture_output=True,
                                text=True,
                                check=True
                            )
                            
                            # Get the installed version
                            result = subprocess.run(
                                [python_exe, "-m", "pip", "show", package],
                                capture_output=True,
                                text=True
                            )
                            
                            if result.returncode == 0:
                                for line in result.stdout.split('\n'):
                                    if line.startswith('Version:'):
                                        version = line.split(':', 1)[1].strip()
                                        package_versions[package] = version
                                        break
                        except Exception as e:
                            logger.warning(f"Failed to install {package}: {e}")
                except Exception as e:
                    logger.warning(f"Failed to create temporary venv: {e}")
                    
        return package_versions
    
    def generate_requirements(self, output_file="requirements.txt", with_versions=True, install=False, include_implicit=True, excluded_packages=None, use_latest=True):
        """
        Generate requirements.txt file.
        
        Args:
            output_file (str): Path to output file
            with_versions (bool): Whether to include version numbers
            install (bool): Whether to install packages to get precise versions
            include_implicit (bool): Whether to include implicit dependencies
            excluded_packages (list, optional): List of package names to exclude
            use_latest (bool): Whether to use latest compatible versions from PyPI
            
        Returns:
            bool: True if successful
        """
        self.analyze()
        
        # Add common dependencies that might not be directly imported
        if include_implicit:
            self.add_known_dependencies()
        
        # Handle excluded packages
        if excluded_packages:
            for pkg in excluded_packages:
                if pkg in self.packages:
                    self.packages.remove(pkg)
                    logger.info(f"Excluded package: {pkg}")
        
        if not self.packages:
            logger.warning("No packages found in the project.")
            return False
        
        if with_versions:
            versions = self.get_package_versions(install=install, use_latest=use_latest)
        
        try:
            with open(output_file, 'w') as f:
                for package in sorted(self.packages):
                    if with_versions and package in versions:
                        f.write(f"{package}=={versions[package]}\n")
                    else:
                        f.write(f"{package}\n")
                        
            logger.info(f"Requirements file generated: {output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to write requirements file: {e}")
            return False
