import sys
import os
from pathlib import Path

# Add the backend src to Python path
backend_path = Path(__file__).parent.parent / "src" / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app
