import typing as ty
from pathlib import Path
import random
from datetime import datetime
from tempfile import mkdtemp
import string
import pydicom

MAGIC_NUMBER = b"LARGE_PET_LM_RAWDATA"

FILENAME_TEMPLATE = "{last_name}_{first_name}.PT.{acquisition_id}.{scan_id}.{image_type}.{date_time}.2.0.{timestamp}.ptd"

DEFAULT_SCAN_DATE = datetime(2023, 8, 25, 15, 50, 5, 123456)


def generate_raw_data(
    dicom_hdr_fspath: Path,
    out_dir: ty.Optional[Path] = None,
    scan_id: int = 602,
    acquisition_id: str = "PET_U_FDG_SWB_LM_(Adult)",
    date_time: datetime = DEFAULT_SCAN_DATE,
    **kwargs: ty.Any,
) -> ty.List[Path]:
    dcm_hdr_bytes = dicom_hdr_fspath.read_bytes()
    dcm = pydicom.dcmread(dicom_hdr_fspath)
    if out_dir is None:
        out_dir = Path(mkdtemp())
    if not out_dir.exists():
        out_dir.mkdir(parents=True)

    # 4 bytes for the int that holds the length of the header
    header_size = len(dcm_hdr_bytes)
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
    fspath.write_bytes(
        f"dummy data for {fname}\n".encode()
        + dcm_hdr_bytes
        + header_size.to_bytes(4, "little")
        + MAGIC_NUMBER
    )
    return [fspath]
