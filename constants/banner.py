"""FastX Startup Banner Constants.

This module contains ASCII art banners and startup messages.
"""

from __future__ import annotations

# ASCII Art Banner - FastX Logo (compact)
FASTX_BANNER: str = r"""
╔═════════════════════════════════════════════╗
║                                             ║
║  ███████╗ █████╗ ███████╗████████╗██╗  ██╗  ║
║  ██╔════╝██╔══██╗██╔════╝╚══██╔══╝╚██╗██╔╝  ║
║  █████╗  ███████║███████╗   ██║    ╚███╔╝   ║
║  ██╔══╝  ██╔══██║╚════██║   ██║    ██╔██╗   ║
║  ██║     ██║  ██║███████║   ██║   ██╔╝ ██╗  ║
║  ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝  ║
║                                             ║
║     Production-grade FastAPI Framework      ║
╚═════════════════════════════════════════════╝
"""

# Section Headers
SERVER_INFO_HEADER: str = "Server Information:"
API_DOCS_HEADER: str = "API Documentation:"
HEALTH_ENDPOINTS_HEADER: str = "Health Endpoints:"
ENVIRONMENT_HEADER: str = "Environment:"
FEATURES_HEADER: str = "Features:"

# Feature Indicators
FEATURE_ENABLED: str = "[+]"
FEATURE_DISABLED: str = "[-]"

# Ready Message
READY_MESSAGE: str = "FastX is ready! Press Ctrl+C to stop."

# Label Widths (for alignment)
LABEL_WIDTH: int = 12

__all__ = [
    "FASTX_BANNER",
    "SERVER_INFO_HEADER",
    "API_DOCS_HEADER",
    "HEALTH_ENDPOINTS_HEADER",
    "ENVIRONMENT_HEADER",
    "FEATURES_HEADER",
    "FEATURE_ENABLED",
    "FEATURE_DISABLED",
    "READY_MESSAGE",
    "LABEL_WIDTH",
]
