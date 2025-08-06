from typing import Any, Dict

from syllabify.constants import VOWEL_TYPES

class Phoneme:
    """Individual phoneme representation"""

    def __init__(self, phoneme):
        self.phoneme = phoneme

    def __str__(self):
        return str(self.phoneme)

class Vowel(Phoneme):
    """Represents an individual phoneme that has been classified as a vowel"""

    def __init__(self, **features: Any) -> None:
        # phoneme string
        self.phoneme: str = features["Vowel"]
        # retrieves appropriate entry from vowel types dictionary
        # for this particular phoneme
        self.vowel_features: Dict[str, str] = VOWEL_TYPES[self.phoneme]
        # stress string
        self.stress: str = features.get("Stress", "0") or "0"
        # length of vowel (short, or long)
        self.length: str = self.vowel_features["length"]

    def __str__(self) -> str:
        return "%s [st:%s ln:%s]" % (self.phoneme, self.stress, self.length)

    def __repr__(self) -> str:
        return f"Vowel(phoneme={self.phoneme}, stress={self.stress}, length={self.length})"

class Consonant(Phoneme):
    """Represents an individual phoneme that has been classified as a consonant"""

    def __init__(self, **features: Any) -> None:
        self.phoneme: str = features["Consonant"]

    def __str__(self) -> str:
        return "%s " % self.phoneme

    def __repr__(self) -> str:
        return f"Consonant(phoneme={self.phoneme})"
