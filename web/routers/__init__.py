"""
web/routers package - Phase 4 safe imports.
We only force-import the ones we know exist to avoid breaking the app
during incremental deploys.
"""

from . import auth
from . import scheduler

# These are imported directly in web/main.py, so we don't need to re-export
# everything here. Keeping this file minimal prevents circular/partial import issues.
