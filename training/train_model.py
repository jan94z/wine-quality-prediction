from sqlalchemy import create_engine
import click
import yaml
from pathlib import Path
import pandas as pd
import utils.utils as utils



def train_rf():
    

@click.command()
#@click.option()
def main():
    script_dir = Path(__file__).resolve().parent
    docker_compose_path = script_dir.parent / "docker" / "docker-compose.yml"
    with open(docker_compose_path, 'r') as file:
        docker_compose = yaml.safe_load(file)
    DATABASE_URL = utils.parse_docker_compose("./docker/docker-compose.yml")
    engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    main()