"""
Phoneme classes for syllabification.

This module provides classes for representing phonemes in syllabification:
- Phoneme: Base class for all phonemes
- Vowel: Represents vowel phonemes with stress and length attributes
- Consonant: Represents consonant phonemes
"""

from typing import Any, Dict

from syllabify.constants import VOWEL_TYPES


class Phoneme:
    """Individual phoneme representation"""

    def __init__(self, phoneme):
        self.phoneme = phoneme

    def __str__(self):
        return str(self.phoneme)

    def __repr__(self):
        return f"Phoneme(phoneme={self.phoneme})"


class Vowel(Phoneme):
    """Represents an individual phoneme that has been classified as a vowel"""

    def __init__(self, **features: Any) -> None:
        # phoneme string
        self.phoneme: str = features["Vowel"]
        # Call parent constructor
        super().__init__(self.phoneme)
        # retrieves appropriate entry from vowel types dictionary
        # for this particular phoneme
        self.vowel_features: Dict[str, str] = VOWEL_TYPES[self.phoneme]
        # stress string
        self.stress: str = features.get("Stress", "0") or "0"
        # length of vowel (short, or long)
        self.length: str = self.vowel_features["length"]

    def __str__(self) -> str:
        return f"{self.phoneme}{self.stress}"

    def __repr__(self) -> str:
        return (
            f"Vowel(phoneme={self.phoneme}, stress={self.stress}, length={self.length})"
        )


class Consonant(Phoneme):
    """Represents an individual phoneme that has been classified as a consonant"""

    def __init__(self, **features: Any) -> None:
        self.phoneme: str = features["Consonant"]
        # Call parent constructor
        super().__init__(self.phoneme)

    def __str__(self) -> str:
        return f"{self.phoneme}"

    def __repr__(self) -> str:
        return f"Consonant(phoneme={self.phoneme})"
