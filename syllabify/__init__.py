"""
Syllabify: Automatically convert plain text into phonemes and syllabify.

This package provides tools for phonetic transcription and syllabification
using the CMU Pronouncing Dictionary.
"""

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("syllabify")
except PackageNotFoundError:
    __version__ = "unknown"

# These imports might fail if the files aren't ready yet, so we'll handle gracefully
try:
    from .syllable import generate, generate_sentence, get_raw
    from .cmu_parser import CMUtranscribe
    from .syllable_types import (
        Cluster,
        Consonant,
        Vowel,
        Empty,
        Rime,
        Syllable,
        VOWEL_TYPES,
    )

    __all__ = [
        "generate",
        "generate_sentence",
        "get_raw",
        "CMUtranscribe",
        "Cluster",
        "Consonant",
        "Vowel",
        "Empty",
        "Rime",
        "Syllable",
        "VOWEL_TYPES",
    ]
except ImportError:
    # If imports fail, just provide basic info
    __all__ = []
