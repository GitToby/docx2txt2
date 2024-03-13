# docx2txt2

[![codecov](https://codecov.io/gh/GitToby/docx2txt2/graph/badge.svg?token=12KF8ARYVZ)](https://codecov.io/gh/GitToby/docx2txt2)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/GitToby/docx2txt2/lint-and-test.yaml)](https://github.com/GitToby/docx2txt2/actions/workflows/lint-and-test.yaml)
[![GitHub file size in bytes](https://img.shields.io/github/size/GitToby/docx2txt2/src%2Fdocx2txt2%2F__init__.py)](https://github.com/GitToby/docx2txt2/blob/master/src/docx2txt2/__init__.py)
[![PyPI - License](https://img.shields.io/pypi/l/docx2txt2)](https://github.com/GitToby/docx2txt2/blob/master/LICENSE.txt)
[![PyPI - Version](https://img.shields.io/pypi/v/docx2txt2)](https://pypi.org/project/docx2txt2/)
[![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FGitToby%2Fdocx2txt2%2Fmaster%2Fpyproject.toml)](https://pypi.org/project/docx2txt2/)

My personal replacement for [docx2txt](https://github.com/ankushshah89/python-docx2txt).

It's intended to be very simple and provide some utilities to match the functionality of the original lib.

Also see:
  - [pptx2txt2](https://github.com/GitToby/pptx2txt2) for docx conversion

## Usage

Install with your fave package manager (anything that pulls from pypi will work. pip, poetry, pdm, etx)

```
pip install docx2txt2
```

Use with any [`PathLike`](https://docs.python.org/3/library/os.html#os.PathLike) object, like a filepath or IO stream.

```python
import io
from pathlib import Path
import docx2txt2

# path
text = docx2txt2.extract_text("path/to/my.docx")
image_paths = docx2txt2.extract_images("path/to/my.docx", "path/to/images/out")

# actual Paths
docx_path = Path(__file__).parent / "my.docx"
image_out = Path(__file__).parent / "my" / "images"
image_out.mkdir(parents=True)

text2 = docx2txt2.extract_text(docx_path)
image_paths2 = docx2txt2.extract_images(docx_path, image_out)

# bytestreams
docx_bytes = b"..."
bytes_io = io.BytesIO(docx_bytes)
text3 = docx2txt2.extract_text(bytes_io)
image_paths3 = docx2txt2.extract_images(bytes_io, "path/to/images/out")
```

## Compatability & Motivation

docx2txt2 provides a superset of all data returned by docx2txt with some caveats (below), so the below is true:

```python
import docx2txt

import docx2txt2

orig_content = docx2txt.process("my/file.docx").split()
new_content = docx2txt2.process("my/file.docx").split()

assert all(orig in new_content for orig in orig_content)
```

_This is a test in `test_extract_data.test_docx2txt_compatability`_

Motivations for rewrite:

- **Speed**, I have lots of word docs to process and I saw some efficiency gains over the original lib.
- **Formatting**, I didn't want to do whitespace removal for every run; this preformats output to only include spaces.

Compatability & Caveats

- Doesn't preserve whitespace or styling like the original; new pages, tabs and the like are now just spaces.
- headers and footers contain "PAGE" where there would be a number, unlike the original which removed them

## Benchmarks

Basic benchmarking using [pytest-benchmark](https://pytest-benchmark.readthedocs.io) with a basic test document on my M1 macbook and on GithubActions.
From these tests it appears this lib is a sneak under ~2x faster on average.

Macbook:

```
----------------------------------------------------------------------------------- benchmark: 2 tests ----------------------------------------------------------------------------------
Name (time in ms)               Min               Max              Mean            StdDev            Median               IQR            Outliers       OPS            Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_benchmark_docx2txt2     1.1498 (1.0)      6.2305 (1.0)      1.1949 (1.0)      0.3096 (1.0)      1.1685 (1.0)      0.0142 (1.0)          3;74  836.9124 (1.0)         724           1
test_benchmark_docx2txt      2.1684 (1.89)     7.5298 (1.21)     2.2469 (1.88)     0.3941 (1.27)     2.2044 (1.89)     0.0231 (1.62)         2;41  445.0671 (0.53)        365           1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

GitHub Actions, python 3.12:

```
----------------------------------------------------------------------------------- benchmark: 2 tests -----------------------------------------------------------------------------------
Name (time in ms)               Min                Max              Mean            StdDev            Median               IQR            Outliers       OPS            Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_benchmark_docx2txt2     1.5368 (1.0)       8.6408 (1.0)      1.6104 (1.0)      0.4961 (1.0)      1.5697 (1.0)      0.0349 (1.0)          3;11  620.9509 (1.0)         565           1
test_benchmark_docx2txt      3.0235 (1.97)     10.1797 (1.18)     3.1365 (1.95)     0.5956 (1.20)     3.0822 (1.96)     0.0356 (1.02)         2;10  318.8220 (0.51)        279           1
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

Disclaimer: More thorough benchmarking could be conducted. This is a faster lib in general but I haven't tested edge cases.
