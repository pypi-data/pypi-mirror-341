# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

TimezoneDef = Literal[
    "Africa/Abidjan",
    "Africa/Accra",
    "Africa/Addis_Ababa",
    "Africa/Algiers",
    "Africa/Asmara",
    "Africa/Bamako",
    "Africa/Bangui",
    "Africa/Banjul",
    "Africa/Bissau",
    "Africa/Blantyre",
    "Africa/Brazzaville",
    "Africa/Bujumbura",
    "Africa/Cairo",
    "Africa/Casablanca",
    "Africa/Ceuta",
    "Africa/Conakry",
    "Africa/Dakar",
    "Africa/Dar_es_Salaam",
    "Africa/Djibouti",
    "Africa/Douala",
    "Africa/El_Aaiun",
    "Africa/Freetown",
    "Africa/Gaborone",
    "Africa/Harare",
    "Africa/Johannesburg",
    "Africa/Juba",
    "Africa/Kampala",
    "Africa/Khartoum",
    "Africa/Kigali",
    "Africa/Kinshasa",
    "Africa/Lagos",
    "Africa/Libreville",
    "Africa/Lome",
    "Africa/Luanda",
    "Africa/Lubumbashi",
    "Africa/Lusaka",
    "Africa/Malabo",
    "Africa/Maputo",
    "Africa/Maseru",
    "Africa/Mbabane",
    "Africa/Mogadishu",
    "Africa/Monrovia",
    "Africa/Nairobi",
    "Africa/Ndjamena",
    "Africa/Niamey",
    "Africa/Nouakchott",
    "Africa/Ouagadougou",
    "Africa/Porto-Novo",
    "Africa/Sao_Tome",
    "Africa/Tripoli",
    "Africa/Tunis",
    "Africa/Windhoek",
    "America/Adak",
    "America/Anchorage",
    "America/Anguilla",
    "America/Antigua",
    "America/Araguaina",
    "America/Argentina/Buenos_Aires",
    "America/Argentina/Catamarca",
    "America/Argentina/Cordoba",
    "America/Argentina/Jujuy",
    "America/Argentina/La_Rioja",
    "America/Argentina/Mendoza",
    "America/Argentina/Rio_Gallegos",
    "America/Argentina/Salta",
    "America/Argentina/San_Juan",
    "America/Argentina/San_Luis",
    "America/Argentina/Tucuman",
    "America/Argentina/Ushuaia",
    "America/Aruba",
    "America/Asuncion",
    "America/Atikokan",
    "America/Bahia",
    "America/Bahia_Banderas",
    "America/Barbados",
    "America/Belem",
    "America/Belize",
    "America/Blanc-Sablon",
    "America/Boa_Vista",
    "America/Bogota",
    "America/Boise",
    "America/Cambridge_Bay",
    "America/Campo_Grande",
    "America/Cancun",
    "America/Caracas",
    "America/Cayenne",
    "America/Cayman",
    "America/Chicago",
    "America/Chihuahua",
    "America/Costa_Rica",
    "America/Creston",
    "America/Cuiaba",
    "America/Curacao",
    "America/Danmarkshavn",
    "America/Dawson",
    "America/Dawson_Creek",
    "America/Denver",
    "America/Detroit",
    "America/Dominica",
    "America/Edmonton",
    "America/Eirunepe",
    "America/El_Salvador",
    "America/Fortaleza",
    "America/Glace_Bay",
    "America/Godthab",
    "America/Goose_Bay",
    "America/Grand_Turk",
    "America/Grenada",
    "America/Guadeloupe",
    "America/Guatemala",
    "America/Guayaquil",
    "America/Guyana",
    "America/Halifax",
    "America/Havana",
    "America/Hermosillo",
    "America/Indiana/Indianapolis",
    "America/Indiana/Knox",
    "America/Indiana/Marengo",
    "America/Indiana/Petersburg",
    "America/Indiana/Tell_City",
    "America/Indiana/Vevay",
    "America/Indiana/Vincennes",
    "America/Indiana/Winamac",
    "America/Inuvik",
    "America/Iqaluit",
    "America/Jamaica",
    "America/Juneau",
    "America/Kentucky/Louisville",
    "America/Kentucky/Monticello",
    "America/Kralendijk",
    "America/La_Paz",
    "America/Lima",
    "America/Los_Angeles",
    "America/Lower_Princes",
    "America/Maceio",
    "America/Managua",
    "America/Manaus",
    "America/Marigot",
    "America/Martinique",
    "America/Matamoros",
    "America/Mazatlan",
    "America/Menominee",
    "America/Merida",
    "America/Metlakatla",
    "America/Mexico_City",
    "America/Miquelon",
    "America/Moncton",
    "America/Monterrey",
    "America/Montevideo",
    "America/Montserrat",
    "America/Nassau",
    "America/New_York",
    "America/Nipigon",
    "America/Nome",
    "America/Noronha",
    "America/North_Dakota/Beulah",
    "America/North_Dakota/Center",
    "America/North_Dakota/New_Salem",
    "America/Ojinaga",
    "America/Panama",
    "America/Pangnirtung",
    "America/Paramaribo",
    "America/Phoenix",
    "America/Port-au-Prince",
    "America/Port_of_Spain",
    "America/Porto_Velho",
    "America/Puerto_Rico",
    "America/Rainy_River",
    "America/Rankin_Inlet",
    "America/Recife",
    "America/Regina",
    "America/Resolute",
    "America/Rio_Branco",
    "America/Santa_Isabel",
    "America/Santarem",
    "America/Santiago",
    "America/Santo_Domingo",
    "America/Sao_Paulo",
    "America/Scoresbysund",
    "America/Sitka",
    "America/St_Barthelemy",
    "America/St_Johns",
    "America/St_Kitts",
    "America/St_Lucia",
    "America/St_Thomas",
    "America/St_Vincent",
    "America/Swift_Current",
    "America/Tegucigalpa",
    "America/Thule",
    "America/Thunder_Bay",
    "America/Tijuana",
    "America/Toronto",
    "America/Tortola",
    "America/Vancouver",
    "America/Whitehorse",
    "America/Winnipeg",
    "America/Yakutat",
    "America/Yellowknife",
    "Antarctica/Casey",
    "Antarctica/Davis",
    "Antarctica/DumontDUrville",
    "Antarctica/Macquarie",
    "Antarctica/Mawson",
    "Antarctica/McMurdo",
    "Antarctica/Palmer",
    "Antarctica/Rothera",
    "Antarctica/Syowa",
    "Antarctica/Vostok",
    "Arctic/Longyearbyen",
    "Asia/Aden",
    "Asia/Almaty",
    "Asia/Amman",
    "Asia/Anadyr",
    "Asia/Aqtau",
    "Asia/Aqtobe",
    "Asia/Ashgabat",
    "Asia/Baghdad",
    "Asia/Bahrain",
    "Asia/Baku",
    "Asia/Bangkok",
    "Asia/Beirut",
    "Asia/Bishkek",
    "Asia/Brunei",
    "Asia/Choibalsan",
    "Asia/Chongqing",
    "Asia/Colombo",
    "Asia/Damascus",
    "Asia/Dhaka",
    "Asia/Dili",
    "Asia/Dubai",
    "Asia/Dushanbe",
    "Asia/Gaza",
    "Asia/Harbin",
    "Asia/Hebron",
    "Asia/Ho_Chi_Minh",
    "Asia/Hong_Kong",
    "Asia/Hovd",
    "Asia/Irkutsk",
    "Asia/Jakarta",
    "Asia/Jayapura",
    "Asia/Jerusalem",
    "Asia/Kabul",
    "Asia/Kamchatka",
    "Asia/Karachi",
    "Asia/Kashgar",
    "Asia/Kathmandu",
    "Asia/Khandyga",
    "Asia/Kolkata",
    "Asia/Krasnoyarsk",
    "Asia/Kuala_Lumpur",
    "Asia/Kuching",
    "Asia/Kuwait",
    "Asia/Macau",
    "Asia/Magadan",
    "Asia/Makassar",
    "Asia/Manila",
    "Asia/Muscat",
    "Asia/Nicosia",
    "Asia/Novokuznetsk",
    "Asia/Novosibirsk",
    "Asia/Omsk",
    "Asia/Oral",
    "Asia/Phnom_Penh",
    "Asia/Pontianak",
    "Asia/Pyongyang",
    "Asia/Qatar",
    "Asia/Qyzylorda",
    "Asia/Rangoon",
    "Asia/Riyadh",
    "Asia/Sakhalin",
    "Asia/Samarkand",
    "Asia/Seoul",
    "Asia/Shanghai",
    "Asia/Singapore",
    "Asia/Taipei",
    "Asia/Tashkent",
    "Asia/Tbilisi",
    "Asia/Tehran",
    "Asia/Thimphu",
    "Asia/Tokyo",
    "Asia/Ulaanbaatar",
    "Asia/Urumqi",
    "Asia/Ust-Nera",
    "Asia/Vientiane",
    "Asia/Vladivostok",
    "Asia/Yakutsk",
    "Asia/Yekaterinburg",
    "Asia/Yerevan",
    "Atlantic/Azores",
    "Atlantic/Bermuda",
    "Atlantic/Canary",
    "Atlantic/Cape_Verde",
    "Atlantic/Faroe",
    "Atlantic/Madeira",
    "Atlantic/Reykjavik",
    "Atlantic/South_Georgia",
    "Atlantic/St_Helena",
    "Atlantic/Stanley",
    "Australia/Adelaide",
    "Australia/Brisbane",
    "Australia/Broken_Hill",
    "Australia/Currie",
    "Australia/Darwin",
    "Australia/Eucla",
    "Australia/Hobart",
    "Australia/Lindeman",
    "Australia/Lord_Howe",
    "Australia/Melbourne",
    "Australia/Perth",
    "Australia/Sydney",
    "Europe/Amsterdam",
    "Europe/Andorra",
    "Europe/Athens",
    "Europe/Belgrade",
    "Europe/Berlin",
    "Europe/Bratislava",
    "Europe/Brussels",
    "Europe/Bucharest",
    "Europe/Budapest",
    "Europe/Busingen",
    "Europe/Chisinau",
    "Europe/Copenhagen",
    "Europe/Dublin",
    "Europe/Gibraltar",
    "Europe/Guernsey",
    "Europe/Helsinki",
    "Europe/Isle_of_Man",
    "Europe/Istanbul",
    "Europe/Jersey",
    "Europe/Kaliningrad",
    "Europe/Kiev",
    "Europe/Lisbon",
    "Europe/Ljubljana",
    "Europe/London",
    "Europe/Luxembourg",
    "Europe/Madrid",
    "Europe/Malta",
    "Europe/Mariehamn",
    "Europe/Minsk",
    "Europe/Monaco",
    "Europe/Moscow",
    "Europe/Oslo",
    "Europe/Paris",
    "Europe/Podgorica",
    "Europe/Prague",
    "Europe/Riga",
    "Europe/Rome",
    "Europe/Samara",
    "Europe/San_Marino",
    "Europe/Sarajevo",
    "Europe/Simferopol",
    "Europe/Skopje",
    "Europe/Sofia",
    "Europe/Stockholm",
    "Europe/Tallinn",
    "Europe/Tirane",
    "Europe/Uzhgorod",
    "Europe/Vaduz",
    "Europe/Vatican",
    "Europe/Vienna",
    "Europe/Vilnius",
    "Europe/Volgograd",
    "Europe/Warsaw",
    "Europe/Zagreb",
    "Europe/Zaporozhye",
    "Europe/Zurich",
    "Indian/Antananarivo",
    "Indian/Chagos",
    "Indian/Christmas",
    "Indian/Cocos",
    "Indian/Comoro",
    "Indian/Kerguelen",
    "Indian/Mahe",
    "Indian/Maldives",
    "Indian/Mauritius",
    "Indian/Mayotte",
    "Indian/Reunion",
    "Pacific/Apia",
    "Pacific/Auckland",
    "Pacific/Chatham",
    "Pacific/Chuuk",
    "Pacific/Easter",
    "Pacific/Efate",
    "Pacific/Enderbury",
    "Pacific/Fakaofo",
    "Pacific/Fiji",
    "Pacific/Funafuti",
    "Pacific/Galapagos",
    "Pacific/Gambier",
    "Pacific/Guadalcanal",
    "Pacific/Guam",
    "Pacific/Honolulu",
    "Pacific/Johnston",
    "Pacific/Kiritimati",
    "Pacific/Kosrae",
    "Pacific/Kwajalein",
    "Pacific/Majuro",
    "Pacific/Marquesas",
    "Pacific/Midway",
    "Pacific/Nauru",
    "Pacific/Niue",
    "Pacific/Norfolk",
    "Pacific/Noumea",
    "Pacific/Pago_Pago",
    "Pacific/Palau",
    "Pacific/Pitcairn",
    "Pacific/Pohnpei",
    "Pacific/Port_Moresby",
    "Pacific/Rarotonga",
    "Pacific/Saipan",
    "Pacific/Tahiti",
    "Pacific/Tarawa",
    "Pacific/Tongatapu",
    "Pacific/Wake",
    "Pacific/Wallis",
    "UTC",
]

DefaultOptionTypeDef = Literal["default"]

UtcTimezoneDef = Literal["UTC"]

ConsoleBaudRateDef = Literal["115200", "1200", "19200", "2400", "38400", "4800", "57600", "9600"]

Value = Literal["9600"]

EpfrDef = Literal["aggressive", "conservative", "disabled", "moderate"]

BasicValue = Literal["disabled"]

SiteTypeListDef = Literal["br", "branch", "cloud", "spoke", "type-1", "type-2", "type-3"]

BasicConsoleBaudRateDef = Literal[
    "115200", "1200", "19200", "2400", "38400", "4800", "57600", "9600"
]

BasicEpfrDef = Literal["aggressive", "conservative", "disabled", "moderate"]

BasicSiteTypeListDef = Literal["br", "branch", "cloud", "spoke", "type-1", "type-2", "type-3"]

SystemBasicConsoleBaudRateDef = Literal[
    "115200", "1200", "19200", "2400", "38400", "4800", "57600", "9600"
]

SystemBasicEpfrDef = Literal["aggressive", "conservative", "disabled", "moderate"]

SystemBasicSiteTypeListDef = Literal["br", "branch", "cloud", "spoke", "type-1", "type-2", "type-3"]


@dataclass
class OneOfTimezoneOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTimezoneOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TimezoneDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTimezoneOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UtcTimezoneDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Clock:
    timezone: Union[OneOfTimezoneOptionsDef1, OneOfTimezoneOptionsDef2, OneOfTimezoneOptionsDef3]


@dataclass
class OneOfDescriptionOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDescriptionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLocationOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLocationOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfLocationOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLongitudeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLongitudeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLongitudeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLatitudeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLatitudeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLatitudeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEnableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnableOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfRangeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRangeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRangeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMobileNumberNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfMobileNumberNumberOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class MobileNumber:
    number: Union[OneOfMobileNumberNumberOptionsDef1, OneOfMobileNumberNumberOptionsDef2]


@dataclass
class Sms:
    enable: Optional[Union[OneOfEnableOptionsDef1, OneOfEnableOptionsDef2]] = _field(default=None)
    # Set device’s geo fencing SMS phone number
    mobile_number: Optional[List[MobileNumber]] = _field(
        default=None, metadata={"alias": "mobileNumber"}
    )


@dataclass
class GeoFencing:
    enable: Optional[Union[OneOfEnableOptionsDef1, OneOfEnableOptionsDef2]] = _field(default=None)
    range: Optional[Union[OneOfRangeOptionsDef1, OneOfRangeOptionsDef2, OneOfRangeOptionsDef3]] = (
        _field(default=None)
    )
    sms: Optional[Sms] = _field(default=None)


@dataclass
class GpsLocation:
    latitude: Union[OneOfLatitudeOptionsDef1, OneOfLatitudeOptionsDef2, OneOfLatitudeOptionsDef3]
    longitude: Union[
        OneOfLongitudeOptionsDef1, OneOfLongitudeOptionsDef2, OneOfLongitudeOptionsDef3
    ]
    geo_fencing: Optional[GeoFencing] = _field(default=None, metadata={"alias": "geoFencing"})


@dataclass
class OneOfDeviceGroupsOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDeviceGroupsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfDeviceGroupsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfControllerGroupListOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerGroupListOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfControllerGroupListOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOverlayIdOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOverlayIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOverlayIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortOffsetOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortOffsetOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortOffsetOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortHopOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortHopOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPortHopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfControlSessionPpsOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControlSessionPpsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfControlSessionPpsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackTransportOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackTransportOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTrackTransportOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTrackInterfaceTagOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackInterfaceTagOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackInterfaceTagOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfConsoleBaudRateOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfConsoleBaudRateOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ConsoleBaudRateDef


@dataclass
class OneOfConsoleBaudRateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMaxOmpSessionsOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMaxOmpSessionsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMaxOmpSessionsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMultiTenantOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMultiTenantOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfMultiTenantOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTrackDefaultGatewayOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackDefaultGatewayOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTrackDefaultGatewayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTrackerDiaStabilizeStatusDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerDiaStabilizeStatusDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTrackerDiaStabilizeStatusDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAdminTechOnFailureOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdminTechOnFailureOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAdminTechOnFailureOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIdleTimeoutOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIdleTimeoutOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIdleTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOnDemandEnableOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnDemandEnableOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnDemandEnableOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnDemandIdleTimeoutOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnDemandIdleTimeoutOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOnDemandIdleTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OnDemand:
    on_demand_enable: Union[
        OneOfOnDemandEnableOptionsDef1,
        OneOfOnDemandEnableOptionsDef2,
        OneOfOnDemandEnableOptionsDef3,
    ] = _field(metadata={"alias": "onDemandEnable"})
    on_demand_idle_timeout: Union[
        OneOfOnDemandIdleTimeoutOptionsDef1,
        OneOfOnDemandIdleTimeoutOptionsDef2,
        OneOfOnDemandIdleTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "onDemandIdleTimeout"})


@dataclass
class OneOfTransportGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTransportGatewayOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTransportGatewayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEpfrOptions1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EpfrDef


@dataclass
class OneOfEpfrOptions2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BasicValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEpfrOptions3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSiteTypeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSiteTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[SiteTypeListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSiteTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAffinityGroupNumberOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAffinityGroupNumberOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAffinityGroupNumberOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAffinityGroupPreferenceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAffinityGroupPreferenceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfAffinityGroupPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAffinityPreferenceAutoOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAffinityPreferenceAutoOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAffinityPreferenceAutoOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfVrfRangeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrfRangeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfVrfRangeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class AffinityPerVrf:
    affinity_group_number: Union[
        OneOfAffinityGroupNumberOptionsDef1,
        OneOfAffinityGroupNumberOptionsDef2,
        OneOfAffinityGroupNumberOptionsDef3,
    ] = _field(metadata={"alias": "affinityGroupNumber"})
    vrf_range: Union[
        OneOfVrfRangeOptionsDef1, OneOfVrfRangeOptionsDef2, OneOfVrfRangeOptionsDef3
    ] = _field(metadata={"alias": "vrfRange"})


@dataclass
class BasicData:
    admin_tech_on_failure: Union[
        OneOfAdminTechOnFailureOptionsDef1,
        OneOfAdminTechOnFailureOptionsDef2,
        OneOfAdminTechOnFailureOptionsDef3,
    ] = _field(metadata={"alias": "adminTechOnFailure"})
    clock: Clock
    console_baud_rate: Union[
        OneOfConsoleBaudRateOptionsDef1,
        OneOfConsoleBaudRateOptionsDef2,
        OneOfConsoleBaudRateOptionsDef3,
    ] = _field(metadata={"alias": "consoleBaudRate"})
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    device_groups: Union[
        OneOfDeviceGroupsOptionsDef1, OneOfDeviceGroupsOptionsDef2, OneOfDeviceGroupsOptionsDef3
    ] = _field(metadata={"alias": "deviceGroups"})
    gps_location: GpsLocation = _field(metadata={"alias": "gpsLocation"})
    location: Union[OneOfLocationOptionsDef1, OneOfLocationOptionsDef2, OneOfLocationOptionsDef3]
    max_omp_sessions: Union[
        OneOfMaxOmpSessionsOptionsDef1,
        OneOfMaxOmpSessionsOptionsDef2,
        OneOfMaxOmpSessionsOptionsDef3,
    ] = _field(metadata={"alias": "maxOmpSessions"})
    on_demand: OnDemand = _field(metadata={"alias": "onDemand"})
    overlay_id: Union[
        OneOfOverlayIdOptionsDef1, OneOfOverlayIdOptionsDef2, OneOfOverlayIdOptionsDef3
    ] = _field(metadata={"alias": "overlayId"})
    port_hop: Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3] = (
        _field(metadata={"alias": "portHop"})
    )
    port_offset: Union[
        OneOfPortOffsetOptionsDef1, OneOfPortOffsetOptionsDef2, OneOfPortOffsetOptionsDef3
    ] = _field(metadata={"alias": "portOffset"})
    affinity_group_number: Optional[
        Union[
            OneOfAffinityGroupNumberOptionsDef1,
            OneOfAffinityGroupNumberOptionsDef2,
            OneOfAffinityGroupNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityGroupNumber"})
    affinity_group_preference: Optional[
        Union[
            OneOfAffinityGroupPreferenceOptionsDef1,
            OneOfAffinityGroupPreferenceOptionsDef2,
            OneOfAffinityGroupPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityGroupPreference"})
    # Affinity Group Number for VRFs
    affinity_per_vrf: Optional[List[AffinityPerVrf]] = _field(
        default=None, metadata={"alias": "affinityPerVrf"}
    )
    affinity_preference_auto: Optional[
        Union[
            OneOfAffinityPreferenceAutoOptionsDef1,
            OneOfAffinityPreferenceAutoOptionsDef2,
            OneOfAffinityPreferenceAutoOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityPreferenceAuto"})
    control_session_pps: Optional[
        Union[
            OneOfControlSessionPpsOptionsDef1,
            OneOfControlSessionPpsOptionsDef2,
            OneOfControlSessionPpsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controlSessionPps"})
    controller_group_list: Optional[
        Union[
            OneOfControllerGroupListOptionsDef1,
            OneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controllerGroupList"})
    epfr: Optional[Union[OneOfEpfrOptions1, OneOfEpfrOptions2, OneOfEpfrOptions3]] = _field(
        default=None
    )
    idle_timeout: Optional[
        Union[OneOfIdleTimeoutOptionsDef1, OneOfIdleTimeoutOptionsDef2, OneOfIdleTimeoutOptionsDef3]
    ] = _field(default=None, metadata={"alias": "idleTimeout"})
    multi_tenant: Optional[
        Union[OneOfMultiTenantOptionsDef1, OneOfMultiTenantOptionsDef2, OneOfMultiTenantOptionsDef3]
    ] = _field(default=None, metadata={"alias": "multiTenant"})
    site_type: Optional[
        Union[OneOfSiteTypeOptionsDef1, OneOfSiteTypeOptionsDef2, OneOfSiteTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "siteType"})
    track_default_gateway: Optional[
        Union[
            OneOfTrackDefaultGatewayOptionsDef1,
            OneOfTrackDefaultGatewayOptionsDef2,
            OneOfTrackDefaultGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackDefaultGateway"})
    track_interface_tag: Optional[
        Union[
            OneOfTrackInterfaceTagOptionsDef1,
            OneOfTrackInterfaceTagOptionsDef2,
            OneOfTrackInterfaceTagOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackInterfaceTag"})
    track_transport: Optional[
        Union[
            OneOfTrackTransportOptionsDef1,
            OneOfTrackTransportOptionsDef2,
            OneOfTrackTransportOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackTransport"})
    tracker_dia_stabilize_status: Optional[
        Union[
            OneOfTrackerDiaStabilizeStatusDef1,
            OneOfTrackerDiaStabilizeStatusDef2,
            OneOfTrackerDiaStabilizeStatusDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackerDiaStabilizeStatus"})
    transport_gateway: Optional[
        Union[
            OneOfTransportGatewayOptionsDef1,
            OneOfTransportGatewayOptionsDef2,
            OneOfTransportGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transportGateway"})


@dataclass
class Payload:
    """
    Basic profile feature schema for POST request
    """

    data: BasicData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


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
    # Basic profile feature schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemBasicPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateBasicProfileFeatureForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemBasicData:
    admin_tech_on_failure: Union[
        OneOfAdminTechOnFailureOptionsDef1,
        OneOfAdminTechOnFailureOptionsDef2,
        OneOfAdminTechOnFailureOptionsDef3,
    ] = _field(metadata={"alias": "adminTechOnFailure"})
    clock: Clock
    console_baud_rate: Union[
        OneOfConsoleBaudRateOptionsDef1,
        OneOfConsoleBaudRateOptionsDef2,
        OneOfConsoleBaudRateOptionsDef3,
    ] = _field(metadata={"alias": "consoleBaudRate"})
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    device_groups: Union[
        OneOfDeviceGroupsOptionsDef1, OneOfDeviceGroupsOptionsDef2, OneOfDeviceGroupsOptionsDef3
    ] = _field(metadata={"alias": "deviceGroups"})
    gps_location: GpsLocation = _field(metadata={"alias": "gpsLocation"})
    location: Union[OneOfLocationOptionsDef1, OneOfLocationOptionsDef2, OneOfLocationOptionsDef3]
    max_omp_sessions: Union[
        OneOfMaxOmpSessionsOptionsDef1,
        OneOfMaxOmpSessionsOptionsDef2,
        OneOfMaxOmpSessionsOptionsDef3,
    ] = _field(metadata={"alias": "maxOmpSessions"})
    on_demand: OnDemand = _field(metadata={"alias": "onDemand"})
    overlay_id: Union[
        OneOfOverlayIdOptionsDef1, OneOfOverlayIdOptionsDef2, OneOfOverlayIdOptionsDef3
    ] = _field(metadata={"alias": "overlayId"})
    port_hop: Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3] = (
        _field(metadata={"alias": "portHop"})
    )
    port_offset: Union[
        OneOfPortOffsetOptionsDef1, OneOfPortOffsetOptionsDef2, OneOfPortOffsetOptionsDef3
    ] = _field(metadata={"alias": "portOffset"})
    affinity_group_number: Optional[
        Union[
            OneOfAffinityGroupNumberOptionsDef1,
            OneOfAffinityGroupNumberOptionsDef2,
            OneOfAffinityGroupNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityGroupNumber"})
    affinity_group_preference: Optional[
        Union[
            OneOfAffinityGroupPreferenceOptionsDef1,
            OneOfAffinityGroupPreferenceOptionsDef2,
            OneOfAffinityGroupPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityGroupPreference"})
    # Affinity Group Number for VRFs
    affinity_per_vrf: Optional[List[AffinityPerVrf]] = _field(
        default=None, metadata={"alias": "affinityPerVrf"}
    )
    affinity_preference_auto: Optional[
        Union[
            OneOfAffinityPreferenceAutoOptionsDef1,
            OneOfAffinityPreferenceAutoOptionsDef2,
            OneOfAffinityPreferenceAutoOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityPreferenceAuto"})
    control_session_pps: Optional[
        Union[
            OneOfControlSessionPpsOptionsDef1,
            OneOfControlSessionPpsOptionsDef2,
            OneOfControlSessionPpsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controlSessionPps"})
    controller_group_list: Optional[
        Union[
            OneOfControllerGroupListOptionsDef1,
            OneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controllerGroupList"})
    epfr: Optional[Union[OneOfEpfrOptions1, OneOfEpfrOptions2, OneOfEpfrOptions3]] = _field(
        default=None
    )
    idle_timeout: Optional[
        Union[OneOfIdleTimeoutOptionsDef1, OneOfIdleTimeoutOptionsDef2, OneOfIdleTimeoutOptionsDef3]
    ] = _field(default=None, metadata={"alias": "idleTimeout"})
    multi_tenant: Optional[
        Union[OneOfMultiTenantOptionsDef1, OneOfMultiTenantOptionsDef2, OneOfMultiTenantOptionsDef3]
    ] = _field(default=None, metadata={"alias": "multiTenant"})
    site_type: Optional[
        Union[OneOfSiteTypeOptionsDef1, OneOfSiteTypeOptionsDef2, OneOfSiteTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "siteType"})
    track_default_gateway: Optional[
        Union[
            OneOfTrackDefaultGatewayOptionsDef1,
            OneOfTrackDefaultGatewayOptionsDef2,
            OneOfTrackDefaultGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackDefaultGateway"})
    track_interface_tag: Optional[
        Union[
            OneOfTrackInterfaceTagOptionsDef1,
            OneOfTrackInterfaceTagOptionsDef2,
            OneOfTrackInterfaceTagOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackInterfaceTag"})
    track_transport: Optional[
        Union[
            OneOfTrackTransportOptionsDef1,
            OneOfTrackTransportOptionsDef2,
            OneOfTrackTransportOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackTransport"})
    tracker_dia_stabilize_status: Optional[
        Union[
            OneOfTrackerDiaStabilizeStatusDef1,
            OneOfTrackerDiaStabilizeStatusDef2,
            OneOfTrackerDiaStabilizeStatusDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackerDiaStabilizeStatus"})
    transport_gateway: Optional[
        Union[
            OneOfTransportGatewayOptionsDef1,
            OneOfTransportGatewayOptionsDef2,
            OneOfTransportGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transportGateway"})


@dataclass
class CreateBasicProfileFeatureForSystemPostRequest:
    """
    Basic profile feature schema for POST request
    """

    data: SystemBasicData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class BasicClock:
    timezone: Union[OneOfTimezoneOptionsDef1, OneOfTimezoneOptionsDef2, OneOfTimezoneOptionsDef3]


@dataclass
class BasicOneOfRangeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfRangeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfMobileNumberNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class BasicMobileNumber:
    number: Union[BasicOneOfMobileNumberNumberOptionsDef1, OneOfMobileNumberNumberOptionsDef2]


@dataclass
class BasicSms:
    enable: Optional[Union[OneOfEnableOptionsDef1, OneOfEnableOptionsDef2]] = _field(default=None)
    # Set device’s geo fencing SMS phone number
    mobile_number: Optional[List[BasicMobileNumber]] = _field(
        default=None, metadata={"alias": "mobileNumber"}
    )


@dataclass
class BasicGeoFencing:
    enable: Optional[Union[OneOfEnableOptionsDef1, OneOfEnableOptionsDef2]] = _field(default=None)
    range: Optional[
        Union[BasicOneOfRangeOptionsDef1, OneOfRangeOptionsDef2, BasicOneOfRangeOptionsDef3]
    ] = _field(default=None)
    sms: Optional[BasicSms] = _field(default=None)


@dataclass
class BasicGpsLocation:
    latitude: Union[OneOfLatitudeOptionsDef1, OneOfLatitudeOptionsDef2, OneOfLatitudeOptionsDef3]
    longitude: Union[
        OneOfLongitudeOptionsDef1, OneOfLongitudeOptionsDef2, OneOfLongitudeOptionsDef3
    ]
    geo_fencing: Optional[BasicGeoFencing] = _field(default=None, metadata={"alias": "geoFencing"})


@dataclass
class BasicOneOfDeviceGroupsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class BasicOneOfControllerGroupListOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class BasicOneOfOverlayIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfPortOffsetOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfControlSessionPpsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfTrackInterfaceTagOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfConsoleBaudRateOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BasicConsoleBaudRateDef


@dataclass
class BasicOneOfMaxOmpSessionsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfIdleTimeoutOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfOnDemandIdleTimeoutOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOnDemand:
    on_demand_enable: Union[
        OneOfOnDemandEnableOptionsDef1,
        OneOfOnDemandEnableOptionsDef2,
        OneOfOnDemandEnableOptionsDef3,
    ] = _field(metadata={"alias": "onDemandEnable"})
    on_demand_idle_timeout: Union[
        OneOfOnDemandIdleTimeoutOptionsDef1,
        BasicOneOfOnDemandIdleTimeoutOptionsDef2,
        OneOfOnDemandIdleTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "onDemandIdleTimeout"})


@dataclass
class BasicOneOfEpfrOptions1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BasicEpfrDef


@dataclass
class BasicOneOfSiteTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[BasicSiteTypeListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class BasicOneOfAffinityGroupNumberOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfAffinityGroupPreferenceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class SystemBasicOneOfAffinityGroupNumberOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BasicOneOfVrfRangeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class BasicAffinityPerVrf:
    affinity_group_number: Union[
        OneOfAffinityGroupNumberOptionsDef1,
        SystemBasicOneOfAffinityGroupNumberOptionsDef2,
        OneOfAffinityGroupNumberOptionsDef3,
    ] = _field(metadata={"alias": "affinityGroupNumber"})
    vrf_range: Union[
        OneOfVrfRangeOptionsDef1, BasicOneOfVrfRangeOptionsDef2, OneOfVrfRangeOptionsDef3
    ] = _field(metadata={"alias": "vrfRange"})


@dataclass
class SdwanSystemBasicData:
    admin_tech_on_failure: Union[
        OneOfAdminTechOnFailureOptionsDef1,
        OneOfAdminTechOnFailureOptionsDef2,
        OneOfAdminTechOnFailureOptionsDef3,
    ] = _field(metadata={"alias": "adminTechOnFailure"})
    clock: BasicClock
    console_baud_rate: Union[
        OneOfConsoleBaudRateOptionsDef1,
        BasicOneOfConsoleBaudRateOptionsDef2,
        OneOfConsoleBaudRateOptionsDef3,
    ] = _field(metadata={"alias": "consoleBaudRate"})
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    device_groups: Union[
        OneOfDeviceGroupsOptionsDef1,
        BasicOneOfDeviceGroupsOptionsDef2,
        OneOfDeviceGroupsOptionsDef3,
    ] = _field(metadata={"alias": "deviceGroups"})
    gps_location: BasicGpsLocation = _field(metadata={"alias": "gpsLocation"})
    location: Union[OneOfLocationOptionsDef1, OneOfLocationOptionsDef2, OneOfLocationOptionsDef3]
    max_omp_sessions: Union[
        OneOfMaxOmpSessionsOptionsDef1,
        BasicOneOfMaxOmpSessionsOptionsDef2,
        OneOfMaxOmpSessionsOptionsDef3,
    ] = _field(metadata={"alias": "maxOmpSessions"})
    on_demand: BasicOnDemand = _field(metadata={"alias": "onDemand"})
    overlay_id: Union[
        OneOfOverlayIdOptionsDef1, BasicOneOfOverlayIdOptionsDef2, OneOfOverlayIdOptionsDef3
    ] = _field(metadata={"alias": "overlayId"})
    port_hop: Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3] = (
        _field(metadata={"alias": "portHop"})
    )
    port_offset: Union[
        OneOfPortOffsetOptionsDef1, BasicOneOfPortOffsetOptionsDef2, OneOfPortOffsetOptionsDef3
    ] = _field(metadata={"alias": "portOffset"})
    affinity_group_number: Optional[
        Union[
            OneOfAffinityGroupNumberOptionsDef1,
            BasicOneOfAffinityGroupNumberOptionsDef2,
            OneOfAffinityGroupNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityGroupNumber"})
    affinity_group_preference: Optional[
        Union[
            OneOfAffinityGroupPreferenceOptionsDef1,
            BasicOneOfAffinityGroupPreferenceOptionsDef2,
            OneOfAffinityGroupPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityGroupPreference"})
    # Affinity Group Number for VRFs
    affinity_per_vrf: Optional[List[BasicAffinityPerVrf]] = _field(
        default=None, metadata={"alias": "affinityPerVrf"}
    )
    affinity_preference_auto: Optional[
        Union[
            OneOfAffinityPreferenceAutoOptionsDef1,
            OneOfAffinityPreferenceAutoOptionsDef2,
            OneOfAffinityPreferenceAutoOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityPreferenceAuto"})
    control_session_pps: Optional[
        Union[
            OneOfControlSessionPpsOptionsDef1,
            BasicOneOfControlSessionPpsOptionsDef2,
            OneOfControlSessionPpsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controlSessionPps"})
    controller_group_list: Optional[
        Union[
            OneOfControllerGroupListOptionsDef1,
            BasicOneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controllerGroupList"})
    epfr: Optional[Union[BasicOneOfEpfrOptions1, OneOfEpfrOptions2, OneOfEpfrOptions3]] = _field(
        default=None
    )
    idle_timeout: Optional[
        Union[
            OneOfIdleTimeoutOptionsDef1,
            BasicOneOfIdleTimeoutOptionsDef2,
            OneOfIdleTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "idleTimeout"})
    multi_tenant: Optional[
        Union[OneOfMultiTenantOptionsDef1, OneOfMultiTenantOptionsDef2, OneOfMultiTenantOptionsDef3]
    ] = _field(default=None, metadata={"alias": "multiTenant"})
    site_type: Optional[
        Union[OneOfSiteTypeOptionsDef1, BasicOneOfSiteTypeOptionsDef2, OneOfSiteTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "siteType"})
    track_default_gateway: Optional[
        Union[
            OneOfTrackDefaultGatewayOptionsDef1,
            OneOfTrackDefaultGatewayOptionsDef2,
            OneOfTrackDefaultGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackDefaultGateway"})
    track_interface_tag: Optional[
        Union[
            OneOfTrackInterfaceTagOptionsDef1,
            BasicOneOfTrackInterfaceTagOptionsDef2,
            OneOfTrackInterfaceTagOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackInterfaceTag"})
    track_transport: Optional[
        Union[
            OneOfTrackTransportOptionsDef1,
            OneOfTrackTransportOptionsDef2,
            OneOfTrackTransportOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackTransport"})
    tracker_dia_stabilize_status: Optional[
        Union[
            OneOfTrackerDiaStabilizeStatusDef1,
            OneOfTrackerDiaStabilizeStatusDef2,
            OneOfTrackerDiaStabilizeStatusDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackerDiaStabilizeStatus"})
    transport_gateway: Optional[
        Union[
            OneOfTransportGatewayOptionsDef1,
            OneOfTransportGatewayOptionsDef2,
            OneOfTransportGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transportGateway"})


@dataclass
class BasicPayload:
    """
    Basic profile feature schema for PUT request
    """

    data: SdwanSystemBasicData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemBasicPayload:
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
    # Basic profile feature schema for PUT request
    payload: Optional[BasicPayload] = _field(default=None)


@dataclass
class EditBasicProfileFeatureForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemBasicClock:
    timezone: Union[OneOfTimezoneOptionsDef1, OneOfTimezoneOptionsDef2, OneOfTimezoneOptionsDef3]


@dataclass
class SystemBasicOneOfRangeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfRangeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfMobileNumberNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemBasicMobileNumber:
    number: Union[SystemBasicOneOfMobileNumberNumberOptionsDef1, OneOfMobileNumberNumberOptionsDef2]


@dataclass
class SystemBasicSms:
    enable: Optional[Union[OneOfEnableOptionsDef1, OneOfEnableOptionsDef2]] = _field(default=None)
    # Set device’s geo fencing SMS phone number
    mobile_number: Optional[List[SystemBasicMobileNumber]] = _field(
        default=None, metadata={"alias": "mobileNumber"}
    )


@dataclass
class SystemBasicGeoFencing:
    enable: Optional[Union[OneOfEnableOptionsDef1, OneOfEnableOptionsDef2]] = _field(default=None)
    range: Optional[
        Union[
            SystemBasicOneOfRangeOptionsDef1,
            OneOfRangeOptionsDef2,
            SystemBasicOneOfRangeOptionsDef3,
        ]
    ] = _field(default=None)
    sms: Optional[SystemBasicSms] = _field(default=None)


@dataclass
class SystemBasicGpsLocation:
    latitude: Union[OneOfLatitudeOptionsDef1, OneOfLatitudeOptionsDef2, OneOfLatitudeOptionsDef3]
    longitude: Union[
        OneOfLongitudeOptionsDef1, OneOfLongitudeOptionsDef2, OneOfLongitudeOptionsDef3
    ]
    geo_fencing: Optional[SystemBasicGeoFencing] = _field(
        default=None, metadata={"alias": "geoFencing"}
    )


@dataclass
class SystemBasicOneOfDeviceGroupsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class SystemBasicOneOfControllerGroupListOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class SystemBasicOneOfOverlayIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfPortOffsetOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfControlSessionPpsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfTrackInterfaceTagOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfConsoleBaudRateOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemBasicConsoleBaudRateDef


@dataclass
class SystemBasicOneOfMaxOmpSessionsOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfIdleTimeoutOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfOnDemandIdleTimeoutOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOnDemand:
    on_demand_enable: Union[
        OneOfOnDemandEnableOptionsDef1,
        OneOfOnDemandEnableOptionsDef2,
        OneOfOnDemandEnableOptionsDef3,
    ] = _field(metadata={"alias": "onDemandEnable"})
    on_demand_idle_timeout: Union[
        OneOfOnDemandIdleTimeoutOptionsDef1,
        SystemBasicOneOfOnDemandIdleTimeoutOptionsDef2,
        OneOfOnDemandIdleTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "onDemandIdleTimeout"})


@dataclass
class SystemBasicOneOfEpfrOptions1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemBasicEpfrDef


@dataclass
class SystemBasicOneOfSiteTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[SystemBasicSiteTypeListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanSystemBasicOneOfAffinityGroupNumberOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfAffinityGroupPreferenceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class FeatureProfileSdwanSystemBasicOneOfAffinityGroupNumberOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemBasicOneOfVrfRangeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SystemBasicAffinityPerVrf:
    affinity_group_number: Union[
        OneOfAffinityGroupNumberOptionsDef1,
        FeatureProfileSdwanSystemBasicOneOfAffinityGroupNumberOptionsDef2,
        OneOfAffinityGroupNumberOptionsDef3,
    ] = _field(metadata={"alias": "affinityGroupNumber"})
    vrf_range: Union[
        OneOfVrfRangeOptionsDef1, SystemBasicOneOfVrfRangeOptionsDef2, OneOfVrfRangeOptionsDef3
    ] = _field(metadata={"alias": "vrfRange"})


@dataclass
class FeatureProfileSdwanSystemBasicData:
    admin_tech_on_failure: Union[
        OneOfAdminTechOnFailureOptionsDef1,
        OneOfAdminTechOnFailureOptionsDef2,
        OneOfAdminTechOnFailureOptionsDef3,
    ] = _field(metadata={"alias": "adminTechOnFailure"})
    clock: SystemBasicClock
    console_baud_rate: Union[
        OneOfConsoleBaudRateOptionsDef1,
        SystemBasicOneOfConsoleBaudRateOptionsDef2,
        OneOfConsoleBaudRateOptionsDef3,
    ] = _field(metadata={"alias": "consoleBaudRate"})
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    device_groups: Union[
        OneOfDeviceGroupsOptionsDef1,
        SystemBasicOneOfDeviceGroupsOptionsDef2,
        OneOfDeviceGroupsOptionsDef3,
    ] = _field(metadata={"alias": "deviceGroups"})
    gps_location: SystemBasicGpsLocation = _field(metadata={"alias": "gpsLocation"})
    location: Union[OneOfLocationOptionsDef1, OneOfLocationOptionsDef2, OneOfLocationOptionsDef3]
    max_omp_sessions: Union[
        OneOfMaxOmpSessionsOptionsDef1,
        SystemBasicOneOfMaxOmpSessionsOptionsDef2,
        OneOfMaxOmpSessionsOptionsDef3,
    ] = _field(metadata={"alias": "maxOmpSessions"})
    on_demand: SystemBasicOnDemand = _field(metadata={"alias": "onDemand"})
    overlay_id: Union[
        OneOfOverlayIdOptionsDef1, SystemBasicOneOfOverlayIdOptionsDef2, OneOfOverlayIdOptionsDef3
    ] = _field(metadata={"alias": "overlayId"})
    port_hop: Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3] = (
        _field(metadata={"alias": "portHop"})
    )
    port_offset: Union[
        OneOfPortOffsetOptionsDef1,
        SystemBasicOneOfPortOffsetOptionsDef2,
        OneOfPortOffsetOptionsDef3,
    ] = _field(metadata={"alias": "portOffset"})
    affinity_group_number: Optional[
        Union[
            OneOfAffinityGroupNumberOptionsDef1,
            SdwanSystemBasicOneOfAffinityGroupNumberOptionsDef2,
            OneOfAffinityGroupNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityGroupNumber"})
    affinity_group_preference: Optional[
        Union[
            OneOfAffinityGroupPreferenceOptionsDef1,
            SystemBasicOneOfAffinityGroupPreferenceOptionsDef2,
            OneOfAffinityGroupPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityGroupPreference"})
    # Affinity Group Number for VRFs
    affinity_per_vrf: Optional[List[SystemBasicAffinityPerVrf]] = _field(
        default=None, metadata={"alias": "affinityPerVrf"}
    )
    affinity_preference_auto: Optional[
        Union[
            OneOfAffinityPreferenceAutoOptionsDef1,
            OneOfAffinityPreferenceAutoOptionsDef2,
            OneOfAffinityPreferenceAutoOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "affinityPreferenceAuto"})
    control_session_pps: Optional[
        Union[
            OneOfControlSessionPpsOptionsDef1,
            SystemBasicOneOfControlSessionPpsOptionsDef2,
            OneOfControlSessionPpsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controlSessionPps"})
    controller_group_list: Optional[
        Union[
            OneOfControllerGroupListOptionsDef1,
            SystemBasicOneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "controllerGroupList"})
    epfr: Optional[Union[SystemBasicOneOfEpfrOptions1, OneOfEpfrOptions2, OneOfEpfrOptions3]] = (
        _field(default=None)
    )
    idle_timeout: Optional[
        Union[
            OneOfIdleTimeoutOptionsDef1,
            SystemBasicOneOfIdleTimeoutOptionsDef2,
            OneOfIdleTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "idleTimeout"})
    multi_tenant: Optional[
        Union[OneOfMultiTenantOptionsDef1, OneOfMultiTenantOptionsDef2, OneOfMultiTenantOptionsDef3]
    ] = _field(default=None, metadata={"alias": "multiTenant"})
    site_type: Optional[
        Union[
            OneOfSiteTypeOptionsDef1, SystemBasicOneOfSiteTypeOptionsDef2, OneOfSiteTypeOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "siteType"})
    track_default_gateway: Optional[
        Union[
            OneOfTrackDefaultGatewayOptionsDef1,
            OneOfTrackDefaultGatewayOptionsDef2,
            OneOfTrackDefaultGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackDefaultGateway"})
    track_interface_tag: Optional[
        Union[
            OneOfTrackInterfaceTagOptionsDef1,
            SystemBasicOneOfTrackInterfaceTagOptionsDef2,
            OneOfTrackInterfaceTagOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackInterfaceTag"})
    track_transport: Optional[
        Union[
            OneOfTrackTransportOptionsDef1,
            OneOfTrackTransportOptionsDef2,
            OneOfTrackTransportOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackTransport"})
    tracker_dia_stabilize_status: Optional[
        Union[
            OneOfTrackerDiaStabilizeStatusDef1,
            OneOfTrackerDiaStabilizeStatusDef2,
            OneOfTrackerDiaStabilizeStatusDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackerDiaStabilizeStatus"})
    transport_gateway: Optional[
        Union[
            OneOfTransportGatewayOptionsDef1,
            OneOfTransportGatewayOptionsDef2,
            OneOfTransportGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transportGateway"})


@dataclass
class EditBasicProfileFeatureForSystemPutRequest:
    """
    Basic profile feature schema for PUT request
    """

    data: FeatureProfileSdwanSystemBasicData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
