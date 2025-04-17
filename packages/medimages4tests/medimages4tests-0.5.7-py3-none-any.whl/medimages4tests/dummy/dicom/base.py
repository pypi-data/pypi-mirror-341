from pathlib import Path
import shutil
import typing as ty
from copy import copy, deepcopy
import pydicom.dataset
import pydicom.datadict
from medimages4tests.utils import invalid_path_chars_re
from medimages4tests.cache_dir import base_cache_dir

cache_dir = base_cache_dir / "dummy" / "dicom"
dicom_pkg_dir = Path(__file__).parent


def default_dicom_dir(file_loc: str, header_vals: ty.Dict[str, ty.Any]):
    """Gets relative path location of module from base DICOM directory

    Parameters
    ----------
    file_loc : str
        File path to module were the

    Returns
    -------
    Path
        Relative path to module
    """
    if header_vals:
        header_str = "__".join(f"{k}_{v}" for k, v in sorted(header_vals.items()))
        header_str = invalid_path_chars_re.sub("_", header_str)
    else:
        header_str = "_"
    return (cache_dir / Path(file_loc).with_suffix("").relative_to(dicom_pkg_dir) / header_str)


def generate_dicom(
    cache_dir: Path,
    num_vols: int,
    constant_hdr: dict,
    collated_data: dict,
    varying_hdr: dict,
):
    """Generates a dummy DICOM dataset for a test fixture

    Parameters
    ----------
    cache_path : Path
        Path to directory to save the DICOM files relative to the base cache dir
    num_vols : int
        Number of volumes in the set
    constant_hdr : dict[str, Any]
        constant header values
    collated_data : dict[str, int]
        data array lengths
    varying_hdr : dict[str, list], optional
        varying header values across a multi-volume set

    Returns
    -------
    Dicom
        Dicom dataset
    """

    cache_dir = Path(cache_dir)
    # Check for non-empty cache directory, and return it if present
    if cache_dir.exists() and len(
        [p for p in cache_dir.iterdir() if not p.name.startswith(".")]
    ):
        return cache_dir

    cache_dir.mkdir(parents=True, exist_ok=True)

    try:
        for i in range(num_vols):
            i = str(i)
            vol_json = copy(constant_hdr)
            if varying_hdr is not None:
                vol_json.update({k: v[i] for k, v in varying_hdr.items() if i in v})
            # Reconstitute large binary fields with dummy data filled with
            # \3 bytes
            for key, val in collated_data.items():
                if i in val:
                    vol_json[key] = {
                        "vr": val[i]["vr"],
                        "InlineBinary": "X" * val[i]["BinaryLength"],
                    }
            ds = pydicom.dataset.Dataset.from_json(vol_json)
            ds.is_implicit_VR = True
            ds.is_little_endian = True
            if pydicom.__version__.split(".")[0] < "3":
                save_kwargs = {"write_like_original": False}
            else:
                save_kwargs = {"enforce_file_format": True}
            ds.save_as(cache_dir / f"{i}.dcm", **save_kwargs)
    except Exception:
        shutil.rmtree(cache_dir)  # Remove directory from cache on error
        raise
    else:
        return cache_dir


def evolve_header(
    dicom_header: ty.Dict[str, ty.Any],
    first_name: str = None,
    last_name: str = None,
    skip_unknown: bool = False,
    **kwargs,
) -> ty.Dict[str, ty.Any]:
    """Evolves a DICOM header with newly update values

    Parameters
    ----------
    dicom_header : dict[str, any]
        DICOM header extracted from a dataset
    **kwargs
        keyword arguments containing values to update in the header
    """
    hdr = deepcopy(dicom_header)
    [getattr(hdr, a) for a in dir(hdr)]  # Ensure data dict keys are loaded
    if first_name or last_name:
        if not first_name or not last_name:
            try:
                patient_names = hdr["00100010"]["Value"][0].split("^")
            except AttributeError:
                raise ValueError(
                    "Must provide both first and last patient names as could "
                    "not read existing ones from the header"
                )
            if first_name is None:
                first_name = patient_names[0]
            else:
                last_name = patient_names[-1]
        kwargs["PatientName"] = last_name + "^" + first_name
    for key, val in kwargs.items():
        tag_decimal = pydicom.datadict.tag_for_keyword(key)
        if not tag_decimal:
            if skip_unknown:
                continue
            raise ValueError(f"Did not find tag corresponding to keyword {key}")
        hex_tag = format(tag_decimal, "08x").upper()
        tag = hdr[hex_tag]
        try:
            elem = tag["Value"]
        except KeyError:
            continue
        assert isinstance(elem, list) and len(elem) == 1
        nested_elem = elem[0]
        if isinstance(nested_elem, dict) and list(nested_elem.keys()) == ["Alphabetic"]:
            nested_elem["Alphabetic"] = val
        else:
            elem[0] = val
    return hdr
