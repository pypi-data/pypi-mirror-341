import yaml
import typer

from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
from dvuploader import DVUploader, File
from dvuploader.utils import add_directory


class CliInput(BaseModel):
    """
    Model for CLI input parameters.

    Attributes:
        api_token (str): API token for authentication with Dataverse
        dataverse_url (str): URL of the Dataverse instance
        persistent_id (str): Persistent identifier of the dataset
        files (List[File]): List of files to upload
        n_jobs (int): Number of parallel upload jobs to run (default: 1)
    """

    api_token: str
    dataverse_url: str
    persistent_id: str
    files: List[File]
    n_jobs: int = 1


app = typer.Typer()

def _enumerate_filepaths(filepaths: List[str], recurse: bool) -> List[File]:
    """
    Take a list of filepaths and transform it into a list of File objects, optionally recursing into each of them.

    Args:
        filepaths (List[str]): a list of files or paths for upload
        recurse (bool): whether to recurse into each given filepath

    Returns:
        List[File]: A list of File objects representing the files extracted from all filepaths.
    
    Raises:
        FileNotFoundError: If a filepath does not exist.
        IsADirectoryError: If recurse is False and a filepath points to a directory instead of a file.
    """
    if not recurse:
        return [File(filepath=filepath) for filepath in filepaths]

    files = []
    for fp in filepaths:
        files.extend(add_directory(fp) if Path(fp).is_dir() else [File(filepath=fp)])
    return files


def _parse_yaml_config(path: str) -> CliInput:
    """
    Parse a YAML/JSON configuration file into a CliInput object.

    Args:
        path (str): Path to a YAML/JSON configuration file containing upload specifications

    Returns:
        CliInput: Object containing upload configuration parameters

    Raises:
        yaml.YAMLError: If the YAML/JSON file is malformed
        ValidationError: If the configuration data does not match the CliInput model
    """
    return CliInput(**yaml.safe_load(open(path)))  # type: ignore


def _validate_inputs(
    filepaths: List[str],
    pid: str,
    dataverse_url: str,
    api_token: str,
    recurse: bool,
    config_path: Optional[str],
) -> None:
    """
    Validate CLI input parameters.

    Checks for valid combinations of configuration file and command line parameters.

    Args:
        filepaths (List[str]): List of files to upload
        pid (str): Persistent identifier of the dataset
        dataverse_url (str): URL of the Dataverse instance
        api_token (str): API token for authentication
        recurse (bool): Whether to recurse into filepaths
        config_path (Optional[str]): Path to configuration file

    Raises:
        typer.BadParameter: If both config file and filepaths are specified
        typer.BadParameter: If both config file and recurse are specified
        typer.BadParameter: If neither config file nor required parameters are provided
    """
    if config_path is not None:
        if len(filepaths) > 0:
            raise typer.BadParameter(
                "Cannot specify both a JSON/YAML file and a list of filepaths."
            )
        if recurse:
            raise typer.BadParameter(
                "Cannot specify both a JSON/YAML file and recurse into filepaths."
            )

    _has_meta_params = all(arg is not None for arg in [pid, dataverse_url, api_token])
    _has_config_file = config_path is not None

    if _has_meta_params and _has_config_file:
        print(
            "\n⚠️  Warning\n"
            "├── You have specified both a configuration file and metadata parameters via the command line.\n"
            "╰── Will use metadata parameters specified in the config file."
        )
    elif not _has_meta_params and not _has_config_file:
        raise typer.BadParameter(
            "You must specify either a JSON/YAML file or metadata parameters (dv_url, api_token, pid, files) via the command line."
        )


@app.command()
def main(
    filepaths: Optional[List[str]] = typer.Argument(
        default=None,
        help="A list of filepaths to upload.",
    ),
    recurse: Optional[bool] = typer.Option(
        default=False,
        help="Enable recursion into filepaths.",
    ),
    pid: str = typer.Option(
        default=None,
        help="The persistent identifier of the Dataverse dataset.",
    ),
    api_token: str = typer.Option(
        default=None,
        help="The API token for the Dataverse repository.",
    ),
    dataverse_url: str = typer.Option(
        default=None,
        help="The URL of the Dataverse repository.",
    ),
    config_path: Optional[str] = typer.Option(
        default=None,
        help="Path to a JSON/YAML file containing specifications for the files to upload.",
    ),
    n_jobs: int = typer.Option(
        default=1,
        help="Number of parallel upload jobs to run.",
    ),
):
    """
    Upload files to a Dataverse repository.

    Files can be specified either directly via command line arguments or through a
    configuration file. The configuration file can be either YAML or JSON format.

    If using command line arguments, you must specify:
    - One or more filepaths to upload
    - (Optional) whether to recurse into the filepaths
    - The dataset's persistent identifier
    - A valid API token
    - The Dataverse repository URL

    If using a configuration file, it should contain:
    - api_token: API token for authentication
    - dataverse_url: URL of the Dataverse instance
    - persistent_id: Dataset persistent identifier
    - files: List of file specifications
    - n_jobs: (optional) Number of parallel upload jobs

    Examples:
        Upload files via command line:
        $ dvuploader file1.txt file2.txt --pid doi:10.5072/FK2/123456 --api-token abc123 --dataverse-url https://demo.dataverse.org

        Upload files via config file:
        $ dvuploader --config-path upload_config.yaml
    """

    if filepaths is None:
        filepaths = []

    _validate_inputs(
        filepaths=filepaths,
        pid=pid,
        dataverse_url=dataverse_url,
        api_token=api_token,
        recurse=recurse,
        config_path=config_path,
    )

    if config_path:
        # PyYAML is a superset of JSON, so we can use the same function to parse both
        cli_input = _parse_yaml_config(config_path)
    else:
        cli_input = CliInput(
            api_token=api_token,
            dataverse_url=dataverse_url,
            persistent_id=pid,
            files=_enumerate_filepaths(filepaths=filepaths, recurse=recurse),
        )

    uploader = DVUploader(files=cli_input.files)
    uploader.upload(
        persistent_id=cli_input.persistent_id,
        dataverse_url=cli_input.dataverse_url,
        api_token=cli_input.api_token,
        n_parallel_uploads=n_jobs,
    )


if __name__ == "__main__":
    app()
