import io
import tempfile
from pathlib import Path
import json
from collections import defaultdict
import pydicom.dataset


def read_dicom(fpath: Path):
    """Reads a DICOM file and returns as dictionary stripped from large binary
    fields

    Parameters
    ----------
    path : Path
        File system path to dicom file

    Returns
    -------
    dict[str, Any]
        Dicom fields and their values. Binrary data fields and the length of
        the binary string they hold
    """
    dcm = pydicom.dcmread(str(fpath))
    js = dcm.to_json_dict()
    header = {k: v for k, v in js.items() if not v["vr"].startswith("O")}
    # Replace data byte string with its length, so it can be recreated with
    # dummy data when it is loaded
    data = {
        k: {"vr": v["vr"], "BinaryLength": len(v["InlineBinary"])}
        for k, v in js.items()
        if v["vr"].startswith("O")
    }
    return header, data


def dicom_series_to_gen_code(dpath: Path, image_type: str):
    """Return

    Parameters
    ----------
    dpath : Path
        Path to the directory holding the DICOM files
    image_type : str
        Name of the image type, used to name the generator that derives the
        image

    Returns
    -------
    str
        Python code that generates a version of the imported image with
        dummy data.
    """
    collated_hdr = defaultdict(dict)
    collated_data = defaultdict(dict)
    num_vols = 0
    for i, fpath in enumerate(dpath.iterdir()):
        if fpath.name.startswith("."):
            continue
        header, data = read_dicom(fpath)
        for k, v in header.items():
            collated_hdr[k][i] = v
        for k, v in data.items():
            collated_data[k][i] = v
        num_vols += 1
    constant_hdr = {
        k: v[0]
        for k, v in collated_hdr.items()
        if (len(v) == num_vols and all(v[0] == x for x in v.values()))
    }
    varying_hdr = {k: v for k, v in collated_hdr.items() if k not in constant_hdr}

    constant_hdr.update(ANONYMOUS_TAGS)

    return DICOM_FILE_TEMPLATE.format(
        num_vols=num_vols,
        image_type=image_type,
        constant_hdr=json.dumps(constant_hdr, indent="    "),
        varying_hdr=json.dumps(varying_hdr),
        collated_data=json.dumps(collated_data),
    )


def raw_pet_to_gen_code(fspath: Path, out_dir: Path):
    """Return

    Parameters
    ----------
    dpath : Path
        Path to the directory holding the DICOM files

    Returns
    -------
    str
        Python code that generates a version of the imported image with
        dummy data.
    """
    if not out_dir.exists():
        out_dir.mkdir(parents=True)

    with open(fspath, "rb") as fp:
        dicom_size_offset = -len("LARGE_PET_LM_RAWDATA") - 4
        fp.seek(dicom_size_offset, io.SEEK_END)
        dicom_size = int.from_bytes(fp.read(4), "little")
        fp.seek(dicom_size_offset - dicom_size, io.SEEK_END)
        dcm_hdr = fp.read(dicom_size)
    # dcm_hdr = dcm_hdr.lstrip(b"\x00")
    tmp_path = Path(tempfile.mkdtemp()) / "tmp-dicom.dcm"
    with open(tmp_path, "wb") as fp:
        fp.write(dcm_hdr)
    header, data = read_dicom(tmp_path)
    constant_hdr = {k: v for k, v in header.items()}
    varying_hdr = {}

    constant_hdr.update(ANONYMOUS_TAGS)
    hdr_fspath = out_dir / "header.py"
    hdr_fspath.write_text(
        RAW_PET_FILE_HDR_TEMPLATE.format(
            num_vols=1,
            constant_hdr=json.dumps(constant_hdr, indent="    "),
            varying_hdr=json.dumps(varying_hdr),
            collated_data=json.dumps(data),
        )
    )
    init_fspath = out_dir / "__init__.py"
    init_fspath.write_text(RAW_PET_FILE_INIT_TEMPLATE)
    init_fspath = out_dir / "data.py"
    init_fspath.write_text(RAW_PET_FILE_DATA_TEMPLATE)


DICOM_FILE_TEMPLATE = """from medimages4tests.dummy.dicom.base import (
    generate_dicom, default_dicom_dir, evolve_header
)


def get_image(out_dir=None, **kwargs):
    if out_dir is None:
        out_dir = default_dicom_dir(__file__, kwargs)
    hdr = evolve_header(constant_hdr, **kwargs)
    return generate_dicom(out_dir, num_vols, hdr,
                          collated_data, varying_hdr)


num_vols = {num_vols}


constant_hdr = {constant_hdr}


varying_hdr = {varying_hdr}


collated_data = {collated_data}


"""


RAW_PET_FILE_HDR_TEMPLATE = """from medimages4tests.dummy.dicom.base import (
    generate_dicom, evolve_header
)


def get_image_header(out_dir, skip_unknown=True, **kwargs):
    hdr = evolve_header(constant_hdr, skip_unknown=skip_unknown, **kwargs)
    return generate_dicom(out_dir, num_vols, hdr,
                          collated_data, {{}})


num_vols = {num_vols}


constant_hdr = {constant_hdr}


collated_data = {collated_data}


"""


RAW_PET_FILE_INIT_TEMPLATE = """from .data import get_data

__all__ = ["get_data"]
"""


RAW_PET_FILE_DATA_TEMPLATE = """import typing as ty
from pathlib import Path
import tempfile
from .header import get_image_header
from ..base import generate_raw_data


def get_data(out_dir: Path = None, **kwargs) -> ty.List[Path]:
    tmp_dir = Path(tempfile.mkdtemp())
    dicom_hdr_fspath = next(get_image_header(tmp_dir, **kwargs).iterdir())
    return generate_raw_data(
        dicom_hdr_fspath=dicom_hdr_fspath,
        out_dir=out_dir,
    )


"""

ANONYMOUS_TAGS = {
    "00200010": {"vr": "SH", "Value": ["PROJECT_ID"]},
    "00104000": {"vr": "LT", "Value": ["Patient comments string"]},
    "00100020": {"vr": "LO", "Value": ["Session Label"]},
    "00100010": {"vr": "PN", "Value": ["FirstName^LastName"]},
    "00081048": {"vr": "PN", "Value": [{"Alphabetic": "Some Phenotype"}]},
    "00081030": {"vr": "LO", "Value": ["Researcher^Project"]},
    "00080081": {"vr": "ST", "Value": ["Address of said institute"]},
    "00080080": {"vr": "LO", "Value": ["An institute"]},
}
