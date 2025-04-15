from hestia_earth.schema import TermTermType, EmissionMethodTier
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.models.utils.aquacultureManagement import valid_site_type
from hestia_earth.models.utils.input import total_excreta_tan
from . import MODEL


REQUIREMENTS = {
    "Cycle": {
        "products": [{
            "@type": "Product",
            "term.termType": "excreta",
            "term.@id": "excretaLiquidFishCrustaceansKgN"
        }]
    }
}

RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 1"
    }]
}

TIER = EmissionMethodTier.TIER_1.value
TERM_ID = 'nh3ToSurfaceWaterAquacultureSystems'
_EXCRETA_TERM_ID = 'excretaLiquidFishCrustaceansKgN'


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [round(value, 7)]
    emission['methodTier'] = TIER
    return emission


def _run(excreta_products: list):
    value = total_excreta_tan(excreta_products)
    return [_emission(value)]


def _valid_excreta(cycle: dict):
    excreta_products = filter_list_term_type(cycle.get('products', []), TermTermType.EXCRETA.value)
    valid_excreta_products = [
        product for product in excreta_products if all([
            product.get('term', {}).get('@id') == _EXCRETA_TERM_ID
        ])
    ]
    return valid_excreta_products


def _should_run(cycle: dict):
    valid_excreta_products = _valid_excreta(cycle)
    should_run = all([
        valid_site_type(cycle),
        bool(valid_excreta_products),
    ])
    return should_run, valid_excreta_products


def run(cycle: dict):
    should_run, valid_excreta_products = _should_run(cycle)
    return _run(valid_excreta_products) if should_run else []
