# Syllabify

[![PyPI](https://img.shields.io/pypi/v/syllabify.svg)](https://pypi.org/project/syllabify/)
[![Python 3.x](https://img.shields.io/pypi/pyversions/syllabify.svg?logo=python&logoColor=white)](https://pypi.org/project/syllabify/)
[![License](https://img.shields.io/github/license/eoleedi/syllabify)](https://github.com/eoleedi/syllabify/blob/main/LICENSE)

Automatically convert plain text into phonemes (US English pronunciation) and syllabify.

Modified from [the repository](https://github.com/cainesap/syllabify) set up by Andrew Caines with some key changes, itemised below:

- Environment management using uv
- Python 3.10+ compatibility
- Easy to access class and function interfaces
- Use up-to-date cmudict versioned by [python-cmudict](https://github.com/prosegrinder/python-cmudict)

> Credits: Many thanks for [@cainesap](https://github.com/cainesap)'s work on porting and fixes & the original author [@anthonysgevans](https://github.com/anthonysgevans)
## Set up

Requires [Python 3](https://www.python.org/downloads) (Anthony Evans used Python 2: if that's what you prefer, see his repo).

```bash
pip install syllabify
```

## Usage

### Package interface

```python
from syllabify import syllabify
word = syllabify("linguistics")
print(word)
```

```text
L IH0 NG {onset: L, nucleus: IH0, coda: NG}
G W IH1 {onset: GW, nucleus: IH1, coda: empty}
S T IH0 K S {onset: ST, nucleus: IH0, coda: KS}
```

You can get the onset, nucleus, and coda of each syllable:

```python
from syllabify import syllabify

word = syllabify("linguistics")
for syllable in word.syllables:
    print(f"Onset: {syllable.onset}")
    print(f"Nucleus: {syllable.nucleus}")
    print(f"Coda: {syllable.coda}")
```

```text
Onset: L
Nucleus: IH0
Coda: NG
Onset: GW
Nucleus: IH1
Coda: empty
Onset: ST
Nucleus: IH0
Coda: KS
```

### Command line interface

One word at a time:

```bash
syllabify linguistics
```

```text
📝 Input: linguistics
🔤 Syllabification:

LIH0NG [L.IH0.NG] | ˈGWIH1 [GW.IH1.∅] | STIH0KS [ST.IH0.KS]

📖 Legend:
  [onset.nucleus.coda] = syllable structure
  ∅ = empty position
  ˈ = primary stress
  ˌ = secondary stress
  | = syllable boundary
```

Or several (space-separated):

```bash
syllabify colorless green ideas
```

```text
📝 Input: colorless green ideas
🔤 Syllabification:

  ˈKAH1L [K.AH1.L] | ER0 [∅.ER0.∅] | LAH0S [L.AH0.S]
  ˈGRIY1N [GR.IY1.N]
  AY0 [∅.AY0.∅] | ˈDIY1 [D.IY1.∅] | AH0Z [∅.AH0.Z]

📖 Legend:
  [onset.nucleus.coda] = syllable structure
  ∅ = empty position
  ˈ = primary stress
  ˌ = secondary stress
  | = syllable boundary
```
