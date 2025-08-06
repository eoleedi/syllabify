"""
Command Line Interface for syllabify
"""

import sys
from syllabify.core import syllabify
from syllabify.syllables import Word, Sentence


def format_syllable(syllable):
    """Format a single syllable with pretty output"""
    onset = str(syllable.onset) if syllable.has_onset() else "∅"
    nucleus = str(syllable.nucleus) if syllable.has_nucleus() else "∅"
    coda = str(syllable.coda) if syllable.has_coda() else "∅"

    # Get stress marking
    stress_mark = ""
    if syllable.has_nucleus() and hasattr(syllable.nucleus, "stress"):
        stress = syllable.stress
        if stress == "1":
            stress_mark = "ˈ"  # Primary stress
        elif stress == "2":
            stress_mark = "ˌ"  # Secondary stress

    # Create syllable structure representation
    syllable_structure = f"[{onset}.{nucleus}.{coda}]"

    # Create phonetic representation
    phonemes = []
    if syllable.has_onset():
        phonemes.extend([str(p) for p in syllable.onset.phonemes])
    if syllable.has_nucleus():
        phonemes.extend([str(p) for p in syllable.nucleus.phonemes])
    if syllable.has_coda():
        phonemes.extend([str(p) for p in syllable.coda.phonemes])

    phonetic = stress_mark + "".join(phonemes)

    return f"{phonetic} {syllable_structure}"


def format_word(word):
    """Format a single word with pretty output"""
    if not word or not word.syllables:
        return "∅"

    syllable_parts = [format_syllable(syl) for syl in word.syllables]
    return " | ".join(syllable_parts)


def format_output(result):
    """Format the syllabification result with pretty output"""
    if result is None:
        return "No syllabification available"

    if isinstance(result, Word):
        return format_word(result)
    if isinstance(result, Sentence):
        word_parts = [format_word(word) for word in result.words]
        return "\n".join(f"  {word}" for word in word_parts)

    return str(result)


def main():
    """Main function for command line usage"""
    if len(sys.argv) > 1:
        words = sys.argv[1:]
        input_text = " ".join(words)

        print(f"📝 Input: {input_text}")
        print("🔤 Syllabification:")
        print()

        syllables = syllabify(input_text)
        formatted_output = format_output(syllables)
        print(formatted_output)

        # Add legend
        print()
        print("📖 Legend:")
        print("  [onset.nucleus.coda] = syllable structure")
        print("  ∅ = empty position")
        print("  ˈ = primary stress")
        print("  ˌ = secondary stress")
        print("  | = syllable boundary")

    else:
        print("🎯 Syllabify - Phonetic Syllable Analyzer")
        print()
        print("Usage:")
        print("  syllabify <word1> [word2] [word3] ...")
        print()
        print("Examples:")
        print("  syllabify linguistics")
        print("  syllabify linguistics phonetics")
        print("  syllabify beautiful")
        print()
        print("📖 The tool will show:")
        print("  • Phonetic transcription with stress marks")
        print("  • Syllable structure breakdown")
        print("  • Clear syllable boundaries")


if __name__ == "__main__":
    main()
