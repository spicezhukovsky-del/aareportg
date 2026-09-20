from functools import lru_cache
from pathlib import Path
from tomllib import load
from typing import Type, TypeVar

from pydantic import BaseModel, SecretStr


ConfigType = TypeVar("ConfigType", bound=BaseModel)


class BotConfig(BaseModel):
    token: SecretStr


@lru_cache
def parse_config_file() -> dict:
    # Формирование пути к файлу settings.toml
    config_path = Path(__file__).parent.parent.parent.parent / "connections_file"
    toml_file_con = config_path / "settings.toml"

    print(toml_file_con)
    print(toml_file_con.exists())

    if not toml_file_con.exists():
        error = "Could not find settings file"
        raise ValueError(error)
    # Читаем сам файл, пытаемся его прочитать как TOML
    with open(toml_file_con, "rb") as file:
        config_data = load(file)
    return config_data


def get_config(model: Type[ConfigType], root_key: str) -> ConfigType:
    config_dict = parse_config_file()
    if root_key not in config_dict:
        error = f"Key {root_key} not found"
        raise ValueError(error)
    return model.model_validate(config_dict[root_key])
