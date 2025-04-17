from medimages4tests.dummy.dicom.base import (
    generate_dicom, evolve_header
)


def get_image_header(out_dir, skip_unknown=True, **kwargs):
    hdr = evolve_header(constant_hdr, skip_unknown=skip_unknown, **kwargs)
    return generate_dicom(out_dir, num_vols, hdr,
                          collated_data, {})


num_vols = 1


constant_hdr = {
    "00080005": {
        "vr": "CS",
        "Value": [
            "ISO_IR 100"
        ]
    },
    "00080008": {
        "vr": "CS",
        "Value": [
            "ORIGINAL",
            "PRIMARY",
            "PET_REPLAY_PARAM"
        ]
    },
    "00080012": {
        "vr": "DA",
        "Value": [
            "20240813"
        ]
    },
    "00080013": {
        "vr": "TM",
        "Value": [
            "144718.990000"
        ]
    },
    "00080016": {
        "vr": "UI",
        "Value": [
            "1.3.12.2.1107.5.9.1"
        ]
    },
    "00080018": {
        "vr": "UI",
        "Value": [
            "1.3.12.2.1107.5.1.4.10016.30000024081223082978000000148"
        ]
    },
    "00080020": {
        "vr": "DA",
        "Value": [
            "20240813"
        ]
    },
    "00080021": {
        "vr": "DA",
        "Value": [
            "20240813"
        ]
    },
    "00080022": {
        "vr": "DA",
        "Value": [
            "20240813"
        ]
    },
    "00080030": {
        "vr": "TM",
        "Value": [
            "134340.204000"
        ]
    },
    "00080031": {
        "vr": "TM",
        "Value": [
            "140639.151000"
        ]
    },
    "00080032": {
        "vr": "TM",
        "Value": [
            "144718.990000"
        ]
    },
    "00080050": {
        "vr": "SH",
        "Value": [
            "2408131400"
        ]
    },
    "00080060": {
        "vr": "CS",
        "Value": [
            "PT"
        ]
    },
    "00080070": {
        "vr": "LO",
        "Value": [
            "SIEMENS"
        ]
    },
    "00080080": {
        "vr": "LO",
        "Value": [
            "An institute"
        ]
    },
    "00080081": {
        "vr": "ST",
        "Value": [
            "Address of said institute"
        ]
    },
    "00080090": {
        "vr": "PN"
    },
    "00081010": {
        "vr": "SH",
        "Value": [
            "QUADRA10016"
        ]
    },
    "00081030": {
        "vr": "LO",
        "Value": [
            "Researcher^Project"
        ]
    },
    "0008103E": {
        "vr": "LO",
        "Value": [
            "PET Brain Dynamic Sinograms"
        ]
    },
    "00081040": {
        "vr": "LO",
        "Value": [
            "PET"
        ]
    },
    "00081090": {
        "vr": "LO",
        "Value": [
            "Biograph128_Vision Quadra Edge-1232"
        ]
    },
    "00100010": {
        "vr": "PN",
        "Value": [
            "FirstName^LastName"
        ]
    },
    "00100020": {
        "vr": "LO",
        "Value": [
            "Session Label"
        ]
    },
    "00100030": {
        "vr": "DA",
        "Value": [
            "19500101"
        ]
    },
    "00100040": {
        "vr": "CS",
        "Value": [
            "F"
        ]
    },
    "00101010": {
        "vr": "AS",
        "Value": [
            "074Y"
        ]
    },
    "00101020": {
        "vr": "DS",
        "Value": [
            1.55
        ]
    },
    "00101030": {
        "vr": "DS",
        "Value": [
            45.0
        ]
    },
    "00104000": {
        "vr": "LT",
        "Value": [
            "Patient comments string"
        ]
    },
    "00181000": {
        "vr": "LO",
        "Value": [
            "10016"
        ]
    },
    "00181020": {
        "vr": "LO",
        "Value": [
            "VR20B"
        ]
    },
    "00181030": {
        "vr": "LO",
        "Value": [
            "U_TBPC230007_MANGO_First (Adult)"
        ]
    },
    "00181200": {
        "vr": "DA",
        "Value": [
            "20240813",
            "20240702"
        ]
    },
    "00181201": {
        "vr": "TM",
        "Value": [
            "010000.000000",
            "091429.000000"
        ]
    },
    "00185100": {
        "vr": "CS",
        "Value": [
            "HFS"
        ]
    },
    "0020000D": {
        "vr": "UI",
        "Value": [
            "1.3.12.2.1107.5.1.4.10016.30000024081207361217700000019"
        ]
    },
    "0020000E": {
        "vr": "UI",
        "Value": [
            "1.3.12.2.1107.5.1.4.10016.30000024081223082978000000103"
        ]
    },
    "00200010": {
        "vr": "SH",
        "Value": [
            "PROJECT_ID"
        ]
    },
    "00200011": {
        "vr": "IS",
        "Value": [
            604
        ]
    },
    "00200013": {
        "vr": "IS",
        "Value": [
            1
        ]
    },
    "00200052": {
        "vr": "UI",
        "Value": [
            "1.3.12.2.1107.5.1.4.10016.30000024081207361337100000047"
        ]
    },
    "00204000": {
        "vr": "LT",
        "Value": [
            "Replay parameters"
        ]
    },
    "00290010": {
        "vr": "LO",
        "Value": [
            "SIEMENS CSA NON-IMAGE"
        ]
    },
    "00291008": {
        "vr": "CS",
        "Value": [
            "PET_REPLAY_T"
        ]
    },
    "00291009": {
        "vr": "LO",
        "Value": [
            "1.3"
        ]
    },
    "00324000": {
        "vr": "LT",
        "Value": [
            "001_Pres_Dyna"
        ]
    },
    "7FE10010": {
        "vr": "LO",
        "Value": [
            "SIEMENS CSA NON-IMAGE"
        ]
    },
    "00081048": {
        "vr": "PN",
        "Value": [
            {
                "Alphabetic": "Some Phenotype"
            }
        ]
    }
}


collated_data = {"00291010": {"vr": "OB", "BinaryLength": 28552}, "7FE11010": {"vr": "OB", "BinaryLength": 352}}


