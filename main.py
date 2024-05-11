import os
import tomli
from pipeline import run_pipeline


with open(os.path.join(os.path.dirname(__file__), "config.toml"), "rb") as f:
    config = tomli.load(f)
    email = config["AUTH"]["EMAIL"]
run_pipeline(email)
