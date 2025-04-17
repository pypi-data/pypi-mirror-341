import typing as ty
from pathlib import Path
import shutil
import tempfile
from .header import get_image_headers
from ..base import generate_raw_data


def get_data(out_dir: Path = None, **kwargs) -> ty.List[Path]:
    tmp_dir = Path(tempfile.mkdtemp())
    data_tmp_dir = Path(tempfile.mkdtemp())
    raw_data = []
    for i, hdr_dir in enumerate(get_image_headers(tmp_dir, **kwargs)):
        dicom_hdr_fspath = next(hdr_dir.iterdir())
        raw_data_file = generate_raw_data(
            dicom_hdr_fspath=dicom_hdr_fspath,
            out_dir=data_tmp_dir,
        )[0]
        out_path = out_dir / f"{raw_data_file.stem}.{i:03d}{raw_data_file.suffix}"
        shutil.move(
            raw_data_file,
            out_path,
        )
        raw_data.append(out_path)
    shutil.rmtree(tmp_dir)
    shutil.rmtree(data_tmp_dir)
    return raw_data
