import solar_topology as api


def test_public_api_inventory_is_total_unique_and_sorted():
    inventory = api.build_public_api_inventory(api.__all__)
    names = [name for name, _status in inventory]
    assert names == sorted(names)
    assert len(names) == len(set(names))
    assert set(names) == set(api.__all__)


def test_explicit_public_api_classification_has_no_duplicates():
    names = api.explicitly_classified_public_names()
    assert names == tuple(sorted(names))
    assert len(names) == len(set(names))


def test_unadjudicated_exports_remain_provisional_not_canonical():
    assert api.public_api_status("definitely-not-an-export") == api.ApiStatus.PROVISIONAL
    assert api.public_api_status("CircuitModel") == api.ApiStatus.CANONICAL
    assert api.public_api_status("INITIAL_CARTRIDGES") == api.ApiStatus.COMPATIBILITY
