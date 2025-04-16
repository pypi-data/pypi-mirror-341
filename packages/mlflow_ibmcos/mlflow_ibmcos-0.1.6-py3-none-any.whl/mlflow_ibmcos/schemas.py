from typing import Union
from typing_extensions import Annotated
from pathlib import Path
from pydantic import AfterValidator


def validate_model_path(v: Union[str, Path]) -> str:
    path_obj = Path(v) if isinstance(v, str) else v
    if not path_obj.exists():
        raise ValueError(f"Path {v} does not exist.")
    return str(path_obj.resolve())


ModelPath = Annotated[Union[str, Path], AfterValidator(validate_model_path)]
