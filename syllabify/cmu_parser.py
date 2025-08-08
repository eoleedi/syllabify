"""
Parses CMU dictionary into Python Dictionary
AC 2017-08-10: updated from Py2 original for Py3
changes other than print() statements noted
"""

import os
import re
import functools

from syllabify.phonemes import Phoneme

# Settings
CMU_DIR = os.path.join(os.path.dirname(__file__), "CMU_dictionary")
# Version
VERSION = "cmudict-0.7b"
# Path
PATH_TO_DICTIONARY = os.path.join(CMU_DIR, VERSION)


class CMUDictionary:
    """CMU Dictionary parser and interface"""

    def __init__(self, path_to_dictionary=PATH_TO_DICTIONARY):
        self.regexp = re.compile(
            r"""
                        (?P<Comment>;;;.*) # ;;; denotes Comment: to be ignore
                        |(?P<Word>'?\w+[^\(\)]*) # Not interested in first character
                        (?P<Alternative> \(\d+\))? # (digit) denotes that another
                        (?P<Seperator> \s\s) # Separator: to be ignored
                        (?P<Phoneme> [^\n]+) # The remainder
                     """,
            re.VERBOSE,
        )

        # import CMU dictionary
        try:
            with open(path_to_dictionary, "r", encoding="latin-1") as self.cmudict_file:
                # create Python CMU dictionary
                self._cmudict = self._create_dictionary()
        except IOError as e:
            print(e, "file not found, check settings...")
            raise

    def __getitem__(self, key):
        try:
            return self._cmudict[key.upper()]
        except (KeyError, UnicodeDecodeError):
            return None

    def get_dictionary(self):
        """Get the CMU dictionary"""
        return self._cmudict

    def _create_dictionary(self):
        dict_temp = {}
        for line in self.cmudict_file.readlines():
            match = re.match(self.regexp, line)
            if match:
                dict_temp = self._update_dictionary(match, dict_temp)
        return dict_temp

    def _update_dictionary(self, match, dictionary):
        if match.group("Word") is None:
            # No word found, do nothing
            return dictionary

        if match.group("Word") and (match.group("Alternative") is None):
            # This is a new word
            # Create an entry, and instantiate a Transcription object
            dictionary[match.group("Word")] = Transcription(match.group("Phoneme"))
            return dictionary

        if match.group("Word") and match.group("Alternative"):
            # There is an alternative phoneme representation of the matched word
            # Append phoneme rep. to dictionary entry for this word
            dictionary[match.group("Word")].append(match.group("Phoneme"))
            return dictionary

        return dictionary


class Transcription:
    """the phoneme transcription of the word"""

    def __init__(self, phoneme):
        self.representation = [Phoneme(phoneme)]

    def __len__(self):
        return len(self.representation)

    def __str__(self):
        return (
            "["
            + functools.reduce(
                lambda x, y: str(x) + str(y) + ", ", self.representation, ""
            )
            + "]"
        )

    def append(self, phoneme):
        """Append phoneme to representation"""
        self.representation.append(Phoneme(phoneme))

    def get_phonemic_representations(self):
        """Return all the phonemes that can represent this word"""
        # return all the phonemes that can represent this word
        return [x.phoneme for x in self.representation]


# create dictionary
cmudict = CMUDictionary()


def cmu_transcribe(word):
    """Transcribe a word using CMU dictionary"""
    try:
        transcription = cmudict[word]
        if transcription:
            return transcription.get_phonemic_representations()
        return None
    except AttributeError:
        # Entry not found
        return None
