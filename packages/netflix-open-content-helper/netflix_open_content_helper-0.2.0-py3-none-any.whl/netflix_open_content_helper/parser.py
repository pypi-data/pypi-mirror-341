import csv
import pathlib

import yaml
from pydantic import TypeAdapter

from netflix_open_content_helper.models import Shot


def parse_shotfile(shotfile: str) -> list[Shot]:
    shots = []
    if shotfile.endswith(".yaml"):
        shots = parse_shotfile_yaml(shotfile)
    elif shotfile.endswith(".json"):
        shots = parse_shotfile_json(shotfile)
    elif shotfile.endswith(".csv"):
        shots = parse_shotfile_csv(shotfile)
    else:
        raise ValueError(f"Unknown file type: {shotfile}")
    return shots


def parse_shotfile_csv(shotfile: str) -> list[Shot]:
    with open(shotfile) as f:
        reader = csv.DictReader(f)
        shots = [Shot.model_validate(row) for row in reader]
    return shots


def parse_shotfile_yaml(shotfile: str) -> list[Shot]:
    with open(shotfile) as stream:
        yaml_contents = yaml.safe_load(stream)
        shots = [Shot.model_validate(shot) for shot in yaml_contents]
    return shots


def parse_shotfile_json(shotfile: str) -> list[Shot]:
    shot_list_adapter = TypeAdapter(list[Shot])
    json_string = pathlib.Path(shotfile).read_text()
    shots = shot_list_adapter.validate_json(json_string)
    return shots
