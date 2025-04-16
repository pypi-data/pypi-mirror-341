import re

import numpy as np
import pandas as pd
import pytest

from asteca.cluster import Cluster


@pytest.fixture
def sample_data(N=50):
    """Fixture for sample data"""
    return pd.DataFrame(
        {
            "ra": np.random.uniform(0, 360, N),
            "dec": np.random.uniform(-90, 90, N),
            "magnitude": np.random.uniform(10, 20, N),
            "e_mag": np.random.uniform(0.1, 0.5, N),
            "color": np.random.uniform(0, 2, N),
            "e_color": np.random.uniform(0.1, 0.5, N),
            "pmra": np.random.uniform(-10, 10, N),
            "e_pmra": np.random.uniform(0.1, 0.5, N),
            "pmde": np.random.uniform(-10, 10, N),
            "e_pmde": np.random.uniform(0.1, 0.5, N),
            "plx": np.random.uniform(0.1, 10, N),
            "e_plx": np.random.uniform(0.1, 0.5, N),
        }
    )


def test_cluster_initialization(sample_data):
    """
    Test basic initialization of the Cluster object with valid data.
    """
    cluster = Cluster(
        ra=sample_data["ra"],
        dec=sample_data["dec"],
        magnitude=sample_data["magnitude"],
        e_mag=sample_data["e_mag"],
        color=sample_data["color"],
        e_color=sample_data["e_color"],
        pmra=sample_data["pmra"],
        e_pmra=sample_data["e_pmra"],
        pmde=sample_data["pmde"],
        e_pmde=sample_data["e_pmde"],
        plx=sample_data["plx"],
        e_plx=sample_data["e_plx"],
    )
    assert (cluster.ra == sample_data["ra"]).all()
    assert (cluster.dec == sample_data["dec"]).all()
    assert (cluster.magnitude == sample_data["magnitude"]).all()
    assert (cluster.e_mag == sample_data["e_mag"]).all()
    assert (cluster.color == sample_data["color"]).all()
    assert (cluster.e_color == sample_data["e_color"]).all()
    assert (cluster.pmra == sample_data["pmra"]).all()
    assert (cluster.e_pmra == sample_data["e_pmra"]).all()
    assert (cluster.pmde == sample_data["pmde"]).all()
    assert (cluster.e_pmde == sample_data["e_pmde"]).all()
    assert (cluster.plx == sample_data["plx"]).all()
    assert (cluster.e_plx == sample_data["e_plx"]).all()
    assert cluster.N_stars == 50, f"Expected 100 stars, but got {cluster.N_stars}"


def test_load_column_data_valid(sample_data):
    """
    Test loading column data with valid inputs.
    """
    cluster = Cluster(
        ra=sample_data["ra"],
        dec=sample_data["dec"],
        magnitude=sample_data["magnitude"],
        e_mag=sample_data["e_mag"],
        color=sample_data["color"],
        e_color=sample_data["e_color"],
        pmra=sample_data["pmra"],
        e_pmra=sample_data["e_pmra"],
        pmde=sample_data["pmde"],
        e_pmde=sample_data["e_pmde"],
        plx=sample_data["plx"],
        e_plx=sample_data["e_plx"],
    )
    assert hasattr(cluster, "ra")
    assert hasattr(cluster, "dec")
    assert hasattr(cluster, "mag")
    assert hasattr(cluster, "e_mag")
    assert hasattr(cluster, "colors")
    assert hasattr(cluster, "e_colors")
    assert hasattr(cluster, "pmra")
    assert hasattr(cluster, "e_pmra")
    assert hasattr(cluster, "pmde")
    assert hasattr(cluster, "e_pmde")
    assert hasattr(cluster, "plx")
    assert hasattr(cluster, "e_plx")


def test_cluster_initialization_missing_columns(sample_data):
    """
    Test initialization of Cluster object with missing required columns.
    """
    # No columns defined
    with pytest.raises(ValueError, match="No column names defined for cluster"):
        Cluster()

    # Missing uncertainties (required when these columns are provided)
    with pytest.raises(ValueError):
        Cluster(magnitude=sample_data["magnitude"])
        Cluster(color=sample_data["color"])
        Cluster(color=sample_data["color2"])
        Cluster(pmra=sample_data["pmra"])
        Cluster(pmra=sample_data["pmde"])
        Cluster(pmra=sample_data["plx"])


def test_load_column_data_invalid_column_names(sample_data):
    """
    Test loading column data with invalid column names.
    """
    with pytest.raises(KeyError):
        Cluster(ra=sample_data["invalid_ra"])


def test_get_center_knn_5d(sample_data):
    """
    Test get_center method with knn_5d algorithm.
    """
    cluster = Cluster(
        ra=sample_data["ra"],
        dec=sample_data["dec"],
        pmra=sample_data["pmra"],
        e_pmra=sample_data["e_pmra"],
        pmde=sample_data["pmde"],
        e_pmde=sample_data["e_pmde"],
        plx=sample_data["plx"],
        e_plx=sample_data["e_plx"],
    )
    cluster.get_center(algo="knn_5d")
    assert hasattr(cluster, "radec_c")
    assert hasattr(cluster, "pms_c")
    assert hasattr(cluster, "plx_c")


def test_get_center_knn_5d_missing_data(sample_data):
    """
    Test get_center method with missing required data for knn_5d algorithm.
    """
    # Missing pmra, pmde, plx
    cluster = Cluster(ra=sample_data["ra"], dec=sample_data["dec"])
    with pytest.raises(
        ValueError,
        match=re.escape("Algorithm 'knn_5d' requires (ra, dec, pmra, pmde, plx) data"),
    ):
        cluster.get_center(algo="knn_5d")


def test_get_center_kde_2d(sample_data):
    """
    Test get_center method with kde_2d algorithm.
    """
    # 'radec' method
    cluster = Cluster(ra=sample_data["ra"], dec=sample_data["dec"])
    cluster.get_center(algo="kde_2d", data_2d="radec")
    assert hasattr(cluster, "radec_c")

    # 'pms' method
    cluster = Cluster(
        pmra=sample_data["pmra"],
        e_pmra=sample_data["e_pmra"],
        pmde=sample_data["pmde"],
        e_pmde=sample_data["e_pmde"],
    )
    cluster.get_center(algo="kde_2d", data_2d="pms")
    assert hasattr(cluster, "pms_c")


def test_get_center_kde_2d_missing_data(sample_data):
    """
    Test get_center method with missing required data for kde_2d algorithm.
    """
    cluster = Cluster(
        ra=sample_data["ra"], pmra=sample_data["pmra"], e_pmra=sample_data["e_pmra"]
    )
    # 'radec' method
    with pytest.raises(ValueError, match=re.escape("Data for (ra, dec) is required")):
        cluster.get_center(algo="kde_2d", data_2d="radec")

    # 'pms' method
    with pytest.raises(
        ValueError, match=re.escape("Data for (pmra, pmde) is required")
    ):
        cluster.get_center(algo="kde_2d", data_2d="pms")


def test_get_center_invalid_algorithm(sample_data):
    """
    Test get_center method with an invalid algorithm.
    """
    cluster = Cluster(ra=sample_data["ra"])
    with pytest.raises(
        ValueError, match=re.escape("Selected method 'invalid_algo' not recognized")
    ):
        cluster.get_center(algo="invalid_algo")


def test_get_nmembers_ripley(sample_data):
    """
    Test get_nmembers method with Ripley algorithm.
    """
    cluster = Cluster(
        ra=sample_data["ra"],
        dec=sample_data["dec"],
        pmra=sample_data["pmra"],
        e_pmra=sample_data["e_pmra"],
        pmde=sample_data["pmde"],
        e_pmde=sample_data["e_pmde"],
        plx=sample_data["plx"],
        e_plx=sample_data["e_plx"],
    )
    cluster.get_center(algo="knn_5d")

    with pytest.warns(
        UserWarning, match=re.escape("The estimated number of cluster members is <25")
    ):
        cluster.get_nmembers(algo="ripley")
    assert hasattr(cluster, "N_cluster"), "Expected N_cluster attribute to be set"


def test_get_nmembers_density(sample_data):
    """
    Test get_nmembers method with density algorithm.
    """
    cluster = Cluster(
        ra=sample_data["ra"],
        dec=sample_data["dec"],
        pmra=sample_data["pmra"],
        e_pmra=sample_data["e_pmra"],
        pmde=sample_data["pmde"],
        e_pmde=sample_data["e_pmde"],
        plx=sample_data["plx"],
        e_plx=sample_data["e_plx"],
    )
    cluster.get_center(algo="knn_5d")
    cluster._get_radius(1.0)  # Manually set radius for testing
    with pytest.warns(
        UserWarning, match=re.escape("The estimated number of cluster members is <25")
    ):
        cluster.get_nmembers(algo="density")
    assert hasattr(cluster, "N_cluster"), "Expected N_cluster attribute to be set"


def test_get_nmembers_missing_attributes(sample_data):
    """
    Test get_nmembers method with missing required attributes.
    """
    cluster = Cluster(ra=sample_data["ra"])
    with pytest.raises(AttributeError):
        cluster.get_nmembers(algo="ripley")
    with pytest.raises(AttributeError):
        cluster.get_nmembers(algo="density")


def test_get_nmembers_invalid_algorithm(sample_data):
    """
    Test get_nmembers method with an invalid algorithm.
    """
    cluster = Cluster(ra=sample_data["ra"])
    with pytest.raises(
        ValueError, match=re.escape("Selected method 'invalid_algo' not recognized")
    ):
        cluster.get_nmembers(algo="invalid_algo")
