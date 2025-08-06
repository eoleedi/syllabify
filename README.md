# Syllabify

[![PyPI](https://img.shields.io/pypi/v/syllabify.svg)](https://pypi.org/project/syllabify/)
[![Python 3.x](https://img.shields.io/pypi/pyversions/syllabify.svg?logo=python&logoColor=white)](https://pypi.org/project/syllabify/)
[![License](https://img.shields.io/github/license/eoleedi/TimeTree-Exporter)](https://github.com/eoleedi/TimeTree-Exporter/blob/main/LICENSE)

Automatically convert plain text into phonemes (US English pronunciation) and syllabify.

Modified from [the repository](https://github.com/cainesap/syllabify) set up by Andrew Caines with some key changes, itemised below:

- Environment management using Poetry
- Python 3.9+ compatibility
- Easy to access class and function interfaces

## Set up

Requires [Python 3](https://www.python.org/downloads) (Anthony Evans used Python 2: if that's what you prefer, see his repo).

```bash
pip install syllabify
```

## Usage

### Package interface

```python
from syllabify import syllabify

syllable = syllabify("linguistics")
print(syllable)

# Output:
# [Syllable(onset=L , nucleus=IH [st:0 ln:short], coda=NG ),
#  Syllable(onset=G W , nucleus=IH [st:1 ln:short], coda=empty),
#  Syllable(onset=S T , nucleus=IH [st:0 ln:short], coda=K S )
# ]
```

You can get the onset, nucleus, and coda of each syllable:

```python
from syllabify import syllabify

syllable = syllabify("linguistics")
print(f"Onset: {syllable.get_onset()}")
print(f"Nucleus: {syllable.get_nucleus()}")
print(f"Coda: {syllable.get_coda()}")

```


### Command line interface

One word at a time:

```bash
syllabify linguistics
```

Or several (space-separated):

```bash
syllabify colourless green ideas
```

## Output

If the input word is found in the dictionary, a phonemic, syllabified transcript is returned. For example, for the word _linguistics_:

```
{onset: L , nucleus: IH [st:0 ln:short], coda: NG }
{onset: G W , nucleus: IH [st:1 ln:short], coda: empty}
{onset: S T , nucleus: IH [st:0 ln:short], coda: K S }
```

There's one syllable per line. Each syllable is made up of an 'onset', 'nucleus', and 'coda'. Phonemes are space-separated and capitalized in [ARPAbet](http://en.wikipedia.org/wiki/ARPABET) format. In line with phonological theory, the nucleus must have content, whereas the onset and coda may be empty. Within the vocalic content of the nucleus there's also an indication whether the syllable is stressed ('st':0 or 1), and whether the length ('ln') is short or long.

## CMU Pronouncing Dictionary

`Syllabify` depends on the [CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) of North American English word pronunciations. Version 0.7b was the current one at time of writing, but it throws a UnicodeDecodeError, so we're still using version 0.7a (amended to remove erroneous 'G' from SUGGEST and related words). Please see the dictionary download website to obtain the current version, add the `cmudict-N.nx(.phones|.symbols)*` files to the `CMU_dictionary` directory, remove the '.txt' suffixes, and update the line `VERSION = 'cmudict-n.nx'` in `cmu_parser.py`
