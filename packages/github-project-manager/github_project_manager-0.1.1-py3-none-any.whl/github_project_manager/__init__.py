"""
GitHub Project Manager

A Python module for managing GitHub Projects (v2), issues, labels, and milestones.
"""

__version__ = "0.1.1"

import logging

# Configure package-wide logger
logger = logging.getLogger("ghpm")
logger.setLevel(logging.INFO)

# Import public classes
from .models import StatusOption, IssueLabel, IssueMilestone
from .project_manager import GitHubProjectManager

__all__ = [
    "GitHubProjectManager",
    "StatusOption",
    "IssueLabel",
    "IssueMilestone",
]
