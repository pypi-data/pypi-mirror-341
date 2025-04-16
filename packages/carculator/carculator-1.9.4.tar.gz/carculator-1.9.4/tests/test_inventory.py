import numpy as np
import pytest

from carculator import (
    CarInputParameters,
    CarModel,
    InventoryCar,
    fill_xarray_from_input_parameters,
)

# generate vehicle parameters
cip = CarInputParameters()
cip.static()

# fill in array with vehicle parameters
scope = {"powertrain": ["ICEV-d", "ICEV-p", "BEV"], "size": ["Medium"]}
_, array = fill_xarray_from_input_parameters(cip, scope=scope)

# build CarModel object
cm = CarModel(array, cycle="WLTC")
# build vehicles
cm.set_all()


def test_scope():
    """Test if scope works as expected"""

    # generate vehicle parameters
    cip = CarInputParameters()
    cip.static()

    # fill in array with vehicle parameters
    scope = {"powertrain": ["ICEV-d", "ICEV-p", "BEV"], "size": ["Medium"]}
    _, array = fill_xarray_from_input_parameters(cip, scope=scope)

    # build CarModel object
    cm = CarModel(array, cycle="WLTC")
    # build vehicles
    cm.set_all()

    ic = InventoryCar(
        cm,
        method="recipe",
        indicator="midpoint",
    )
    results = ic.calculate_impacts()

    assert "Large" not in results.coords["size"].values
    assert "FCEV" not in results.coords["powertrain"].values


def test_plausibility_of_GWP():
    """Test if GWP scores make sense"""

    for method in ["recipe", "ef"]:
        ic = InventoryCar(cm, method=method, indicator="midpoint")
        results = ic.calculate_impacts()

        m = "climate change"

        gwp_icev = results.sel(
            impact_category=m,
            powertrain=["ICEV-d", "ICEV-p"],
            value=0,
            year=2020,
            size="Medium",
        )

        # Are the medium ICEVs between 0.28 and 0.35 kg CO2-eq./vkm?

        if method == "recipe":
            assert (gwp_icev.sum(dim="impact") > 0.24).all() and (
                gwp_icev.sum(dim="impact") < 0.36
            ).all(), gwp_icev.sum(dim="impact")

            # Are the medium ICEVs direct emissions between 0.13 and  0.18 kg CO2-eq./vkm?
            assert (gwp_icev.sel(impact="direct - exhaust") > 0.13).all() and (
                gwp_icev.sel(impact="direct - exhaust") < 0.19
            ).all(), gwp_icev.sel(impact="direct - exhaust")

        # Is the GWP score for batteries of Medium BEVs between 0.025 and 0.035 kg Co2-eq./vkm?
        gwp_bev = results.sel(
            impact_category=m, powertrain="BEV", value=0, year=2020, size="Medium"
        )

        assert (gwp_bev.sel(impact="energy storage") > 0.02).all() and (
            gwp_bev.sel(impact="energy storage") < 0.04
        ).all()

        assert gwp_bev.sel(impact="direct - exhaust") == 0


def test_fuel_blend():
    """Test if fuel blends defined by the user are considered"""

    bc = {
        "petrol": {
            "primary": {
                "type": "petrol",
                "share": [0.9, 0.9, 0.9, 0.9, 0.9, 0.9],
            },
        },
        "diesel": {
            "primary": {
                "type": "diesel",
                "share": [0.93, 0.93, 0.93, 0.93, 0.93, 0.93],
            },
        },
        "hydrogen": {
            "primary": {
                "type": "hydrogen - electrolysis - PEM",
                "share": [0.9, 0.9, 0.9, 0.9, 0.9, 0.9],
            },
        },
        "methane": {
            "primary": {
                "type": "methane - biomethane - sewage sludge",
                "share": [
                    1,
                    1,
                    1,
                    1,
                    1,
                    1,
                ],
            }
        },
    }

    cm = CarModel(array, cycle="WLTC", fuel_blend=bc)
    cm.set_all()

    assert np.array_equal(
        cm.fuel_blend["petrol"]["primary"]["share"],
        np.array(
            [
                0.9,
                0.9,
                0.9,
                0.9,
                0.9,
                0.9,
            ]
        ),
    )

    assert np.array_equal(
        cm.fuel_blend["diesel"]["primary"]["share"],
        np.array(
            [
                0.93,
                0.93,
                0.93,
                0.93,
                0.93,
                0.93,
            ]
        ),
    )
    assert np.array_equal(
        cm.fuel_blend["methane"]["primary"]["share"], np.array([1, 1, 1, 1, 1, 1])
    )
    assert np.allclose(
        np.sum(cm.fuel_blend["methane"]["secondary"]["share"]), np.zeros(6)
    )

    for fuels in [
        ("petrol", "diesel", "hydrogen - electrolysis - PEM", "methane"),
        (
            "petrol - bioethanol - wheat straw",
            "diesel - biodiesel - palm oil",
            "hydrogen - smr - natural gas",
            "methane - biomethane - sewage sludge",
        ),
        (
            "petrol - bioethanol - forest residues",
            "diesel - biodiesel - rapeseed oil",
            "hydrogen - smr - natural gas with CCS",
            "methane - synthetic - coal",
        ),
        (
            "petrol - bioethanol - maize starch",
            "diesel - biodiesel - cooking oil",
            "hydrogen - wood gasification",
            "methane - synthetic - biological",
        ),
        (
            "petrol - synthetic - methanol - electrolysis - energy allocation",
            "diesel - synthetic - FT - coal - economic allocation",
            "hydrogen - atr - biogas",
            "methane - synthetic - biological",
        ),
        (
            "petrol - synthetic - methanol - cement - energy allocation",
            "diesel - synthetic - methanol - cement - economic allocation",
            "hydrogen - wood gasification with CCS",
            "methane - synthetic - electrochemical",
        ),
    ]:
        bc["petrol"]["primary"]["type"] = fuels[0]
        bc["diesel"]["primary"]["type"] = fuels[1]
        bc["hydrogen"]["primary"]["type"] = fuels[2]
        bc["methane"]["primary"]["type"] = fuels[3]

        cm = CarModel(array, cycle="WLTC", fuel_blend=bc)
        cm.set_all()
        ic = InventoryCar(cm)
        ic.calculate_impacts()


def test_countries():
    """Test that calculation works with all countries"""
    for c in [
        "AO",
        "AT",
        "AU",
        "BE",
    ]:
        ic = InventoryCar(
            cm,
            method="recipe",
            indicator="midpoint",
            background_configuration={
                "country": c,
                "energy storage": {"electric": {"type": "NMC-622"}, "origin": c},
            },
        )
        ic.calculate_impacts()


def test_endpoint():
    """Test if the correct impact categories are considered"""
    ic = InventoryCar(cm, method="recipe", indicator="endpoint")
    results = ic.calculate_impacts()
    assert "human toxicity: carcinogenic" in [
        i.lower() for i in results.impact_category.values
    ]
    assert len(results.impact_category.values) == 26
    #
    #     """Test if it errors properly if an incorrect method type is give"""
    with pytest.raises(ValueError) as wrapped_error:
        ic = InventoryCar(cm, method="recipe", indicator="endpint")
        ic.calculate_impacts()
    assert wrapped_error.type == ValueError


def test_static_scenario():
    """Test if the static scenario works as expected"""
    ic = InventoryCar(cm, method="recipe", indicator="midpoint", scenario="static")
    ic.calculate_impacts()


def test_EF_indicators():
    ic = InventoryCar(
        cm,
        method="ef",
        indicator="midpoint",
    )
    ic.calculate_impacts()


def test_sulfur_concentration():
    ic = InventoryCar(
        cm,
    )
    ic.get_sulfur_content(location="FR", fuel="diesel")


def test_custom_electricity_mix():
    """Test if a wrong number of electricity mixes throws an error"""

    # Passing four mixes instead of 6
    mix_1 = np.zeros((5, 15))
    mix_1[:, 0] = 1

    mixes = [mix_1]

    for mix in mixes:
        with pytest.raises(ValueError) as wrapped_error:
            InventoryCar(
                cm,
                background_configuration={"custom electricity mix": mix},
            )
        assert wrapped_error.type == ValueError


def test_export_to_bw():
    """Test that inventories export successfully"""
    # generate vehicle parameters
    cip = CarInputParameters()
    cip.static()

    # fill in array with vehicle parameters
    scope = {"powertrain": ["ICEV-d", "ICEV-p", "BEV"], "size": ["Medium"]}
    _, array = fill_xarray_from_input_parameters(cip, scope=scope)

    # build CarModel object
    cm = CarModel(array, cycle="WLTC")
    # build vehicles
    cm.set_all()

    ic = InventoryCar(
        cm,
    )
    #

    for b in ("3.9",):
        ic.export_lci(
            ecoinvent_version=b,
        )


def test_export_to_excel():
    """Test that inventories export successfully to Excel/CSV"""
    # generate vehicle parameters
    cip = CarInputParameters()
    cip.static()

    # fill in array with vehicle parameters
    scope = {"powertrain": ["ICEV-d", "ICEV-p", "BEV"], "size": ["Medium"]}
    _, array = fill_xarray_from_input_parameters(cip, scope=scope)

    # build CarModel object
    cm = CarModel(array, cycle="WLTC")
    # build vehicles
    cm.set_all()
    ic = InventoryCar(cm, method="recipe", indicator="endpoint")

    for s in ("brightway2", "simapro"):
        for d in ("file", "bw2io"):
            ic.export_lci(
                ecoinvent_version="3.10",
                format=d,
                software=s,
                directory="directory",
            )
