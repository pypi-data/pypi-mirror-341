# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

Type = Literal["urlallowed", "urlblocked"]

EntriesProtocolNameDef = Literal[
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

EntriesCountryDef = Literal[
    "ABW",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
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

EntriesContinentDef = Literal["AF", "AN", "AS", "EU", "NA", "OC", "SA"]

EntriesCriteriaDef = Literal[
    "jitter",
    "jitter-latency",
    "jitter-latency-loss",
    "jitter-loss",
    "jitter-loss-latency",
    "latency",
    "latency-jitter",
    "latency-jitter-loss",
    "latency-loss",
    "latency-loss-jitter",
    "loss",
    "loss-jitter",
    "loss-jitter-latency",
    "loss-latency",
    "loss-latency-jitter",
]

EntriesQueueDef = Literal["0", "1", "2", "3", "4", "5", "6", "7"]

DefaultOptionTypeDef = Literal["default"]

EntriesExceedDef = Literal["drop", "remark"]

EntriesMapColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesEncapDef = Literal["gre", "ipsec"]

PolicyObjectEntriesColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

Value = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesPathPreferenceDef = Literal["all-paths", "direct-path", "multi-hop-path"]

PolicyObjectListTypeParam = Literal[
    "app-list",
    "app-probe",
    "as-path",
    "class",
    "color",
    "data-ipv6-prefix",
    "data-prefix",
    "expanded-community",
    "ext-community",
    "ipv4-network-object-group",
    "ipv4-service-object-group",
    "ipv6-prefix",
    "mirror",
    "policer",
    "preferred-color-group",
    "prefix",
    "security-data-ip-prefix",
    "security-fqdn",
    "security-geolocation",
    "security-identity",
    "security-ipssignature",
    "security-localapp",
    "security-localdomain",
    "security-port",
    "security-protocolname",
    "security-scalablegrouptag",
    "security-urllist",
    "security-zone",
    "sla-class",
    "standard-community",
    "tloc",
    "vpn-group",
]

SdwanPolicyObjectEntriesColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

PolicyObjectEntriesProtocolNameDef = Literal[
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

PolicyObjectEntriesCountryDef = Literal[
    "ABW",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
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

PolicyObjectEntriesContinentDef = Literal["AF", "AN", "AS", "EU", "NA", "OC", "SA"]

SdwanPolicyObjectEntriesCountryDef = Literal[
    "ABW",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
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

SdwanPolicyObjectEntriesContinentDef = Literal["AF", "AN", "AS", "EU", "NA", "OC", "SA"]

PolicyObjectEntriesCriteriaDef = Literal[
    "jitter",
    "jitter-latency",
    "jitter-latency-loss",
    "jitter-loss",
    "jitter-loss-latency",
    "latency",
    "latency-jitter",
    "latency-jitter-loss",
    "latency-loss",
    "latency-loss-jitter",
    "loss",
    "loss-jitter",
    "loss-jitter-latency",
    "loss-latency",
    "loss-latency-jitter",
]

SdwanPolicyObjectEntriesCriteriaDef = Literal[
    "jitter",
    "jitter-latency",
    "jitter-latency-loss",
    "jitter-loss",
    "jitter-loss-latency",
    "latency",
    "latency-jitter",
    "latency-jitter-loss",
    "latency-loss",
    "latency-loss-jitter",
    "loss",
    "loss-jitter",
    "loss-jitter-latency",
    "loss-latency",
    "loss-latency-jitter",
]

FeatureProfileSdwanPolicyObjectEntriesCriteriaDef = Literal[
    "jitter",
    "jitter-latency",
    "jitter-latency-loss",
    "jitter-loss",
    "jitter-loss-latency",
    "latency",
    "latency-jitter",
    "latency-jitter-loss",
    "latency-loss",
    "latency-loss-jitter",
    "loss",
    "loss-jitter",
    "loss-jitter-latency",
    "loss-latency",
    "loss-latency-jitter",
]

PolicyObjectEntriesQueueDef = Literal["0", "1", "2", "3", "4", "5", "6", "7"]

PolicyObjectEntriesExceedDef = Literal["drop", "remark"]

PolicyObjectEntriesMapColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

FeatureProfileSdwanPolicyObjectEntriesColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

PolicyObjectEntriesEncapDef = Literal["gre", "ipsec"]

V1FeatureProfileSdwanPolicyObjectEntriesColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

PolicyObjectValue = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

PolicyObjectEntriesPathPreferenceDef = Literal["all-paths", "direct-path", "multi-hop-path"]

SdwanPolicyObjectValue = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

SdwanPolicyObjectEntriesPathPreferenceDef = Literal["all-paths", "direct-path", "multi-hop-path"]

FeatureProfileSdwanPolicyObjectValue = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

FeatureProfileSdwanPolicyObjectEntriesPathPreferenceDef = Literal[
    "all-paths", "direct-path", "multi-hop-path"
]

V1FeatureProfileSdwanPolicyObjectValue = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

V1FeatureProfileSdwanPolicyObjectEntriesPathPreferenceDef = Literal[
    "all-paths", "direct-path", "multi-hop-path"
]

SdwanPolicyObjectEntriesProtocolNameDef = Literal[
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

FeatureProfileSdwanPolicyObjectEntriesCountryDef = Literal[
    "ABW",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
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

FeatureProfileSdwanPolicyObjectEntriesContinentDef = Literal[
    "AF", "AN", "AS", "EU", "NA", "OC", "SA"
]

V1FeatureProfileSdwanPolicyObjectEntriesCountryDef = Literal[
    "ABW",
    "AFG",
    "AGO",
    "AIA",
    "ALA",
    "ALB",
    "AND",
    "ANT",
    "ARE",
    "ARG",
    "ARM",
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

V1FeatureProfileSdwanPolicyObjectEntriesContinentDef = Literal[
    "AF", "AN", "AS", "EU", "NA", "OC", "SA"
]

V1FeatureProfileSdwanPolicyObjectEntriesCriteriaDef = Literal[
    "jitter",
    "jitter-latency",
    "jitter-latency-loss",
    "jitter-loss",
    "jitter-loss-latency",
    "latency",
    "latency-jitter",
    "latency-jitter-loss",
    "latency-loss",
    "latency-loss-jitter",
    "loss",
    "loss-jitter",
    "loss-jitter-latency",
    "loss-latency",
    "loss-latency-jitter",
]

EntriesCriteriaDef1 = Literal[
    "jitter",
    "jitter-latency",
    "jitter-latency-loss",
    "jitter-loss",
    "jitter-loss-latency",
    "latency",
    "latency-jitter",
    "latency-jitter-loss",
    "latency-loss",
    "latency-loss-jitter",
    "loss",
    "loss-jitter",
    "loss-jitter-latency",
    "loss-latency",
    "loss-latency-jitter",
]

EntriesCriteriaDef2 = Literal[
    "jitter",
    "jitter-latency",
    "jitter-latency-loss",
    "jitter-loss",
    "jitter-loss-latency",
    "latency",
    "latency-jitter",
    "latency-jitter-loss",
    "latency-loss",
    "latency-loss-jitter",
    "loss",
    "loss-jitter",
    "loss-jitter-latency",
    "loss-latency",
    "loss-latency-jitter",
]

SdwanPolicyObjectEntriesQueueDef = Literal["0", "1", "2", "3", "4", "5", "6", "7"]

SdwanPolicyObjectEntriesExceedDef = Literal["drop", "remark"]

SdwanPolicyObjectEntriesMapColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesColorDef1 = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

SdwanPolicyObjectEntriesEncapDef = Literal["gre", "ipsec"]

EntriesColorDef2 = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

Value1 = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesPathPreferenceDef1 = Literal["all-paths", "direct-path", "multi-hop-path"]

Value2 = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesPathPreferenceDef2 = Literal["all-paths", "direct-path", "multi-hop-path"]

Value3 = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesPathPreferenceDef3 = Literal["all-paths", "direct-path", "multi-hop-path"]

Value4 = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EntriesPathPreferenceDef4 = Literal["all-paths", "direct-path", "multi-hop-path"]


@dataclass
class OneOfIpv4PrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv4PrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Entries:
    ip_prefix: Union[OneOfIpv4PrefixOptionsDef1, OneOfIpv4PrefixOptionsDef2] = _field(
        metadata={"alias": "ipPrefix"}
    )


@dataclass
class PolicyObjectData:
    entries: List[Entries]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost1:
    """
    security-data-ip-prefix profile parcel schema for POST request
    """

    data: PolicyObjectData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesPatternOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Must be valid FQDN
    value: str


@dataclass
class PolicyObjectEntries:
    pattern: OneOfEntriesPatternOptionsDef


@dataclass
class SdwanPolicyObjectData:
    entries: List[PolicyObjectEntries]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost2:
    """
    security-data-fqdn-prefix profile parcel schema for POST request
    """

    data: SdwanPolicyObjectData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanPolicyObjectEntries:
    port: OneOfEntriesPortOptionsDef


@dataclass
class FeatureProfileSdwanPolicyObjectData:
    # Port List
    entries: List[SdwanPolicyObjectEntries]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost3:
    """
    Port profile parcel schema for POST request
    """

    data: FeatureProfileSdwanPolicyObjectData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesAppOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries1:
    app: OneOfEntriesAppOptionsDef
    app_family: Optional[OneOfEntriesAppFamilyOptionsDef] = _field(
        default=None, metadata={"alias": "appFamily"}
    )


@dataclass
class Entries2:
    app_family: OneOfEntriesAppFamilyOptionsDef = _field(metadata={"alias": "appFamily"})
    app: Optional[OneOfEntriesAppOptionsDef] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanPolicyObjectData:
    # Localapp list
    entries: List[Union[Entries1, Entries2]]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost4:
    """
    security-localapp profile parcel schema for POST request
    """

    data: V1FeatureProfileSdwanPolicyObjectData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesNameServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Must be valid utd regex. String cannot start with a '*' or a '+', be empty, or be more than 240 characters
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectEntries:
    name_server: OneOfEntriesNameServerOptionsDef = _field(metadata={"alias": "nameServer"})


@dataclass
class Data1:
    entries: List[FeatureProfileSdwanPolicyObjectEntries]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost5:
    """
    security-localdomain profile parcel schema for POST request
    """

    data: Data1
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesGeneratorIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesSignatureIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntries:
    generator_id: OneOfEntriesGeneratorIdOptionsDef = _field(metadata={"alias": "generatorId"})
    signature_id: OneOfEntriesSignatureIdOptionsDef = _field(metadata={"alias": "signatureId"})


@dataclass
class Data2:
    # Ips Signature
    entries: List[V1FeatureProfileSdwanPolicyObjectEntries]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost6:
    """
    security-ipssignature profile parcel schema for POST request
    """

    data: Data2
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesUrlListOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries11:
    pattern: EntriesUrlListOptionsDef


@dataclass
class Data3:
    # URL List
    entries: List[Entries11]
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost7:
    """
    URL List profile parcel schema for POST request
    """

    data: Data3
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesProtocolNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesProtocolNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries21:
    protocol_name: OneOfEntriesProtocolNameOptionsDef = _field(metadata={"alias": "protocolName"})


@dataclass
class Data4:
    entries: List[Entries21]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost8:
    """
    security-protocolname profile parcel schema for POST request
    """

    data: Data4
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesCountryOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesCountryDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesContinentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesContinentDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectEntries1:
    country: OneOfEntriesCountryOptionsDef
    continent: Optional[OneOfEntriesContinentOptionsDef] = _field(default=None)


@dataclass
class PolicyObjectEntries2:
    continent: OneOfEntriesContinentOptionsDef
    country: Optional[OneOfEntriesCountryOptionsDef] = _field(default=None)


@dataclass
class Data5:
    # Geolocation  List
    entries: List[Union[PolicyObjectEntries1, PolicyObjectEntries2]]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost9:
    """
    Geolocation profile parcel schema for POST request
    """

    data: Data5
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesUserOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class OneOfEntriesUserGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class SdwanPolicyObjectEntries1:
    user: OneOfEntriesUserOptionsDef
    user_group: Optional[OneOfEntriesUserGroupOptionsDef] = _field(
        default=None, metadata={"alias": "userGroup"}
    )


@dataclass
class SdwanPolicyObjectEntries2:
    user_group: OneOfEntriesUserGroupOptionsDef = _field(metadata={"alias": "userGroup"})
    user: Optional[OneOfEntriesUserOptionsDef] = _field(default=None)


@dataclass
class Data6:
    # Array of Users and User Groups
    entries: List[Union[SdwanPolicyObjectEntries1, SdwanPolicyObjectEntries2]]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost10:
    """
    security-identity profile parcel schema for POST request
    """

    data: Data6
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesSgtNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesTagOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries3:
    sgt_name: OneOfEntriesSgtNameOptionsDef = _field(metadata={"alias": "sgtName"})
    tag: OneOfEntriesTagOptionsDef


@dataclass
class Data7:
    entries: List[Entries3]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost11:
    """
    security-scalablegrouptag profile parcel schema for POST request
    """

    data: Data7
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data8:
    entries: List[None]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost12:
    """
    security-zone profile parcel schema for POST request
    """

    data: Data8
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesAppOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectOneOfEntriesAppFamilyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectEntries1:
    app: PolicyObjectOneOfEntriesAppOptionsDef
    app_family: Optional[PolicyObjectOneOfEntriesAppFamilyOptionsDef] = _field(
        default=None, metadata={"alias": "appFamily"}
    )


@dataclass
class SdwanPolicyObjectOneOfEntriesAppOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanPolicyObjectOneOfEntriesAppFamilyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectEntries2:
    app_family: SdwanPolicyObjectOneOfEntriesAppFamilyOptionsDef = _field(
        metadata={"alias": "appFamily"}
    )
    app: Optional[SdwanPolicyObjectOneOfEntriesAppOptionsDef] = _field(default=None)


@dataclass
class Data9:
    # Centralized Policy App List
    entries: List[
        Union[FeatureProfileSdwanPolicyObjectEntries1, FeatureProfileSdwanPolicyObjectEntries2]
    ]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost13:
    """
    Centralized Policy App List profile parcel schema for POST request
    """

    data: Data9
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesLatencyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLossOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfEntriesCriteriaOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesCriteriaDef


@dataclass
class FallbackBestTunnel:
    """
    Object with a criteria and variance
    """

    criteria: Optional[OneOfEntriesCriteriaOptionsDef] = _field(default=None)
    jitter_variance: Optional[OneOfEntriesJitterOptionsDef] = _field(
        default=None, metadata={"alias": "jitterVariance"}
    )
    latency_variance: Optional[OneOfEntriesLatencyOptionsDef] = _field(
        default=None, metadata={"alias": "latencyVariance"}
    )
    loss_variance: Optional[OneOfEntriesLossOptionsDef] = _field(
        default=None, metadata={"alias": "lossVariance"}
    )


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntries1:
    latency: OneOfEntriesLatencyOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[OneOfEntriesJitterOptionsDef] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntries2:
    loss: OneOfEntriesLossOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[OneOfEntriesJitterOptionsDef] = _field(default=None)
    latency: Optional[OneOfEntriesLatencyOptionsDef] = _field(default=None)


@dataclass
class PolicyObjectEntries3:
    jitter: OneOfEntriesJitterOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    latency: Optional[OneOfEntriesLatencyOptionsDef] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef] = _field(default=None)


@dataclass
class Data10:
    # Sla class List
    entries: List[
        Union[
            V1FeatureProfileSdwanPolicyObjectEntries1,
            V1FeatureProfileSdwanPolicyObjectEntries2,
            PolicyObjectEntries3,
        ]
    ]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost14:
    """
    Sla class profile parcel schema for POST request
    """

    data: Data10
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class AsPathListNum:
    """
    As path List Number
    """

    option_type: Optional[GlobalOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class EntriesAsPathOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries4:
    as_path: EntriesAsPathOptionsDef = _field(metadata={"alias": "asPath"})


@dataclass
class Data11:
    # As path List Number
    as_path_list_num: AsPathListNum = _field(metadata={"alias": "asPathListNum"})
    # AS Path List
    entries: List[Entries4]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost15:
    """
    as path profile parcel schema
    """

    data: Data11
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesQueueOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesQueueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries5:
    queue: EntriesQueueOptionsDef


@dataclass
class Data12:
    # class map List
    entries: List[Entries5]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost16:
    """
    class profile parcel schema
    """

    data: Data12
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesIpv6AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EntriesIpv6PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries6:
    ipv6_address: EntriesIpv6AddressOptionsDef = _field(metadata={"alias": "ipv6Address"})
    ipv6_prefix_length: EntriesIpv6PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )


@dataclass
class Data13:
    # IPv6 Prefix List
    entries: Optional[List[Entries6]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost17:
    """
    Ipv6 data prefix profile parcel schema for POST request
    """

    data: Data13
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesIpv4AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EntriesIpv4PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries7:
    ipv4_address: EntriesIpv4AddressOptionsDef = _field(metadata={"alias": "ipv4Address"})
    ipv4_prefix_length: EntriesIpv4PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )


@dataclass
class Data14:
    # IPv4 Data Prefix List
    entries: Optional[List[Entries7]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost18:
    """
    ipv4 data prefix profile parcel schema for POST request
    """

    data: Data14
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfExpandedCommunityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfExpandedCommunityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Data15:
    expanded_community_list: Union[
        OneOfExpandedCommunityOptionsDef1, OneOfExpandedCommunityOptionsDef2
    ] = _field(metadata={"alias": "expandedCommunityList"})


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost19:
    """
    expanded Community list profile parcel schema
    """

    data: Data15
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesExtCommunityOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries8:
    ext_community: EntriesExtCommunityOptionsDef = _field(metadata={"alias": "extCommunity"})


@dataclass
class Data16:
    # Extended Community List
    entries: List[Entries8]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost20:
    """
    extended community list profile parcel schema
    """

    data: Data16
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDescriptionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesAddressTypeHostOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesHostOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesHostOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Entries12:
    address_type: OneOfEntriesAddressTypeHostOptionsDef = _field(metadata={"alias": "addressType"})
    host: Union[OneOfEntriesHostOptionsDef1, OneOfEntriesHostOptionsDef2]


@dataclass
class OneOfEntriesAddressTypeIpPrefixOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesIpPrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesIpPrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Entries22:
    address_type: OneOfEntriesAddressTypeIpPrefixOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    ip_prefix: Union[OneOfEntriesIpPrefixOptionsDef1, OneOfEntriesIpPrefixOptionsDef2] = _field(
        metadata={"alias": "ipPrefix"}
    )


@dataclass
class OneOfEntriesAddressTypeObjectGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SdwanPolicyObjectEntries3:
    address_type: OneOfEntriesAddressTypeObjectGroupOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class OneOfEntriesAddressTypeHostRangeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesHostRangeStartOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesHostRangeStartOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEntriesHostRangeEndOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesHostRangeEndOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class HostRange:
    """
    Host Address Range
    """

    end: Union[OneOfEntriesHostRangeEndOptionsDef1, OneOfEntriesHostRangeEndOptionsDef2]
    start: Union[OneOfEntriesHostRangeStartOptionsDef1, OneOfEntriesHostRangeStartOptionsDef2]


@dataclass
class PolicyObjectEntries4:
    address_type: OneOfEntriesAddressTypeHostRangeOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    # Host Address Range
    host_range: HostRange = _field(metadata={"alias": "hostRange"})


@dataclass
class Data17:
    # object-group Entries
    entries: List[Union[Entries12, Entries22, SdwanPolicyObjectEntries3, PolicyObjectEntries4]]
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost21:
    """
    Ipv4 Network Object Group profile parcel schema
    """

    data: Data17
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries13:
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class Protocol:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesOperatorLtOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesPortLtValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesPortLtValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourcePorts1:
    lt_value: Union[OneOfEntriesPortLtValueOptionsDef1, OneOfEntriesPortLtValueOptionsDef2] = (
        _field(metadata={"alias": "ltValue"})
    )
    operator: OneOfEntriesOperatorLtOptionsDef


@dataclass
class OneOfEntriesOperatorEqOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesTcpPortEqValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfEntriesTcpPortEqValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class EqValue1:
    tcp_eq_value: Union[
        OneOfEntriesTcpPortEqValueOptionsDef1, OneOfEntriesTcpPortEqValueOptionsDef2
    ] = _field(metadata={"alias": "tcpEqValue"})


@dataclass
class OneOfEntriesUdpPortEqValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfEntriesUdpPortEqValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class EqValue2:
    udp_eq_value: Union[
        OneOfEntriesUdpPortEqValueOptionsDef1, OneOfEntriesUdpPortEqValueOptionsDef2
    ] = _field(metadata={"alias": "udpEqValue"})


@dataclass
class OneOfEntriesTcpUdpPortEqValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfEntriesTcpUdpPortEqValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class EqValue3:
    tcp_udp_eq_value: Union[
        OneOfEntriesTcpUdpPortEqValueOptionsDef1, OneOfEntriesTcpUdpPortEqValueOptionsDef2
    ] = _field(metadata={"alias": "tcpUdpEqValue"})


@dataclass
class SourcePorts2:
    # Source Port That is Equal to This Value
    eq_value: Union[EqValue1, EqValue2, EqValue3] = _field(metadata={"alias": "eqValue"})
    operator: OneOfEntriesOperatorEqOptionsDef


@dataclass
class OneOfEntriesOperatorGtOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesPortGtValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesPortGtValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourcePorts3:
    gt_value: Union[OneOfEntriesPortGtValueOptionsDef1, OneOfEntriesPortGtValueOptionsDef2] = (
        _field(metadata={"alias": "gtValue"})
    )
    operator: OneOfEntriesOperatorGtOptionsDef


@dataclass
class OneOfEntriesOperatorRangeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfEntriesPortRangeStartOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesPortRangeStartOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEntriesPortRangeEndOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesPortRangeEndOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Range:
    """
    Source Port Range
    """

    end: Union[OneOfEntriesPortRangeEndOptionsDef1, OneOfEntriesPortRangeEndOptionsDef2]
    start: Union[OneOfEntriesPortRangeStartOptionsDef1, OneOfEntriesPortRangeStartOptionsDef2]


@dataclass
class SourcePorts4:
    operator: OneOfEntriesOperatorRangeOptionsDef
    # Source Port Range
    range: Range


@dataclass
class DestinationPorts:
    eq_value: Optional[Any] = _field(default=None, metadata={"alias": "eqValue"})


@dataclass
class OneOfEntriesIcmpMsgOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfEntriesIcmpMsgOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class PolicyObjectEntries21:
    protocol: Protocol
    destination_ports: Optional[DestinationPorts] = _field(
        default=None, metadata={"alias": "destinationPorts"}
    )
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class OneOfEntriesProtocolOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class DestinationPorts1:
    lt_value: Union[OneOfEntriesPortLtValueOptionsDef1, OneOfEntriesPortLtValueOptionsDef2] = (
        _field(metadata={"alias": "ltValue"})
    )
    operator: OneOfEntriesOperatorLtOptionsDef


@dataclass
class DestinationPorts2:
    # Destination Port That is Equal to This Value
    eq_value: Union[EqValue1, EqValue2, EqValue3] = _field(metadata={"alias": "eqValue"})
    operator: OneOfEntriesOperatorEqOptionsDef


@dataclass
class DestinationPorts3:
    gt_value: Union[OneOfEntriesPortGtValueOptionsDef1, OneOfEntriesPortGtValueOptionsDef2] = (
        _field(metadata={"alias": "gtValue"})
    )
    operator: OneOfEntriesOperatorGtOptionsDef


@dataclass
class PolicyObjectRange:
    """
    Destination Port Range
    """

    end: Union[OneOfEntriesPortRangeEndOptionsDef1, OneOfEntriesPortRangeEndOptionsDef2]
    start: Union[OneOfEntriesPortRangeStartOptionsDef1, OneOfEntriesPortRangeStartOptionsDef2]


@dataclass
class DestinationPorts4:
    operator: OneOfEntriesOperatorRangeOptionsDef
    # Destination Port Range
    range: PolicyObjectRange


@dataclass
class PolicyObjectEntries22:
    protocol: OneOfEntriesProtocolOptionsDef
    # Destination Ports
    destination_ports: Optional[
        Union[DestinationPorts1, DestinationPorts2, DestinationPorts3, DestinationPorts4]
    ] = _field(default=None, metadata={"alias": "destinationPorts"})
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class Data18:
    # object-group Entries
    entries: List[Union[Entries13, Union[PolicyObjectEntries21, PolicyObjectEntries22]]]
    description: Optional[
        Union[
            PolicyObjectOneOfDescriptionOptionsDef1,
            OneOfDescriptionOptionsDef2,
            OneOfDescriptionOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost22:
    """
    Ipv4 Service Object Group profile parcel schema
    """

    data: Data18
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectEntriesIpv6AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectEntriesIpv6PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EntriesLeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EntriesGeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries9:
    ipv6_address: PolicyObjectEntriesIpv6AddressOptionsDef = _field(
        metadata={"alias": "ipv6Address"}
    )
    ipv6_prefix_length: PolicyObjectEntriesIpv6PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )
    ge_range_prefix_length: Optional[EntriesGeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "geRangePrefixLength"}
    )
    le_range_prefix_length: Optional[EntriesLeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "leRangePrefixLength"}
    )


@dataclass
class Data19:
    # IPv6 Prefix List
    entries: List[Entries9]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost23:
    """
    Ipv6 prefix profile parcel schema
    """

    data: Data19
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesRemoteDestIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class EntriesSourceIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class Entries10:
    remote_dest_ip: EntriesRemoteDestIpOptionsDef = _field(metadata={"alias": "remoteDestIp"})
    source_ip: EntriesSourceIpOptionsDef = _field(metadata={"alias": "sourceIp"})


@dataclass
class Data20:
    # Mirror List
    entries: List[Entries10]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost24:
    """
    mirror profile parcel schema for POST request
    """

    data: Data20
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesBurstOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EntriesExceedOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesExceedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EntriesRateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries11_1:
    burst: EntriesBurstOptionsDef
    exceed: EntriesExceedOptionsDef
    rate: EntriesRateOptionsDef


@dataclass
class Data21:
    # Policer Entries
    entries: List[Entries11_1]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost25:
    """
    policer profile parcel schema for POST request
    """

    data: Data21
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectEntriesIpv4AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectEntriesIpv4PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyObjectEntriesLeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyObjectEntriesGeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries12_1:
    ipv4_address: PolicyObjectEntriesIpv4AddressOptionsDef = _field(
        metadata={"alias": "ipv4Address"}
    )
    ipv4_prefix_length: PolicyObjectEntriesIpv4PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )
    ge_range_prefix_length: Optional[PolicyObjectEntriesGeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "geRangePrefixLength"}
    )
    le_range_prefix_length: Optional[PolicyObjectEntriesLeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "leRangePrefixLength"}
    )


@dataclass
class Data22:
    # IPv4 Prefix List
    entries: List[Entries12_1]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost26:
    """
    Ipv4 prefix profile parcel schema
    """

    data: Data22
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class StandardCommunityOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries13_1:
    standard_community: StandardCommunityOptionsDef = _field(
        metadata={"alias": "standardCommunity"}
    )


@dataclass
class Data23:
    # Standard Community List
    entries: List[Entries13_1]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost27:
    """
    standard Community list profile parcel schema
    """

    data: Data23
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesVpnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class Entries14:
    vpn: EntriesVpnOptionsDef


@dataclass
class Data24:
    # VPN List
    entries: List[Entries14]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost28:
    """
    vpn list profile parcel schema
    """

    data: Data24
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesMapColorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesMapColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesMapDscpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Map:
    color: OneOfEntriesMapColorOptionsDef
    dscp: Optional[OneOfEntriesMapDscpOptionsDef] = _field(default=None)


@dataclass
class ForwardingClass1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ForwardingClass2:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class Entries15:
    # Forwarding Class Name
    forwarding_class: Union[ForwardingClass1, ForwardingClass2] = _field(
        metadata={"alias": "forwardingClass"}
    )
    # Map
    map: List[Map]


@dataclass
class Data25:
    # App Probe List
    entries: List[Entries15]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost29:
    """
    app-probe profile parcel schema for POST request
    """

    data: Data25
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesTlocOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesColorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries16:
    color: OneOfEntriesColorOptionsDef
    encap: OneOfEntriesEncapOptionsDef
    tloc: OneOfEntriesTlocOptionsDef
    preference: Optional[OneOfEntriesPreferenceOptionsDef] = _field(default=None)


@dataclass
class Data26:
    # TLOC List
    entries: Optional[List[Entries16]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost30:
    """
    tloc profile parcel schema for POST request
    """

    data: Data26
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesColorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries17:
    color: PolicyObjectOneOfEntriesColorOptionsDef


@dataclass
class Data27:
    # Color List
    entries: Optional[List[Entries17]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost31:
    """
    color profile parcel schema for POST request
    """

    data: Data27
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class OneOfEntriesColorPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Value]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesPathPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesPathPreferenceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PrimaryPreference1:
    color_preference: OneOfEntriesColorPreferenceOptionsDef = _field(
        metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class PrimaryPreference2:
    path_preference: OneOfEntriesPathPreferenceOptionsDef = _field(
        metadata={"alias": "pathPreference"}
    )
    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )


@dataclass
class SecondaryPreference:
    """
    Object with an color and path preference
    """

    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class TertiaryPreference:
    """
    Object with an color and path preference
    """

    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class Entries18:
    # Object with an color and path preference
    primary_preference: Union[PrimaryPreference1, PrimaryPreference2] = _field(
        metadata={"alias": "primaryPreference"}
    )
    # Object with an color and path preference
    secondary_preference: Optional[SecondaryPreference] = _field(
        default=None, metadata={"alias": "secondaryPreference"}
    )
    # Object with an color and path preference
    tertiary_preference: Optional[TertiaryPreference] = _field(
        default=None, metadata={"alias": "tertiaryPreference"}
    )


@dataclass
class Data28:
    # Preferred Color Group List
    entries: Optional[List[Entries18]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePost32:
    """
    preferred-color-group profile parcel schema for POST request
    """

    data: Data28
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


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
    payload: Optional[
        Union[
            Schema2HubGeneratedPolicyobjectlisttypePost1,
            Schema2HubGeneratedPolicyobjectlisttypePost2,
            Schema2HubGeneratedPolicyobjectlisttypePost3,
            Schema2HubGeneratedPolicyobjectlisttypePost4,
            Schema2HubGeneratedPolicyobjectlisttypePost5,
            Schema2HubGeneratedPolicyobjectlisttypePost6,
            Schema2HubGeneratedPolicyobjectlisttypePost7,
            Schema2HubGeneratedPolicyobjectlisttypePost8,
            Schema2HubGeneratedPolicyobjectlisttypePost9,
            Schema2HubGeneratedPolicyobjectlisttypePost10,
            Schema2HubGeneratedPolicyobjectlisttypePost11,
            Schema2HubGeneratedPolicyobjectlisttypePost12,
            Schema2HubGeneratedPolicyobjectlisttypePost13,
            Schema2HubGeneratedPolicyobjectlisttypePost14,
            Schema2HubGeneratedPolicyobjectlisttypePost15,
            Schema2HubGeneratedPolicyobjectlisttypePost16,
            Schema2HubGeneratedPolicyobjectlisttypePost17,
            Schema2HubGeneratedPolicyobjectlisttypePost18,
            Schema2HubGeneratedPolicyobjectlisttypePost19,
            Schema2HubGeneratedPolicyobjectlisttypePost20,
            Schema2HubGeneratedPolicyobjectlisttypePost21,
            Schema2HubGeneratedPolicyobjectlisttypePost22,
            Schema2HubGeneratedPolicyobjectlisttypePost23,
            Schema2HubGeneratedPolicyobjectlisttypePost24,
            Schema2HubGeneratedPolicyobjectlisttypePost25,
            Schema2HubGeneratedPolicyobjectlisttypePost26,
            Schema2HubGeneratedPolicyobjectlisttypePost27,
            Schema2HubGeneratedPolicyobjectlisttypePost28,
            Schema2HubGeneratedPolicyobjectlisttypePost29,
            Schema2HubGeneratedPolicyobjectlisttypePost30,
            Schema2HubGeneratedPolicyobjectlisttypePost31,
            Schema2HubGeneratedPolicyobjectlisttypePost32,
        ]
    ] = _field(default=None)


@dataclass
class GetListSdwanPolicyObjectSecurityDataIpPrefixPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data29:
    entries: List[Entries]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest1:
    """
    security-data-ip-prefix profile parcel schema for POST request
    """

    data: Data29
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries19:
    pattern: OneOfEntriesPatternOptionsDef


@dataclass
class Data30:
    entries: List[Entries19]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest2:
    """
    security-data-fqdn-prefix profile parcel schema for POST request
    """

    data: Data30
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries20:
    port: OneOfEntriesPortOptionsDef


@dataclass
class Data31:
    # Port List
    entries: List[Entries20]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest3:
    """
    Port profile parcel schema for POST request
    """

    data: Data31
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data32:
    # Localapp list
    entries: List[Union[Entries1, Entries2]]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest4:
    """
    security-localapp profile parcel schema for POST request
    """

    data: Data32
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries21_1:
    name_server: OneOfEntriesNameServerOptionsDef = _field(metadata={"alias": "nameServer"})


@dataclass
class Data33:
    entries: List[Entries21_1]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest5:
    """
    security-localdomain profile parcel schema for POST request
    """

    data: Data33
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries22_1:
    generator_id: OneOfEntriesGeneratorIdOptionsDef = _field(metadata={"alias": "generatorId"})
    signature_id: OneOfEntriesSignatureIdOptionsDef = _field(metadata={"alias": "signatureId"})


@dataclass
class Data34:
    # Ips Signature
    entries: List[Entries22_1]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest6:
    """
    security-ipssignature profile parcel schema for POST request
    """

    data: Data34
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries23:
    pattern: EntriesUrlListOptionsDef


@dataclass
class Data35:
    # URL List
    entries: List[Entries23]
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest7:
    """
    URL List profile parcel schema for POST request
    """

    data: Data35
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries24:
    protocol_name: OneOfEntriesProtocolNameOptionsDef = _field(metadata={"alias": "protocolName"})


@dataclass
class Data36:
    entries: List[Entries24]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest8:
    """
    security-protocolname profile parcel schema for POST request
    """

    data: Data36
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries14_1:
    country: OneOfEntriesCountryOptionsDef
    continent: Optional[OneOfEntriesContinentOptionsDef] = _field(default=None)


@dataclass
class Entries23_1:
    continent: OneOfEntriesContinentOptionsDef
    country: Optional[OneOfEntriesCountryOptionsDef] = _field(default=None)


@dataclass
class Data37:
    # Geolocation  List
    entries: List[Union[Entries14_1, Entries23_1]]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest9:
    """
    Geolocation profile parcel schema for POST request
    """

    data: Data37
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries15_1:
    user: OneOfEntriesUserOptionsDef
    user_group: Optional[OneOfEntriesUserGroupOptionsDef] = _field(
        default=None, metadata={"alias": "userGroup"}
    )


@dataclass
class Entries24_1:
    user_group: OneOfEntriesUserGroupOptionsDef = _field(metadata={"alias": "userGroup"})
    user: Optional[OneOfEntriesUserOptionsDef] = _field(default=None)


@dataclass
class Data38:
    # Array of Users and User Groups
    entries: List[Union[Entries15_1, Entries24_1]]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest10:
    """
    security-identity profile parcel schema for POST request
    """

    data: Data38
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries25:
    sgt_name: OneOfEntriesSgtNameOptionsDef = _field(metadata={"alias": "sgtName"})
    tag: OneOfEntriesTagOptionsDef


@dataclass
class Data39:
    entries: List[Entries25]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest11:
    """
    security-scalablegrouptag profile parcel schema for POST request
    """

    data: Data39
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data40:
    entries: List[None]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest12:
    """
    security-zone profile parcel schema for POST request
    """

    data: Data40
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesAppOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesAppFamilyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries16_1:
    app: FeatureProfileSdwanPolicyObjectOneOfEntriesAppOptionsDef
    app_family: Optional[FeatureProfileSdwanPolicyObjectOneOfEntriesAppFamilyOptionsDef] = _field(
        default=None, metadata={"alias": "appFamily"}
    )


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesAppOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesAppFamilyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries25_1:
    app_family: V1FeatureProfileSdwanPolicyObjectOneOfEntriesAppFamilyOptionsDef = _field(
        metadata={"alias": "appFamily"}
    )
    app: Optional[V1FeatureProfileSdwanPolicyObjectOneOfEntriesAppOptionsDef] = _field(default=None)


@dataclass
class Data41:
    # Centralized Policy App List
    entries: List[Union[Entries16_1, Entries25_1]]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest13:
    """
    Centralized Policy App List profile parcel schema for POST request
    """

    data: Data41
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries17_1:
    latency: OneOfEntriesLatencyOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[OneOfEntriesJitterOptionsDef] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef] = _field(default=None)


@dataclass
class Entries26:
    loss: OneOfEntriesLossOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[OneOfEntriesJitterOptionsDef] = _field(default=None)
    latency: Optional[OneOfEntriesLatencyOptionsDef] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectEntries3:
    jitter: OneOfEntriesJitterOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    latency: Optional[OneOfEntriesLatencyOptionsDef] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef] = _field(default=None)


@dataclass
class Data42:
    # Sla class List
    entries: List[Union[Entries17_1, Entries26, FeatureProfileSdwanPolicyObjectEntries3]]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest14:
    """
    Sla class profile parcel schema for POST request
    """

    data: Data42
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries26_1:
    as_path: EntriesAsPathOptionsDef = _field(metadata={"alias": "asPath"})


@dataclass
class Data43:
    # As path List Number
    as_path_list_num: AsPathListNum = _field(metadata={"alias": "asPathListNum"})
    # AS Path List
    entries: List[Entries26_1]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest15:
    """
    as path profile parcel schema
    """

    data: Data43
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries27:
    queue: EntriesQueueOptionsDef


@dataclass
class Data44:
    # class map List
    entries: List[Entries27]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest16:
    """
    class profile parcel schema
    """

    data: Data44
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries28:
    ipv6_address: EntriesIpv6AddressOptionsDef = _field(metadata={"alias": "ipv6Address"})
    ipv6_prefix_length: EntriesIpv6PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )


@dataclass
class Data45:
    # IPv6 Prefix List
    entries: Optional[List[Entries28]] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest17:
    """
    Ipv6 data prefix profile parcel schema for POST request
    """

    data: Data45
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries29:
    ipv4_address: EntriesIpv4AddressOptionsDef = _field(metadata={"alias": "ipv4Address"})
    ipv4_prefix_length: EntriesIpv4PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )


@dataclass
class Data46:
    # IPv4 Data Prefix List
    entries: Optional[List[Entries29]] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest18:
    """
    ipv4 data prefix profile parcel schema for POST request
    """

    data: Data46
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data47:
    expanded_community_list: Union[
        OneOfExpandedCommunityOptionsDef1, OneOfExpandedCommunityOptionsDef2
    ] = _field(metadata={"alias": "expandedCommunityList"})


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest19:
    """
    expanded Community list profile parcel schema
    """

    data: Data47
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries30:
    ext_community: EntriesExtCommunityOptionsDef = _field(metadata={"alias": "extCommunity"})


@dataclass
class Data48:
    # Extended Community List
    entries: List[Entries30]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest20:
    """
    extended community list profile parcel schema
    """

    data: Data48
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries18_1:
    address_type: OneOfEntriesAddressTypeHostOptionsDef = _field(metadata={"alias": "addressType"})
    host: Union[OneOfEntriesHostOptionsDef1, OneOfEntriesHostOptionsDef2]


@dataclass
class Entries27_1:
    address_type: OneOfEntriesAddressTypeIpPrefixOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    ip_prefix: Union[OneOfEntriesIpPrefixOptionsDef1, OneOfEntriesIpPrefixOptionsDef2] = _field(
        metadata={"alias": "ipPrefix"}
    )


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntries3:
    address_type: OneOfEntriesAddressTypeObjectGroupOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class SdwanPolicyObjectEntries4:
    address_type: OneOfEntriesAddressTypeHostRangeOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    # Host Address Range
    host_range: HostRange = _field(metadata={"alias": "hostRange"})


@dataclass
class Data49:
    # object-group Entries
    entries: List[
        Union[
            Entries18_1,
            Entries27_1,
            V1FeatureProfileSdwanPolicyObjectEntries3,
            SdwanPolicyObjectEntries4,
        ]
    ]
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest21:
    """
    Ipv4 Network Object Group profile parcel schema
    """

    data: Data49
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries19_1:
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class SdwanPolicyObjectEntries21:
    protocol: Protocol
    destination_ports: Optional[DestinationPorts] = _field(
        default=None, metadata={"alias": "destinationPorts"}
    )
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class SdwanPolicyObjectEntries22:
    protocol: OneOfEntriesProtocolOptionsDef
    # Destination Ports
    destination_ports: Optional[
        Union[DestinationPorts1, DestinationPorts2, DestinationPorts3, DestinationPorts4]
    ] = _field(default=None, metadata={"alias": "destinationPorts"})
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class Data50:
    # object-group Entries
    entries: List[Union[Entries19_1, Union[SdwanPolicyObjectEntries21, SdwanPolicyObjectEntries22]]]
    description: Optional[
        Union[
            SdwanPolicyObjectOneOfDescriptionOptionsDef1,
            OneOfDescriptionOptionsDef2,
            OneOfDescriptionOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest22:
    """
    Ipv4 Service Object Group profile parcel schema
    """

    data: Data50
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectEntriesIpv6AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanPolicyObjectEntriesIpv6PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries31:
    ipv6_address: SdwanPolicyObjectEntriesIpv6AddressOptionsDef = _field(
        metadata={"alias": "ipv6Address"}
    )
    ipv6_prefix_length: SdwanPolicyObjectEntriesIpv6PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )
    ge_range_prefix_length: Optional[EntriesGeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "geRangePrefixLength"}
    )
    le_range_prefix_length: Optional[EntriesLeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "leRangePrefixLength"}
    )


@dataclass
class Data51:
    # IPv6 Prefix List
    entries: List[Entries31]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest23:
    """
    Ipv6 prefix profile parcel schema
    """

    data: Data51
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries32:
    remote_dest_ip: EntriesRemoteDestIpOptionsDef = _field(metadata={"alias": "remoteDestIp"})
    source_ip: EntriesSourceIpOptionsDef = _field(metadata={"alias": "sourceIp"})


@dataclass
class Data52:
    # Mirror List
    entries: List[Entries32]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest24:
    """
    mirror profile parcel schema for POST request
    """

    data: Data52
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries33:
    burst: EntriesBurstOptionsDef
    exceed: EntriesExceedOptionsDef
    rate: EntriesRateOptionsDef


@dataclass
class Data53:
    # Policer Entries
    entries: List[Entries33]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest25:
    """
    policer profile parcel schema for POST request
    """

    data: Data53
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectEntriesIpv4AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanPolicyObjectEntriesIpv4PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanPolicyObjectEntriesLeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanPolicyObjectEntriesGeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries34:
    ipv4_address: SdwanPolicyObjectEntriesIpv4AddressOptionsDef = _field(
        metadata={"alias": "ipv4Address"}
    )
    ipv4_prefix_length: SdwanPolicyObjectEntriesIpv4PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )
    ge_range_prefix_length: Optional[SdwanPolicyObjectEntriesGeRangePrefixLengthOptionsDef] = (
        _field(default=None, metadata={"alias": "geRangePrefixLength"})
    )
    le_range_prefix_length: Optional[SdwanPolicyObjectEntriesLeRangePrefixLengthOptionsDef] = (
        _field(default=None, metadata={"alias": "leRangePrefixLength"})
    )


@dataclass
class Data54:
    # IPv4 Prefix List
    entries: List[Entries34]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest26:
    """
    Ipv4 prefix profile parcel schema
    """

    data: Data54
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries35:
    standard_community: StandardCommunityOptionsDef = _field(
        metadata={"alias": "standardCommunity"}
    )


@dataclass
class Data55:
    # Standard Community List
    entries: List[Entries35]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest27:
    """
    standard Community list profile parcel schema
    """

    data: Data55
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries36:
    vpn: EntriesVpnOptionsDef


@dataclass
class Data56:
    # VPN List
    entries: List[Entries36]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest28:
    """
    vpn list profile parcel schema
    """

    data: Data56
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries37:
    # Forwarding Class Name
    forwarding_class: Union[ForwardingClass1, ForwardingClass2] = _field(
        metadata={"alias": "forwardingClass"}
    )
    # Map
    map: List[Map]


@dataclass
class Data57:
    # App Probe List
    entries: List[Entries37]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest29:
    """
    app-probe profile parcel schema for POST request
    """

    data: Data57
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries38:
    color: OneOfEntriesColorOptionsDef
    encap: OneOfEntriesEncapOptionsDef
    tloc: OneOfEntriesTlocOptionsDef
    preference: Optional[OneOfEntriesPreferenceOptionsDef] = _field(default=None)


@dataclass
class Data58:
    # TLOC List
    entries: Optional[List[Entries38]] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest30:
    """
    tloc profile parcel schema for POST request
    """

    data: Data58
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesColorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries39:
    color: SdwanPolicyObjectOneOfEntriesColorOptionsDef


@dataclass
class Data59:
    # Color List
    entries: Optional[List[Entries39]] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest31:
    """
    color profile parcel schema for POST request
    """

    data: Data59
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class Entries40:
    # Object with an color and path preference
    primary_preference: Union[PrimaryPreference1, PrimaryPreference2] = _field(
        metadata={"alias": "primaryPreference"}
    )
    # Object with an color and path preference
    secondary_preference: Optional[SecondaryPreference] = _field(
        default=None, metadata={"alias": "secondaryPreference"}
    )
    # Object with an color and path preference
    tertiary_preference: Optional[TertiaryPreference] = _field(
        default=None, metadata={"alias": "tertiaryPreference"}
    )


@dataclass
class Data60:
    # Preferred Color Group List
    entries: Optional[List[Entries40]] = _field(default=None)


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest32:
    """
    preferred-color-group profile parcel schema for POST request
    """

    data: Data60
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class Data61:
    entries: List[Entries]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut1:
    """
    security-data-ip-prefix profile parcel schema for PUT request
    """

    data: Data61
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesPatternOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Must be valid FQDN
    value: str


@dataclass
class Entries41:
    pattern: PolicyObjectOneOfEntriesPatternOptionsDef


@dataclass
class Data62:
    entries: List[Entries41]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut2:
    """
    security-data-fqdn-prefix profile parcel schema for PUT request
    """

    data: Data62
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries42:
    port: PolicyObjectOneOfEntriesPortOptionsDef


@dataclass
class Data63:
    # Port List
    entries: List[Entries42]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut3:
    """
    Port profile parcel schema for PUT request
    """

    data: Data63
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesAppOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries110:
    app: OneOfEntriesAppOptionsDef1
    app_family: Optional[OneOfEntriesAppFamilyOptionsDef1] = _field(
        default=None, metadata={"alias": "appFamily"}
    )


@dataclass
class OneOfEntriesAppOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries28_1:
    app_family: OneOfEntriesAppFamilyOptionsDef2 = _field(metadata={"alias": "appFamily"})
    app: Optional[OneOfEntriesAppOptionsDef2] = _field(default=None)


@dataclass
class Data64:
    # Localapp list
    entries: List[Union[Entries110, Entries28_1]]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut4:
    """
    security-localapp profile parcel schema for PUT request
    """

    data: Data64
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesNameServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # String cannot start with a '.' or a '*', be empty, or be more than 240 characters
    value: str


@dataclass
class Entries43:
    name_server: PolicyObjectOneOfEntriesNameServerOptionsDef = _field(
        metadata={"alias": "nameServer"}
    )


@dataclass
class Data65:
    entries: List[Entries43]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut5:
    """
    security-localdomain profile parcel schema for PUT request
    """

    data: Data65
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesGeneratorIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectOneOfEntriesSignatureIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries44:
    generator_id: PolicyObjectOneOfEntriesGeneratorIdOptionsDef = _field(
        metadata={"alias": "generatorId"}
    )
    signature_id: PolicyObjectOneOfEntriesSignatureIdOptionsDef = _field(
        metadata={"alias": "signatureId"}
    )


@dataclass
class Data66:
    # Ips Signature
    entries: List[Entries44]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut6:
    """
    security-ipssignature profile parcel schema for PUT request
    """

    data: Data66
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectEntriesUrlListOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries45:
    pattern: PolicyObjectEntriesUrlListOptionsDef


@dataclass
class Data67:
    # URL List
    entries: List[Entries45]
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut7:
    """
    URL List profile parcel schema for PUT request
    """

    data: Data67
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesProtocolNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesProtocolNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries46:
    protocol_name: PolicyObjectOneOfEntriesProtocolNameOptionsDef = _field(
        metadata={"alias": "protocolName"}
    )


@dataclass
class Data68:
    entries: List[Entries46]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut8:
    """
    security-protocolname profile parcel schema for PUT request
    """

    data: Data68
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesCountryOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesCountryDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectOneOfEntriesContinentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesContinentDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries111:
    country: PolicyObjectOneOfEntriesCountryOptionsDef
    continent: Optional[PolicyObjectOneOfEntriesContinentOptionsDef] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesCountryOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesCountryDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectOneOfEntriesContinentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesContinentDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries29_1:
    continent: SdwanPolicyObjectOneOfEntriesContinentOptionsDef
    country: Optional[SdwanPolicyObjectOneOfEntriesCountryOptionsDef] = _field(default=None)


@dataclass
class Data69:
    # Geolocation  List
    entries: List[Union[Entries111, Entries29_1]]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut9:
    """
    Geolocation profile parcel schema for PUT request
    """

    data: Data69
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesUserOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class PolicyObjectOneOfEntriesUserGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class Entries112:
    user: PolicyObjectOneOfEntriesUserOptionsDef
    user_group: Optional[PolicyObjectOneOfEntriesUserGroupOptionsDef] = _field(
        default=None, metadata={"alias": "userGroup"}
    )


@dataclass
class SdwanPolicyObjectOneOfEntriesUserOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class SdwanPolicyObjectOneOfEntriesUserGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class Entries210:
    user_group: SdwanPolicyObjectOneOfEntriesUserGroupOptionsDef = _field(
        metadata={"alias": "userGroup"}
    )
    user: Optional[SdwanPolicyObjectOneOfEntriesUserOptionsDef] = _field(default=None)


@dataclass
class Data70:
    # Array of Users and User Groups
    entries: List[Union[Entries112, Entries210]]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut10:
    """
    security-identity profile parcel schema for PUT request
    """

    data: Data70
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesSgtNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectOneOfEntriesTagOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries47:
    sgt_name: PolicyObjectOneOfEntriesSgtNameOptionsDef = _field(metadata={"alias": "sgtName"})
    tag: PolicyObjectOneOfEntriesTagOptionsDef


@dataclass
class Data71:
    entries: List[Entries47]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut11:
    """
    security-scalablegrouptag profile parcel schema for PUT request
    """

    data: Data71
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data72:
    entries: List[None]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut12:
    """
    security-zone profile parcel schema for PUT request
    """

    data: Data72
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesAppOptionsDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries113:
    app: OneOfEntriesAppOptionsDef3
    app_family: Optional[OneOfEntriesAppFamilyOptionsDef3] = _field(
        default=None, metadata={"alias": "appFamily"}
    )


@dataclass
class OneOfEntriesAppOptionsDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries211:
    app_family: OneOfEntriesAppFamilyOptionsDef4 = _field(metadata={"alias": "appFamily"})
    app: Optional[OneOfEntriesAppOptionsDef4] = _field(default=None)


@dataclass
class Data73:
    # centralized-applist list
    entries: List[Union[Entries113, Entries211]]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut13:
    """
    security-localapp profile parcel schema for PUT request
    """

    data: Data73
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesLatencyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyObjectOneOfEntriesLossOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyObjectOneOfEntriesJitterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyObjectOneOfEntriesCriteriaOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesCriteriaDef


@dataclass
class SdwanPolicyObjectOneOfEntriesLossOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanPolicyObjectOneOfEntriesLatencyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanPolicyObjectOneOfEntriesJitterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyObjectFallbackBestTunnel:
    """
    Object with a criteria and variance
    """

    criteria: Optional[PolicyObjectOneOfEntriesCriteriaOptionsDef] = _field(default=None)
    jitter_variance: Optional[SdwanPolicyObjectOneOfEntriesJitterOptionsDef] = _field(
        default=None, metadata={"alias": "jitterVariance"}
    )
    latency_variance: Optional[SdwanPolicyObjectOneOfEntriesLatencyOptionsDef] = _field(
        default=None, metadata={"alias": "latencyVariance"}
    )
    loss_variance: Optional[SdwanPolicyObjectOneOfEntriesLossOptionsDef] = _field(
        default=None, metadata={"alias": "lossVariance"}
    )


@dataclass
class Entries114:
    latency: PolicyObjectOneOfEntriesLatencyOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[PolicyObjectFallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[PolicyObjectOneOfEntriesJitterOptionsDef] = _field(default=None)
    loss: Optional[PolicyObjectOneOfEntriesLossOptionsDef] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesLatencyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesLossOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesJitterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanPolicyObjectOneOfEntriesCriteriaOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesCriteriaDef


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesLossOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesLatencyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesJitterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanPolicyObjectFallbackBestTunnel:
    """
    Object with a criteria and variance
    """

    criteria: Optional[SdwanPolicyObjectOneOfEntriesCriteriaOptionsDef] = _field(default=None)
    jitter_variance: Optional[V1FeatureProfileSdwanPolicyObjectOneOfEntriesJitterOptionsDef] = (
        _field(default=None, metadata={"alias": "jitterVariance"})
    )
    latency_variance: Optional[V1FeatureProfileSdwanPolicyObjectOneOfEntriesLatencyOptionsDef] = (
        _field(default=None, metadata={"alias": "latencyVariance"})
    )
    loss_variance: Optional[V1FeatureProfileSdwanPolicyObjectOneOfEntriesLossOptionsDef] = _field(
        default=None, metadata={"alias": "lossVariance"}
    )


@dataclass
class Entries212:
    loss: FeatureProfileSdwanPolicyObjectOneOfEntriesLossOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[SdwanPolicyObjectFallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[FeatureProfileSdwanPolicyObjectOneOfEntriesJitterOptionsDef] = _field(
        default=None
    )
    latency: Optional[FeatureProfileSdwanPolicyObjectOneOfEntriesLatencyOptionsDef] = _field(
        default=None
    )


@dataclass
class OneOfEntriesLatencyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLossOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesCriteriaOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanPolicyObjectEntriesCriteriaDef


@dataclass
class OneOfEntriesLossOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLatencyOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanPolicyObjectFallbackBestTunnel:
    """
    Object with a criteria and variance
    """

    criteria: Optional[FeatureProfileSdwanPolicyObjectOneOfEntriesCriteriaOptionsDef] = _field(
        default=None
    )
    jitter_variance: Optional[OneOfEntriesJitterOptionsDef2] = _field(
        default=None, metadata={"alias": "jitterVariance"}
    )
    latency_variance: Optional[OneOfEntriesLatencyOptionsDef2] = _field(
        default=None, metadata={"alias": "latencyVariance"}
    )
    loss_variance: Optional[OneOfEntriesLossOptionsDef2] = _field(
        default=None, metadata={"alias": "lossVariance"}
    )


@dataclass
class Entries31_1:
    jitter: OneOfEntriesJitterOptionsDef1
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FeatureProfileSdwanPolicyObjectFallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    latency: Optional[OneOfEntriesLatencyOptionsDef1] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef1] = _field(default=None)


@dataclass
class Data74:
    # Sla class List
    entries: List[Union[Entries114, Entries212, Entries31_1]]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut14:
    """
    Sla class profile parcel schema for PUT request
    """

    data: Data74
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries48:
    as_path: EntriesAsPathOptionsDef = _field(metadata={"alias": "asPath"})


@dataclass
class Data75:
    # As path List Number
    as_path_list_num: AsPathListNum = _field(metadata={"alias": "asPathListNum"})
    # AS Path List
    entries: List[Entries48]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut15:
    """
    as path profile parcel schema
    """

    data: Data75
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectEntriesQueueOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesQueueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries49:
    queue: PolicyObjectEntriesQueueOptionsDef


@dataclass
class Data76:
    # class map List
    entries: List[Entries49]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut16:
    """
    class profile parcel schema for PUT request
    """

    data: Data76
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectEntriesIpv6AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectEntriesIpv6PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries50:
    ipv6_address: FeatureProfileSdwanPolicyObjectEntriesIpv6AddressOptionsDef = _field(
        metadata={"alias": "ipv6Address"}
    )
    ipv6_prefix_length: FeatureProfileSdwanPolicyObjectEntriesIpv6PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )


@dataclass
class Data77:
    # IPv6 Prefix List
    entries: Optional[List[Entries50]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut17:
    """
    Ipv6 data prefix profile parcel schema for PUT request
    """

    data: Data77
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectEntriesIpv4AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectEntriesIpv4PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries51:
    ipv4_address: FeatureProfileSdwanPolicyObjectEntriesIpv4AddressOptionsDef = _field(
        metadata={"alias": "ipv4Address"}
    )
    ipv4_prefix_length: FeatureProfileSdwanPolicyObjectEntriesIpv4PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )


@dataclass
class Data78:
    # IPv4 Data Prefix List
    entries: Optional[List[Entries51]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut18:
    """
    ipv4 data prefix profile parcel schema for PUT request
    """

    data: Data78
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class Data79:
    expanded_community_list: Union[
        OneOfExpandedCommunityOptionsDef1, OneOfExpandedCommunityOptionsDef2
    ] = _field(metadata={"alias": "expandedCommunityList"})


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut19:
    """
    expanded Community list profile parcel schema
    """

    data: Data79
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries52:
    ext_community: EntriesExtCommunityOptionsDef = _field(metadata={"alias": "extCommunity"})


@dataclass
class Data80:
    # Extended Community List
    entries: List[Entries52]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut20:
    """
    extended community list profile parcel schema
    """

    data: Data80
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries115:
    address_type: OneOfEntriesAddressTypeHostOptionsDef = _field(metadata={"alias": "addressType"})
    host: Union[OneOfEntriesHostOptionsDef1, OneOfEntriesHostOptionsDef2]


@dataclass
class Entries213:
    address_type: OneOfEntriesAddressTypeIpPrefixOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    ip_prefix: Union[OneOfEntriesIpPrefixOptionsDef1, OneOfEntriesIpPrefixOptionsDef2] = _field(
        metadata={"alias": "ipPrefix"}
    )


@dataclass
class Entries32_1:
    address_type: OneOfEntriesAddressTypeObjectGroupOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class FeatureProfileSdwanPolicyObjectEntries4:
    address_type: OneOfEntriesAddressTypeHostRangeOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    # Host Address Range
    host_range: HostRange = _field(metadata={"alias": "hostRange"})


@dataclass
class Data81:
    # object-group Entries
    entries: List[
        Union[Entries115, Entries213, Entries32_1, FeatureProfileSdwanPolicyObjectEntries4]
    ]
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut21:
    """
    Ipv4 Network Object Group profile parcel schema
    """

    data: Data81
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries116:
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class FeatureProfileSdwanPolicyObjectEntries21:
    protocol: Protocol
    destination_ports: Optional[DestinationPorts] = _field(
        default=None, metadata={"alias": "destinationPorts"}
    )
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class FeatureProfileSdwanPolicyObjectEntries22:
    protocol: OneOfEntriesProtocolOptionsDef
    # Destination Ports
    destination_ports: Optional[
        Union[DestinationPorts1, DestinationPorts2, DestinationPorts3, DestinationPorts4]
    ] = _field(default=None, metadata={"alias": "destinationPorts"})
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class Data82:
    # object-group Entries
    entries: List[
        Union[
            Entries116,
            Union[
                FeatureProfileSdwanPolicyObjectEntries21, FeatureProfileSdwanPolicyObjectEntries22
            ],
        ]
    ]
    description: Optional[
        Union[
            FeatureProfileSdwanPolicyObjectOneOfDescriptionOptionsDef1,
            OneOfDescriptionOptionsDef2,
            OneOfDescriptionOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut22:
    """
    Ipv4 Service Object Group profile parcel schema
    """

    data: Data82
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntriesIpv6AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntriesIpv6PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries53:
    ipv6_address: V1FeatureProfileSdwanPolicyObjectEntriesIpv6AddressOptionsDef = _field(
        metadata={"alias": "ipv6Address"}
    )
    ipv6_prefix_length: V1FeatureProfileSdwanPolicyObjectEntriesIpv6PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )
    ge_range_prefix_length: Optional[EntriesGeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "geRangePrefixLength"}
    )
    le_range_prefix_length: Optional[EntriesLeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "leRangePrefixLength"}
    )


@dataclass
class Data83:
    # IPv6 Prefix List
    entries: List[Entries53]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut23:
    """
    Ipv6 prefix profile parcel schema
    """

    data: Data83
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectEntriesRemoteDestIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class PolicyObjectEntriesSourceIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class Entries54:
    remote_dest_ip: PolicyObjectEntriesRemoteDestIpOptionsDef = _field(
        metadata={"alias": "remoteDestIp"}
    )
    source_ip: PolicyObjectEntriesSourceIpOptionsDef = _field(metadata={"alias": "sourceIp"})


@dataclass
class Data84:
    # Mirror List
    entries: List[Entries54]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut24:
    """
    mirror profile parcel schema for PUT request
    """

    data: Data84
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class PolicyObjectEntriesBurstOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyObjectEntriesExceedOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesExceedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectEntriesRateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries55:
    burst: PolicyObjectEntriesBurstOptionsDef
    exceed: PolicyObjectEntriesExceedOptionsDef
    rate: PolicyObjectEntriesRateOptionsDef


@dataclass
class Data85:
    # Policer Entries
    entries: List[Entries55]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut25:
    """
    policer profile parcel schema for PUT request
    """

    data: Data85
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntriesIpv4AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntriesIpv4PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanPolicyObjectEntriesLeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanPolicyObjectEntriesGeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries56:
    ipv4_address: V1FeatureProfileSdwanPolicyObjectEntriesIpv4AddressOptionsDef = _field(
        metadata={"alias": "ipv4Address"}
    )
    ipv4_prefix_length: V1FeatureProfileSdwanPolicyObjectEntriesIpv4PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )
    ge_range_prefix_length: Optional[
        FeatureProfileSdwanPolicyObjectEntriesGeRangePrefixLengthOptionsDef
    ] = _field(default=None, metadata={"alias": "geRangePrefixLength"})
    le_range_prefix_length: Optional[
        FeatureProfileSdwanPolicyObjectEntriesLeRangePrefixLengthOptionsDef
    ] = _field(default=None, metadata={"alias": "leRangePrefixLength"})


@dataclass
class Data86:
    # IPv4 Prefix List
    entries: List[Entries56]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut26:
    """
    Ipv4 prefix profile parcel schema
    """

    data: Data86
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries57:
    standard_community: StandardCommunityOptionsDef = _field(
        metadata={"alias": "standardCommunity"}
    )


@dataclass
class Data87:
    # Standard Community List
    entries: List[Entries57]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut27:
    """
    standard Community list profile parcel schema
    """

    data: Data87
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries58:
    vpn: EntriesVpnOptionsDef


@dataclass
class Data88:
    # VPN List
    entries: List[Entries58]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut28:
    """
    vpn list profile parcel schema
    """

    data: Data88
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesMapColorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesMapColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectOneOfEntriesMapDscpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyObjectMap:
    color: PolicyObjectOneOfEntriesMapColorOptionsDef
    dscp: Optional[PolicyObjectOneOfEntriesMapDscpOptionsDef] = _field(default=None)


@dataclass
class PolicyObjectForwardingClass1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries59:
    # Forwarding Class Name
    forwarding_class: Union[PolicyObjectForwardingClass1, ForwardingClass2] = _field(
        metadata={"alias": "forwardingClass"}
    )
    # Map
    map: List[PolicyObjectMap]


@dataclass
class Data89:
    # App Probe List
    entries: List[Entries59]


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut29:
    """
    app-probe profile parcel schema for PUT request
    """

    data: Data89
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesTlocOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesColorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        FeatureProfileSdwanPolicyObjectEntriesColorDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class PolicyObjectOneOfEntriesEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectOneOfEntriesPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries60:
    color: FeatureProfileSdwanPolicyObjectOneOfEntriesColorOptionsDef
    encap: PolicyObjectOneOfEntriesEncapOptionsDef
    tloc: PolicyObjectOneOfEntriesTlocOptionsDef
    preference: Optional[PolicyObjectOneOfEntriesPreferenceOptionsDef] = _field(default=None)


@dataclass
class Data90:
    # TLOC List
    entries: Optional[List[Entries60]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut30:
    """
    tloc profile parcel schema for PUT request
    """

    data: Data90
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesColorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        V1FeatureProfileSdwanPolicyObjectEntriesColorDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class Entries61:
    color: V1FeatureProfileSdwanPolicyObjectOneOfEntriesColorOptionsDef


@dataclass
class Data91:
    # Color List
    entries: Optional[List[Entries61]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut31:
    """
    color profile parcel schema for PUT request
    """

    data: Data91
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class PolicyObjectOneOfEntriesColorPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[PolicyObjectValue]  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectOneOfEntriesPathPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectEntriesPathPreferenceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectPrimaryPreference1:
    color_preference: PolicyObjectOneOfEntriesColorPreferenceOptionsDef = _field(
        metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[PolicyObjectOneOfEntriesPathPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class SdwanPolicyObjectOneOfEntriesColorPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[SdwanPolicyObjectValue]  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectOneOfEntriesPathPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesPathPreferenceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectPrimaryPreference2:
    path_preference: SdwanPolicyObjectOneOfEntriesPathPreferenceOptionsDef = _field(
        metadata={"alias": "pathPreference"}
    )
    color_preference: Optional[SdwanPolicyObjectOneOfEntriesColorPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesColorPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[FeatureProfileSdwanPolicyObjectValue]  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesPathPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanPolicyObjectEntriesPathPreferenceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectSecondaryPreference:
    """
    Object with an color and path preference
    """

    color_preference: Optional[
        FeatureProfileSdwanPolicyObjectOneOfEntriesColorPreferenceOptionsDef
    ] = _field(default=None, metadata={"alias": "colorPreference"})
    path_preference: Optional[
        FeatureProfileSdwanPolicyObjectOneOfEntriesPathPreferenceOptionsDef
    ] = _field(default=None, metadata={"alias": "pathPreference"})


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesColorPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[V1FeatureProfileSdwanPolicyObjectValue]  # pytype: disable=annotation-type-mismatch


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesPathPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanPolicyObjectEntriesPathPreferenceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectTertiaryPreference:
    """
    Object with an color and path preference
    """

    color_preference: Optional[
        V1FeatureProfileSdwanPolicyObjectOneOfEntriesColorPreferenceOptionsDef
    ] = _field(default=None, metadata={"alias": "colorPreference"})
    path_preference: Optional[
        V1FeatureProfileSdwanPolicyObjectOneOfEntriesPathPreferenceOptionsDef
    ] = _field(default=None, metadata={"alias": "pathPreference"})


@dataclass
class Entries62:
    # Object with an color and path preference
    primary_preference: Union[PolicyObjectPrimaryPreference1, PolicyObjectPrimaryPreference2] = (
        _field(metadata={"alias": "primaryPreference"})
    )
    # Object with an color and path preference
    secondary_preference: Optional[PolicyObjectSecondaryPreference] = _field(
        default=None, metadata={"alias": "secondaryPreference"}
    )
    # Object with an color and path preference
    tertiary_preference: Optional[PolicyObjectTertiaryPreference] = _field(
        default=None, metadata={"alias": "tertiaryPreference"}
    )


@dataclass
class Data92:
    # Preferred Color Group List
    entries: Optional[List[Entries62]] = _field(default=None)


@dataclass
class Schema2HubGeneratedPolicyobjectlisttypePut32:
    """
    preferred-color-group profile parcel schema for PUT request
    """

    data: Data92
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanPolicyObjectSecurityDataIpPrefixPayload:
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
    payload: Optional[
        Union[
            Schema2HubGeneratedPolicyobjectlisttypePut1,
            Schema2HubGeneratedPolicyobjectlisttypePut2,
            Schema2HubGeneratedPolicyobjectlisttypePut3,
            Schema2HubGeneratedPolicyobjectlisttypePut4,
            Schema2HubGeneratedPolicyobjectlisttypePut5,
            Schema2HubGeneratedPolicyobjectlisttypePut6,
            Schema2HubGeneratedPolicyobjectlisttypePut7,
            Schema2HubGeneratedPolicyobjectlisttypePut8,
            Schema2HubGeneratedPolicyobjectlisttypePut9,
            Schema2HubGeneratedPolicyobjectlisttypePut10,
            Schema2HubGeneratedPolicyobjectlisttypePut11,
            Schema2HubGeneratedPolicyobjectlisttypePut12,
            Schema2HubGeneratedPolicyobjectlisttypePut13,
            Schema2HubGeneratedPolicyobjectlisttypePut14,
            Schema2HubGeneratedPolicyobjectlisttypePut15,
            Schema2HubGeneratedPolicyobjectlisttypePut16,
            Schema2HubGeneratedPolicyobjectlisttypePut17,
            Schema2HubGeneratedPolicyobjectlisttypePut18,
            Schema2HubGeneratedPolicyobjectlisttypePut19,
            Schema2HubGeneratedPolicyobjectlisttypePut20,
            Schema2HubGeneratedPolicyobjectlisttypePut21,
            Schema2HubGeneratedPolicyobjectlisttypePut22,
            Schema2HubGeneratedPolicyobjectlisttypePut23,
            Schema2HubGeneratedPolicyobjectlisttypePut24,
            Schema2HubGeneratedPolicyobjectlisttypePut25,
            Schema2HubGeneratedPolicyobjectlisttypePut26,
            Schema2HubGeneratedPolicyobjectlisttypePut27,
            Schema2HubGeneratedPolicyobjectlisttypePut28,
            Schema2HubGeneratedPolicyobjectlisttypePut29,
            Schema2HubGeneratedPolicyobjectlisttypePut30,
            Schema2HubGeneratedPolicyobjectlisttypePut31,
            Schema2HubGeneratedPolicyobjectlisttypePut32,
        ]
    ] = _field(default=None)


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data93:
    entries: List[Entries]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest1:
    """
    security-data-ip-prefix profile parcel schema for PUT request
    """

    data: Data93
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesPatternOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Must be valid FQDN
    value: str


@dataclass
class Entries63:
    pattern: SdwanPolicyObjectOneOfEntriesPatternOptionsDef


@dataclass
class Data94:
    entries: List[Entries63]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest2:
    """
    security-data-fqdn-prefix profile parcel schema for PUT request
    """

    data: Data94
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries64:
    port: SdwanPolicyObjectOneOfEntriesPortOptionsDef


@dataclass
class Data95:
    # Port List
    entries: List[Entries64]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest3:
    """
    Port profile parcel schema for PUT request
    """

    data: Data95
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesAppOptionsDef5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries117:
    app: OneOfEntriesAppOptionsDef5
    app_family: Optional[OneOfEntriesAppFamilyOptionsDef5] = _field(
        default=None, metadata={"alias": "appFamily"}
    )


@dataclass
class OneOfEntriesAppOptionsDef6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries214:
    app_family: OneOfEntriesAppFamilyOptionsDef6 = _field(metadata={"alias": "appFamily"})
    app: Optional[OneOfEntriesAppOptionsDef6] = _field(default=None)


@dataclass
class Data96:
    # Localapp list
    entries: List[Union[Entries117, Entries214]]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest4:
    """
    security-localapp profile parcel schema for PUT request
    """

    data: Data96
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesNameServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # String cannot start with a '.' or a '*', be empty, or be more than 240 characters
    value: str


@dataclass
class Entries65:
    name_server: SdwanPolicyObjectOneOfEntriesNameServerOptionsDef = _field(
        metadata={"alias": "nameServer"}
    )


@dataclass
class Data97:
    entries: List[Entries65]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest5:
    """
    security-localdomain profile parcel schema for PUT request
    """

    data: Data97
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesGeneratorIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanPolicyObjectOneOfEntriesSignatureIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries66:
    generator_id: SdwanPolicyObjectOneOfEntriesGeneratorIdOptionsDef = _field(
        metadata={"alias": "generatorId"}
    )
    signature_id: SdwanPolicyObjectOneOfEntriesSignatureIdOptionsDef = _field(
        metadata={"alias": "signatureId"}
    )


@dataclass
class Data98:
    # Ips Signature
    entries: List[Entries66]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest6:
    """
    security-ipssignature profile parcel schema for PUT request
    """

    data: Data98
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectEntriesUrlListOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries67:
    pattern: SdwanPolicyObjectEntriesUrlListOptionsDef


@dataclass
class Data99:
    # URL List
    entries: List[Entries67]
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest7:
    """
    URL List profile parcel schema for PUT request
    """

    data: Data99
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesProtocolNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesProtocolNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries68:
    protocol_name: SdwanPolicyObjectOneOfEntriesProtocolNameOptionsDef = _field(
        metadata={"alias": "protocolName"}
    )


@dataclass
class Data100:
    entries: List[Entries68]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest8:
    """
    security-protocolname profile parcel schema for PUT request
    """

    data: Data100
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesCountryOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        FeatureProfileSdwanPolicyObjectEntriesCountryDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesContinentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanPolicyObjectEntriesContinentDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries118:
    country: FeatureProfileSdwanPolicyObjectOneOfEntriesCountryOptionsDef
    continent: Optional[FeatureProfileSdwanPolicyObjectOneOfEntriesContinentOptionsDef] = _field(
        default=None
    )


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesCountryOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanPolicyObjectEntriesCountryDef  # pytype: disable=annotation-type-mismatch


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesContinentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanPolicyObjectEntriesContinentDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries215:
    continent: V1FeatureProfileSdwanPolicyObjectOneOfEntriesContinentOptionsDef
    country: Optional[V1FeatureProfileSdwanPolicyObjectOneOfEntriesCountryOptionsDef] = _field(
        default=None
    )


@dataclass
class Data101:
    # Geolocation  List
    entries: List[Union[Entries118, Entries215]]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest9:
    """
    Geolocation profile parcel schema for PUT request
    """

    data: Data101
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesUserOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectOneOfEntriesUserGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class Entries119:
    user: FeatureProfileSdwanPolicyObjectOneOfEntriesUserOptionsDef
    user_group: Optional[FeatureProfileSdwanPolicyObjectOneOfEntriesUserGroupOptionsDef] = _field(
        default=None, metadata={"alias": "userGroup"}
    )


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesUserOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesUserGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    # Mustn't contain non standard unicode characters
    value: str


@dataclass
class Entries216:
    user_group: V1FeatureProfileSdwanPolicyObjectOneOfEntriesUserGroupOptionsDef = _field(
        metadata={"alias": "userGroup"}
    )
    user: Optional[V1FeatureProfileSdwanPolicyObjectOneOfEntriesUserOptionsDef] = _field(
        default=None
    )


@dataclass
class Data102:
    # Array of Users and User Groups
    entries: List[Union[Entries119, Entries216]]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest10:
    """
    security-identity profile parcel schema for PUT request
    """

    data: Data102
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesSgtNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanPolicyObjectOneOfEntriesTagOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries69:
    sgt_name: SdwanPolicyObjectOneOfEntriesSgtNameOptionsDef = _field(metadata={"alias": "sgtName"})
    tag: SdwanPolicyObjectOneOfEntriesTagOptionsDef


@dataclass
class Data103:
    entries: List[Entries69]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest11:
    """
    security-scalablegrouptag profile parcel schema for PUT request
    """

    data: Data103
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data104:
    entries: List[None]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest12:
    """
    security-zone profile parcel schema for PUT request
    """

    data: Data104
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesAppOptionsDef7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries120:
    app: OneOfEntriesAppOptionsDef7
    app_family: Optional[OneOfEntriesAppFamilyOptionsDef7] = _field(
        default=None, metadata={"alias": "appFamily"}
    )


@dataclass
class OneOfEntriesAppOptionsDef8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesAppFamilyOptionsDef8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries217:
    app_family: OneOfEntriesAppFamilyOptionsDef8 = _field(metadata={"alias": "appFamily"})
    app: Optional[OneOfEntriesAppOptionsDef8] = _field(default=None)


@dataclass
class Data105:
    # centralized-applist list
    entries: List[Union[Entries120, Entries217]]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest13:
    """
    security-localapp profile parcel schema for PUT request
    """

    data: Data105
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesLatencyOptionsDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLossOptionsDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfEntriesCriteriaOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanPolicyObjectEntriesCriteriaDef


@dataclass
class OneOfEntriesLossOptionsDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLatencyOptionsDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanPolicyObjectFallbackBestTunnel:
    """
    Object with a criteria and variance
    """

    criteria: Optional[V1FeatureProfileSdwanPolicyObjectOneOfEntriesCriteriaOptionsDef] = _field(
        default=None
    )
    jitter_variance: Optional[OneOfEntriesJitterOptionsDef4] = _field(
        default=None, metadata={"alias": "jitterVariance"}
    )
    latency_variance: Optional[OneOfEntriesLatencyOptionsDef4] = _field(
        default=None, metadata={"alias": "latencyVariance"}
    )
    loss_variance: Optional[OneOfEntriesLossOptionsDef4] = _field(
        default=None, metadata={"alias": "lossVariance"}
    )


@dataclass
class Entries121:
    latency: OneOfEntriesLatencyOptionsDef3
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[V1FeatureProfileSdwanPolicyObjectFallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[OneOfEntriesJitterOptionsDef3] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef3] = _field(default=None)


@dataclass
class OneOfEntriesLatencyOptionsDef5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLossOptionsDef5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesCriteriaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesCriteriaDef1


@dataclass
class OneOfEntriesLossOptionsDef6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLatencyOptionsDef6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FallbackBestTunnel1:
    """
    Object with a criteria and variance
    """

    criteria: Optional[OneOfEntriesCriteriaOptionsDef1] = _field(default=None)
    jitter_variance: Optional[OneOfEntriesJitterOptionsDef6] = _field(
        default=None, metadata={"alias": "jitterVariance"}
    )
    latency_variance: Optional[OneOfEntriesLatencyOptionsDef6] = _field(
        default=None, metadata={"alias": "latencyVariance"}
    )
    loss_variance: Optional[OneOfEntriesLossOptionsDef6] = _field(
        default=None, metadata={"alias": "lossVariance"}
    )


@dataclass
class Entries218:
    loss: OneOfEntriesLossOptionsDef5
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel1] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[OneOfEntriesJitterOptionsDef5] = _field(default=None)
    latency: Optional[OneOfEntriesLatencyOptionsDef5] = _field(default=None)


@dataclass
class OneOfEntriesLatencyOptionsDef7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLossOptionsDef7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesCriteriaOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesCriteriaDef2


@dataclass
class OneOfEntriesLossOptionsDef8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLatencyOptionsDef8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FallbackBestTunnel2:
    """
    Object with a criteria and variance
    """

    criteria: Optional[OneOfEntriesCriteriaOptionsDef2] = _field(default=None)
    jitter_variance: Optional[OneOfEntriesJitterOptionsDef8] = _field(
        default=None, metadata={"alias": "jitterVariance"}
    )
    latency_variance: Optional[OneOfEntriesLatencyOptionsDef8] = _field(
        default=None, metadata={"alias": "latencyVariance"}
    )
    loss_variance: Optional[OneOfEntriesLossOptionsDef8] = _field(
        default=None, metadata={"alias": "lossVariance"}
    )


@dataclass
class Entries33_1:
    jitter: OneOfEntriesJitterOptionsDef7
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel2] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    latency: Optional[OneOfEntriesLatencyOptionsDef7] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef7] = _field(default=None)


@dataclass
class Data106:
    # Sla class List
    entries: List[Union[Entries121, Entries218, Entries33_1]]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest14:
    """
    Sla class profile parcel schema for PUT request
    """

    data: Data106
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries70:
    as_path: EntriesAsPathOptionsDef = _field(metadata={"alias": "asPath"})


@dataclass
class Data107:
    # As path List Number
    as_path_list_num: AsPathListNum = _field(metadata={"alias": "asPathListNum"})
    # AS Path List
    entries: List[Entries70]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest15:
    """
    as path profile parcel schema
    """

    data: Data107
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectEntriesQueueOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesQueueDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries71:
    queue: SdwanPolicyObjectEntriesQueueOptionsDef


@dataclass
class Data108:
    # class map List
    entries: List[Entries71]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest16:
    """
    class profile parcel schema for PUT request
    """

    data: Data108
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class EntriesIpv6AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EntriesIpv6PrefixLengthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries72:
    ipv6_address: EntriesIpv6AddressOptionsDef1 = _field(metadata={"alias": "ipv6Address"})
    ipv6_prefix_length: EntriesIpv6PrefixLengthOptionsDef1 = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )


@dataclass
class Data109:
    # IPv6 Prefix List
    entries: Optional[List[Entries72]] = _field(default=None)


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest17:
    """
    Ipv6 data prefix profile parcel schema for PUT request
    """

    data: Data109
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class EntriesIpv4AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EntriesIpv4PrefixLengthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries73:
    ipv4_address: EntriesIpv4AddressOptionsDef1 = _field(metadata={"alias": "ipv4Address"})
    ipv4_prefix_length: EntriesIpv4PrefixLengthOptionsDef1 = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )


@dataclass
class Data110:
    # IPv4 Data Prefix List
    entries: Optional[List[Entries73]] = _field(default=None)


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest18:
    """
    ipv4 data prefix profile parcel schema for PUT request
    """

    data: Data110
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class Data111:
    expanded_community_list: Union[
        OneOfExpandedCommunityOptionsDef1, OneOfExpandedCommunityOptionsDef2
    ] = _field(metadata={"alias": "expandedCommunityList"})


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest19:
    """
    expanded Community list profile parcel schema
    """

    data: Data111
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries74:
    ext_community: EntriesExtCommunityOptionsDef = _field(metadata={"alias": "extCommunity"})


@dataclass
class Data112:
    # Extended Community List
    entries: List[Entries74]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest20:
    """
    extended community list profile parcel schema
    """

    data: Data112
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries122:
    address_type: OneOfEntriesAddressTypeHostOptionsDef = _field(metadata={"alias": "addressType"})
    host: Union[OneOfEntriesHostOptionsDef1, OneOfEntriesHostOptionsDef2]


@dataclass
class Entries219:
    address_type: OneOfEntriesAddressTypeIpPrefixOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    ip_prefix: Union[OneOfEntriesIpPrefixOptionsDef1, OneOfEntriesIpPrefixOptionsDef2] = _field(
        metadata={"alias": "ipPrefix"}
    )


@dataclass
class Entries34_1:
    address_type: OneOfEntriesAddressTypeObjectGroupOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntries4:
    address_type: OneOfEntriesAddressTypeHostRangeOptionsDef = _field(
        metadata={"alias": "addressType"}
    )
    # Host Address Range
    host_range: HostRange = _field(metadata={"alias": "hostRange"})


@dataclass
class Data113:
    # object-group Entries
    entries: List[
        Union[Entries122, Entries219, Entries34_1, V1FeatureProfileSdwanPolicyObjectEntries4]
    ]
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest21:
    """
    Ipv4 Network Object Group profile parcel schema
    """

    data: Data113
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanPolicyObjectOneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries123:
    object_group: ParcelReferenceDef = _field(metadata={"alias": "objectGroup"})


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntries21:
    protocol: Protocol
    destination_ports: Optional[DestinationPorts] = _field(
        default=None, metadata={"alias": "destinationPorts"}
    )
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntries22:
    protocol: OneOfEntriesProtocolOptionsDef
    # Destination Ports
    destination_ports: Optional[
        Union[DestinationPorts1, DestinationPorts2, DestinationPorts3, DestinationPorts4]
    ] = _field(default=None, metadata={"alias": "destinationPorts"})
    icmp_msg: Optional[Union[OneOfEntriesIcmpMsgOptionsDef1, OneOfEntriesIcmpMsgOptionsDef2]] = (
        _field(default=None, metadata={"alias": "icmpMsg"})
    )
    # Source Ports
    source_ports: Optional[Union[SourcePorts1, SourcePorts2, SourcePorts3, SourcePorts4]] = _field(
        default=None, metadata={"alias": "sourcePorts"}
    )


@dataclass
class Data114:
    # object-group Entries
    entries: List[
        Union[
            Entries123,
            Union[
                V1FeatureProfileSdwanPolicyObjectEntries21,
                V1FeatureProfileSdwanPolicyObjectEntries22,
            ],
        ]
    ]
    description: Optional[
        Union[
            V1FeatureProfileSdwanPolicyObjectOneOfDescriptionOptionsDef1,
            OneOfDescriptionOptionsDef2,
            OneOfDescriptionOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest22:
    """
    Ipv4 Service Object Group profile parcel schema
    """

    data: Data114
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EntriesIpv6AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EntriesIpv6PrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries75:
    ipv6_address: EntriesIpv6AddressOptionsDef2 = _field(metadata={"alias": "ipv6Address"})
    ipv6_prefix_length: EntriesIpv6PrefixLengthOptionsDef2 = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )
    ge_range_prefix_length: Optional[EntriesGeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "geRangePrefixLength"}
    )
    le_range_prefix_length: Optional[EntriesLeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "leRangePrefixLength"}
    )


@dataclass
class Data115:
    # IPv6 Prefix List
    entries: List[Entries75]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest23:
    """
    Ipv6 prefix profile parcel schema
    """

    data: Data115
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectEntriesRemoteDestIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SdwanPolicyObjectEntriesSourceIpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class Entries76:
    remote_dest_ip: SdwanPolicyObjectEntriesRemoteDestIpOptionsDef = _field(
        metadata={"alias": "remoteDestIp"}
    )
    source_ip: SdwanPolicyObjectEntriesSourceIpOptionsDef = _field(metadata={"alias": "sourceIp"})


@dataclass
class Data116:
    # Mirror List
    entries: List[Entries76]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest24:
    """
    mirror profile parcel schema for PUT request
    """

    data: Data116
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class SdwanPolicyObjectEntriesBurstOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanPolicyObjectEntriesExceedOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesExceedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectEntriesRateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries77:
    burst: SdwanPolicyObjectEntriesBurstOptionsDef
    exceed: SdwanPolicyObjectEntriesExceedOptionsDef
    rate: SdwanPolicyObjectEntriesRateOptionsDef


@dataclass
class Data117:
    # Policer Entries
    entries: List[Entries77]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest25:
    """
    policer profile parcel schema for PUT request
    """

    data: Data117
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class EntriesIpv4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EntriesIpv4PrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntriesLeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanPolicyObjectEntriesGeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries78:
    ipv4_address: EntriesIpv4AddressOptionsDef2 = _field(metadata={"alias": "ipv4Address"})
    ipv4_prefix_length: EntriesIpv4PrefixLengthOptionsDef2 = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )
    ge_range_prefix_length: Optional[
        V1FeatureProfileSdwanPolicyObjectEntriesGeRangePrefixLengthOptionsDef
    ] = _field(default=None, metadata={"alias": "geRangePrefixLength"})
    le_range_prefix_length: Optional[
        V1FeatureProfileSdwanPolicyObjectEntriesLeRangePrefixLengthOptionsDef
    ] = _field(default=None, metadata={"alias": "leRangePrefixLength"})


@dataclass
class Data118:
    # IPv4 Prefix List
    entries: List[Entries78]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest26:
    """
    Ipv4 prefix profile parcel schema
    """

    data: Data118
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries79:
    standard_community: StandardCommunityOptionsDef = _field(
        metadata={"alias": "standardCommunity"}
    )


@dataclass
class Data119:
    # Standard Community List
    entries: List[Entries79]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest27:
    """
    standard Community list profile parcel schema
    """

    data: Data119
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Entries80:
    vpn: EntriesVpnOptionsDef


@dataclass
class Data120:
    # VPN List
    entries: List[Entries80]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest28:
    """
    vpn list profile parcel schema
    """

    data: Data120
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesMapColorOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesMapColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectOneOfEntriesMapDscpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanPolicyObjectMap:
    color: SdwanPolicyObjectOneOfEntriesMapColorOptionsDef
    dscp: Optional[SdwanPolicyObjectOneOfEntriesMapDscpOptionsDef] = _field(default=None)


@dataclass
class SdwanPolicyObjectForwardingClass1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries81:
    # Forwarding Class Name
    forwarding_class: Union[SdwanPolicyObjectForwardingClass1, ForwardingClass2] = _field(
        metadata={"alias": "forwardingClass"}
    )
    # Map
    map: List[SdwanPolicyObjectMap]


@dataclass
class Data121:
    # App Probe List
    entries: List[Entries81]


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest29:
    """
    app-probe profile parcel schema for PUT request
    """

    data: Data121
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanPolicyObjectOneOfEntriesTlocOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesColorDef1  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectOneOfEntriesEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectEntriesEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectOneOfEntriesPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries82:
    color: OneOfEntriesColorOptionsDef1
    encap: SdwanPolicyObjectOneOfEntriesEncapOptionsDef
    tloc: SdwanPolicyObjectOneOfEntriesTlocOptionsDef
    preference: Optional[SdwanPolicyObjectOneOfEntriesPreferenceOptionsDef] = _field(default=None)


@dataclass
class Data122:
    # TLOC List
    entries: Optional[List[Entries82]] = _field(default=None)


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest30:
    """
    tloc profile parcel schema for PUT request
    """

    data: Data122
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfEntriesColorOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesColorDef2  # pytype: disable=annotation-type-mismatch


@dataclass
class Entries83:
    color: OneOfEntriesColorOptionsDef2


@dataclass
class Data123:
    # Color List
    entries: Optional[List[Entries83]] = _field(default=None)


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest31:
    """
    color profile parcel schema for PUT request
    """

    data: Data123
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class OneOfEntriesColorPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Value1]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesPathPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesPathPreferenceDef1  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectPrimaryPreference1:
    color_preference: OneOfEntriesColorPreferenceOptionsDef1 = _field(
        metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef1] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class OneOfEntriesColorPreferenceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Value2]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesPathPreferenceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesPathPreferenceDef2  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectPrimaryPreference2:
    path_preference: OneOfEntriesPathPreferenceOptionsDef2 = _field(
        metadata={"alias": "pathPreference"}
    )
    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef2] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )


@dataclass
class OneOfEntriesColorPreferenceOptionsDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Value3]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesPathPreferenceOptionsDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesPathPreferenceDef3  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectSecondaryPreference:
    """
    Object with an color and path preference
    """

    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef3] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef3] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class OneOfEntriesColorPreferenceOptionsDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Value4]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEntriesPathPreferenceOptionsDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesPathPreferenceDef4  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectTertiaryPreference:
    """
    Object with an color and path preference
    """

    color_preference: Optional[OneOfEntriesColorPreferenceOptionsDef4] = _field(
        default=None, metadata={"alias": "colorPreference"}
    )
    path_preference: Optional[OneOfEntriesPathPreferenceOptionsDef4] = _field(
        default=None, metadata={"alias": "pathPreference"}
    )


@dataclass
class Entries84:
    # Object with an color and path preference
    primary_preference: Union[
        SdwanPolicyObjectPrimaryPreference1, SdwanPolicyObjectPrimaryPreference2
    ] = _field(metadata={"alias": "primaryPreference"})
    # Object with an color and path preference
    secondary_preference: Optional[SdwanPolicyObjectSecondaryPreference] = _field(
        default=None, metadata={"alias": "secondaryPreference"}
    )
    # Object with an color and path preference
    tertiary_preference: Optional[SdwanPolicyObjectTertiaryPreference] = _field(
        default=None, metadata={"alias": "tertiaryPreference"}
    )


@dataclass
class Data124:
    # Preferred Color Group List
    entries: Optional[List[Entries84]] = _field(default=None)


@dataclass
class EditDataPrefixProfileParcelForPolicyObjectPutRequest32:
    """
    preferred-color-group profile parcel schema for PUT request
    """

    data: Data124
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
