import numpy as np
import pytest

from asteca.isochrones import Isochrones


# Mock the isochrones_priv module to avoid actual file loading
class MockIsochronesPriv:
    @staticmethod
    def load(
        model,
        isochs_path,
        magnitude,
        color,
        color2,
        column_names,
        N_interp,
        parsec_rm_stage_9,
    ):
        # Return mock data for testing
        theor_tracks = np.random.rand(5, 10, 2, 2500)  # Mock theoretical tracks
        color_filters = {
            "color1": ("filter1", "filter2"),
            "color2": ("filter3", "filter4"),
        }
        met_age_dict = {
            "met": np.array([0.01, 0.02, 0.03]),
            "loga": np.array([7.0, 8.0, 9.0]),
        }
        N_isoch_files = 3
        return theor_tracks, color_filters, met_age_dict, N_isoch_files


# Fixture to create an instance of Isochrones with mock data
@pytest.fixture
def isochrones_instance():
    model = "PARSEC"
    isochs_path = "dummy_path"
    magnitude = "Gmag"
    color = ("G_BPmag", "G_RPmag")
    color2 = ("Jmag", "Hmag")
    magnitude_effl = 5000.0
    color_effl = (4000.0, 6000.0)
    color2_effl = (7000.0, 8000.0)
    z_to_FeH = 0.02
    N_interp = 2500
    parsec_rm_stage_9 = True
    column_names = {"mass_col": "Mini", "met_col": "Zini", "age_col": "logAge"}
    verbose = 1

    # Patch the isochrones_priv module with the mock
    import asteca.isochrones as isochrones_module

    isochrones_module.isochrones_priv = MockIsochronesPriv

    return Isochrones(
        model=model,
        isochs_path=isochs_path,
        magnitude=magnitude,
        color=color,
        color2=color2,
        magnitude_effl=magnitude_effl,
        color_effl=color_effl,
        color2_effl=color2_effl,
        z_to_FeH=z_to_FeH,
        N_interp=N_interp,
        parsec_rm_stage_9=parsec_rm_stage_9,
        column_names=column_names,
        verbose=verbose,
    )


# Test initialization of Isochrones class
def test_isochrones_initialization(isochrones_instance):
    assert isochrones_instance.model == "PARSEC"
    assert isochrones_instance.isochs_path == "dummy_path"
    assert isochrones_instance.magnitude == "Gmag"
    assert isochrones_instance.color == ("G_BPmag", "G_RPmag")
    assert isochrones_instance.color2 == ("Jmag", "Hmag")
    assert isochrones_instance.magnitude_effl == 5000.0
    assert isochrones_instance.color_effl == (4000.0, 6000.0)
    assert isochrones_instance.color2_effl == (7000.0, 8000.0)
    assert isochrones_instance.z_to_FeH == 0.02
    assert isochrones_instance.N_interp == 2500
    assert isochrones_instance.parsec_rm_stage_9 is True
    assert isochrones_instance.column_names == {
        "mass_col": "Mini",
        "met_col": "Zini",
        "age_col": "logAge",
    }
    assert isochrones_instance.verbose == 1


# Test validation of color and color2 parameters
def test_color_validation():
    with pytest.raises(
        ValueError,
        match="Second color is defined but its effective lambdas are missing.",
    ):
        Isochrones(
            model="PARSEC",
            isochs_path="dummy_path",
            magnitude="Gmag",
            color=("G_BPmag", "G_RPmag"),
            color2=("Jmag", "Hmag"),
            magnitude_effl=5000.0,
            color_effl=(4000.0, 6000.0),
            color2_effl=None,
            z_to_FeH=0.02,
            N_interp=2500,
            parsec_rm_stage_9=True,
            column_names={"mass_col": "Mini", "met_col": "Zini", "age_col": "logAge"},
            verbose=1,
        )

    with pytest.raises(
        ValueError,
        match="Lambdas for the second color are defined but second color is missing.",
    ):
        Isochrones(
            model="PARSEC",
            isochs_path="dummy_path",
            magnitude="Gmag",
            color=("G_BPmag", "G_RPmag"),
            color2=None,
            magnitude_effl=5000.0,
            color_effl=(4000.0, 6000.0),
            color2_effl=(7000.0, 8000.0),
            z_to_FeH=0.02,
            N_interp=2500,
            parsec_rm_stage_9=True,
            column_names={"mass_col": "Mini", "met_col": "Zini", "age_col": "logAge"},
            verbose=1,
        )


# Test model validation
def test_model_validation():
    with pytest.raises(
        ValueError, match="Model 'INVALID' not recognized. Should be one of"
    ):
        Isochrones(
            model="INVALID",
            isochs_path="dummy_path",
            magnitude="Gmag",
            color=("G_BPmag", "G_RPmag"),
            color2=None,
            magnitude_effl=5000.0,
            color_effl=(4000.0, 6000.0),
            color2_effl=None,
            z_to_FeH=0.02,
            N_interp=2500,
            parsec_rm_stage_9=True,
            column_names={"mass_col": "Mini", "met_col": "Zini", "age_col": "logAge"},
            verbose=1,
        )


# Test z_to_FeH conversion
def test_z_to_FeH_conversion(isochrones_instance):
    assert "FeH" in str(isochrones_instance.met_age_dict["met"])


# Test verbose print method
def test_verbose_print(isochrones_instance, capsys):
    isochrones_instance._vp("Test message", level=0)
    captured = capsys.readouterr()
    assert "Test message" in captured.out

    isochrones_instance._vp("Hidden message", level=2)
    captured = capsys.readouterr()
    assert "Hidden message" not in captured.out


# Test for missing required parameters
def test_missing_required_parameters():
    with pytest.raises(TypeError):
        Isochrones()  # Missing all required parameters


# Test for effective wavelength validation
def test_effective_wavelength_validation():
    with pytest.raises(
        ValueError,
        match="Lambdas for the second color are defined but second color is missing.",
    ):
        Isochrones(
            model="PARSEC",
            isochs_path="dummy_path",
            magnitude="Gmag",
            color=("G_BPmag", "G_RPmag"),
            color2=None,
            magnitude_effl=5000.0,
            color_effl=(4000.0, 6000.0),
            color2_effl=(7000.0, 8000.0),
            z_to_FeH=0.02,
            N_interp=2500,
            parsec_rm_stage_9=True,
            column_names={"mass_col": "Mini", "met_col": "Zini", "age_col": "logAge"},
            verbose=1,
        )


# Test for column names validation
def test_column_names_validation():
    with pytest.raises(ValueError, match="Column names dictionary must contain"):
        Isochrones(
            model="PARSEC",
            isochs_path="dummy_path",
            magnitude="Gmag",
            color=("G_BPmag", "G_RPmag"),
            color2=None,
            magnitude_effl=5000.0,
            color_effl=(4000.0, 6000.0),
            color2_effl=None,
            z_to_FeH=0.02,
            N_interp=2500,
            parsec_rm_stage_9=True,
            column_names={"mass_col": "Mini"},  # Missing required keys
            verbose=1,
        )


# Test for interpolation points
def test_interpolation_points(isochrones_instance):
    assert isochrones_instance.N_interp == 2500


# Test for PARSEC stage 9 removal
def test_parsec_stage_9_removal(isochrones_instance):
    assert isochrones_instance.parsec_rm_stage_9 is True


# Test for metallicity and age ranges
def test_metallicity_age_ranges(isochrones_instance):
    assert isochrones_instance.zmin == 0.01
    assert isochrones_instance.zmax == 0.03
    assert isochrones_instance.amin == 7.0
    assert isochrones_instance.amax == 9.0


def test_verbose_level(isochrones_instance, capsys):
    # Test verbose level 1 (default)
    isochrones_instance._vp("Test message level 1", level=0)
    captured = capsys.readouterr()
    assert "Test message level 1" in captured.out  # Should print the message

    # Test verbose level 2 (higher than current verbose level)
    isochrones_instance._vp("Test message level 2", level=2)
    captured = capsys.readouterr()
    assert "Test message level 2" not in captured.out  # Should not print the message

    # Change verbose level to 2 and test again
    isochrones_instance.verbose = 2
    isochrones_instance._vp("Test message level 2 updated", level=2)
    captured = capsys.readouterr()
    assert "Test message level 2 updated" in captured.out  # Should print the message

    # Test verbose level 0 (no output)
    isochrones_instance.verbose = 0
    isochrones_instance._vp("Test message level 0", level=0)
    captured = capsys.readouterr()
    assert "Test message level 0" not in captured.out  # Should not print the message
