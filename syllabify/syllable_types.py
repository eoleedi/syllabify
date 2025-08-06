"""
Data types for syllabification
"""

import functools
from typing import List, Optional, Union, Any, Dict

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


class Cluster:
    """Represents groups of phonemes. Clusters contain either Vowels, or Consonants - never both"""

    def __init__(self, phoneme: Optional[Union["Vowel", "Consonant"]] = None) -> None:
        self.phoneme_list: List[Union["Vowel", "Consonant"]] = []
        if phoneme:
            self.add_phoneme(phoneme)
        # all phonemes have a string representation
        self.comparator = self.get_phoneme_string()

    def get_phoneme(self) -> List[Union["Vowel", "Consonant"]]:
        return self.phoneme_list

    def get_phoneme_string(self) -> str:
        # syllable without an onset, or coda has a phoneme of '' empty string
        string = ""
        for ph in self.phoneme_list:
            string += ph.phoneme
        return string

    def add_phenome(self, phoneme: Union["Vowel", "Consonant"]) -> None:
        """Legacy method name - use add_phoneme instead"""
        self.add_phoneme(phoneme)

    def add_phoneme(self, phoneme: Union["Vowel", "Consonant"]) -> None:
        self.phoneme_list.append(phoneme)
        self._update_comparator()

    def _update_comparator(self) -> None:
        self.comparator = self.get_phoneme_string()

    def get_stress(self) -> str:
        if self.type() == Vowel:
            # mapping function that returns the stress value of a Vowel
            def get_phoneme_stress(x):
                return x.stress

            # return the maximum stress value in the cluster
            return functools.reduce(
                lambda x, y: x if int(x) > int(y) else y,
                map(get_phoneme_stress, self.phoneme_list),
                "0",
            )
        return "0"

    def type(self) -> Optional[type]:
        """returns the type of the phoneme cluster: either Vowel, or Consonant"""
        if self.phoneme_list == []:
            return None
        else:
            return type(self.phoneme_list[-1])

    # Boolean Methods
    def is_short(self) -> bool:
        if self.type() == Vowel:
            # Rule for determining if vowel is short
            return (
                len(self.phoneme_list) == 1 and self.phoneme_list[0].length == "short"
            )
        return False

    def is_long(self) -> bool:
        return not self.is_short()

    def has_phoneme(self) -> bool:
        return bool(self.phoneme_list != [])

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
        return self.phoneme_list != []

    def __str__(self) -> str:
        return functools.reduce(lambda x, y: str(x) + str(y), self.phoneme_list, "")
    
    def __repr__(self) -> str:
        return "Cluster(" + str(self.get_phoneme_string()) + ")"


class Empty:
    """container for the empty syllable cluster"""

    def __init__(self) -> None:
        self.phoneme: Optional[str] = None
        self.comparator: Optional[str] = None

    def __str__(self) -> str:
        return "empty"

    def has_phoneme(self) -> bool:
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


class Syllable:
    """groups phonemes into syllables"""

    def __init__(
        self,
        onset: Union[Cluster, Empty, None] = None,
        nucleus: Union[Cluster, Empty, None] = None,
        coda: Union[Cluster, Empty, None] = None,
    ) -> None:
        self.onset = onset if onset is not None else Empty()
        self.rime = Rime(nucleus, coda)

    # Setters
    def set_onset(self, cluster: Union[Cluster, Empty]) -> None:
        self.onset = cluster

    def set_nucleus(self, cluster: Union[Cluster, Empty]) -> None:
        self.rime.set_nucleus(cluster)

    def set_coda(self, cluster: Union[Cluster, Empty]) -> None:
        self.rime.set_coda(cluster)

    # Getters
    def get_onset(self) -> Union[Cluster, Empty]:
        return self.onset

    def get_nucleus(self) -> Union[Cluster, Empty]:
        return self.rime.get_nucleus()

    def get_coda(self) -> Union[Cluster, Empty]:
        return self.rime.get_coda()

    def get_stress(self) -> str:
        return self.rime.get_stress()

    def get_rime(self) -> "Rime":
        return self.rime

    # Boolean Methods
    def is_light(self) -> bool:
        return self.is_short() and self.coda_is_empty()

    def is_short(self) -> bool:
        return (
            self.rime.nucleus.is_short()
            if hasattr(self.rime.nucleus, "is_short")
            else False
        )

    def has_onset(self) -> bool:
        return (
            bool(self.onset.has_phoneme())
            if hasattr(self.onset, "has_phoneme")
            else False
        )

    def onset_is_empty(self) -> bool:
        return not self.has_onset()

    def has_nucleus(self) -> bool:
        return self.rime.has_nucleus()

    def nucleus_is_empty(self) -> bool:
        return not self.has_nucleus()

    def has_coda(self) -> bool:
        return self.rime.has_coda()

    def coda_is_empty(self) -> bool:
        return not self.rime.has_coda()

    def __str__(self) -> str:
        return (
            "{onset: "
            + str(self.get_onset())
            + ", nucleus: "
            + str(self.get_nucleus())
            + ", coda: "
            + str(self.get_coda())
            + "}"
        )
    def __repr__(self):
        return (
            "Syllable(onset="
            + str(self.get_onset())
            + ", nucleus="
            + str(self.get_nucleus())
            + ", coda="
            + str(self.get_coda())
            + ")"
        )


class Word:
    """Represents a word, which is a collection of syllables"""

    def __init__(self, syllables: Optional[List[Syllable]] = None) -> None:
        self.syllables: List[Syllable] = syllables if syllables else []

    def add_syllable(self, syllable: Syllable) -> None:
        self.syllables.append(syllable)

    def get_syllables(self) -> List[Syllable]:
        return self.syllables

    def __str__(self) -> str:
        return " ".join(str(s) for s in self.syllables)

    def __repr__(self) -> str:
        return "Word(syllables=[" + ", ".join(repr(s) for s in self.syllables) + "])"

class Rime:
    """Rime Class"""

    def __init__(
        self,
        nucleus: Union[Cluster, Empty, None] = None,
        coda: Union[Cluster, Empty, None] = None,
    ) -> None:
        self.nucleus = nucleus if nucleus is not None else Empty()
        self.coda = coda if coda is not None else Empty()

    # Setters
    def set_nucleus(self, cluster: Union[Cluster, Empty]) -> None:
        self.nucleus = cluster

    def set_coda(self, cluster: Union[Cluster, Empty]) -> None:
        self.coda = cluster

    # Boolean Methods
    def has_nucleus(self) -> bool:
        return (
            bool(self.nucleus.has_phoneme())
            if hasattr(self.nucleus, "has_phoneme")
            else False
        )

    def has_coda(self) -> bool:
        return (
            bool(self.coda.has_phoneme())
            if hasattr(self.coda, "has_phoneme")
            else False
        )

    def get_nucleus(self) -> Union[Cluster, Empty]:
        return self.nucleus

    def get_coda(self) -> Union[Cluster, Empty]:
        return self.coda

    def get_stress(self) -> str:
        return self.nucleus.get_stress() if hasattr(self.nucleus, "get_stress") else "0"



class Vowel:
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


class Consonant:
    """Represents an individual phoneme that has been classified as a consonant"""

    def __init__(self, **features: Any) -> None:
        self.phoneme: str = features["Consonant"]

    def __str__(self) -> str:
        return "%s " % self.phoneme

    def __repr__(self) -> str:
        return f"Consonant(phoneme={self.phoneme})"
