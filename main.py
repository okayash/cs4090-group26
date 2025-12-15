import sys
from pathlib import Path

# Add backend/src to Python path
backend_src = Path(__file__).parent / "backend" / "src"
sys.path.insert(0, str(backend_src))

from clio.app import *

if __name__ == "__main__":
    main()