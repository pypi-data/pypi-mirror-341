from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition, TermTermType
from hestia_earth.utils.model import filter_list_term_type, find_term_match
from hestia_earth.utils.tools import list_sum, safe_parse_float

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.product import has_flooded_rice
from hestia_earth.models.utils.organicFertiliser import get_cycle_inputs as get_organicFertiliser_inputs
from hestia_earth.models.utils.lookup import get_region_lookup_value
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "practices": [{"@type": "Practice", "value": "", "term.@id": "croppingDuration"}],
        "site": {
            "@type": "Site",
            "country": {"@type": "Term", "termType": "region"}
        },
        "optional": {
            "inputs": [
                {
                    "@type": "Input",
                    "value": "",
                    "term.termType": "organicFertiliser"
                },
                {
                    "@type": "Input",
                    "value": "",
                    "term.termType": "fertiliserBrandName",
                    "properties": [{"@type": "Property", "value": "", "key.termType": "organicFertiliser"}]
                }
            ],
            "products": [{"@type": "Product", "value": "", "term.@id": "aboveGroundCropResidueIncorporated"}],
            "practices": [
                {"@type": "Practice", "value": "", "term.termType": "cropResidueManagement"},
                {"@type": "Practice", "value": "", "term.termType": "landUseManagement"},
                {"@type": "Practice", "value": "", "term.termType": "waterRegime"}
            ]
        }
    }
}
LOOKUPS = {
    "landUseManagement": [
        "IPCC_2019_CH4_rice_SFw", "IPCC_2019_CH4_rice_SFw-min", "IPCC_2019_CH4_rice_SFw-max",
        "IPCC_2019_CH4_rice_SFw-sd",
        "IPCC_2019_CH4_rice_SFp", "IPCC_2019_CH4_rice_SFp-min", "IPCC_2019_CH4_rice_SFp-max",
        "IPCC_2019_CH4_rice_SFp-sd"
    ],
    "waterRegime": [
        "IPCC_2019_CH4_rice_SFw", "IPCC_2019_CH4_rice_SFw-min", "IPCC_2019_CH4_rice_SFw-max",
        "IPCC_2019_CH4_rice_SFw-sd",
        "IPCC_2019_CH4_rice_SFp", "IPCC_2019_CH4_rice_SFp-min", "IPCC_2019_CH4_rice_SFp-max",
        "IPCC_2019_CH4_rice_SFp-sd"
    ],
    "organicFertiliser": ["IPCC_2019_CH4_rice_CFOA_kg_fresh_weight", "IPCC_2019_CH4_rice_CFOA_kg_dry_weight"],
    "region-ch4ef-IPCC2019": ["CH4_ef", "CH4_ef_min", "CH4_ef_max", "CH4_ef_sd"]
}
RETURNS = {
    "Emission": [{
        "value": "",
        "min": "",
        "max": "",
        "sd": "",
        "methodTier": "tier 1",
        "statsDefinition": "modelled"
    }]
}
TERM_ID = 'ch4ToAirFloodedRice'
TIER = EmissionMethodTier.TIER_1.value


def _emission(value: float, min: float, max: float, sd: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['min'] = [min]
    emission['max'] = [max]
    emission['sd'] = [sd]
    emission['methodTier'] = TIER
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _get_CH4_ef(country: str, suffix: str = ''):
    lookup_name = 'region-ch4ef-IPCC2019.csv'
    return safe_parse_float(
        get_region_lookup_value(lookup_name, country, 'CH4_ef' + suffix, model=MODEL, term=TERM_ID)
    )


def _get_practice_lookup(term: dict, col: str):
    return safe_parse_float(get_lookup_value(term, col, model=MODEL, term=TERM_ID))


def _get_cropResidue_value(cycle: dict, suffix: str = ''):
    abgIncorporated = list_sum(
        find_term_match(cycle.get('products', []), 'aboveGroundCropResidueIncorporated').get('value', [])
    )
    abgManagement = filter_list_term_type(cycle.get('practices', []), TermTermType.CROPRESIDUEMANAGEMENT)
    term = abgManagement[0].get('term', {}) if len(abgManagement) > 0 else None
    factor = safe_parse_float(
        get_lookup_value(term, LOOKUPS['organicFertiliser'][1] + suffix, model=MODEL, term=TERM_ID)
    ) if term else 0
    return abgIncorporated * factor


def _get_fertiliser_value(input: dict, suffix: str = ''):
    term = input.get('term', {})
    factor = safe_parse_float(
        get_lookup_value(term, LOOKUPS['organicFertiliser'][0] + suffix, model=MODEL, term=TERM_ID)
    )
    return list_sum(input.get('value', [])) * factor


def _calculate_SFo(cycle: dict, suffix: str = ''):
    cropResidue = _get_cropResidue_value(cycle, suffix)
    fertilisers = get_organicFertiliser_inputs(cycle)
    fert_value = list_sum([_get_fertiliser_value(i, suffix) for i in fertilisers])
    return (1 + (fert_value/1000) + (cropResidue/1000)) ** 0.59


def _calculate_SF_average(practices: list, factor: str):
    values = [
        (_get_practice_lookup(p.get('term', {}), factor), list_sum(p.get('value', []), None)) for p in practices
    ]
    # sum only values that are numbers
    return list_sum([factor * percent / 100 for factor, percent in values if percent is not None])


def _calculate_factor(cycle: dict, country: str, practices: list, suffix: str = ''):
    CH4_ef = _get_CH4_ef(country, suffix)
    SFw = _calculate_SF_average(practices, 'IPCC_2019_CH4_rice_SFw' + suffix)
    SFp = _calculate_SF_average(practices, 'IPCC_2019_CH4_rice_SFp' + suffix)
    SFo = _calculate_SFo(cycle, suffix)
    debugValues(cycle, model=MODEL, term=TERM_ID, **{
        'CH4_ef' + suffix: CH4_ef,
        'SFw' + suffix: SFw,
        'SFp' + suffix: SFp,
        'SFo' + suffix: SFo
    })
    return CH4_ef * (SFw if SFw > 0 else 1) * (SFp if SFp > 0 else 1) * SFo


def _get_croppingDuration(croppingDuration: dict, key: str = 'value'):
    return list_sum(croppingDuration.get(key, croppingDuration.get('value', [])))


def _run(cycle: dict, croppingDuration: dict, country: str):
    practices = filter_list_term_type(cycle.get('practices', []), [
        TermTermType.WATERREGIME, TermTermType.LANDUSEMANAGEMENT
    ])

    value = _calculate_factor(cycle, country, practices) * _get_croppingDuration(croppingDuration)
    min = _calculate_factor(cycle, country, practices, '_min') * _get_croppingDuration(croppingDuration, 'min')
    max = _calculate_factor(cycle, country, practices, '_max') * _get_croppingDuration(croppingDuration, 'max')
    sd = (max-min)/4

    return [_emission(value, min, max, sd)]


def _should_run(cycle: dict):
    country = cycle.get('site', {}).get('country', {}).get('@id')

    flooded_rice = has_flooded_rice(cycle.get('products', []))

    croppingDuration = find_term_match(cycle.get('practices', []), 'croppingDuration', None)
    has_croppingDuration = croppingDuration is not None

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    has_flooded_rice=flooded_rice,
                    has_croppingDuration=has_croppingDuration,
                    country=country)

    should_run = all([flooded_rice, has_croppingDuration, country])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, croppingDuration, country


def run(cycle: dict):
    should_run, croppingDuration, country = _should_run(cycle)
    return _run(cycle, croppingDuration, country) if should_run else []
