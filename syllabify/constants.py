"""
Constants for syllabification including vowel type definitions.
"""

from typing import Dict

VOWEL_TYPES: Dict[str, Dict[str, str]] = {
    # Short Vowels
    "AO": {"length": "short"},
    "UW": {"length": "short"},
    "EH": {"length": "short"},
    "AH": {"length": "short"},
    "AA": {"length": "short"},
    "IY": {"length": "short"},
    "IH": {"length": "short"},
    "UH": {"length": "short"},
    "AE": {"length": "short"},
    # Long Vowels
    "AW": {"length": "long"},
    "AY": {"length": "long"},
    "ER": {"length": "long"},
    "EY": {"length": "long"},
    "OW": {"length": "long"},
    "OY": {"length": "long"},
}
