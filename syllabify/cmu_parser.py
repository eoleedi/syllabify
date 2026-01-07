"""
Parses CMU dictionary using python-cmudict package
"""

import cmudict


class CMUDictionary:
    """CMU Dictionary interface using python-cmudict package"""

    def __init__(self):
        # Load the CMU dictionary using python-cmudict
        self._cmudict = cmudict.dict()

    def __getitem__(self, key):
        try:
            return Transcription(self._cmudict.get(key.lower()))
        except (KeyError, AttributeError):
            return None

    def get_dictionary(self):
        """Get the CMU dictionary"""
        return self._cmudict


class Transcription:
    """the phoneme transcription of the word"""

    def __init__(self, phoneme_lists):
        """
        Initialize with phoneme lists from python-cmudict
        phoneme_lists is a list of lists, where each inner list is a pronunciation
        """
        if phoneme_lists is None:
            self.representation = []
        else:
            # Convert list of phoneme lists to space-separated strings
            # to maintain compatibility with existing Phoneme class
            self.representation = [" ".join(phonemes) for phonemes in phoneme_lists]

    def __len__(self):
        return len(self.representation)

    def __str__(self):
        return "[" + ", ".join(self.representation) + "]"

    def get_phonemic_representations(self):
        """Return all the phonemes that can represent this word"""
        return self.representation


# create dictionary
cmudict_instance = CMUDictionary()


def cmu_transcribe(word):
    """Transcribe a word using CMU dictionary"""
    try:
        transcription = cmudict_instance[word]
        if transcription and len(transcription) > 0:
            return transcription.get_phonemic_representations()
        return None
    except (AttributeError, TypeError):
        # Entry not found
        return None
