# ABP Tools

![ABP Logo](https://mazegroup.org//wiki/images/e/ed/ABP_logo.png)

ABP (Additional Binary Patterns) is a string encryption algorithm, designed on March 31, 2025. It is based on the use of a table of patterns to transform a text in a reversible way.
_From the [MazeGroup Wiki page](https://mazegroup.org/wiki/index.php/ABP) (in french)._

## Installation

### With PyPi :

Use the command `pip install abp-tools`.

## Usage

### Importation

The code below imports ABP :
```py
from abp import *
```

### Encoding

The function `encode(text: str, patterns: list[list[int]]) -> bytes` takes the string to encode/encrypt and a list of list of numbers (the table of patterns), it returns a bytes string.

### Decoding

The function `decode(ciphertext: bytes, patterns: list[list[int]]) -> str` takes the bytes string and the table of patterns to decode, it returns a string.

### Key to patterns (K2P)

The function `generate_patterns(key: str, num_patterns: int = 100) -> list` takes a string key and a number of patterns to generate, it returns the table of patterns corresponding to the parameters.
