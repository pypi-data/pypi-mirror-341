# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DefaultActionTypeDef = Literal["drop", "pass"]

SequencesBaseActionDef = Literal["drop", "inspect", "pass"]

VariableOptionTypeDef = Literal["variable"]

Value = Literal[
    "ABW",
    "AF",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AN",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
    "AS",
    "ASM",
    "ATA",
    "ATF",
    "ATG",
    "AUS",
    "AUT",
    "AZE",
    "BDI",
    "BEL",
    "BEN",
    "BES",
    "BFA",
    "BGD",
    "BGR",
    "BHR",
    "BHS",
    "BIH",
    "BLM",
    "BLR",
    "BLZ",
    "BMU",
    "BOL",
    "BRA",
    "BRB",
    "BRN",
    "BTN",
    "BVT",
    "BWA",
    "CAF",
    "CAN",
    "CCK",
    "CHE",
    "CHL",
    "CHN",
    "CIV",
    "CMR",
    "COD",
    "COG",
    "COK",
    "COL",
    "COM",
    "CPV",
    "CRI",
    "CUB",
    "CUW",
    "CXR",
    "CYM",
    "CYP",
    "CZE",
    "DEU",
    "DJI",
    "DMA",
    "DNK",
    "DOM",
    "DZA",
    "ECU",
    "EGY",
    "ERI",
    "ESH",
    "ESP",
    "EST",
    "ETH",
    "EU",
    "FIN",
    "FJI",
    "FLK",
    "FRA",
    "FRO",
    "FSM",
    "GAB",
    "GBR",
    "GEO",
    "GGY",
    "GHA",
    "GIB",
    "GIN",
    "GLP",
    "GMB",
    "GNB",
    "GNQ",
    "GRC",
    "GRD",
    "GRL",
    "GTM",
    "GUF",
    "GUM",
    "GUY",
    "HKG",
    "HMD",
    "HND",
    "HRV",
    "HTI",
    "HUN",
    "IDN",
    "IMN",
    "IND",
    "IOT",
    "IRL",
    "IRN",
    "IRQ",
    "ISL",
    "ISR",
    "ITA",
    "JAM",
    "JEY",
    "JOR",
    "JPN",
    "KAZ",
    "KEN",
    "KGZ",
    "KHM",
    "KIR",
    "KNA",
    "KOR",
    "KWT",
    "LAO",
    "LBN",
    "LBR",
    "LBY",
    "LCA",
    "LIE",
    "LKA",
    "LSO",
    "LTU",
    "LUX",
    "LVA",
    "MAC",
    "MAF",
    "MAR",
    "MCO",
    "MDA",
    "MDG",
    "MDV",
    "MEX",
    "MHL",
    "MKD",
    "MLI",
    "MLT",
    "MMR",
    "MNE",
    "MNG",
    "MNP",
    "MOZ",
    "MRT",
    "MSR",
    "MTQ",
    "MUS",
    "MWI",
    "MYS",
    "MYT",
    "NA",
    "NAM",
    "NCL",
    "NER",
    "NFK",
    "NGA",
    "NIC",
    "NIU",
    "NLD",
    "NOR",
    "NPL",
    "NRU",
    "NZL",
    "OC",
    "OMN",
    "PAK",
    "PAN",
    "PCN",
    "PER",
    "PHL",
    "PLW",
    "PNG",
    "POL",
    "PRI",
    "PRK",
    "PRT",
    "PRY",
    "PSE",
    "PYF",
    "QAT",
    "REU",
    "ROU",
    "RUS",
    "RWA",
    "SA",
    "SAU",
    "SDN",
    "SEN",
    "SGP",
    "SGS",
    "SHN",
    "SJM",
    "SLB",
    "SLE",
    "SLV",
    "SMR",
    "SOM",
    "SPM",
    "SRB",
    "SSD",
    "STP",
    "SUR",
    "SVK",
    "SVN",
    "SWE",
    "SWZ",
    "SXM",
    "SYC",
    "SYR",
    "TCA",
    "TCD",
    "TGO",
    "THA",
    "TJK",
    "TKL",
    "TKM",
    "TLS",
    "TON",
    "TTO",
    "TUN",
    "TUR",
    "TUV",
    "TWN",
    "TZA",
    "UGA",
    "UKR",
    "UMI",
    "URY",
    "USA",
    "UZB",
    "VAT",
    "VCT",
    "VEN",
    "VGB",
    "VIR",
    "VNM",
    "VUT",
    "WLF",
    "WSM",
    "YEM",
    "ZAF",
    "ZMB",
    "ZWE",
]

NgfirewallValue = Literal[
    "802-11-iapp",
    "ace-svr",
    "aol",
    "appleqtc",
    "bgp",
    "biff",
    "bootpc",
    "bootps",
    "cddbp",
    "cifs",
    "cisco-fna",
    "cisco-net-mgmt",
    "cisco-svcs",
    "cisco-sys",
    "cisco-tdp",
    "cisco-tna",
    "citrix",
    "citriximaclient",
    "clp",
    "creativepartnr",
    "creativeserver",
    "cuseeme",
    "daytime",
    "dbase",
    "dbcontrol_agent",
    "ddns-v3",
    "dhcp-failover",
    "discard",
    "dns",
    "dnsix",
    "echo",
    "entrust-svc-hand",
    "entrust-svcs",
    "exec",
    "fcip-port",
    "finger",
    "ftp",
    "ftps",
    "gdoi",
    "giop",
    "gopher",
    "gtpv0",
    "gtpv1",
    "h225ras",
    "h323",
    "h323callsigalt",
    "hp-alarm-mgr",
    "hp-collector",
    "hp-managed-node",
    "hsrp",
    "http",
    "https",
    "ica",
    "icabrowser",
    "icmp",
    "ident",
    "igmpv3lite",
    "imap",
    "imap3",
    "imaps",
    "ipass",
    "ipsec-msft",
    "ipx",
    "irc",
    "irc-serv",
    "ircs",
    "ircu",
    "isakmp",
    "iscsi",
    "iscsi-target",
    "kazaa",
    "kerberos",
    "kermit",
    "l2tp",
    "ldap",
    "ldap-admin",
    "ldaps",
    "login",
    "lotusmtap",
    "lotusnote",
    "mgcp",
    "microsoft-ds",
    "ms-cluster-net",
    "ms-dotnetster",
    "ms-sna",
    "ms-sql",
    "ms-sql-m",
    "msexch-routing",
    "msnmsgr",
    "msrpc",
    "mysql",
    "n2h2server",
    "ncp",
    "net8-cman",
    "netbios-dgm",
    "netbios-ns",
    "netshow",
    "netstat",
    "nfs",
    "nntp",
    "ntp",
    "oem-agent",
    "oracle",
    "oracle-em-vp",
    "oraclenames",
    "orasrv",
    "pcanywheredata",
    "pcanywherestat",
    "pop3",
    "pop3s",
    "pptp",
    "pwdgen",
    "qmtp",
    "r-winsock",
    "radius",
    "rdb-dbs-disp",
    "realmedia",
    "realsecure",
    "router",
    "rsvd",
    "rsvp-encap",
    "rsvp_tunnel",
    "rtc-pm-port",
    "rtelnet",
    "rtsp",
    "send",
    "shell",
    "sip",
    "sip-tls",
    "skinny",
    "sms",
    "smtp",
    "snmp",
    "snmptrap",
    "socks",
    "sql-net",
    "sqlserv",
    "sqlsrv",
    "ssh",
    "sshell",
    "ssp",
    "streamworks",
    "stun",
    "sunrpc",
    "syslog",
    "syslog-conn",
    "tacacs",
    "tacacs-ds",
    "tarantella",
    "tcp",
    "telnet",
    "telnets",
    "tftp",
    "time",
    "timed",
    "tr-rsrb",
    "ttc",
    "udp",
    "uucp",
    "vdolive",
    "vqp",
    "webster",
    "who",
    "wins",
    "x11",
    "xdmcp",
    "ymsgr",
]

SequencesActionsTypeDef = Literal["connectionEvents", "log"]

NgfirewallDefaultActionTypeDef = Literal["drop", "pass"]

NgfirewallSequencesBaseActionDef = Literal["drop", "inspect", "pass"]

UnifiedNgfirewallValue = Literal[
    "ABW",
    "AF",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AN",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
    "AS",
    "ASM",
    "ATA",
    "ATF",
    "ATG",
    "AUS",
    "AUT",
    "AZE",
    "BDI",
    "BEL",
    "BEN",
    "BES",
    "BFA",
    "BGD",
    "BGR",
    "BHR",
    "BHS",
    "BIH",
    "BLM",
    "BLR",
    "BLZ",
    "BMU",
    "BOL",
    "BRA",
    "BRB",
    "BRN",
    "BTN",
    "BVT",
    "BWA",
    "CAF",
    "CAN",
    "CCK",
    "CHE",
    "CHL",
    "CHN",
    "CIV",
    "CMR",
    "COD",
    "COG",
    "COK",
    "COL",
    "COM",
    "CPV",
    "CRI",
    "CUB",
    "CUW",
    "CXR",
    "CYM",
    "CYP",
    "CZE",
    "DEU",
    "DJI",
    "DMA",
    "DNK",
    "DOM",
    "DZA",
    "ECU",
    "EGY",
    "ERI",
    "ESH",
    "ESP",
    "EST",
    "ETH",
    "EU",
    "FIN",
    "FJI",
    "FLK",
    "FRA",
    "FRO",
    "FSM",
    "GAB",
    "GBR",
    "GEO",
    "GGY",
    "GHA",
    "GIB",
    "GIN",
    "GLP",
    "GMB",
    "GNB",
    "GNQ",
    "GRC",
    "GRD",
    "GRL",
    "GTM",
    "GUF",
    "GUM",
    "GUY",
    "HKG",
    "HMD",
    "HND",
    "HRV",
    "HTI",
    "HUN",
    "IDN",
    "IMN",
    "IND",
    "IOT",
    "IRL",
    "IRN",
    "IRQ",
    "ISL",
    "ISR",
    "ITA",
    "JAM",
    "JEY",
    "JOR",
    "JPN",
    "KAZ",
    "KEN",
    "KGZ",
    "KHM",
    "KIR",
    "KNA",
    "KOR",
    "KWT",
    "LAO",
    "LBN",
    "LBR",
    "LBY",
    "LCA",
    "LIE",
    "LKA",
    "LSO",
    "LTU",
    "LUX",
    "LVA",
    "MAC",
    "MAF",
    "MAR",
    "MCO",
    "MDA",
    "MDG",
    "MDV",
    "MEX",
    "MHL",
    "MKD",
    "MLI",
    "MLT",
    "MMR",
    "MNE",
    "MNG",
    "MNP",
    "MOZ",
    "MRT",
    "MSR",
    "MTQ",
    "MUS",
    "MWI",
    "MYS",
    "MYT",
    "NA",
    "NAM",
    "NCL",
    "NER",
    "NFK",
    "NGA",
    "NIC",
    "NIU",
    "NLD",
    "NOR",
    "NPL",
    "NRU",
    "NZL",
    "OC",
    "OMN",
    "PAK",
    "PAN",
    "PCN",
    "PER",
    "PHL",
    "PLW",
    "PNG",
    "POL",
    "PRI",
    "PRK",
    "PRT",
    "PRY",
    "PSE",
    "PYF",
    "QAT",
    "REU",
    "ROU",
    "RUS",
    "RWA",
    "SA",
    "SAU",
    "SDN",
    "SEN",
    "SGP",
    "SGS",
    "SHN",
    "SJM",
    "SLB",
    "SLE",
    "SLV",
    "SMR",
    "SOM",
    "SPM",
    "SRB",
    "SSD",
    "STP",
    "SUR",
    "SVK",
    "SVN",
    "SWE",
    "SWZ",
    "SXM",
    "SYC",
    "SYR",
    "TCA",
    "TCD",
    "TGO",
    "THA",
    "TJK",
    "TKL",
    "TKM",
    "TLS",
    "TON",
    "TTO",
    "TUN",
    "TUR",
    "TUV",
    "TWN",
    "TZA",
    "UGA",
    "UKR",
    "UMI",
    "URY",
    "USA",
    "UZB",
    "VAT",
    "VCT",
    "VEN",
    "VGB",
    "VIR",
    "VNM",
    "VUT",
    "WLF",
    "WSM",
    "YEM",
    "ZAF",
    "ZMB",
    "ZWE",
]

EmbeddedSecurityUnifiedNgfirewallValue = Literal[
    "ABW",
    "AF",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AN",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
    "AS",
    "ASM",
    "ATA",
    "ATF",
    "ATG",
    "AUS",
    "AUT",
    "AZE",
    "BDI",
    "BEL",
    "BEN",
    "BES",
    "BFA",
    "BGD",
    "BGR",
    "BHR",
    "BHS",
    "BIH",
    "BLM",
    "BLR",
    "BLZ",
    "BMU",
    "BOL",
    "BRA",
    "BRB",
    "BRN",
    "BTN",
    "BVT",
    "BWA",
    "CAF",
    "CAN",
    "CCK",
    "CHE",
    "CHL",
    "CHN",
    "CIV",
    "CMR",
    "COD",
    "COG",
    "COK",
    "COL",
    "COM",
    "CPV",
    "CRI",
    "CUB",
    "CUW",
    "CXR",
    "CYM",
    "CYP",
    "CZE",
    "DEU",
    "DJI",
    "DMA",
    "DNK",
    "DOM",
    "DZA",
    "ECU",
    "EGY",
    "ERI",
    "ESH",
    "ESP",
    "EST",
    "ETH",
    "EU",
    "FIN",
    "FJI",
    "FLK",
    "FRA",
    "FRO",
    "FSM",
    "GAB",
    "GBR",
    "GEO",
    "GGY",
    "GHA",
    "GIB",
    "GIN",
    "GLP",
    "GMB",
    "GNB",
    "GNQ",
    "GRC",
    "GRD",
    "GRL",
    "GTM",
    "GUF",
    "GUM",
    "GUY",
    "HKG",
    "HMD",
    "HND",
    "HRV",
    "HTI",
    "HUN",
    "IDN",
    "IMN",
    "IND",
    "IOT",
    "IRL",
    "IRN",
    "IRQ",
    "ISL",
    "ISR",
    "ITA",
    "JAM",
    "JEY",
    "JOR",
    "JPN",
    "KAZ",
    "KEN",
    "KGZ",
    "KHM",
    "KIR",
    "KNA",
    "KOR",
    "KWT",
    "LAO",
    "LBN",
    "LBR",
    "LBY",
    "LCA",
    "LIE",
    "LKA",
    "LSO",
    "LTU",
    "LUX",
    "LVA",
    "MAC",
    "MAF",
    "MAR",
    "MCO",
    "MDA",
    "MDG",
    "MDV",
    "MEX",
    "MHL",
    "MKD",
    "MLI",
    "MLT",
    "MMR",
    "MNE",
    "MNG",
    "MNP",
    "MOZ",
    "MRT",
    "MSR",
    "MTQ",
    "MUS",
    "MWI",
    "MYS",
    "MYT",
    "NA",
    "NAM",
    "NCL",
    "NER",
    "NFK",
    "NGA",
    "NIC",
    "NIU",
    "NLD",
    "NOR",
    "NPL",
    "NRU",
    "NZL",
    "OC",
    "OMN",
    "PAK",
    "PAN",
    "PCN",
    "PER",
    "PHL",
    "PLW",
    "PNG",
    "POL",
    "PRI",
    "PRK",
    "PRT",
    "PRY",
    "PSE",
    "PYF",
    "QAT",
    "REU",
    "ROU",
    "RUS",
    "RWA",
    "SA",
    "SAU",
    "SDN",
    "SEN",
    "SGP",
    "SGS",
    "SHN",
    "SJM",
    "SLB",
    "SLE",
    "SLV",
    "SMR",
    "SOM",
    "SPM",
    "SRB",
    "SSD",
    "STP",
    "SUR",
    "SVK",
    "SVN",
    "SWE",
    "SWZ",
    "SXM",
    "SYC",
    "SYR",
    "TCA",
    "TCD",
    "TGO",
    "THA",
    "TJK",
    "TKL",
    "TKM",
    "TLS",
    "TON",
    "TTO",
    "TUN",
    "TUR",
    "TUV",
    "TWN",
    "TZA",
    "UGA",
    "UKR",
    "UMI",
    "URY",
    "USA",
    "UZB",
    "VAT",
    "VCT",
    "VEN",
    "VGB",
    "VIR",
    "VNM",
    "VUT",
    "WLF",
    "WSM",
    "YEM",
    "ZAF",
    "ZMB",
    "ZWE",
]

SdwanEmbeddedSecurityUnifiedNgfirewallValue = Literal[
    "802-11-iapp",
    "ace-svr",
    "aol",
    "appleqtc",
    "bgp",
    "biff",
    "bootpc",
    "bootps",
    "cddbp",
    "cifs",
    "cisco-fna",
    "cisco-net-mgmt",
    "cisco-svcs",
    "cisco-sys",
    "cisco-tdp",
    "cisco-tna",
    "citrix",
    "citriximaclient",
    "clp",
    "creativepartnr",
    "creativeserver",
    "cuseeme",
    "daytime",
    "dbase",
    "dbcontrol_agent",
    "ddns-v3",
    "dhcp-failover",
    "discard",
    "dns",
    "dnsix",
    "echo",
    "entrust-svc-hand",
    "entrust-svcs",
    "exec",
    "fcip-port",
    "finger",
    "ftp",
    "ftps",
    "gdoi",
    "giop",
    "gopher",
    "gtpv0",
    "gtpv1",
    "h225ras",
    "h323",
    "h323callsigalt",
    "hp-alarm-mgr",
    "hp-collector",
    "hp-managed-node",
    "hsrp",
    "http",
    "https",
    "ica",
    "icabrowser",
    "icmp",
    "ident",
    "igmpv3lite",
    "imap",
    "imap3",
    "imaps",
    "ipass",
    "ipsec-msft",
    "ipx",
    "irc",
    "irc-serv",
    "ircs",
    "ircu",
    "isakmp",
    "iscsi",
    "iscsi-target",
    "kazaa",
    "kerberos",
    "kermit",
    "l2tp",
    "ldap",
    "ldap-admin",
    "ldaps",
    "login",
    "lotusmtap",
    "lotusnote",
    "mgcp",
    "microsoft-ds",
    "ms-cluster-net",
    "ms-dotnetster",
    "ms-sna",
    "ms-sql",
    "ms-sql-m",
    "msexch-routing",
    "msnmsgr",
    "msrpc",
    "mysql",
    "n2h2server",
    "ncp",
    "net8-cman",
    "netbios-dgm",
    "netbios-ns",
    "netshow",
    "netstat",
    "nfs",
    "nntp",
    "ntp",
    "oem-agent",
    "oracle",
    "oracle-em-vp",
    "oraclenames",
    "orasrv",
    "pcanywheredata",
    "pcanywherestat",
    "pop3",
    "pop3s",
    "pptp",
    "pwdgen",
    "qmtp",
    "r-winsock",
    "radius",
    "rdb-dbs-disp",
    "realmedia",
    "realsecure",
    "router",
    "rsvd",
    "rsvp-encap",
    "rsvp_tunnel",
    "rtc-pm-port",
    "rtelnet",
    "rtsp",
    "send",
    "shell",
    "sip",
    "sip-tls",
    "skinny",
    "sms",
    "smtp",
    "snmp",
    "snmptrap",
    "socks",
    "sql-net",
    "sqlserv",
    "sqlsrv",
    "ssh",
    "sshell",
    "ssp",
    "streamworks",
    "stun",
    "sunrpc",
    "syslog",
    "syslog-conn",
    "tacacs",
    "tacacs-ds",
    "tarantella",
    "tcp",
    "telnet",
    "telnets",
    "tftp",
    "time",
    "timed",
    "tr-rsrb",
    "ttc",
    "udp",
    "uucp",
    "vdolive",
    "vqp",
    "webster",
    "who",
    "wins",
    "x11",
    "xdmcp",
    "ymsgr",
]

NgfirewallSequencesActionsTypeDef = Literal["connectionEvents", "log"]

UnifiedNgfirewallDefaultActionTypeDef = Literal["drop", "pass"]

UnifiedNgfirewallSequencesBaseActionDef = Literal["drop", "inspect", "pass"]

FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallValue = Literal[
    "ABW",
    "AF",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AN",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
    "AS",
    "ASM",
    "ATA",
    "ATF",
    "ATG",
    "AUS",
    "AUT",
    "AZE",
    "BDI",
    "BEL",
    "BEN",
    "BES",
    "BFA",
    "BGD",
    "BGR",
    "BHR",
    "BHS",
    "BIH",
    "BLM",
    "BLR",
    "BLZ",
    "BMU",
    "BOL",
    "BRA",
    "BRB",
    "BRN",
    "BTN",
    "BVT",
    "BWA",
    "CAF",
    "CAN",
    "CCK",
    "CHE",
    "CHL",
    "CHN",
    "CIV",
    "CMR",
    "COD",
    "COG",
    "COK",
    "COL",
    "COM",
    "CPV",
    "CRI",
    "CUB",
    "CUW",
    "CXR",
    "CYM",
    "CYP",
    "CZE",
    "DEU",
    "DJI",
    "DMA",
    "DNK",
    "DOM",
    "DZA",
    "ECU",
    "EGY",
    "ERI",
    "ESH",
    "ESP",
    "EST",
    "ETH",
    "EU",
    "FIN",
    "FJI",
    "FLK",
    "FRA",
    "FRO",
    "FSM",
    "GAB",
    "GBR",
    "GEO",
    "GGY",
    "GHA",
    "GIB",
    "GIN",
    "GLP",
    "GMB",
    "GNB",
    "GNQ",
    "GRC",
    "GRD",
    "GRL",
    "GTM",
    "GUF",
    "GUM",
    "GUY",
    "HKG",
    "HMD",
    "HND",
    "HRV",
    "HTI",
    "HUN",
    "IDN",
    "IMN",
    "IND",
    "IOT",
    "IRL",
    "IRN",
    "IRQ",
    "ISL",
    "ISR",
    "ITA",
    "JAM",
    "JEY",
    "JOR",
    "JPN",
    "KAZ",
    "KEN",
    "KGZ",
    "KHM",
    "KIR",
    "KNA",
    "KOR",
    "KWT",
    "LAO",
    "LBN",
    "LBR",
    "LBY",
    "LCA",
    "LIE",
    "LKA",
    "LSO",
    "LTU",
    "LUX",
    "LVA",
    "MAC",
    "MAF",
    "MAR",
    "MCO",
    "MDA",
    "MDG",
    "MDV",
    "MEX",
    "MHL",
    "MKD",
    "MLI",
    "MLT",
    "MMR",
    "MNE",
    "MNG",
    "MNP",
    "MOZ",
    "MRT",
    "MSR",
    "MTQ",
    "MUS",
    "MWI",
    "MYS",
    "MYT",
    "NA",
    "NAM",
    "NCL",
    "NER",
    "NFK",
    "NGA",
    "NIC",
    "NIU",
    "NLD",
    "NOR",
    "NPL",
    "NRU",
    "NZL",
    "OC",
    "OMN",
    "PAK",
    "PAN",
    "PCN",
    "PER",
    "PHL",
    "PLW",
    "PNG",
    "POL",
    "PRI",
    "PRK",
    "PRT",
    "PRY",
    "PSE",
    "PYF",
    "QAT",
    "REU",
    "ROU",
    "RUS",
    "RWA",
    "SA",
    "SAU",
    "SDN",
    "SEN",
    "SGP",
    "SGS",
    "SHN",
    "SJM",
    "SLB",
    "SLE",
    "SLV",
    "SMR",
    "SOM",
    "SPM",
    "SRB",
    "SSD",
    "STP",
    "SUR",
    "SVK",
    "SVN",
    "SWE",
    "SWZ",
    "SXM",
    "SYC",
    "SYR",
    "TCA",
    "TCD",
    "TGO",
    "THA",
    "TJK",
    "TKL",
    "TKM",
    "TLS",
    "TON",
    "TTO",
    "TUN",
    "TUR",
    "TUV",
    "TWN",
    "TZA",
    "UGA",
    "UKR",
    "UMI",
    "URY",
    "USA",
    "UZB",
    "VAT",
    "VCT",
    "VEN",
    "VGB",
    "VIR",
    "VNM",
    "VUT",
    "WLF",
    "WSM",
    "YEM",
    "ZAF",
    "ZMB",
    "ZWE",
]

V1FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallValue = Literal[
    "ABW",
    "AF",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AN",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
    "AS",
    "ASM",
    "ATA",
    "ATF",
    "ATG",
    "AUS",
    "AUT",
    "AZE",
    "BDI",
    "BEL",
    "BEN",
    "BES",
    "BFA",
    "BGD",
    "BGR",
    "BHR",
    "BHS",
    "BIH",
    "BLM",
    "BLR",
    "BLZ",
    "BMU",
    "BOL",
    "BRA",
    "BRB",
    "BRN",
    "BTN",
    "BVT",
    "BWA",
    "CAF",
    "CAN",
    "CCK",
    "CHE",
    "CHL",
    "CHN",
    "CIV",
    "CMR",
    "COD",
    "COG",
    "COK",
    "COL",
    "COM",
    "CPV",
    "CRI",
    "CUB",
    "CUW",
    "CXR",
    "CYM",
    "CYP",
    "CZE",
    "DEU",
    "DJI",
    "DMA",
    "DNK",
    "DOM",
    "DZA",
    "ECU",
    "EGY",
    "ERI",
    "ESH",
    "ESP",
    "EST",
    "ETH",
    "EU",
    "FIN",
    "FJI",
    "FLK",
    "FRA",
    "FRO",
    "FSM",
    "GAB",
    "GBR",
    "GEO",
    "GGY",
    "GHA",
    "GIB",
    "GIN",
    "GLP",
    "GMB",
    "GNB",
    "GNQ",
    "GRC",
    "GRD",
    "GRL",
    "GTM",
    "GUF",
    "GUM",
    "GUY",
    "HKG",
    "HMD",
    "HND",
    "HRV",
    "HTI",
    "HUN",
    "IDN",
    "IMN",
    "IND",
    "IOT",
    "IRL",
    "IRN",
    "IRQ",
    "ISL",
    "ISR",
    "ITA",
    "JAM",
    "JEY",
    "JOR",
    "JPN",
    "KAZ",
    "KEN",
    "KGZ",
    "KHM",
    "KIR",
    "KNA",
    "KOR",
    "KWT",
    "LAO",
    "LBN",
    "LBR",
    "LBY",
    "LCA",
    "LIE",
    "LKA",
    "LSO",
    "LTU",
    "LUX",
    "LVA",
    "MAC",
    "MAF",
    "MAR",
    "MCO",
    "MDA",
    "MDG",
    "MDV",
    "MEX",
    "MHL",
    "MKD",
    "MLI",
    "MLT",
    "MMR",
    "MNE",
    "MNG",
    "MNP",
    "MOZ",
    "MRT",
    "MSR",
    "MTQ",
    "MUS",
    "MWI",
    "MYS",
    "MYT",
    "NA",
    "NAM",
    "NCL",
    "NER",
    "NFK",
    "NGA",
    "NIC",
    "NIU",
    "NLD",
    "NOR",
    "NPL",
    "NRU",
    "NZL",
    "OC",
    "OMN",
    "PAK",
    "PAN",
    "PCN",
    "PER",
    "PHL",
    "PLW",
    "PNG",
    "POL",
    "PRI",
    "PRK",
    "PRT",
    "PRY",
    "PSE",
    "PYF",
    "QAT",
    "REU",
    "ROU",
    "RUS",
    "RWA",
    "SA",
    "SAU",
    "SDN",
    "SEN",
    "SGP",
    "SGS",
    "SHN",
    "SJM",
    "SLB",
    "SLE",
    "SLV",
    "SMR",
    "SOM",
    "SPM",
    "SRB",
    "SSD",
    "STP",
    "SUR",
    "SVK",
    "SVN",
    "SWE",
    "SWZ",
    "SXM",
    "SYC",
    "SYR",
    "TCA",
    "TCD",
    "TGO",
    "THA",
    "TJK",
    "TKL",
    "TKM",
    "TLS",
    "TON",
    "TTO",
    "TUN",
    "TUR",
    "TUV",
    "TWN",
    "TZA",
    "UGA",
    "UKR",
    "UMI",
    "URY",
    "USA",
    "UZB",
    "VAT",
    "VCT",
    "VEN",
    "VGB",
    "VIR",
    "VNM",
    "VUT",
    "WLF",
    "WSM",
    "YEM",
    "ZAF",
    "ZMB",
    "ZWE",
]

Value1 = Literal[
    "802-11-iapp",
    "ace-svr",
    "aol",
    "appleqtc",
    "bgp",
    "biff",
    "bootpc",
    "bootps",
    "cddbp",
    "cifs",
    "cisco-fna",
    "cisco-net-mgmt",
    "cisco-svcs",
    "cisco-sys",
    "cisco-tdp",
    "cisco-tna",
    "citrix",
    "citriximaclient",
    "clp",
    "creativepartnr",
    "creativeserver",
    "cuseeme",
    "daytime",
    "dbase",
    "dbcontrol_agent",
    "ddns-v3",
    "dhcp-failover",
    "discard",
    "dns",
    "dnsix",
    "echo",
    "entrust-svc-hand",
    "entrust-svcs",
    "exec",
    "fcip-port",
    "finger",
    "ftp",
    "ftps",
    "gdoi",
    "giop",
    "gopher",
    "gtpv0",
    "gtpv1",
    "h225ras",
    "h323",
    "h323callsigalt",
    "hp-alarm-mgr",
    "hp-collector",
    "hp-managed-node",
    "hsrp",
    "http",
    "https",
    "ica",
    "icabrowser",
    "icmp",
    "ident",
    "igmpv3lite",
    "imap",
    "imap3",
    "imaps",
    "ipass",
    "ipsec-msft",
    "ipx",
    "irc",
    "irc-serv",
    "ircs",
    "ircu",
    "isakmp",
    "iscsi",
    "iscsi-target",
    "kazaa",
    "kerberos",
    "kermit",
    "l2tp",
    "ldap",
    "ldap-admin",
    "ldaps",
    "login",
    "lotusmtap",
    "lotusnote",
    "mgcp",
    "microsoft-ds",
    "ms-cluster-net",
    "ms-dotnetster",
    "ms-sna",
    "ms-sql",
    "ms-sql-m",
    "msexch-routing",
    "msnmsgr",
    "msrpc",
    "mysql",
    "n2h2server",
    "ncp",
    "net8-cman",
    "netbios-dgm",
    "netbios-ns",
    "netshow",
    "netstat",
    "nfs",
    "nntp",
    "ntp",
    "oem-agent",
    "oracle",
    "oracle-em-vp",
    "oraclenames",
    "orasrv",
    "pcanywheredata",
    "pcanywherestat",
    "pop3",
    "pop3s",
    "pptp",
    "pwdgen",
    "qmtp",
    "r-winsock",
    "radius",
    "rdb-dbs-disp",
    "realmedia",
    "realsecure",
    "router",
    "rsvd",
    "rsvp-encap",
    "rsvp_tunnel",
    "rtc-pm-port",
    "rtelnet",
    "rtsp",
    "send",
    "shell",
    "sip",
    "sip-tls",
    "skinny",
    "sms",
    "smtp",
    "snmp",
    "snmptrap",
    "socks",
    "sql-net",
    "sqlserv",
    "sqlsrv",
    "ssh",
    "sshell",
    "ssp",
    "streamworks",
    "stun",
    "sunrpc",
    "syslog",
    "syslog-conn",
    "tacacs",
    "tacacs-ds",
    "tarantella",
    "tcp",
    "telnet",
    "telnets",
    "tftp",
    "time",
    "timed",
    "tr-rsrb",
    "ttc",
    "udp",
    "uucp",
    "vdolive",
    "vqp",
    "webster",
    "who",
    "wins",
    "x11",
    "xdmcp",
    "ymsgr",
]

UnifiedNgfirewallSequencesActionsTypeDef = Literal["connectionEvents", "log"]


@dataclass
class OneOfDefaultActionTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultActionTypeDef


@dataclass
class OneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SequencesBaseActionDef


@dataclass
class OneOfSequencesSequenceTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefIdArrayValue:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef:
    ref_id: RefIdArrayValue = _field(metadata={"alias": "refId"})


@dataclass
class Ipv4InputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class Ipv4InputDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Ipv4MatchDef:
    ipv4_value: Union[Ipv4InputDef1, Ipv4InputDef2] = _field(metadata={"alias": "ipv4Value"})


@dataclass
class FqdnInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class FqdnInputDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class FqdnMatchDef:
    fqdn_value: Union[FqdnInputDef1, FqdnInputDef2] = _field(metadata={"alias": "fqdnValue"})


@dataclass
class SourcePortInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]


@dataclass
class SourcePortInputDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourcePortMatchDef:
    port_value: Union[SourcePortInputDef1, SourcePortInputDef2] = _field(
        metadata={"alias": "portValue"}
    )


@dataclass
class AppMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class DestinationPortInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]
    app: Optional[AppMatchDef] = _field(default=None)


@dataclass
class DestinationPortInputDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class DestinationPortMatchDef:
    port_value: Union[DestinationPortInputDef1, DestinationPortInputDef2] = _field(
        metadata={"alias": "portValue"}
    )


@dataclass
class GeoLocationMatchDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Value]  # pytype: disable=annotation-type-mismatch


@dataclass
class GeoLocationMatchDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class IdentityUserMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class IdentityUsergroupMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ProtocolMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]
    app: Optional[AppMatchDef] = _field(default=None)


@dataclass
class ProtocolNameMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[NgfirewallValue]  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries:
    app: Optional[AppMatchDef] = _field(default=None)
    app_family: Optional[AppMatchDef] = _field(default=None, metadata={"alias": "appFamily"})
    app_list: Optional[ListDef] = _field(default=None, metadata={"alias": "appList"})
    app_list_flat: Optional[ListDef] = _field(default=None, metadata={"alias": "appListFlat"})
    destination_data_prefix_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "destinationDataPrefixList"}
    )
    destination_fqdn: Optional[FqdnMatchDef] = _field(
        default=None, metadata={"alias": "destinationFqdn"}
    )
    destination_fqdn_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "destinationFqdnList"}
    )
    destination_geo_location: Optional[Union[GeoLocationMatchDef1, GeoLocationMatchDef2]] = _field(
        default=None, metadata={"alias": "destinationGeoLocation"}
    )
    destination_geo_location_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "destinationGeoLocationList"}
    )
    destination_ip: Optional[Ipv4MatchDef] = _field(
        default=None, metadata={"alias": "destinationIp"}
    )
    destination_port: Optional[DestinationPortMatchDef] = _field(
        default=None, metadata={"alias": "destinationPort"}
    )
    destination_port_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "destinationPortList"}
    )
    destination_scalable_group_tag_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "destinationScalableGroupTagList"}
    )
    destination_security_group: Optional[ListDef] = _field(
        default=None, metadata={"alias": "destinationSecurityGroup"}
    )
    protocol: Optional[ProtocolMatchDef] = _field(default=None)
    protocol_name: Optional[ProtocolNameMatchDef] = _field(
        default=None, metadata={"alias": "protocolName"}
    )
    protocol_name_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "protocolNameList"}
    )
    rule_set_list: Optional[ListDef] = _field(default=None, metadata={"alias": "ruleSetList"})
    source_data_prefix_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "sourceDataPrefixList"}
    )
    source_geo_location: Optional[Union[GeoLocationMatchDef1, GeoLocationMatchDef2]] = _field(
        default=None, metadata={"alias": "sourceGeoLocation"}
    )
    source_geo_location_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "sourceGeoLocationList"}
    )
    source_identity_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "sourceIdentityList"}
    )
    source_identity_user: Optional[IdentityUserMatchDef] = _field(
        default=None, metadata={"alias": "sourceIdentityUser"}
    )
    source_identity_usergroup: Optional[IdentityUsergroupMatchDef] = _field(
        default=None, metadata={"alias": "sourceIdentityUsergroup"}
    )
    source_ip: Optional[Ipv4MatchDef] = _field(default=None, metadata={"alias": "sourceIp"})
    source_port: Optional[SourcePortMatchDef] = _field(
        default=None, metadata={"alias": "sourcePort"}
    )
    source_port_list: Optional[ListDef] = _field(default=None, metadata={"alias": "sourcePortList"})
    source_scalable_group_tag_list: Optional[ListDef] = _field(
        default=None, metadata={"alias": "sourceScalableGroupTagList"}
    )
    source_security_group: Optional[ListDef] = _field(
        default=None, metadata={"alias": "sourceSecurityGroup"}
    )


@dataclass
class Match:
    entries: List[Entries]


@dataclass
class OneOfSequencesActionsTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SequencesActionsTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSequencesActionsParameterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Actions1:
    parameter: OneOfSequencesActionsParameterOptionsDef
    type_: OneOfSequencesActionsTypeOptionsDef = _field(metadata={"alias": "type"})


@dataclass
class Type:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefId:
    option_type: str = _field(metadata={"alias": "optionType"})
    value: str


@dataclass
class Parameter:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class Actions2:
    parameter: Parameter
    type_: Type = _field(metadata={"alias": "type"})


@dataclass
class OneOfdisableSequenceDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Sequences:
    # can be empty array or with type or parameter
    actions: List[Union[Actions1, Actions2]]
    base_action: OneOfSequencesBaseActionOptionsDef = _field(metadata={"alias": "baseAction"})
    match_: Match = _field(metadata={"alias": "match"})
    sequence_id: OneOfSequencesSequenceIdOptionsDef = _field(metadata={"alias": "sequenceId"})
    sequence_name: OneOfSequencesSequenceNameOptionsDef = _field(metadata={"alias": "sequenceName"})
    sequence_type: OneOfSequencesSequenceTypeOptionsDef = _field(metadata={"alias": "sequenceType"})
    disable_sequence: Optional[OneOfdisableSequenceDef] = _field(
        default=None, metadata={"alias": "disableSequence"}
    )


@dataclass
class NgfirewallData:
    default_action_type: OneOfDefaultActionTypeOptionsDef = _field(
        metadata={"alias": "defaultActionType"}
    )
    sequences: List[Sequences]


@dataclass
class Payload:
    """
    ngfirewall profile feature schema for POST request
    """

    data: NgfirewallData
    description: str
    name: str
    contains_tls: Optional[bool] = _field(default=False, metadata={"alias": "containsTls"})
    contains_utd: Optional[bool] = _field(default=False, metadata={"alias": "containsUtd"})
    metadata: Optional[Any] = _field(default=None)
    optimized: Optional[bool] = _field(default=True)


@dataclass
class Data:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # ngfirewall profile feature schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanEmbeddedSecurityUnifiedNgfirewallPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdwanNgfirewallFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedNgfirewallData:
    default_action_type: OneOfDefaultActionTypeOptionsDef = _field(
        metadata={"alias": "defaultActionType"}
    )
    sequences: List[Sequences]


@dataclass
class CreateSdwanNgfirewallFeaturePostRequest:
    """
    ngfirewall profile feature schema for POST request
    """

    data: UnifiedNgfirewallData
    description: str
    name: str
    contains_tls: Optional[bool] = _field(default=False, metadata={"alias": "containsTls"})
    contains_utd: Optional[bool] = _field(default=False, metadata={"alias": "containsUtd"})
    metadata: Optional[Any] = _field(default=None)
    optimized: Optional[bool] = _field(default=True)


@dataclass
class NgfirewallOneOfDefaultActionTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NgfirewallDefaultActionTypeDef


@dataclass
class NgfirewallOneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NgfirewallOneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NgfirewallOneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NgfirewallSequencesBaseActionDef


@dataclass
class NgfirewallOneOfSequencesSequenceTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NgfirewallRefIdArrayValue:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class NgfirewallListDef:
    ref_id: NgfirewallRefIdArrayValue = _field(metadata={"alias": "refId"})


@dataclass
class UnifiedNgfirewallRefIdArrayValue:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class UnifiedNgfirewallListDef:
    ref_id: UnifiedNgfirewallRefIdArrayValue = _field(metadata={"alias": "refId"})


@dataclass
class EmbeddedSecurityUnifiedNgfirewallRefIdArrayValue:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class EmbeddedSecurityUnifiedNgfirewallListDef:
    ref_id: EmbeddedSecurityUnifiedNgfirewallRefIdArrayValue = _field(metadata={"alias": "refId"})


@dataclass
class SdwanEmbeddedSecurityUnifiedNgfirewallRefIdArrayValue:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class SdwanEmbeddedSecurityUnifiedNgfirewallListDef:
    ref_id: SdwanEmbeddedSecurityUnifiedNgfirewallRefIdArrayValue = _field(
        metadata={"alias": "refId"}
    )


@dataclass
class FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallRefIdArrayValue:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallListDef:
    ref_id: FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallRefIdArrayValue = _field(
        metadata={"alias": "refId"}
    )


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallRefIdArrayValue:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallListDef:
    ref_id: V1FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallRefIdArrayValue = _field(
        metadata={"alias": "refId"}
    )


@dataclass
class RefIdArrayValue1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef1:
    ref_id: RefIdArrayValue1 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef2:
    ref_id: RefIdArrayValue2 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef3:
    ref_id: RefIdArrayValue3 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef4:
    ref_id: RefIdArrayValue4 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef5:
    ref_id: RefIdArrayValue5 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef6:
    ref_id: RefIdArrayValue6 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef7:
    ref_id: RefIdArrayValue7 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef8:
    ref_id: RefIdArrayValue8 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue9:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef9:
    ref_id: RefIdArrayValue9 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue10:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef10:
    ref_id: RefIdArrayValue10 = _field(metadata={"alias": "refId"})


@dataclass
class NgfirewallIpv4MatchDef:
    ipv4_value: Union[Ipv4InputDef1, Ipv4InputDef2] = _field(metadata={"alias": "ipv4Value"})


@dataclass
class UnifiedNgfirewallIpv4MatchDef:
    ipv4_value: Union[Ipv4InputDef1, Ipv4InputDef2] = _field(metadata={"alias": "ipv4Value"})


@dataclass
class NgfirewallFqdnInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class NgfirewallFqdnMatchDef:
    fqdn_value: Union[NgfirewallFqdnInputDef1, FqdnInputDef2] = _field(
        metadata={"alias": "fqdnValue"}
    )


@dataclass
class NgfirewallSourcePortInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]


@dataclass
class NgfirewallSourcePortMatchDef:
    port_value: Union[NgfirewallSourcePortInputDef1, SourcePortInputDef2] = _field(
        metadata={"alias": "portValue"}
    )


@dataclass
class NgfirewallAppMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class NgfirewallDestinationPortInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]
    app: Optional[NgfirewallAppMatchDef] = _field(default=None)


@dataclass
class NgfirewallDestinationPortMatchDef:
    port_value: Union[NgfirewallDestinationPortInputDef1, DestinationPortInputDef2] = _field(
        metadata={"alias": "portValue"}
    )


@dataclass
class NgfirewallGeoLocationMatchDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[UnifiedNgfirewallValue]  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedNgfirewallGeoLocationMatchDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[EmbeddedSecurityUnifiedNgfirewallValue]  # pytype: disable=annotation-type-mismatch


@dataclass
class NgfirewallIdentityUserMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class NgfirewallIdentityUsergroupMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class UnifiedNgfirewallAppMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class EmbeddedSecurityUnifiedNgfirewallAppMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class SdwanEmbeddedSecurityUnifiedNgfirewallAppMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class NgfirewallProtocolMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]
    app: Optional[SdwanEmbeddedSecurityUnifiedNgfirewallAppMatchDef] = _field(default=None)


@dataclass
class NgfirewallProtocolNameMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[
        SdwanEmbeddedSecurityUnifiedNgfirewallValue
    ]  # pytype: disable=annotation-type-mismatch


@dataclass
class NgfirewallEntries:
    app: Optional[UnifiedNgfirewallAppMatchDef] = _field(default=None)
    app_family: Optional[EmbeddedSecurityUnifiedNgfirewallAppMatchDef] = _field(
        default=None, metadata={"alias": "appFamily"}
    )
    app_list: Optional[ListDef6] = _field(default=None, metadata={"alias": "appList"})
    app_list_flat: Optional[ListDef7] = _field(default=None, metadata={"alias": "appListFlat"})
    destination_data_prefix_list: Optional[UnifiedNgfirewallListDef] = _field(
        default=None, metadata={"alias": "destinationDataPrefixList"}
    )
    destination_fqdn: Optional[NgfirewallFqdnMatchDef] = _field(
        default=None, metadata={"alias": "destinationFqdn"}
    )
    destination_fqdn_list: Optional[EmbeddedSecurityUnifiedNgfirewallListDef] = _field(
        default=None, metadata={"alias": "destinationFqdnList"}
    )
    destination_geo_location: Optional[
        Union[UnifiedNgfirewallGeoLocationMatchDef1, GeoLocationMatchDef2]
    ] = _field(default=None, metadata={"alias": "destinationGeoLocation"})
    destination_geo_location_list: Optional[
        FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallListDef
    ] = _field(default=None, metadata={"alias": "destinationGeoLocationList"})
    destination_ip: Optional[UnifiedNgfirewallIpv4MatchDef] = _field(
        default=None, metadata={"alias": "destinationIp"}
    )
    destination_port: Optional[NgfirewallDestinationPortMatchDef] = _field(
        default=None, metadata={"alias": "destinationPort"}
    )
    destination_port_list: Optional[ListDef1] = _field(
        default=None, metadata={"alias": "destinationPortList"}
    )
    destination_scalable_group_tag_list: Optional[ListDef3] = _field(
        default=None, metadata={"alias": "destinationScalableGroupTagList"}
    )
    destination_security_group: Optional[ListDef10] = _field(
        default=None, metadata={"alias": "destinationSecurityGroup"}
    )
    protocol: Optional[NgfirewallProtocolMatchDef] = _field(default=None)
    protocol_name: Optional[NgfirewallProtocolNameMatchDef] = _field(
        default=None, metadata={"alias": "protocolName"}
    )
    protocol_name_list: Optional[ListDef5] = _field(
        default=None, metadata={"alias": "protocolNameList"}
    )
    rule_set_list: Optional[ListDef8] = _field(default=None, metadata={"alias": "ruleSetList"})
    source_data_prefix_list: Optional[NgfirewallListDef] = _field(
        default=None, metadata={"alias": "sourceDataPrefixList"}
    )
    source_geo_location: Optional[Union[NgfirewallGeoLocationMatchDef1, GeoLocationMatchDef2]] = (
        _field(default=None, metadata={"alias": "sourceGeoLocation"})
    )
    source_geo_location_list: Optional[SdwanEmbeddedSecurityUnifiedNgfirewallListDef] = _field(
        default=None, metadata={"alias": "sourceGeoLocationList"}
    )
    source_identity_list: Optional[ListDef4] = _field(
        default=None, metadata={"alias": "sourceIdentityList"}
    )
    source_identity_user: Optional[NgfirewallIdentityUserMatchDef] = _field(
        default=None, metadata={"alias": "sourceIdentityUser"}
    )
    source_identity_usergroup: Optional[NgfirewallIdentityUsergroupMatchDef] = _field(
        default=None, metadata={"alias": "sourceIdentityUsergroup"}
    )
    source_ip: Optional[NgfirewallIpv4MatchDef] = _field(
        default=None, metadata={"alias": "sourceIp"}
    )
    source_port: Optional[NgfirewallSourcePortMatchDef] = _field(
        default=None, metadata={"alias": "sourcePort"}
    )
    source_port_list: Optional[V1FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallListDef] = (
        _field(default=None, metadata={"alias": "sourcePortList"})
    )
    source_scalable_group_tag_list: Optional[ListDef2] = _field(
        default=None, metadata={"alias": "sourceScalableGroupTagList"}
    )
    source_security_group: Optional[ListDef9] = _field(
        default=None, metadata={"alias": "sourceSecurityGroup"}
    )


@dataclass
class NgfirewallMatch:
    entries: List[NgfirewallEntries]


@dataclass
class NgfirewallOneOfSequencesActionsTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NgfirewallSequencesActionsTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class NgfirewallOneOfSequencesActionsParameterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NgfirewallActions1:
    parameter: NgfirewallOneOfSequencesActionsParameterOptionsDef
    type_: NgfirewallOneOfSequencesActionsTypeOptionsDef = _field(metadata={"alias": "type"})


@dataclass
class NgfirewallSequences:
    # can be empty array or with type or parameter
    actions: List[Union[NgfirewallActions1, Actions2]]
    base_action: NgfirewallOneOfSequencesBaseActionOptionsDef = _field(
        metadata={"alias": "baseAction"}
    )
    match_: NgfirewallMatch = _field(metadata={"alias": "match"})
    sequence_id: NgfirewallOneOfSequencesSequenceIdOptionsDef = _field(
        metadata={"alias": "sequenceId"}
    )
    sequence_name: NgfirewallOneOfSequencesSequenceNameOptionsDef = _field(
        metadata={"alias": "sequenceName"}
    )
    sequence_type: NgfirewallOneOfSequencesSequenceTypeOptionsDef = _field(
        metadata={"alias": "sequenceType"}
    )
    disable_sequence: Optional[OneOfdisableSequenceDef] = _field(
        default=None, metadata={"alias": "disableSequence"}
    )


@dataclass
class EmbeddedSecurityUnifiedNgfirewallData:
    default_action_type: NgfirewallOneOfDefaultActionTypeOptionsDef = _field(
        metadata={"alias": "defaultActionType"}
    )
    sequences: List[NgfirewallSequences]


@dataclass
class NgfirewallPayload:
    """
    ngfirewall profile feature schema for PUT request
    """

    data: EmbeddedSecurityUnifiedNgfirewallData
    description: str
    name: str
    contains_tls: Optional[bool] = _field(default=False, metadata={"alias": "containsTls"})
    contains_utd: Optional[bool] = _field(default=False, metadata={"alias": "containsUtd"})
    metadata: Optional[Any] = _field(default=None)
    optimized: Optional[bool] = _field(default=True)


@dataclass
class GetSingleSdwanEmbeddedSecurityUnifiedNgfirewallPayload:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # ngfirewall profile feature schema for PUT request
    payload: Optional[NgfirewallPayload] = _field(default=None)


@dataclass
class EditSdwanNgfirewallFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedNgfirewallOneOfDefaultActionTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedNgfirewallDefaultActionTypeDef


@dataclass
class UnifiedNgfirewallOneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedNgfirewallOneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedNgfirewallOneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedNgfirewallSequencesBaseActionDef


@dataclass
class UnifiedNgfirewallOneOfSequencesSequenceTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RefIdArrayValue11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef11:
    ref_id: RefIdArrayValue11 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef12:
    ref_id: RefIdArrayValue12 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef13:
    ref_id: RefIdArrayValue13 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue14:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef14:
    ref_id: RefIdArrayValue14 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue15:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef15:
    ref_id: RefIdArrayValue15 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue16:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef16:
    ref_id: RefIdArrayValue16 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue17:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef17:
    ref_id: RefIdArrayValue17 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue18:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef18:
    ref_id: RefIdArrayValue18 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue19:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef19:
    ref_id: RefIdArrayValue19 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue20:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef20:
    ref_id: RefIdArrayValue20 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue21:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef21:
    ref_id: RefIdArrayValue21 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue22:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef22:
    ref_id: RefIdArrayValue22 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue23:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef23:
    ref_id: RefIdArrayValue23 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue24:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef24:
    ref_id: RefIdArrayValue24 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue25:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef25:
    ref_id: RefIdArrayValue25 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdArrayValue26:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class ListDef26:
    ref_id: RefIdArrayValue26 = _field(metadata={"alias": "refId"})


@dataclass
class EmbeddedSecurityUnifiedNgfirewallIpv4MatchDef:
    ipv4_value: Union[Ipv4InputDef1, Ipv4InputDef2] = _field(metadata={"alias": "ipv4Value"})


@dataclass
class SdwanEmbeddedSecurityUnifiedNgfirewallIpv4MatchDef:
    ipv4_value: Union[Ipv4InputDef1, Ipv4InputDef2] = _field(metadata={"alias": "ipv4Value"})


@dataclass
class UnifiedNgfirewallFqdnInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class UnifiedNgfirewallFqdnMatchDef:
    fqdn_value: Union[UnifiedNgfirewallFqdnInputDef1, FqdnInputDef2] = _field(
        metadata={"alias": "fqdnValue"}
    )


@dataclass
class UnifiedNgfirewallSourcePortInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]


@dataclass
class UnifiedNgfirewallSourcePortMatchDef:
    port_value: Union[UnifiedNgfirewallSourcePortInputDef1, SourcePortInputDef2] = _field(
        metadata={"alias": "portValue"}
    )


@dataclass
class FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallAppMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class UnifiedNgfirewallDestinationPortInputDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[str, str]]
    app: Optional[FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallAppMatchDef] = _field(
        default=None
    )


@dataclass
class UnifiedNgfirewallDestinationPortMatchDef:
    port_value: Union[UnifiedNgfirewallDestinationPortInputDef1, DestinationPortInputDef2] = _field(
        metadata={"alias": "portValue"}
    )


@dataclass
class EmbeddedSecurityUnifiedNgfirewallGeoLocationMatchDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[
        FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallValue
    ]  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanEmbeddedSecurityUnifiedNgfirewallGeoLocationMatchDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[
        V1FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallValue
    ]  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedNgfirewallIdentityUserMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class UnifiedNgfirewallIdentityUsergroupMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class V1FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallAppMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class AppMatchDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class AppMatchDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class UnifiedNgfirewallProtocolMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]
    app: Optional[AppMatchDef2] = _field(default=None)


@dataclass
class UnifiedNgfirewallProtocolNameMatchDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Value1]  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedNgfirewallEntries:
    app: Optional[V1FeatureProfileSdwanEmbeddedSecurityUnifiedNgfirewallAppMatchDef] = _field(
        default=None
    )
    app_family: Optional[AppMatchDef1] = _field(default=None, metadata={"alias": "appFamily"})
    app_list: Optional[ListDef22] = _field(default=None, metadata={"alias": "appList"})
    app_list_flat: Optional[ListDef23] = _field(default=None, metadata={"alias": "appListFlat"})
    destination_data_prefix_list: Optional[ListDef12] = _field(
        default=None, metadata={"alias": "destinationDataPrefixList"}
    )
    destination_fqdn: Optional[UnifiedNgfirewallFqdnMatchDef] = _field(
        default=None, metadata={"alias": "destinationFqdn"}
    )
    destination_fqdn_list: Optional[ListDef13] = _field(
        default=None, metadata={"alias": "destinationFqdnList"}
    )
    destination_geo_location: Optional[
        Union[SdwanEmbeddedSecurityUnifiedNgfirewallGeoLocationMatchDef1, GeoLocationMatchDef2]
    ] = _field(default=None, metadata={"alias": "destinationGeoLocation"})
    destination_geo_location_list: Optional[ListDef15] = _field(
        default=None, metadata={"alias": "destinationGeoLocationList"}
    )
    destination_ip: Optional[SdwanEmbeddedSecurityUnifiedNgfirewallIpv4MatchDef] = _field(
        default=None, metadata={"alias": "destinationIp"}
    )
    destination_port: Optional[UnifiedNgfirewallDestinationPortMatchDef] = _field(
        default=None, metadata={"alias": "destinationPort"}
    )
    destination_port_list: Optional[ListDef17] = _field(
        default=None, metadata={"alias": "destinationPortList"}
    )
    destination_scalable_group_tag_list: Optional[ListDef19] = _field(
        default=None, metadata={"alias": "destinationScalableGroupTagList"}
    )
    destination_security_group: Optional[ListDef26] = _field(
        default=None, metadata={"alias": "destinationSecurityGroup"}
    )
    protocol: Optional[UnifiedNgfirewallProtocolMatchDef] = _field(default=None)
    protocol_name: Optional[UnifiedNgfirewallProtocolNameMatchDef] = _field(
        default=None, metadata={"alias": "protocolName"}
    )
    protocol_name_list: Optional[ListDef21] = _field(
        default=None, metadata={"alias": "protocolNameList"}
    )
    rule_set_list: Optional[ListDef24] = _field(default=None, metadata={"alias": "ruleSetList"})
    source_data_prefix_list: Optional[ListDef11] = _field(
        default=None, metadata={"alias": "sourceDataPrefixList"}
    )
    source_geo_location: Optional[
        Union[EmbeddedSecurityUnifiedNgfirewallGeoLocationMatchDef1, GeoLocationMatchDef2]
    ] = _field(default=None, metadata={"alias": "sourceGeoLocation"})
    source_geo_location_list: Optional[ListDef14] = _field(
        default=None, metadata={"alias": "sourceGeoLocationList"}
    )
    source_identity_list: Optional[ListDef20] = _field(
        default=None, metadata={"alias": "sourceIdentityList"}
    )
    source_identity_user: Optional[UnifiedNgfirewallIdentityUserMatchDef] = _field(
        default=None, metadata={"alias": "sourceIdentityUser"}
    )
    source_identity_usergroup: Optional[UnifiedNgfirewallIdentityUsergroupMatchDef] = _field(
        default=None, metadata={"alias": "sourceIdentityUsergroup"}
    )
    source_ip: Optional[EmbeddedSecurityUnifiedNgfirewallIpv4MatchDef] = _field(
        default=None, metadata={"alias": "sourceIp"}
    )
    source_port: Optional[UnifiedNgfirewallSourcePortMatchDef] = _field(
        default=None, metadata={"alias": "sourcePort"}
    )
    source_port_list: Optional[ListDef16] = _field(
        default=None, metadata={"alias": "sourcePortList"}
    )
    source_scalable_group_tag_list: Optional[ListDef18] = _field(
        default=None, metadata={"alias": "sourceScalableGroupTagList"}
    )
    source_security_group: Optional[ListDef25] = _field(
        default=None, metadata={"alias": "sourceSecurityGroup"}
    )


@dataclass
class UnifiedNgfirewallMatch:
    entries: List[UnifiedNgfirewallEntries]


@dataclass
class UnifiedNgfirewallOneOfSequencesActionsTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedNgfirewallSequencesActionsTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedNgfirewallOneOfSequencesActionsParameterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedNgfirewallActions1:
    parameter: UnifiedNgfirewallOneOfSequencesActionsParameterOptionsDef
    type_: UnifiedNgfirewallOneOfSequencesActionsTypeOptionsDef = _field(metadata={"alias": "type"})


@dataclass
class UnifiedNgfirewallSequences:
    # can be empty array or with type or parameter
    actions: List[Union[UnifiedNgfirewallActions1, Actions2]]
    base_action: UnifiedNgfirewallOneOfSequencesBaseActionOptionsDef = _field(
        metadata={"alias": "baseAction"}
    )
    match_: UnifiedNgfirewallMatch = _field(metadata={"alias": "match"})
    sequence_id: UnifiedNgfirewallOneOfSequencesSequenceIdOptionsDef = _field(
        metadata={"alias": "sequenceId"}
    )
    sequence_name: UnifiedNgfirewallOneOfSequencesSequenceNameOptionsDef = _field(
        metadata={"alias": "sequenceName"}
    )
    sequence_type: UnifiedNgfirewallOneOfSequencesSequenceTypeOptionsDef = _field(
        metadata={"alias": "sequenceType"}
    )
    disable_sequence: Optional[OneOfdisableSequenceDef] = _field(
        default=None, metadata={"alias": "disableSequence"}
    )


@dataclass
class SdwanEmbeddedSecurityUnifiedNgfirewallData:
    default_action_type: UnifiedNgfirewallOneOfDefaultActionTypeOptionsDef = _field(
        metadata={"alias": "defaultActionType"}
    )
    sequences: List[UnifiedNgfirewallSequences]


@dataclass
class EditSdwanNgfirewallFeaturePutRequest:
    """
    ngfirewall profile feature schema for PUT request
    """

    data: SdwanEmbeddedSecurityUnifiedNgfirewallData
    description: str
    name: str
    contains_tls: Optional[bool] = _field(default=False, metadata={"alias": "containsTls"})
    contains_utd: Optional[bool] = _field(default=False, metadata={"alias": "containsUtd"})
    metadata: Optional[Any] = _field(default=None)
    optimized: Optional[bool] = _field(default=True)
