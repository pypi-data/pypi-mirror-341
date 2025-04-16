"""Test realistic scenarios, which are slower."""

import pickle

from pathlib import Path

import numpy as np
import pytest
import xarray as xr

import particle_tracking_manager as ptm


# set up an alternate dataset on-the-fly
ds = xr.Dataset(
    data_vars={
        "u": (("ocean_time", "Z", "Y", "X"), np.zeros((2, 3, 2, 3))),
        "v": (("ocean_time", "Z", "Y", "X"), np.zeros((2, 3, 2, 3))),
        "w": (("ocean_time", "Z", "Y", "X"), np.zeros((2, 3, 2, 3))),
        "salt": (("ocean_time", "Z", "Y", "X"), np.zeros((2, 3, 2, 3))),
        "temp": (("ocean_time", "Z", "Y", "X"), np.zeros((2, 3, 2, 3))),
        "wetdry_mask_rho": (("ocean_time", "Z", "Y", "X"), np.zeros((2, 3, 2, 3))),
        "mask_rho": (("Y", "X"), np.zeros((2, 3))),
        "Uwind": (("ocean_time", "Y", "X"), np.zeros((2, 2, 3))),
        "Vwind": (("ocean_time", "Y", "X"), np.zeros((2, 2, 3))),
        "Cs_r": (("Z"), np.linspace(-1, 0, 3)),
        "hc": 16,
    },
    coords={
        "ocean_time": ("ocean_time", [0, 1], {"units": "seconds since 1970-01-01"}),
        "s_rho": (("Z"), np.linspace(-1, 0, 3)),
        "lon_rho": (("Y", "X"), np.array([[1, 2, 3], [1, 2, 3]])),
        "lat_rho": (("Y", "X"), np.array([[1, 1, 1], [2, 2, 2]])),
    },
)
ds_info = dict(
    lon_min=1, lon_max=3, lat_min=1, lat_max=2, start_time_model=0, end_time_fixed=1
)

ptm.config_ocean_model.register_on_the_fly(ds_info)


# also to use the user-defined template of the TXLA model, need to input where pooch is downloading
# the file
ptm.config_ocean_model.update_TXLA_with_download_location()


@pytest.mark.slow
def test_add_new_reader():
    """Add a separate reader from the defaults using ds."""

    manager = ptm.OpenDriftModel(
        steps=1, ocean_model="ONTHEFLY", lon=2, lat=1.5, start_time=0, time_step=0.01
    )
    manager.add_reader(ds=ds)


@pytest.mark.slow
def test_run_parquet():
    """Set up and run."""

    seeding_kwargs = dict(lon=-90, lat=28.7, number=1, start_time="2009-11-19T12:00:00")
    manager = ptm.OpenDriftModel(
        **seeding_kwargs,
        use_static_masks=True,
        steps=2,
        output_format="parquet",
        ocean_model="TXLA",
        ocean_model_local=False,
    )
    manager.run_all()

    assert "parquet" in manager.o.outfile_name


@pytest.mark.slow
def test_run_netcdf_and_plot():
    """Set up and run."""

    import tempfile

    ts = 6 * 60  # 6 minutes in seconds

    seeding_kwargs = dict(lon=-90, lat=28.7, number=1, start_time="2009-11-19T12:00:00")
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        manager = ptm.OpenDriftModel(
            **seeding_kwargs,
            use_static_masks=True,
            steps=2,
            output_format="netcdf",
            use_cache=True,
            interpolator_filename=temp_file.name,
            ocean_model="TXLA",
            ocean_model_local=False,
            plots={
                "all": {},
            },
            time_step=ts,
        )
        manager.run_all()

        assert "nc" in manager.o.outfile_name
        assert manager.config.interpolator_filename == Path(temp_file.name).with_suffix(
            ".pickle"
        )

        # Replace 'path_to_pickle_file.pkl' with the actual path to your pickle file
        with open(manager.config.interpolator_filename, "rb") as file:
            data = pickle.load(file)
        assert "spl_x" in data
        assert "spl_y" in data

    # check time_step across access points
    assert (
        # m.o._config["general:time_step_minutes"]["value"]  # this is not correct, don't know why
        manager.o.time_step.total_seconds()
        == ts
        == manager.config.time_step
        # == m.o.get_configspec()["general:time_step_minutes"]["value"]  # this is not correct, don't know why
    )
