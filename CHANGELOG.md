# Changelog

## [0.4.0](https://github.com/eoleedi/syllabify/compare/v0.3.2...v0.4.0) (2025-08-08)


### Features

* handle possessive ([e3be56b](https://github.com/eoleedi/syllabify/commit/e3be56b33d34ce2a918eb6663bb8c5b4eac4bdce))
* support custom fallback_fn for transcribe ([c25e4aa](https://github.com/eoleedi/syllabify/commit/c25e4aa3606e8d3915e1783bf243c77b0df4aa6d))


### Bug Fixes

* add Phoneme to the package top level ([04a38c2](https://github.com/eoleedi/syllabify/commit/04a38c2873fbb43f0a1bdba0cab966eff9da13df))

## [0.3.2](https://github.com/eoleedi/syllabify/compare/v0.3.1...v0.3.2) (2025-08-08)


### Bug Fixes

* add iter and getitem function to word and sentence ([4721218](https://github.com/eoleedi/syllabify/commit/4721218c68f361287c6cc0bc3dc2580f22d7b1b9))
* add space between phonemes ([1dfac42](https://github.com/eoleedi/syllabify/commit/1dfac42dee753b3d4e4deefba4da7514fbd13f4a))
* add the space directly in cluster str ([a36a82b](https://github.com/eoleedi/syllabify/commit/a36a82b078e4894b0d0f1541388f7cdd54742e97))
* **deps:** update cmudict to version 0.7b ([b6f037b](https://github.com/eoleedi/syllabify/commit/b6f037bc08624467997334d580a64f1e2a32c073))
* raise ValueError when word is not found in CMU Dictionary ([3739a7f](https://github.com/eoleedi/syllabify/commit/3739a7f06017379e08d4a0c1a9202460648feb4c))
* remove get_stress function ([1c7e25b](https://github.com/eoleedi/syllabify/commit/1c7e25b5800d6e059a442022a634f78263d90aef))
* remove unused cmu parser test function ([ffaf8d5](https://github.com/eoleedi/syllabify/commit/ffaf8d58c6da77310ecc618c41554d83f09b475c))
* remove unused legacy function ([ec93fb1](https://github.com/eoleedi/syllabify/commit/ec93fb1b4535ebfe3d5ec39557721cf5034c3553))
* return  either Sentence or list of sentence for consistency ([eccb61c](https://github.com/eoleedi/syllabify/commit/eccb61c286ea7f49214658ad92ac6022acf448df))

## [0.3.1](https://github.com/eoleedi/syllabify/compare/v0.3.0...v0.3.1) (2025-08-08)


### Bug Fixes

* incorrect import in __init__.py ([b3bde12](https://github.com/eoleedi/syllabify/commit/b3bde12b7caf058943dc4fab3588634133878fec))

## [0.3.0](https://github.com/eoleedi/syllabify/compare/v0.2.0...v0.3.0) (2025-08-06)


### Features

* add get_phoneme function & refactor all the str function ([f294857](https://github.com/eoleedi/syllabify/commit/f294857e5f8d1196e3b382680ed4f06f5c21e24c))
* prettify cli ([595881d](https://github.com/eoleedi/syllabify/commit/595881d029b5c24c6424ec826ae6ef93384b85dd))


### Bug Fixes

* cli ([cd21bc8](https://github.com/eoleedi/syllabify/commit/cd21bc8c7b1e3a7ae8cddf86a9eb50fbdc9a2e7b))


### Documentation

* update README.md ([f8f74f0](https://github.com/eoleedi/syllabify/commit/f8f74f099f77b620b0be2be50ba4abe9211badbd))

## [0.2.0](https://github.com/eoleedi/syllabify/compare/v0.1.0...v0.2.0) (2025-08-06)


### Features

* add word class for structured senetence generation ([8feefd8](https://github.com/eoleedi/syllabify/commit/8feefd8e3bd377c3c1c919bbaf18cddee4e90633))


### Bug Fixes

* add generate_sentence function to top level ([383c0f6](https://github.com/eoleedi/syllabify/commit/383c0f675483127d42d33322fe4e8ec10e5647a9))


### Documentation

* add badge ([5e4b31f](https://github.com/eoleedi/syllabify/commit/5e4b31f400934e430f883fbc91c5732b44e2504b))

## 0.1.0 (2025-08-05)


### Features

* first commit of the syllabify custom fork by eoleedi ([26d82d3](https://github.com/eoleedi/syllabify/commit/26d82d3f0ff2aabd294db5d16fccd56472e7cedc))
