from medimages4tests.dummy.dicom.base import (
    generate_dicom,
    evolve_header,
)


def get_image_header(out_dir, skip_unknown=True, **kwargs):
    hdr = evolve_header(constant_hdr, skip_unknown=skip_unknown, **kwargs)
    return generate_dicom(out_dir, num_vols, hdr, collated_data, {})


num_vols = 1


constant_hdr = {
    "00080005": {"vr": "CS", "Value": ["ISO_IR 100"]},
    "00080008": {"vr": "CS", "Value": ["ORIGINAL", "PRIMARY", "PET_CALIBRATION"]},
    "00080012": {"vr": "DA", "Value": ["20230725"]},
    "00080013": {"vr": "TM", "Value": ["071306.000000"]},
    "00080016": {"vr": "UI", "Value": ["1.3.12.2.1107.5.9.1"]},
    "00080018": {
        "vr": "UI",
        "Value": ["1.3.12.2.1107.5.1.4.10016.30000023072501543220300000001"],
    },
    "00080020": {"vr": "DA", "Value": ["20230725"]},
    "00080021": {"vr": "DA", "Value": ["20230725"]},
    "00080022": {"vr": "DA", "Value": ["20230725"]},
    "00080030": {"vr": "TM", "Value": ["114938.720000"]},
    "00080031": {"vr": "TM", "Value": ["115432.206000"]},
    "00080032": {"vr": "TM", "Value": ["071306.000000"]},
    "00080050": {"vr": "SH"},
    "00080060": {"vr": "CS", "Value": ["PT"]},
    "00080070": {"vr": "LO", "Value": ["SIEMENS"]},
    "00080080": {"vr": "LO", "Value": ["An institute"]},
    "00080081": {"vr": "ST", "Value": ["Address of said institute"]},
    "00080090": {"vr": "PN"},
    "00081010": {"vr": "SH", "Value": ["QUADRA10016"]},
    "00081030": {"vr": "LO", "Value": ["Researcher^Project"]},
    "0008103E": {"vr": "LO", "Value": ["PET Raw Data"]},
    "00081040": {"vr": "LO", "Value": ["PET"]},
    "00081090": {"vr": "LO", "Value": ["Biograph128_Vision Quadra Edge-1232"]},
    "00082111": {"vr": "ST", "Value": ["PETCT"]},
    "00100010": {"vr": "PN", "Value": ["FirstName^LastName"]},
    "00100020": {"vr": "LO", "Value": ["Session Label"]},
    "00100030": {"vr": "DA", "Value": ["19700101"]},
    "00100040": {"vr": "CS", "Value": ["O"]},
    "00101010": {"vr": "AS", "Value": ["053Y"]},
    "00101030": {"vr": "DS", "Value": [1.27]},
    "00181000": {"vr": "LO", "Value": ["10016"]},
    "00181020": {"vr": "LO", "Value": ["VR20B"]},
    "00181030": {"vr": "LO", "Value": ["Onco (Adult)"]},
    "00181200": {"vr": "DA", "Value": ["20230725", "20230611"]},
    "00181201": {"vr": "TM", "Value": ["071306.000000", "134228.000000"]},
    "00185100": {"vr": "CS", "Value": ["HFS"]},
    "0020000D": {
        "vr": "UI",
        "Value": ["1.3.12.2.1107.5.1.4.10016.30000023072501493873200000001"],
    },
    "0020000E": {
        "vr": "UI",
        "Value": ["1.3.12.2.1107.5.1.4.10016.30000023072501543220300000002"],
    },
    "00200010": {"vr": "SH", "Value": ["PROJECT_ID"]},
    "00200011": {"vr": "IS", "Value": [602]},
    "00200012": {"vr": "IS", "Value": [1]},
    "00200013": {"vr": "IS", "Value": [1]},
    "00200052": {
        "vr": "UI",
        "Value": ["1.3.12.2.1107.5.1.4.10016.30000023072501494590400000000"],
    },
    "00204000": {"vr": "LT", "Value": ["PET Normalization"]},
    "00290010": {"vr": "LO", "Value": ["SIEMENS CSA NON-IMAGE"]},
    "00290011": {"vr": "LO", "Value": ["SIEMENS CSA HEADER"]},
    "00290012": {"vr": "LO", "Value": ["SIEMENS MEDCOM HEADER"]},
    "00291008": {"vr": "CS", "Value": ["PET_CALIB_T"]},
    "00291009": {"vr": "LO", "Value": ["1.3"]},
    "00291108": {"vr": "CS", "Value": ["PET_HDR_QC"]},
    "00291109": {"vr": "LO", "Value": ["1.3"]},
    "7FE10010": {"vr": "LO", "Value": ["SIEMENS CSA NON-IMAGE"]},
    "00104000": {"vr": "LT", "Value": ["Patient comments string"]},
    "00081048": {"vr": "PN", "Value": [{"Alphabetic": "Some Phenotype"}]},
}


collated_data = {
    "00291010": {"vr": "OB", "BinaryLength": 3168},
    "00291110": {"vr": "OB", "BinaryLength": 1220},
    "00291220": {"vr": "OB", "BinaryLength": 80},
    "7FE11010": {"vr": "OB", "BinaryLength": 352},
}
