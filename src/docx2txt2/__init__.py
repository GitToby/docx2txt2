from __future__ import annotations

import itertools
import os
import zipfile
from pathlib import Path
from typing import Any, IO
from xml.etree.ElementTree import XML


def extract_text(docx_path: IO[Any] | os.PathLike[Any] | str) -> str:
    """Read a Word document into a string. Doesn't preserve whitespace.

    Parameters
    ----------
    docx_path : IO[Any] | os.PathLike[Any]
        The path to the Word document .docx file from which the text is to be extracted.

    Returns
    -------
    text : str
        The text from the Word document as a single string.
    """
    text_parts: list[str] = []

    with zipfile.ZipFile(docx_path, mode="r") as zip_:
        # These files where the ones considered in the original docx2txt
        # https://github.com/ankushshah89/python-docx2txt/blob/master/docx2txt/docx2txt.py#L87
        namelist = zip_.namelist()
        header_files = (f for f in namelist if "header" in f)
        footer_files = (f for f in namelist if "footer" in f)

        for file in itertools.chain(
            sorted(header_files), ["word/document.xml"], sorted(footer_files)
        ):
            data = zip_.read(file)
            root = XML(data)
            text_parts.extend(root.itertext())

    # Some parts may end up with multiple spaces; we just brute a replacement to 1 space to keep formatting nice
    # question, should we allow different join patterns in the api?
    multi_space_join = " ".join(text_parts)
    content_ = " ".join(multi_space_join.split())
    for char in (".", ",", "?"):
        content_ = content_.replace(f" {char}", char)
    return content_


def extract_images(
    docx_path: IO[Any] | os.PathLike[Any] | str, img_dir: os.PathLike[Any] | str
):
    """Extract all images from the Word document and save in the directory `img_dir`

    Parameters
    ----------
    docx_path : IO[Any] | os.PathLike[Any]
        The path to the Word document .docx file from which the images are to be extracted.

    img_dir : os.PathLike[Any]
        The path to a directory where the images extracted from the Word document will be written to.

    Returns
    -------
    extracted_paths : list[Path]
        A list of image paths that were extracted from the document.

    Raises
    ------
    OSError
        If the `img_dir` is not a dir or doesn't exist.
    """
    img_dir_path = Path(img_dir)
    if not img_dir_path.is_dir():
        raise OSError(f"{img_dir} is not a directory.")

    extracted_paths: list[Path] = []

    with zipfile.ZipFile(docx_path, mode="r") as zip_:
        filtered_files = (
            _file
            for _file in zip_.filelist
            if _file.filename.endswith(
                (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".avif", ".svg")
            )
        )

        for file in filtered_files:
            # We only want the filename added to our outdir
            out_file_name = Path(file.filename)
            out_path = img_dir_path / out_file_name.parts[-1]

            # Reading the file needs to be done in the zip.
            file_data = zip_.read(file.filename)
            with open(out_path, "wb") as f:
                f.write(file_data)
            extracted_paths.append(out_path)

    return extracted_paths


# Drop in for the original
# https://github.com/ankushshah89/python-docx2txt/blob/master/docx2txt/docx2txt.py#L72
def process(
    docx: IO[Any] | os.PathLike[Any] | str,
    img_dir: os.PathLike[Any] | str | None = None,
) -> str:
    """Read a Word document into a string. Doesn't preserve whitespace. If `img_dir` is specified,
    extract all images from the Word document and save in the directory `img_dir`.

    This function dosent return the list of paths


    Parameters
    ----------
    docx : str
        The path to the Word document from which the text and images are to be extracted.
    img_dir : str | None, default None
        The path to a directory where the images extracted from the Word document will be written to.
        If not specified, no images will be extracted.

    Returns
    -------
    text : str
        The text from the Word document as a single string.

    See Also
    --------
    extract_text : extract text from a Word doc
    extract_images : extract images from a Word doc and retrieve the extracted paths.
    """
    if img_dir:
        extract_images(docx, img_dir)
    return extract_text(docx)
