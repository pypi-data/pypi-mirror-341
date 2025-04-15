from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission

from hestia_earth.models.hestia.nh3ToSurfaceWaterAquacultureSystems import MODEL, TERM_ID, run, _should_run

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"{class_path}.valid_site_type", return_value=True)
def test_should_run(mock_valid_excreta, *args):
    cycle = {}
    should_run, *args = _should_run(cycle)
    assert not should_run

    # without the right type of excreta => no run
    cycle['products'] = [
        {
            'term': {
                '@id': 'excretaSolidFishCrustaceansKgN',
                'termType': 'excreta'
            }
        }
    ]
    should_run, *args = _should_run(cycle)
    assert not should_run

    # with fish_excreta_tan => run
    cycle['products'] = [
        {
            'term': {
                '@id': 'excretaLiquidFishCrustaceansKgN',
                'termType': 'excreta'
            }
        }
    ]
    should_run, *args = _should_run(cycle)
    assert should_run is True


@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
def test_run(*args):
    with open(f"{fixtures_folder}/cycle.jsonld", encoding="utf-8") as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding="utf-8") as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
