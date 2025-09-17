from pathlib import Path
import logging

# Define base directory (project root)
BASE_DIR = Path(__file__).parent.parent

def load_clinic_info() -> str:
    """
    Loads clinic information from a text file.

    Returns:
        str: The content of `clinic_info.txt`, or a default message if not found.
    """
    clinic_file = BASE_DIR / "clinic_info.txt"

    try:
        with open(clinic_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.warning(f"Could not load clinic info from {clinic_file}: {e}")
        return "Dental clinic information could not be loaded."
