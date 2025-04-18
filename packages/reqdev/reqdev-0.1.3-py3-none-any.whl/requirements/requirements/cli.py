"""
Command-line interface for the reqdev package.
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
import colorama
from colorama import Fore, Style
try:
    from tqdm import tqdm
except ImportError:
    # Create a simple fallback if tqdm is not available
    def tqdm(iterable, **kwargs):
        return iterable

from .analyzer import ImportAnalyzer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize colorama
colorama.init()

# List of known problematic packages for modern Python
PROBLEMATIC_PACKAGES = [
    'pysql',        # Incompatible with Python 3.7+
    'pysqlite3',    # Most users should use built-in sqlite3
    'mysql-python', # Replaced by mysql-connector-python
    'distribute',   # Merged into setuptools
    'django-redis-cache', # Maintenance issues
    'django-celery', # Deprecated
]

def setup_argparser():
    """
    Set up the argument parser for command line arguments.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog="reqdev",
        description="Smartly generate requirements.txt from Python code without a virtual environment",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Path to the project directory"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="requirements.txt",
        help="Output file path"
    )
    
    parser.add_argument(
        "--no-versions", "-n",
        action="store_true",
        help="Generate requirements without version numbers"
    )
    
    parser.add_argument(
        "--install", "-i",
        action="store_true",
        help="Temporarily install packages to get precise versions"
    )
    
    parser.add_argument(
        "--no-notebooks", "-nb",
        action="store_true",
        help="Skip Jupyter notebooks"
    )
    
    parser.add_argument(
        "--no-implicit", "-ni",
        action="store_true",
        help="Skip adding implicit dependencies (like pymysql, pillow) based on project structure"
    )
    
    parser.add_argument(
        "--compat", "-c", 
        action="store_true",
        help="Filter out packages known to be problematic with your Python version"
    )
    
    parser.add_argument(
        "--latest", "-l",
        action="store_true",
        help="Use latest versions from PyPI instead of installed versions"
    )
    
    parser.add_argument(
        "--exclude", "-e",
        nargs="+",
        default=[],
        help="Packages to exclude from requirements.txt"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable detailed debug output"
    )
    
    return parser

def print_results(imports, versions=None, debug=False, using_latest=False):
    """
    Print the analysis results in a visually appealing format.
    
    Args:
        imports (dict): Dictionary mapping package names to the files they're used in
        versions (dict, optional): Dictionary mapping package names to versions
        debug (bool): Whether to print additional debug information
        using_latest (bool): Whether the user is already using the --latest flag
    """
    # Terminal width
    try:
        terminal_width = os.get_terminal_size().columns
    except (AttributeError, OSError):
        terminal_width = 80
    
    # Create a horizontal line of appropriate width
    h_line = "─" * terminal_width
    
    # Print header
    print(f"\n{Fore.BLUE}{'╭' + h_line[1:-1] + '╮'}{Style.RESET_ALL}")
    
    # Calculate padding for centered title
    title = " 📦 PACKAGE ANALYSIS RESULTS 📦 "
    padding = (terminal_width - len(title)) // 2
    print(f"{Fore.BLUE}│{Style.RESET_ALL}{' ' * padding}{Fore.GREEN}{Style.BRIGHT}{title}{Style.RESET_ALL}{' ' * (terminal_width - padding - len(title) - 2)}{Fore.BLUE}│{Style.RESET_ALL}")
    
    print(f"{Fore.BLUE}{'├' + h_line[1:-1] + '┤'}{Style.RESET_ALL}")
    
    if debug:
        # Print SQL-related packages specifically
        sql_packages = [pkg for pkg in imports.keys() if any(term in pkg.lower() for term in ['sql', 'mysql', 'pg', 'postgre', 'sqlite'])]
        if sql_packages:
            print(f"{Fore.BLUE}│{Style.RESET_ALL} {Fore.MAGENTA}Database Packages:{Style.RESET_ALL} {', '.join(sql_packages)}{' ' * (terminal_width - len(' Database Packages: ' + ', '.join(sql_packages)) - 2)}{Fore.BLUE}│{Style.RESET_ALL}")
        
        # Print environment-related packages
        env_packages = [pkg for pkg in imports.keys() if any(term in pkg.lower() for term in ['dotenv', 'env', 'environ'])]
        if env_packages:
            print(f"{Fore.BLUE}│{Style.RESET_ALL} {Fore.MAGENTA}Environment Packages:{Style.RESET_ALL} {', '.join(env_packages)}{' ' * (terminal_width - len(' Environment Packages: ' + ', '.join(env_packages)) - 2)}{Fore.BLUE}│{Style.RESET_ALL}")
        
        # Print a separator
        print(f"{Fore.BLUE}{'├' + h_line[1:-1] + '┤'}{Style.RESET_ALL}")
    
    # Package count display
    count_text = f" Found {len(imports)} required packages "
    padding = (terminal_width - len(count_text)) // 2
    print(f"{Fore.BLUE}│{Style.RESET_ALL}{' ' * padding}{Fore.YELLOW}{count_text}{Style.RESET_ALL}{' ' * (terminal_width - padding - len(count_text) - 2)}{Fore.BLUE}│{Style.RESET_ALL}")
    
    # Print a separator
    print(f"{Fore.BLUE}{'├' + h_line[1:-1] + '┤'}{Style.RESET_ALL}")
    
    # Print a header for the package table
    if versions:
        header_format = " {:<30} {:<15} {:<30} "
        print(f"{Fore.BLUE}│{Style.RESET_ALL}{Fore.CYAN}{header_format.format('PACKAGE', 'VERSION', 'USED IN')}{Style.RESET_ALL}{' ' * (terminal_width - len(header_format.format('PACKAGE', 'VERSION', 'USED IN')) - 2)}{Fore.BLUE}│{Style.RESET_ALL}")
    else:
        header_format = " {:<30} {:<45} "
        print(f"{Fore.BLUE}│{Style.RESET_ALL}{Fore.CYAN}{header_format.format('PACKAGE', 'USED IN')}{Style.RESET_ALL}{' ' * (terminal_width - len(header_format.format('PACKAGE', 'USED IN')) - 2)}{Fore.BLUE}│{Style.RESET_ALL}")

    # Print a separator
    print(f"{Fore.BLUE}{'├' + h_line[1:-1] + '┤'}{Style.RESET_ALL}")
    
    # Print each package
    for pkg_name, files in sorted(imports.items()):
        file_list = ', '.join(sorted(files)[:3])
        if len(files) > 3:
            file_list += f" (+{len(files) - 3} more)"
        
        if versions and pkg_name in versions:
            version_str = versions[pkg_name]
            pkg_format = " {:<30} {:<15} {:<30} "
            line = pkg_format.format(pkg_name, version_str, file_list)
        else:
            pkg_format = " {:<30} {:<45} "
            line = pkg_format.format(pkg_name, file_list)
        
        # Trim line if it's too long for the terminal
        if len(line) > terminal_width - 4:
            line = line[:terminal_width - 7] + "..."
        
        # Print with padding to fill the terminal width
        padding = terminal_width - len(line) - 2
        print(f"{Fore.BLUE}│{Style.RESET_ALL}{Fore.GREEN}{line}{Style.RESET_ALL}{' ' * padding}{Fore.BLUE}│{Style.RESET_ALL}")
    
    # Print footer
    print(f"{Fore.BLUE}{'╰' + h_line[1:-1] + '╯'}{Style.RESET_ALL}\n")
    
    # Animated checkmark when done
    sys.stdout.write(f"{Fore.GREEN}Generating requirements.txt... ")
    sys.stdout.flush()
    time.sleep(0.5)  # Short pause for effect
    print(f"✓{Style.RESET_ALL}")
    
    # Suggestion for next steps - only if not already using latest
    if not using_latest and versions:
        print(f"{Fore.YELLOW}Tip:{Style.RESET_ALL} Use {Fore.GREEN}--latest{Style.RESET_ALL} flag to get the most up-to-date package versions\n")

def filter_problematic_packages(packages, debug=False):
    """
    Filter out problematic packages based on the current Python version.
    
    Args:
        packages (set): Set of packages to filter
        debug (bool): Whether to print debug information
        
    Returns:
        set: Filtered set of packages
    """
    python_version = tuple(map(int, sys.version.split()[0].split('.')))
    
    excluded = set()
    for pkg in PROBLEMATIC_PACKAGES:
        if pkg in packages:
            excluded.add(pkg)
            packages.remove(pkg)
            
    if excluded and debug:
        print(f"{Fore.YELLOW}Excluded {len(excluded)} problematic packages: {', '.join(excluded)}{Style.RESET_ALL}")
        
    return packages

def show_loading_animation(text, duration=1.0):
    """
    Show a simple loading animation.
    
    Args:
        text (str): The text to display during loading
        duration (float): Duration in seconds to show the animation
    """
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    
    try:
        while time.time() < end_time:
            sys.stdout.write(f"\r{Fore.BLUE}{spinner[i % len(spinner)]}{Style.RESET_ALL} {text}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write(f"\r{' ' * (len(text) + 2)}\r")
        sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write(f"\r{' ' * (len(text) + 2)}\r")
        sys.stdout.flush()
        raise

def print_project_features(imports, debug=False):
    """
    Print a summary of detected project features.
    
    Args:
        imports (dict): Dictionary mapping package names to the files they're used in
        debug (bool): Whether to print additional debug information
    """
    # Terminal width
    try:
        terminal_width = os.get_terminal_size().columns
    except (AttributeError, OSError):
        terminal_width = 80
        
    # Calculate title padding
    title = " 🔍 Project Features "
    padding = (terminal_width - len(title)) // 2
    
    # Create box
    h_line = "─" * terminal_width
    print(f"{Fore.CYAN}{'╭' + h_line[1:-1] + '╮'}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}│{Style.RESET_ALL}{' ' * padding}{Fore.YELLOW}{Style.BRIGHT}{title}{Style.RESET_ALL}{' ' * (terminal_width - padding - len(title) - 2)}{Fore.CYAN}│{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'├' + h_line[1:-1] + '┤'}{Style.RESET_ALL}")
    
    # Check for different types of projects
    features = []
    
    # Web frameworks
    if any(fw in imports for fw in ['flask', 'django', 'fastapi']):
        if 'flask' in imports:
            features.append(f"{Fore.GREEN}✓{Style.RESET_ALL} Flask web application")
        elif 'django' in imports:
            features.append(f"{Fore.GREEN}✓{Style.RESET_ALL} Django web application")
        elif 'fastapi' in imports:
            features.append(f"{Fore.GREEN}✓{Style.RESET_ALL} FastAPI web application")
    
    # Database usage
    db_packages = [pkg for pkg in imports.keys() if any(term in pkg.lower() for term in ['sql', 'mysql', 'pg', 'postgre', 'sqlite', 'mongo', 'redis'])]
    if db_packages:
        features.append(f"{Fore.GREEN}✓{Style.RESET_ALL} Database integration ({', '.join(db_packages[:2])})")
    
    # Data science
    if any(ds in imports for ds in ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'torch']):
        features.append(f"{Fore.GREEN}✓{Style.RESET_ALL} Data science / ML project")
    
    # Environment files
    if 'python-dotenv' in imports:
        features.append(f"{Fore.GREEN}✓{Style.RESET_ALL} Environment file configuration")
    
    # Testing frameworks
    if any(test in imports for test in ['pytest', 'unittest']):
        features.append(f"{Fore.GREEN}✓{Style.RESET_ALL} Test framework")
    
    # Display features or "basic Python project" if none found
    if features:
        for feature in features:
            print(f"{Fore.CYAN}│{Style.RESET_ALL} {feature}{' ' * (terminal_width - len(feature) - 11)}{Fore.CYAN}│{Style.RESET_ALL}")
    else:
        msg = f" {Fore.GREEN}✓{Style.RESET_ALL} Basic Python project"
        print(f"{Fore.CYAN}│{Style.RESET_ALL}{msg}{' ' * (terminal_width - len(msg) - 9)}{Fore.CYAN}│{Style.RESET_ALL}")
    
    # Close box
    print(f"{Fore.CYAN}{'╰' + h_line[1:-1] + '╯'}{Style.RESET_ALL}\n")

def main():
    """Main entry point for the CLI."""
    parser = setup_argparser()
    args = parser.parse_args()
    
    if args.verbose or args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        project_path = Path(args.path).resolve()
        if not project_path.exists():
            logger.error(f"Project path does not exist: {project_path}")
            return 1
        
        # Show fancy loading animation
        show_loading_animation("Initializing ReqDev", 1.0)
        
        print(f"{Fore.GREEN}Analyzing Python project: {project_path}{Style.RESET_ALL}")
        
        analyzer = ImportAnalyzer(
            project_path=project_path,
            include_notebooks=not args.no_notebooks
        )
        
        imports = analyzer.analyze()
        
        if not imports:
            print(f"{Fore.YELLOW}No packages found in the project.{Style.RESET_ALL}")
            return 0
        
        # Show project features based on detected imports
        print_project_features(imports, args.debug)
        
        with_versions = not args.no_versions
        include_implicit = not args.no_implicit
        
        if include_implicit:
            print(f"{Fore.GREEN}Adding implicit dependencies...{Style.RESET_ALL}")
            analyzer.add_known_dependencies()
            
            if args.debug:
                print(f"{Fore.MAGENTA}After implicit detection, found packages: {', '.join(sorted(analyzer.packages))}{Style.RESET_ALL}")
        
        # Handle compatibility and exclusions
        if args.compat:
            print(f"{Fore.GREEN}Filtering out problematic packages...{Style.RESET_ALL}")
            analyzer.packages = filter_problematic_packages(analyzer.packages, args.debug)
            
        # Handle manual exclusions
        if args.exclude:
            before_count = len(analyzer.packages)
            for pkg in args.exclude:
                if pkg in analyzer.packages:
                    analyzer.packages.remove(pkg)
                    if pkg in analyzer.imports:
                        del analyzer.imports[pkg]
            
            after_count = len(analyzer.packages)
            if before_count != after_count and (args.verbose or args.debug):
                print(f"{Fore.YELLOW}Excluded {before_count - after_count} packages: {', '.join(args.exclude)}{Style.RESET_ALL}")
        
        if with_versions:
            print(f"{Fore.GREEN}Getting package versions...{Style.RESET_ALL}")
            if args.latest:
                print(f"{Fore.GREEN}Fetching latest versions from PyPI...{Style.RESET_ALL}")
            versions = analyzer.get_package_versions(install=args.install, use_latest=args.latest)
        else:
            versions = None
            
        print_results(analyzer.imports, versions, debug=args.debug, using_latest=args.latest)
        
        output_file = args.output
        success = analyzer.generate_requirements(
            output_file=output_file,
            with_versions=with_versions,
            install=args.install,
            include_implicit=include_implicit,
            excluded_packages=args.exclude,
            use_latest=args.latest
        )
        
        if success:
            abs_path = os.path.abspath(output_file)
            # Terminal width
            try:
                terminal_width = os.get_terminal_size().columns
            except (AttributeError, OSError):
                terminal_width = 80
            
            # Get fancy line
            h_line = "─" * terminal_width
            
            # Show success message in a nice box
            print(f"{Fore.GREEN}{'╭' + h_line[1:-1] + '╮'}{Style.RESET_ALL}")
            
            success_msg = f" ✓ Requirements file generated successfully! "
            padding = (terminal_width - len(success_msg)) // 2
            print(f"{Fore.GREEN}│{Style.RESET_ALL}{' ' * padding}{Fore.GREEN}{Style.BRIGHT}{success_msg}{Style.RESET_ALL}{' ' * (terminal_width - padding - len(success_msg) - 2)}{Fore.GREEN}│{Style.RESET_ALL}")
            
            file_msg = f" 📄 {abs_path} "
            padding = (terminal_width - len(file_msg)) // 2
            print(f"{Fore.GREEN}│{Style.RESET_ALL}{' ' * padding}{file_msg}{' ' * (terminal_width - padding - len(file_msg) - 2)}{Fore.GREEN}│{Style.RESET_ALL}")
            
            print(f"{Fore.GREEN}{'╰' + h_line[1:-1] + '╯'}{Style.RESET_ALL}\n")
            return 0
        else:
            print(f"{Fore.RED}Failed to generate requirements file.{Style.RESET_ALL}")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}")
        return 130
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
