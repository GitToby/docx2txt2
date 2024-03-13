import glob
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from docx2txt import docx2txt  # type: ignore

import docx2txt2

RESOURCES_DIR = Path(__file__).parent / "resources"


@pytest.fixture
def docx_path():
    return RESOURCES_DIR / "example_1.docx"


def test_example_1_extract_text(docx_path):
    text = docx2txt2.extract_text(docx_path)

    assert text

    # Starts with header/s
    assert text.startswith("Hello Header. Page PAGE")

    # ends with footer/s
    assert text.endswith("This is the bottom of the document. footer page: PAGE")

    # check each part of the middle exists in the page

    # 1 main title
    assert "Hello There!" in text

    # 2 main para parts
    assert (
        "I'm a Word doc with some content. I have bold bits, italic bits, and bits of both."
        in text
    )
    assert "There are maybe two or three fonts and even an extra colour or two." in text
    assert "Some docs, like this one even have emojis ☺️." in text
    assert "Remember that links are a thing too. And tables" in text

    # 3 Table
    assert "A Table as well with bold italic colour ⁉️ fonts" in text

    # 4 image desc
    assert "There is even an image." in text


def test_example_1_extract_images(docx_path):
    with TemporaryDirectory() as tempdir:
        images = docx2txt2.extract_images(docx_path, tempdir)

        assert len(images) == 1
        assert tempdir in str(images[0])


def test_example_1_extract_images_bad_dir(docx_path):
    with pytest.raises(OSError):
        docx2txt2.extract_images(docx_path, "/non/existent/dir")


def test_docx2txt_compatability(docx_path):
    with TemporaryDirectory() as tempdir1:
        docx2txt2_res = docx2txt2.process(docx_path, tempdir1)
        glob_str_1 = str(Path(tempdir1) / "*")
        assert len(glob.glob(glob_str_1)) == 1

    with TemporaryDirectory() as tempdir2:
        docx2txt_res = docx2txt.process(docx_path, tempdir2)
        glob_str_2 = str(Path(tempdir2) / "*")
        assert len(glob.glob(glob_str_2)) == 1

    # general case
    orig_content = docx2txt_res.split()
    new_content = docx2txt2_res.split()
    assert all(orig in new_content for orig in orig_content)

    # We maintain PAGE in header and footer blocks
    docx2txt2_res = docx2txt2_res.replace("PAGE", "")
    # We also place img indicators into the docs where applicable
    docx2txt2_res = docx2txt2_res.replace("1362075 180975", "")
    # remove extra whitespace for tests
    docx2txt2_res = " ".join(docx2txt2_res.split())

    # remove extra whitespace in original. as we don't maintain that compatability
    docx2txt_res = " ".join(docx2txt_res.split())

    assert docx2txt2_res == docx2txt_res


def test_benchmark_docx2txt(benchmark, docx_path):
    res = benchmark(docx2txt.process, docx_path)
    assert res


def test_benchmark_docx2txt2(benchmark, docx_path):
    res = benchmark(docx2txt2.process, docx_path)
    assert res
