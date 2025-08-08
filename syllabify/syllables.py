"""
Data types for syllabification
"""

import functools
from typing import List, Optional, Union

from syllabify.phonemes import Vowel, Consonant


class Cluster:
    """Represents groups of phonemes. Clusters contain either Vowels, or Consonants - never both"""

    def __init__(self, phoneme: Optional[Union[Vowel, Consonant]] = None) -> None:
        self.phonemes: List[Union[Vowel, Consonant]] = []
        if phoneme:
            self.add_phoneme(phoneme)
        # all phonemes have a string representation
        self.comparator = self.get_phoneme_string()

    def get_phoneme_string(self) -> str:
        """Get string representation of all phonemes in this cluster."""
        # syllable without an onset, or coda has a phoneme of '' empty string
        string = ""
        for ph in self.phonemes:
            string += ph.phoneme
        return string

    def add_phoneme(self, phoneme: Union[Vowel, Consonant]) -> None:
        """Add a phoneme to this cluster."""
        self.phonemes.append(phoneme)
        self._update_comparator()

    def _update_comparator(self) -> None:
        """Update the comparator string after adding phonemes."""
        self.comparator = self.get_phoneme_string()

    @property
    def stress(self) -> str:
        """Get the stress level of this cluster (only applicable for vowel clusters)."""
        if self.type() == Vowel:
            # mapping function that returns the stress value of a Vowel
            def get_phoneme_stress(x):
                return x.stress

            # return the maximum stress value in the cluster
            return functools.reduce(
                lambda x, y: x if int(x) > int(y) else y,
                map(get_phoneme_stress, self.phonemes),
                "0",
            )
        return "0"

    def type(self) -> Optional[type]:
        """returns the type of the phoneme cluster: either Vowel, or Consonant"""
        if not self.phonemes:
            return None
        return type(self.phonemes[-1])

    # Boolean Methods
    def is_short(self) -> bool:
        """Check if this cluster represents a short vowel."""
        if self.type() == Vowel:
            # Rule for determining if vowel is short
            return len(self.phonemes) == 1 and self.phonemes[0].length == "short"
        return False

    def is_long(self) -> bool:
        """Check if this cluster represents a long vowel."""
        return not self.is_short()

    def has_phoneme(self) -> bool:
        """Check if this cluster contains any phonemes."""
        return bool(self.phonemes)

    def get_phoneme(self) -> List[Union[Vowel, Consonant]]:
        """Returns a list of phonemes in this cluster."""
        return self.phonemes.copy()

    def __eq__(self, other: object) -> bool:
        """compare cluster objects"""
        if isinstance(other, Cluster):
            return self.comparator == other.comparator
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Cluster):
            return self.comparator != other.comparator
        return True

    def __bool__(self) -> bool:
        return bool(self.phonemes)

    def __str__(self) -> str:
        return " ".join(str(p) for p in self.phonemes)

    def __repr__(self) -> str:
        return "Cluster(" + str(self.get_phoneme_string()) + ")"

    def __iter__(self):
        return iter(self.phonemes)

    def __getitem__(self, index):
        return self.phonemes[index]


class Empty:
    """container for the empty syllable cluster"""

    def __init__(self) -> None:
        self.phoneme: Optional[str] = None
        self.comparator: Optional[str] = None

    def __str__(self) -> str:
        return "empty"

    def has_phoneme(self) -> bool:
        """Check if this empty cluster has any phonemes (always False)."""
        return False

    def __bool__(self) -> bool:
        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Empty):
            return self.comparator == other.comparator
        return False

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Empty):
            return self.comparator != other.comparator
        return True

    def __repr__(self) -> str:
        return "Empty()"

    def __iter__(self):
        return iter([self])


class Syllable:
    """groups phonemes into syllables"""

    def __init__(
        self,
        onset: Union[Cluster, Empty, None] = None,
        nucleus: Union[Cluster, Empty, None] = None,
        coda: Union[Cluster, Empty, None] = None,
    ) -> None:
        self.onset = onset if onset is not None else Empty()
        self.nucleus = nucleus if nucleus is not None else Empty()
        self.coda = coda if coda is not None else Empty()

    @property
    def stress(self) -> str:
        """Get the stress level of this syllable."""
        return self.nucleus.stress if hasattr(self.nucleus, "stress") else "0"

    @property
    def phonemes(self) -> List[Union[Vowel, Consonant]]:
        """Returns a list of phonemes in the syllable"""
        phonemes = []

        # Add phonemes from onset
        if self.has_onset() and hasattr(self.onset, "phonemes"):
            phonemes.extend(self.onset.phonemes)

        # Add phonemes from nucleus
        if self.has_nucleus() and hasattr(self.nucleus, "phonemes"):
            phonemes.extend(self.nucleus.phonemes)

        # Add phonemes from coda
        if self.has_coda() and hasattr(self.coda, "phonemes"):
            phonemes.extend(self.coda.phonemes)

        return phonemes

    # Boolean Methods
    def is_light(self) -> bool:
        """Check if this syllable is light (short vowel and no coda)."""
        return self.is_short() and self.coda_is_empty()

    def is_short(self) -> bool:
        """Check if this syllable has a short vowel."""
        return self.nucleus.is_short() if hasattr(self.nucleus, "is_short") else False

    def has_onset(self) -> bool:
        """Check if this syllable has an onset."""
        return (
            bool(self.onset.has_phoneme())
            if hasattr(self.onset, "has_phoneme")
            else False
        )

    def onset_is_empty(self) -> bool:
        """Check if this syllable's onset is empty."""
        return not self.has_onset()

    def has_nucleus(self) -> bool:
        """Check if this syllable has a nucleus."""
        return (
            bool(self.nucleus.has_phoneme())
            if hasattr(self.nucleus, "has_phoneme")
            else False
        )

    def nucleus_is_empty(self) -> bool:
        """Check if this syllable's nucleus is empty."""
        return not self.has_nucleus()

    def has_coda(self) -> bool:
        """Check if this syllable has a coda."""
        return (
            bool(self.coda.has_phoneme())
            if hasattr(self.coda, "has_phoneme")
            else False
        )

    def coda_is_empty(self) -> bool:
        """Check if this syllable's coda is empty."""
        return not self.has_coda()

    def __str__(self) -> str:
        return (
            " ".join(map(str, self.phonemes)) + " "
            "{onset: "
            + " ".join(map(str, self.onset))
            + ", nucleus: "
            + " ".join(map(str, self.nucleus))
            + ", coda: "
            + " ".join(map(str, self.coda))
            + "}"
        )

    def __repr__(self):
        return (
            "Syllable(onset="
            + " ".join(map(str, self.onset))
            + ", nucleus="
            + " ".join(map(str, self.nucleus))
            + ", coda="
            + " ".join(map(str, self.coda))
            + ")"
        )


class Word:
    """Represents a word, which is a collection of syllables"""

    def __init__(self, syllables: Optional[List[Syllable]] = None) -> None:
        self.syllables: List[Syllable] = syllables if syllables else []

    def add_syllable(self, syllable: Syllable) -> None:
        """Add a syllable to this word."""
        self.syllables.append(syllable)

    def get_phoneme(self) -> List[Union[Vowel, Consonant]]:
        """Returns a list of all phonemes in the word"""
        phonemes = []
        for syllable in self.syllables:
            phonemes.extend(syllable.get_phoneme())
        return phonemes

    def __str__(self) -> str:
        return " ".join(str(s) for s in self.syllables)

    def __repr__(self) -> str:
        return "Word(syllables=[" + ", ".join(repr(s) for s in self.syllables) + "])"

    def __iter__(self):
        """Iterate over syllables in the word."""
        return iter(self.syllables)

    def __getitem__(self, index):
        """Get a syllable by index or slice."""
        return self.syllables[index]

    def __len__(self):
        """Get the number of syllables in the word."""
        return len(self.syllables)


class Sentence:
    """Represents a sentence, which is a collection of words"""

    def __init__(self, words: Optional[List[Word]] = None) -> None:
        self.words: List[Word] = words if words else []

    def add_word(self, word: Word) -> None:
        """Add a word to this sentence."""
        self.words.append(word)

    def get_phoneme(self) -> List[Union[Vowel, Consonant]]:
        """Returns a list of all phonemes in the sentence"""
        phonemes = []
        for word in self.words:
            phonemes.extend(word.get_phoneme())
        return phonemes

    def __str__(self) -> str:
        return " | ".join(str(w) for w in self.words)

    def __repr__(self) -> str:
        return "Sentence(words=[" + ", ".join(repr(w) for w in self.words) + "])"

    def __iter__(self):
        """Iterate over words in the sentence."""
        return iter(self.words)

    def __getitem__(self, index):
        """Get a word by index or slice."""
        return self.words[index]

    def __len__(self):
        """Get the number of words in the sentence."""
        return len(self.words)


class Rime:  # pylint: disable=too-few-public-methods
    """Rime Class"""

    def __init__(
        self,
        nucleus: Union[Cluster, Empty, None] = None,
        coda: Union[Cluster, Empty, None] = None,
    ) -> None:
        self.nucleus = nucleus if nucleus is not None else Empty()
        self.coda = coda if coda is not None else Empty()

    @property
    def stress(self) -> str:
        """Get the stress level of this rime's nucleus."""
        return self.nucleus.stress if hasattr(self.nucleus, "stress") else "0"
