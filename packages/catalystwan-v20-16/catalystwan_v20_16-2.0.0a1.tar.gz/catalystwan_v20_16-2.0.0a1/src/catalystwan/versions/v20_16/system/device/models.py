# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Literal, Optional

ModelParam = Literal[
    "vEdge-5000",
    "vbond",
    "vedge-100",
    "vedge-100-B",
    "vedge-100-M",
    "vedge-100-WM",
    "vedge-1000",
    "vedge-2000",
    "vedge-ASR-1001-HX",
    "vedge-ASR-1001-X",
    "vedge-ASR-1002-HX",
    "vedge-ASR-1002-X",
    "vedge-ASR-1006-X",
    "vedge-C1100TG-1N24P32A",
    "vedge-C1100TGX-1N24P32A",
    "vedge-C1101-4P",
    "vedge-C1101-4PLTEP",
    "vedge-C1101-4PLTEPW",
    "vedge-C1109-2PLTEGB",
    "vedge-C1109-2PLTEUS",
    "vedge-C1109-2PLTEVZ",
    "vedge-C1109-4PLTE2P",
    "vedge-C1109-4PLTE2PW",
    "vedge-C1111-4P",
    "vedge-C1111-4PLTEEA",
    "vedge-C1111-4PLTELA,vedge-C1116-4P",
    "vedge-C1111-4PW",
    "vedge-C1111-8P",
    "vedge-C1111-8PLTEEA",
    "vedge-C1111-8PLTEEAW",
    "vedge-C1111-8PLTELA",
    "vedge-C1111-8PLTELAW",
    "vedge-C1111-8PW",
    "vedge-C1111X-8P",
    "vedge-C1112-8P",
    "vedge-C1112-8PLTEEA",
    "vedge-C1112-8PLTEEAWE",
    "vedge-C1112-8PWE",
    "vedge-C1113-8P",
    "vedge-C1113-8PLTEEA",
    "vedge-C1113-8PLTEEAW",
    "vedge-C1113-8PLTELA",
    "vedge-C1113-8PLTELAWZ",
    "vedge-C1113-8PLTEW",
    "vedge-C1113-8PM",
    "vedge-C1113-8PMLTEEA",
    "vedge-C1113-8PMWE",
    "vedge-C1113-8PW",
    "vedge-C1116-4PLTEEA",
    "vedge-C1116-4PLTEEAWE",
    "vedge-C1116-4PWE",
    "vedge-C1117-4P",
    "vedge-C1117-4PLTEEA",
    "vedge-C1117-4PLTEEAW",
    "vedge-C1117-4PLTELA",
    "vedge-C1117-4PLTELAWZ",
    "vedge-C1117-4PM",
    "vedge-C1117-4PMLTEEA",
    "vedge-C1117-4PMLTEEAWE",
    "vedge-C1117-4PMWE",
    "vedge-C1117-4PW",
    "vedge-C1118-8P",
    "vedge-C1121-4P",
    "vedge-C1121-4PLTEP",
    "vedge-C1121-8P",
    "vedge-C1121-8PLTEP",
    "vedge-C1121-8PLTEPW",
    "vedge-C1121X-8P",
    "vedge-C1121X-8PLTEP",
    "vedge-C1121X-8PLTEPW",
    "vedge-C1126-8PLTEP",
    "vedge-C1126X-8PLTEP",
    "vedge-C1127-8PLTEP",
    "vedge-C1127-8PMLTEP",
    "vedge-C1127X-8PLTEP",
    "vedge-C1127X-8PMLTEP",
    "vedge-C1128-8PLTEP",
    "vedge-C1131-8PLTEPW",
    "vedge-C1131-8PW",
    "vedge-C1131X-8PLTEPW",
    "vedge-C1131X-8PW",
    "vedge-C1161-8P",
    "vedge-C1161-8PLTEP",
    "vedge-C1161X-8P",
    "vedge-C1161X-8PLTEP",
    "vedge-C8000V",
    "vedge-C8200-1N-4T",
    "vedge-C8200L-1N-4T",
    "vedge-C8300-1N1S-4T2X",
    "vedge-C8300-1N1S-6T",
    "vedge-C8300-2N2S-4T2X",
    "vedge-C8300-2N2S-6T",
    "vedge-C8500-12X",
    "vedge-C8500-12X4QC",
    "vedge-C8500L-8S4X",
    "vedge-CSR-1000v",
    "vedge-ESR-6300",
    "vedge-ESR-6300",
    "vedge-IR-1101",
    "vedge-IR-1101",
    "vedge-IR-1821",
    "vedge-IR-1831",
    "vedge-IR-1833",
    "vedge-IR-1835",
    "vedge-IR-8140H",
    "vedge-IR-8340",
    "vedge-IR8140H-P",
    "vedge-ISR-4221",
    "vedge-ISR-4221",
    "vedge-ISR-4221X",
    "vedge-ISR-4321",
    "vedge-ISR-4321",
    "vedge-ISR-4331",
    "vedge-ISR-4331",
    "vedge-ISR-4351",
    "vedge-ISR-4351",
    "vedge-ISR-4431",
    "vedge-ISR-4451-X",
    "vedge-ISR-4461",
    "vedge-ISR1100-4G",
    "vedge-ISR1100-4GLTE",
    "vedge-ISR1100-6G",
    "vedge-ISR1100X-4G",
    "vedge-ISR1100X-6G",
    "vedge-ISRv",
    "vedge-cloud",
    "vmanage",
    "vsmart",
]

FamilyParam = Literal["aon", "cedge"]

TopologyParam = Literal["hub", "spoke"]


@dataclass
class CertificateStates:
    """
    This is valid Certificate States
    """

    certificate_types: Optional[str] = _field(default=None, metadata={"alias": "certificateTypes"})


@dataclass
class DeviceUuid:
    """
    This is valid DeviceUuid
    """

    device_uuid: Optional[str] = _field(default=None, metadata={"alias": "deviceUuid"})


@dataclass
class DeviceIp:
    """
    This is the valid DeviceIP
    """

    device_ip: Optional[str] = _field(default=None, metadata={"alias": "deviceIp"})


@dataclass
class CertificateValidity:
    """
    This is Certificate Validity
    """

    certificate_validity: Optional[str] = _field(
        default=None, metadata={"alias": "certificateValidity"}
    )


@dataclass
class DeleteDevice:
    status: Optional[str] = _field(default=None)
