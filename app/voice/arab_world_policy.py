"""Country-aware outreach policy for Hamed.

This module keeps the initial voice-sales scope limited to Arab countries and
requires a compliant outreach path before a call can be placed. It is a
policy layer, not legal advice; country-specific telecom/privacy requirements
must be reviewed before production launch.
"""

ARAB_COUNTRIES = {
    "EG": {"name_ar": "مصر", "currency": "EGP", "timezone": "Africa/Cairo"},
    "SA": {"name_ar": "السعودية", "currency": "SAR", "timezone": "Asia/Riyadh"},
    "AE": {"name_ar": "الإمارات", "currency": "AED", "timezone": "Asia/Dubai"},
    "QA": {"name_ar": "قطر", "currency": "QAR", "timezone": "Asia/Qatar"},
    "KW": {"name_ar": "الكويت", "currency": "KWD", "timezone": "Asia/Kuwait"},
    "BH": {"name_ar": "البحرين", "currency": "BHD", "timezone": "Asia/Bahrain"},
    "OM": {"name_ar": "عُمان", "currency": "OMR", "timezone": "Asia/Muscat"},
    "JO": {"name_ar": "الأردن", "currency": "JOD", "timezone": "Asia/Amman"},
    "LB": {"name_ar": "لبنان", "currency": "LBP", "timezone": "Asia/Beirut"},
    "IQ": {"name_ar": "العراق", "currency": "IQD", "timezone": "Asia/Baghdad"},
    "YE": {"name_ar": "اليمن", "currency": "YER", "timezone": "Asia/Aden"},
    "PS": {"name_ar": "فلسطين", "currency": "ILS", "timezone": "Asia/Gaza"},
    "SY": {"name_ar": "سوريا", "currency": "SYP", "timezone": "Asia/Damascus"},
    "MA": {"name_ar": "المغرب", "currency": "MAD", "timezone": "Africa/Casablanca"},
    "DZ": {"name_ar": "الجزائر", "currency": "DZD", "timezone": "Africa/Algiers"},
    "TN": {"name_ar": "تونس", "currency": "TND", "timezone": "Africa/Tunis"},
    "LY": {"name_ar": "ليبيا", "currency": "LYD", "timezone": "Africa/Tripoli"},
    "SD": {"name_ar": "السودان", "currency": "SDG", "timezone": "Africa/Khartoum"},
    "SO": {"name_ar": "الصومال", "currency": "SOS", "timezone": "Africa/Mogadishu"},
    "DJ": {"name_ar": "جيبوتي", "currency": "DJF", "timezone": "Africa/Djibouti"},
    "KM": {"name_ar": "جزر القمر", "currency": "KMF", "timezone": "Indian/Comoro"},
    "MR": {"name_ar": "موريتانيا", "currency": "MRU", "timezone": "Africa/Nouakchott"},
}


def get_country(country_code: str) -> dict:
    code = country_code.upper()
    if code not in ARAB_COUNTRIES:
        raise ValueError("Hamed voice outreach is restricted to configured Arab countries.")
    return ARAB_COUNTRIES[code]


def can_place_call(*, country_code: str, opted_in: bool, approved_lead: bool,
                   do_not_contact: bool = False, provider_compliance_ready: bool = False) -> tuple[bool, str]:
    """Return whether a marketing call is eligible for placement."""
    get_country(country_code)
    if not provider_compliance_ready:
        return False, "telecom_provider_compliance_not_confirmed"
    if do_not_contact:
        return False, "do_not_contact"
    if not opted_in and not approved_lead:
        return False, "no_valid_marketing_permission_or_approved_lead"
    return True, "eligible"


def system_rules(country_code: str) -> str:
    country = get_country(country_code)
    return (
        f"Country: {country['name_ar']}. Currency: {country['currency']}. "
        "Speak Arabic naturally and adapt wording to the local market. "
        "Identify Hamed as an AI assistant. Respect opt-out requests immediately. "
        "Do not misrepresent identity, create urgency deceptively, or make commitments "
        "outside authorized commercial limits. Follow the telecom/privacy rules of the "
        "customer's country and the calling provider before placing marketing calls."
    )
