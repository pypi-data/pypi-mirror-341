import typing as ty
from pathlib import Path
import random
import string
import tempfile
import pydicom
import datetime
from .header import get_image_header
from ..base import FILENAME_TEMPLATE


def get_data(
    out_dir: Path = None,
    scan_id=1,
    acquisition_id=1,
    **kwargs,
) -> ty.List[Path]:
    tmp_dir = Path(tempfile.mkdtemp())
    dicom_hdr_fspath = next(get_image_header(tmp_dir, **kwargs).iterdir())
    dcm = pydicom.dcmread(dicom_hdr_fspath)
    date_time = datetime.datetime.strptime(
        dcm.AcquisitionDate + dcm.AcquisitionTime, "%Y%m%d%H%M%S.%f"
    )
    fname = FILENAME_TEMPLATE.format(
        last_name=dcm.PatientName.family_name.replace(" ", "_"),
        first_name=dcm.PatientName.given_name.replace(" ", "_"),
        scan_id=scan_id,
        acquisition_id=acquisition_id,
        date_time=date_time.strftime("%Y.%m.%d.%H.%M.%S.%f"),
        image_type=dcm.ImageType[-1],
        timestamp="".join(random.choices(string.digits, k=8)),
    )
    fspath = out_dir / fname
    with open(fspath, "wb") as f:
        f.write(b"dummy data" + dicom_hdr_fspath.read_bytes() + b"END!" + b"1234567890")
    return [fspath]
