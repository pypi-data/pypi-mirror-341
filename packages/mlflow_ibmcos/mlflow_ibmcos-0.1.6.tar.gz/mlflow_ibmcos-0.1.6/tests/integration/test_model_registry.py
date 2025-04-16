from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List

import mlflow
import mlflow.exceptions
from pydantic import ValidationError
from mlflow_ibmcos.exceptions import MODEL_ALREADY_EXISTS, ModelAlreadyExistsError
from mlflow_ibmcos.model_registry import COSModelRegistry
import pytest
import os
from pytest_mock import MockerFixture

FIXTURES_PATH = Path(__file__).parent / "fixtures"


@pytest.fixture
def models_to_delete(request: pytest.FixtureRequest) -> Callable:
    """
    A fixture that provides a function to delete model versions.
    The models will be deleted immediately when the function is called,
    and a cleanup hook ensures all registered models are deleted when the test finishes.
    """
    models_to_delete: List[COSModelRegistry] = []

    def wrapper(model: COSModelRegistry) -> None:
        # Register the model for potential cleanup at the end of the test
        models_to_delete.append(model)

    def finalizer():
        # Cleanup hook that runs when the test function finishes
        for model in models_to_delete:
            try:
                model.delete_model_version(confirm=True)
            except Exception:
                # Ignore errors during cleanup - model might already be deleted
                pass

    request.addfinalizer(finalizer)

    return wrapper


@pytest.fixture
def bucket_name() -> str:
    return os.getenv("COS_BUCKET_NAME", "")


@pytest.fixture
def proxy() -> Dict[str, str]:
    """
    Fixture to provide proxy settings for the test environment.
    This fixture retrieves the HTTP and HTTPS proxy settings from environment variables
    """
    return {
        "http": os.getenv("HTTP_PROXY", ""),
        "https": os.getenv("HTTPS_PROXY", ""),
    }


@pytest.fixture
def push_tagged_model(bucket_name: str) -> Generator[COSModelRegistry, Any, None]:
    """
    Creates a test tagged model and pushes it to the COS Model Registry.

    This function serves as a test fixture that creates a COSModelRegistry instance,
    logs a PyFunc model as code, and yields the registry for testing purposes.
    After the test is complete, it cleans up by deleting the model version.

    Parameters
    ----------
    bucket_name : str
        The name of the COS bucket to use for the model registry.

    Yields
    ------
    COSModelRegistry
        A configured model registry instance with a test model pushed to it.

    Notes
    -----
    This is designed to be used as a pytest fixture with cleanup handling.
    """

    # Create a test model and push it to the registry
    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="0.0.1",
    )
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
    )
    yield registry

    # Clean up the test model
    registry.delete_model_version(confirm=True)


@pytest.fixture
def mock_hash(mocker: MockerFixture):
    """
    Creates a test fixture that mocks the COSModelRegistry.write_hash method.

    This fixture allows tests to capture the generated fingerprint hash during model registration
    by copying it to a specified temporary path. This is useful for verifying that fingerprinting
    is correctly performed in tests without having to recalculate hashes.

    Args:
        mocker (MockerFixture): The pytest-mock fixture that provides patching functionality.

    Returns:
        callable: A wrapper function that accepts a tmp_path parameter and returns the mock patch.
            The returned function signature is:
                wrapper(tmp_path: Path) -> MagicMock
    """
    original_write_hash = COSModelRegistry.write_hash

    def mocked_write_hash(directory: str, tmp_path: Path):
        original_write_hash(directory)
        with open(os.path.join(directory, "fingerprint")) as f:
            hash_ = f.read()
        with open(os.path.join(tmp_path, "fingerprint"), "w") as f:
            f.write(hash_)
        return

    def wrapper(tmp_path: Path):
        return mocker.patch.object(
            target=COSModelRegistry,
            attribute="write_hash",
            new=partial(mocked_write_hash, tmp_path=tmp_path),
        )

    return wrapper


def test_model_registration_process(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    """
    Test the end-to-end model registration process using COSModelRegistry.

    This test verifies the full workflow of:
    1. Logging a PyFunc model with code and artifacts to the registry
    2. Verifying the model fingerprint
    3. Downloading the model artifacts
    4. Checking the structure of downloaded artifacts
    5. Loading the model
    6. Making predictions with the loaded model

    Parameters
    ----------
    bucket_name : str
        Name of the COS bucket to use for the model registry.
        You can set this up using the environment variable COS_BUCKET_NAME.
    mock_hash : Callable
        Mock function for generating fingerprints
    tmp_path : Path
        Temporary path provided by pytest fixture for artifact storage

    Notes
    -----
    This test requires fixture files: modelcode.py and model.pkl
    """
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="latest",
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
    )
    assert registry.artifact_uri == f"s3://{bucket_name}/{registry.PREFIX}/test/latest"
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/latest/modelcode.py"),
        tmp_path.joinpath("test/latest/python_env.yaml"),
        tmp_path.joinpath("test/latest/conda.yaml"),
        tmp_path.joinpath("test/latest/requirements.txt"),
        tmp_path.joinpath("test/latest/artifacts/model.pkl"),
        tmp_path.joinpath("test/latest/MLmodel"),
        tmp_path.joinpath("test/latest/fingerprint"),
        tmp_path.joinpath("test/latest/artifacts"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert prediction == ["5", "5"]


def test_model_registration_with_tagged_model_and_no_bucket(
    mock_hash: Callable, models_to_delete: Callable, tmp_path: Path
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        model_name="test",
        model_version="0.0.0",
    )
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
    )
    models_to_delete(registry)
    assert (
        registry.artifact_uri == f"s3://{registry._bucket}/{registry.PREFIX}/test/0.0.0"
    )

    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/0.0.0/modelcode.py"),
        tmp_path.joinpath("test/0.0.0/python_env.yaml"),
        tmp_path.joinpath("test/0.0.0/conda.yaml"),
        tmp_path.joinpath("test/0.0.0/requirements.txt"),
        tmp_path.joinpath("test/0.0.0/artifacts/model.pkl"),
        tmp_path.joinpath("test/0.0.0/MLmodel"),
        tmp_path.joinpath("test/0.0.0/fingerprint"),
        tmp_path.joinpath("test/0.0.0/artifacts"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert prediction == ["5", "5"]


def test_registering_model_which_already_exists(push_tagged_model: COSModelRegistry):
    """
    Test that attempting to register a tagged model that already exists raises ModelAlreadyExistsError.

    This test verifies that the COSModelRegistry correctly raises a ModelAlreadyExistsError
    when trying to log a PyFunc model that has already been registered. The test expects
    the error message to match the predefined MODEL_ALREADY_EXISTS constant.

    Args:
        push_model (COSModelRegistry): A fixture providing a COSModelRegistry instance
                                      with a model already registered.
    """

    with pytest.raises(
        expected_exception=ModelAlreadyExistsError, match=MODEL_ALREADY_EXISTS
    ):
        push_tagged_model.log_pyfunc_model_as_code(
            model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
            artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
        )


def test_model_registration_process_with_custom_config(
    bucket_name: str,
    tmp_path: Path,
    proxy: Dict[str, str],
    mock_hash: Callable,
    models_to_delete: Callable,
):
    """
    Test the custom configuration of the COSModelRegistry class.

    This test verifies that the custom configuration is correctly applied
    and that the model registry behaves as expected with the custom settings.
    """
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="test",
        model_version="latest",
        config=dict(proxies=proxy),
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcode.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "model.pkl"},
    )
    assert registry.artifact_uri == f"s3://{bucket_name}/{registry.PREFIX}/test/latest"
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("test/latest/modelcode.py"),
        tmp_path.joinpath("test/latest/python_env.yaml"),
        tmp_path.joinpath("test/latest/conda.yaml"),
        tmp_path.joinpath("test/latest/requirements.txt"),
        tmp_path.joinpath("test/latest/artifacts/model.pkl"),
        tmp_path.joinpath("test/latest/MLmodel"),
        tmp_path.joinpath("test/latest/fingerprint"),
        tmp_path.joinpath("test/latest/artifacts"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        [
            {"text": "Hello"},
            {"text": "World"},
        ]
    )
    assert prediction == ["5", "5"]


def test_model_registration_process_with_params(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="testwithparams",
        model_version="latest",
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcodewithparams.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "modelwithparams.pkl"},
        input_example=(
            ["hello", "world"],
            {
                "capitalize_only_first": True,
                "add_prefix": "prefix_",
            },
        ),
    )
    assert (
        registry.artifact_uri
        == f"s3://{bucket_name}/{registry.PREFIX}/testwithparams/latest"
    )
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("testwithparams/latest/modelcodewithparams.py"),
        tmp_path.joinpath("testwithparams/latest/python_env.yaml"),
        tmp_path.joinpath("testwithparams/latest/conda.yaml"),
        tmp_path.joinpath("testwithparams/latest/requirements.txt"),
        tmp_path.joinpath("testwithparams/latest/artifacts/modelwithparams.pkl"),
        tmp_path.joinpath("testwithparams/latest/MLmodel"),
        tmp_path.joinpath("testwithparams/latest/fingerprint"),
        tmp_path.joinpath("testwithparams/latest/artifacts"),
        tmp_path.joinpath("testwithparams/latest/serving_input_example.json"),
        tmp_path.joinpath("testwithparams/latest/input_example.json"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)

    prediction = model.predict(
        ["hi", "there"],
        params={
            "capitalize_only_first": False,
            "add_prefix": "prefix_",
        },
    )
    assert prediction == ["prefix_HI", "prefix_THERE"]

    # If we don't pass the params, it should use the default values
    # which are: capitalize_only_first=True, add_prefix="prefix_"
    prediction = model.predict(
        ["hi", "there"],
    )
    assert prediction == ["prefix_Hi", "prefix_There"]

    # If we juts pass the capitalize_only_first param, it should use the default value for add_prefix
    # which is: add_prefix="prefix_"
    prediction = model.predict(
        ["hi", "there"],
        params={
            "capitalize_only_first": False,
        },
    )
    assert prediction == ["prefix_HI", "prefix_THERE"]


def test_model_registration_process_with_none_params(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="testwithparams",
        model_version="latest",
    )
    models_to_delete(registry)
    with pytest.raises(expected_exception=mlflow.exceptions.MlflowException):
        registry.log_pyfunc_model_as_code(
            model_code_path=FIXTURES_PATH / "modelascode" / "modelcodewithparams.py",
            artifacts={"model": FIXTURES_PATH / "artifacts" / "modelwithparams.pkl"},
            input_example=(
                ["hello", "world"],
                {
                    "capitalize_only_first": True,
                    "add_prefix": None,
                },
            ),
        )
    assert (
        registry.artifact_uri
        == f"s3://{bucket_name}/{registry.PREFIX}/testwithparams/latest"
    )


def test_model_registration_process_without_required_params(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="testwithparams",
        model_version="latest",
    )
    models_to_delete(registry)
    registry.log_pyfunc_model_as_code(
        model_code_path=FIXTURES_PATH / "modelascode" / "modelcodewithparams.py",
        artifacts={"model": FIXTURES_PATH / "artifacts" / "modelwithparams.pkl"},
        input_example=["hello", "world"],
    )
    assert (
        registry.artifact_uri
        == f"s3://{bucket_name}/{registry.PREFIX}/testwithparams/latest"
    )
    assert (
        registry.artifact_uri
        == f"s3://{bucket_name}/{registry.PREFIX}/testwithparams/latest"
    )
    remote_fingerprint = registry._get_remote_fingerprint()
    assert tmp_path.joinpath("fingerprint").read_text() == remote_fingerprint

    # Now download the model
    path = registry.download_artifacts(dst_path=tmp_path)
    model_files = set(Path(path).glob("**/*"))
    expected_files = {
        tmp_path.joinpath("testwithparams/latest/modelcodewithparams.py"),
        tmp_path.joinpath("testwithparams/latest/python_env.yaml"),
        tmp_path.joinpath("testwithparams/latest/conda.yaml"),
        tmp_path.joinpath("testwithparams/latest/requirements.txt"),
        tmp_path.joinpath("testwithparams/latest/artifacts/modelwithparams.pkl"),
        tmp_path.joinpath("testwithparams/latest/MLmodel"),
        tmp_path.joinpath("testwithparams/latest/fingerprint"),
        tmp_path.joinpath("testwithparams/latest/artifacts"),
        tmp_path.joinpath("testwithparams/latest/serving_input_example.json"),
        tmp_path.joinpath("testwithparams/latest/input_example.json"),
    }
    assert model_files == expected_files

    model = registry.load_model(model_local_path=path)
    with pytest.raises(expected_exception=KeyError):
        model.predict(
            ["hi", "there"],
            params={
                "capitalize_only_first": False,
                "add_prefix": "prefix_",
            },
        )


def test_model_registration_wrong_artifacts_path(
    bucket_name: str, mock_hash: Callable, tmp_path: Path, models_to_delete: Callable
):
    mock_hash(tmp_path)

    registry = COSModelRegistry(
        bucket=bucket_name,
        model_name="testnoartifacts",
        model_version="latest",
    )
    models_to_delete(registry)
    with pytest.raises(
        expected_exception=ValidationError, match="Path fakepath does not exist"
    ):
        registry.log_pyfunc_model_as_code(
            model_code_path=FIXTURES_PATH / "modelascode" / "modelcodewithparams.py",
            artifacts={"model": "fakepath"},
            input_example=(
                ["hello", "world"],
                {
                    "capitalize_only_first": True,
                    "add_prefix": None,
                },
            ),
        )
