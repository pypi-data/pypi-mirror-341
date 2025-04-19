from usdm4_excel.__version__ import __package_version__, __model_version__


def test_package_version():
    """Test that the package version is a valid string."""
    assert isinstance(__package_version__, str)
    assert __package_version__ == "0.3.0"


def test_model_version():
    """Test that the model version is a valid string."""
    assert isinstance(__model_version__, str)
    assert __model_version__ == "3.12.0"
