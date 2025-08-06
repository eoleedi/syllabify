"""
Syllabify main module
Updated to Python 3 from Python 2 original
"""

import re
import copy
import functools
from typing import List

from syllabify.cmu_parser import cmu_transcribe
from syllabify.syllables import Cluster, Syllable, Word, Sentence
from syllabify.phonemes import Vowel, Consonant
from syllabify.symbols import (
    NG,
    HH,
    W,
    Y,
    S,
    CH,
    JH,
    DH,
    F,
    SH,
    TH,
    V,
    ZH,
    Z,
    B,
    D,
    G,
    K,
    P,
    T,
    M,
    N,
    L,
    R,
)


phoneme_classify = re.compile(
    r"""
                        ((?P<Vowel>AO|UW|EH|AH|AA|IY|IH|UH|AE|AW|AY|ER|EY|OW|OY)
                        |(?P<Consonant>CH|DH|HH|JH|NG|SH|TH|ZH|Z|S|P|R|K|L|M|N|F|G|D|B|T|V|W|Y\d*)
                        )
                        ((?P<Stress>0|1|2)
                        )?
                        """,
    re.VERBOSE,
)


def _create_phoneme_object(phoneme):
    """Create a phoneme object from a phoneme string."""
    # match against regular expression
    phoneme_feature = re.match(phoneme_classify, phoneme).groupdict()

    # input is phoneme feature dictionary
    if phoneme_feature["Consonant"]:
        # return consonant object
        return Consonant(**phoneme_feature)
    if phoneme_feature["Vowel"]:
        # return vowel object
        return Vowel(**phoneme_feature)
    # unknown phoneme class
    raise ValueError("unknown Phoneme Class: cannot create appropriate Phoneme object")


def _create_cluster(cluster_list, phoneme):
    """Create phoneme clusters from individual phonemes."""
    current_cluster = cluster_list.pop()

    # Consonants must be grouped together into clusters
    if (
        current_cluster.type() == Consonant
        and isinstance(phoneme, Consonant)
        or current_cluster.type() is None
    ):
        # Adjacent phonemes of type consonant belong to the same cluster, if the
        # current cluster.last_phoneme == None that means it's empty
        # update current cluster
        # AC 2017-08-12: provided it's not NG (should not be clustered)
        if NG in current_cluster.get_phoneme_string():
            # create new cluster add phoneme to it and return
            cluster_list.append(current_cluster)
            cluster_list.append(Cluster(phoneme))
        else:
            current_cluster.add_phoneme(phoneme)
            # append to cluster list
            cluster_list.append(current_cluster)
        # return cluster list
        return cluster_list
    # create new cluster add phoneme to it and return
    cluster_list.append(current_cluster)
    cluster_list.append(Cluster(phoneme))
    return cluster_list


def _create_syllable(syllable_list, cluster):
    """Create syllables from phoneme clusters."""
    syllable = syllable_list.pop()
    push = syllable_list.append

    if (
        syllable.onset_is_empty()
        and syllable.nucleus_is_empty()
        and cluster.type() == Consonant
    ):
        # cluster is assigned to the onset of the current syllable
        syllable.onset = cluster
        push(syllable)
        return syllable_list

    if cluster.type() == Vowel:
        if syllable.has_nucleus():
            # this cluster becomes the nucleus of a new syllable
            # push current syllable back on the syllable stack
            push(syllable)
            # create new syllable
            new_syllable = Syllable(nucleus=cluster)
            # push new_syllable onto the stack
            push(new_syllable)
            return syllable_list
        # syllable does not have nucleus so this cluster becomes the
        # nucleus on the current syllable
        syllable.nucleus = cluster
        push(syllable)
        return syllable_list

    if syllable.has_nucleus() and cluster.type() == Consonant:
        if syllable.has_coda():
            # this cluster is the onset of the next syllable
            new_syllable = Syllable(onset=cluster)
            # push syllable onto stack
            push(new_syllable)
            return syllable_list
        if syllable.coda_is_empty():
            # Onset Maximalism dictates we push consonant clusters to
            # the onset of the next syllable, unless the nuclear cluster is LIGHT and
            # has primary stress
            maximal_coda, maximal_onset = onset_rules(cluster)

            # AC 2017-09-15: removed ambisyllabicity as a theoretical stance
            # add cluster only to the next syllable
            if maximal_coda:
                syllable.coda = maximal_coda
                push(syllable)
            else:
                push(syllable)
            if maximal_onset:
                new_syllable = Syllable(onset=maximal_onset)
            else:
                new_syllable = Syllable()
            push(new_syllable)
            return syllable_list
    return syllable_list  # Add explicit return for consistency


def _validate_last_syllable(syllable_list):
    """Validate and fix the last syllable in the list."""
    # the syllable algorithm may assign a consonant cluster to a syllable that does not have
    # a nucleus, this is not allowed in the English language.

    # check the last syllable
    syllable = syllable_list.pop()
    push = syllable_list.append

    if syllable.nucleus_is_empty():
        if syllable.has_onset():
            # pop the previous syllable
            prev_syllable = syllable_list.pop()
            onset = syllable.onset
            # set the coda of the previous syllable to the value of the orphan onset
            if prev_syllable.has_coda():
                # add phoneme
                coda_cluster = prev_syllable.coda
                if coda_cluster != onset:
                    for phoneme in onset.phonemes:
                        coda_cluster.add_phoneme(phoneme)
                    push(prev_syllable)
                else:
                    push(prev_syllable)
            else:
                prev_syllable.coda = onset
                push(prev_syllable)
        return syllable_list
    # There is no violation, push syllable back on the stack
    push(syllable)

    return syllable_list


def factory(phoneme):
    """argument is a string of phonemes e.g.'B IH0 K AH0 Z'"""
    phonemes = phoneme.split()

    # Create a list of phoneme clusters from phoneme list
    cluster_list = functools.reduce(
        _create_cluster, map(_create_phoneme_object, phonemes), [Cluster()]
    )

    # Apply syllable creation rules to list of phoneme clusters
    syllable_list = functools.reduce(_create_syllable, cluster_list, [Syllable()])

    # Validate last syllable, and return completed syllable list
    return _validate_last_syllable(syllable_list)


def coda_rules(cluster):
    """checks if the cluster is a valid onset or whether it needs to be split"""

    coda_cluster = copy.deepcopy(cluster)
    phonemes = map(str, coda_cluster.phonemes)
    phonemelist = list(
        phonemes
    )  # grabbed list of phonemes to move away from Py3 map problem, and strip trailing spaces
    list_of_phonemes = []
    for phone in phonemelist:
        list_of_phonemes.append(phone.rstrip())

    def _split_and_update(phoneme, phonemes=None, cluster=None):
        if phonemes is None:
            phonemes = list_of_phonemes.copy()
        if cluster is None:
            cluster = coda_cluster
        index = phonemes.index(phoneme)
        # split on phoneme and discard the rest
        head = cluster.phonemes[: index - 1]
        # update cluster
        cluster.phonemes = head
        # update string list
        phonemes = phonemes[: index - 1]

        return (phonemes, cluster)

    # rule 1 - no /HH/ in coda
    if HH in list_of_phonemes:
        list_of_phonemes, coda_cluster = _split_and_update("HH")

    # rule 2 - no glides in coda
    # if L in list_of_phonemes:  # commented out by AC
    #     list_of_phonemes, coda_cluster = _split_and_update('L')

    # if R in list_of_phonemes:  # commented out by AC
    #     list_of_phonemes, coda_cluster = _split_and_update('R')

    if W in list_of_phonemes:
        list_of_phonemes, coda_cluster = _split_and_update("W")

    if Y in list_of_phonemes:
        list_of_phonemes, coda_cluster = _split_and_update("Y")

    # rule 3 - if complex coda second consonant must not be
    # /NG/ /ZH/ /DH/
    if len(list_of_phonemes) > 1 and list_of_phonemes[1] in [NG, DH, ZH]:
        phoneme = coda_cluster.phonemes[1]
        # update cluster
        coda_cluster.phonemes = [phoneme]
        # update string list
        phonemes = list_of_phonemes[0:1]

    if coda_cluster.phonemes == []:
        coda_cluster = None

    return coda_cluster


def onset_rules(cluster):  # pylint: disable=too-many-branches
    """checks if the cluster is a valid onset or whether it needs to be split"""

    phonemes = map(str, cluster.phonemes)
    phonemelist = list(
        phonemes
    )  # grabbed list of phonemes to move away from Py3 map problem, and strip trailing spaces
    list_of_phonemes = []
    for phone in phonemelist:
        list_of_phonemes.append(phone.rstrip())
    coda_cluster = Cluster()

    def _split_and_update(phoneme):
        # get index of phoneme
        index = list_of_phonemes.index(phoneme)
        # split on phoneme and add tail coda cluster
        tail = cluster.phonemes[:index]
        # remaining phonemes
        head = cluster.phonemes[index:]
        # extend list
        coda_cluster.phonemes.extend(tail)
        # update cluster
        cluster.phonemes = head
        # update string list
        updated_phonemes = list_of_phonemes[index:]
        return (updated_phonemes, coda_cluster)

    def _remove_and_update():
        head = cluster.phonemes[0]
        rest = cluster.phonemes[1:]
        # extend list
        coda_cluster.phonemes.extend([head])
        # update cluster
        cluster.phonemes = rest
        # update string list
        updated_phonemes = list_of_phonemes[1:]
        return (updated_phonemes, coda_cluster)

    # rule 1 - /NG/ cannot exist in a valid onset
    # does /NG? exist? split on NG add NG to coda
    if NG in list_of_phonemes:
        list_of_phonemes, coda_cluster = _remove_and_update()

    # rule 2a - no affricates in complex onsets
    # /CH/ exist? split on affricate
    if CH in list_of_phonemes:
        list_of_phonemes, coda_cluster = _split_and_update("CH")

    # rule 2b - no affricates in complex onsets
    # /JH/ exist? split on affricate
    if JH in list_of_phonemes:
        list_of_phonemes, coda_cluster = _split_and_update("JH")

    # rule 3 - first consonant in a complex onset must be obstruent
    # if first consonant stop or fricative or nasal
    if len(list_of_phonemes) > 1 and list_of_phonemes[0] not in [
        B,
        D,
        G,
        K,
        P,
        T,
        DH,
        F,
        S,
        SH,
        TH,
        V,
        ZH,
        M,
        N,
    ]:
        list_of_phonemes, coda_cluster = _remove_and_update()

    # rule 4 - second consonant in a complex onset must be a voiced obstruent
    # if not OBSTRUENT and VOICED? split on second consonant
    if (
        len(list_of_phonemes) > 1
        and list_of_phonemes[0] != S
        and list_of_phonemes[1] not in [B, M, V, D, N, Z, ZH, R, Y]
    ):
        list_of_phonemes, coda_cluster = _remove_and_update()

    # rule 5 - if first consonant in a complex onset is not /s/
    # the second consonant must be liquid or glide /L/ /R/ /W/ /Y/
    if (
        len(list_of_phonemes) > 1
        and list_of_phonemes[0] != S
        and list_of_phonemes[1] not in [L, R, W, Y]
        and len(list_of_phonemes) < 3
    ):
        list_of_phonemes, coda_cluster = _remove_and_update()

    # rule 6 - deal with N|DR, ND|L, T|BR clusters
    if (
        len(list_of_phonemes) > 2
        and list_of_phonemes[0] in ["N", "T", "TH"]
        and list_of_phonemes[1] in ["D", "B"]
    ):
        if (
            list_of_phonemes[0] in ["R", "T"]
            and list_of_phonemes[1] in ["B"]
            and list_of_phonemes[2] in ["R"]
        ):  # heartbreak
            list_of_phonemes, coda_cluster = _split_and_update(list_of_phonemes[0])
        elif list_of_phonemes[0] in ["TH"]:  # toothbrush
            list_of_phonemes, coda_cluster = _split_and_update(list_of_phonemes[1])
        elif list_of_phonemes[0] in ["N"] or list_of_phonemes[2] in ["L", "M"]:
            if list_of_phonemes[1] in ["D"] and list_of_phonemes[2] in ["R"]:  # undress
                list_of_phonemes, coda_cluster = _split_and_update(list_of_phonemes[1])
            else:  # endless, handbag
                list_of_phonemes, coda_cluster = _split_and_update(list_of_phonemes[2])

    if coda_cluster.phonemes == []:
        coda_cluster = None

    if cluster.phonemes == []:
        cluster = None

    return (coda_cluster, cluster)


def syllabify(input_data) -> Word | Sentence | List[Sentence]:
    """
    Enhanced syllabify function that supports:
    - Single word (str) -> Word object
    - Single sentence (str) -> Sentence object
    - List of sentences (List[str]) -> List[Sentence] objects
    """

    if isinstance(input_data, str):
        # Check if input contains multiple words
        words = input_data.strip().split()

        if len(words) == 1:
            # Single word processing
            phonemes = cmu_transcribe(words[0])
            if phonemes:
                syllables = factory(phonemes[0])  # first version only
                return Word(syllables) if syllables else None
            print(words[0] + " not in CMU dictionary, sorry, please try again...")
            return None

        # Multiple words processing (sentence)
        word_objects = []
        for word in words:
            phonemes = cmu_transcribe(word.rstrip())
            if phonemes:
                syllables = factory(phonemes[0])
                if syllables:
                    word_objects.append(Word(syllables))
        return Sentence(word_objects) if word_objects else None

    if isinstance(input_data, list):
        # List of sentences processing
        sentence_objects = []
        for sentence_str in input_data:
            if isinstance(sentence_str, str):
                sentence_result = syllabify(sentence_str)
                if isinstance(sentence_result, Sentence):
                    sentence_objects.append(sentence_result)
                elif isinstance(sentence_result, Word):
                    # Single word treated as sentence with one word
                    sentence_objects.append(Sentence([sentence_result]))
        return sentence_objects

    raise TypeError("Input must be a string or list of strings")


def get_raw(word):
    """Get raw phoneme transcription"""
    return cmu_transcribe(word)
