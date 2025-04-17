import typing as ty
from pathlib import Path
import tempfile
from .header import get_image_header
from ..base import generate_raw_data


def get_data(out_dir: Path = None, **kwargs: ty.Any) -> ty.List[Path]:
    tmp_dir = Path(tempfile.mkdtemp())
    dicom_hdr_fspath = next(get_image_header(tmp_dir, **kwargs).iterdir())
    return generate_raw_data(
        dicom_hdr_fspath=dicom_hdr_fspath, out_dir=out_dir, **kwargs
    )
