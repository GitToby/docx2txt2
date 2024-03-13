# docx2txt2

My personal replacement for [docx2txt](https://github.com/ankushshah89/python-docx2txt).

It's intended to be very simple and provide some utilities to match the functionality of the original lib.

## Usage
Install with your fave package manager (anything that pulls from pypi will work. pip, poetry, pdm, etx)

```
pip install docx2txt2
```

Use with any [`PathLike`](https://docs.python.org/3/library/os.html#os.PathLike) object, like a filepath or IO stream.

```python
import io
from pathlib import Path
from docx2txt2 import extract_text

# path
text = extract_text("path/to/my.docx")

# actual Path
docx_path = Path(__file__).parent / "my.docx"
text2 = extract_text(docx_path)

# bytestream
docx_bytes = b"..."
bytes_io = io.BytesIO(docx_bytes)
text3 = extract_text(bytes_io)
```

## Compatability & Motivation

Motivations for rewrite:
- **Speed**, I have lots of word docs to process and I saw some efficiency gains over the original lib.
- **Formatting**, I didn't want to do whitespace removal for every run; this one doesn't.

Compatability &  Caveats
- Doesn't preserve whitespace or styling like the original; new pages, tabs and the like are now just spaces.
- headers and footers contain "PAGE" where there would be a number, unlike the original which removed them

## Benchmarks
Basic benchmarking using [pytest-benchmark](https://pytest-benchmark.readthedocs.io) with a basic test document on my M1 macbook and on GithubActions.
From these tests it appears this lib is ~1.88x faster on average.

```
----------------------------------------------------------------------------------- benchmark: 2 tests ----------------------------------------------------------------------------------
Name (time in ms)               Min               Max              Mean            StdDev            Median               IQR            Outliers       OPS            Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_benchmark_docx2txt2     1.1498 (1.0)      6.2305 (1.0)      1.1949 (1.0)      0.3096 (1.0)      1.1685 (1.0)      0.0142 (1.0)          3;74  836.9124 (1.0)         724           1
test_benchmark_docx2txt      2.1684 (1.89)     7.5298 (1.21)     2.2469 (1.88)     0.3941 (1.27)     2.2044 (1.89)     0.0231 (1.62)         2;41  445.0671 (0.53)        365           1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

Disclaimer: More thorough benchmarking could be conducted. This is a faster lib in general but I haven't tested edge cases.
