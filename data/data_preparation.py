import pandas as pd 
from sqlalchemy import create_engine
from pathlib import Path
import click
import yaml

def data_exploration(df:pd.DataFrame, title:str) -> None:
    """
    Function to explore the dataset.
    Args:
        df (pd.DataFrame): The DataFrame to explore.
        title (str): Title for the exploration output.
    """ 
    print("-----------------------------------")
    print(f'{title} - Head:\n', df.head())
    print("-----------------------------------")
    print('Columns:', len(df.columns))
    print('Rows:', len(df))
    print("-----------------------------------")
    print('Summary:\n', df.describe().round(2))
    print("-----------------------------------")
    print("Missing Values:\n", df.isnull().sum())
    print("-----------------------------------")

def insert_data_into_db(docker_compose: yaml, wine_quality_df: pd.DataFrame, table_name:str) -> None:     
    user = docker_compose["services"]["postgres"]["environment"]["POSTGRES_USER"]
    password = docker_compose["services"]["postgres"]["environment"]["POSTGRES_PASSWORD"]
    host = "localhost"
    port = docker_compose["services"]["postgres"]["ports"][0].split(':')[0]
    database = docker_compose["services"]["postgres"]["environment"]["POSTGRES_DB"]
    
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(DATABASE_URL)

    wine_quality_df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Finished import into table '{table_name}'.")

@click.command()
@click.option('--path', '--p', help='Path to the data directory')
@click.option('--explore', '--e', is_flag=True, help='Explore the data')
def main(path: str, explore: bool) -> None:
    # Prepare paths
    input_path = Path(path)
    white_path = input_path / 'winequality-white.csv'
    red_path = input_path / 'winequality-red.csv'

    # Load datasets
    white = pd.read_csv(white_path, sep=';')
    red = pd.read_csv(red_path, sep=';')

    # Add wine type column
    white["wine_type"] = "white"
    red["wine_type"] = "red"

    # Combine datasets into one
    combined_df = pd.concat([white, red], ignore_index=True)

    # Explore data
    if explore:
        data_exploration(red, "Red Wine Quality Dataset")
        data_exploration(white, "White Wine Quality Dataset")
        data_exploration(combined_df, "Combined Dataset")

    # Load docker-compose config
    try:
        script_dir = Path(__file__).resolve().parent
        docker_compose_path = script_dir.parent / "docker" / "docker-compose.yml"
        with open(docker_compose_path, 'r') as file:
            docker_compose = yaml.safe_load(file)
    except FileNotFoundError:
        print("docker-compose.yml not found. Please check the path.")
        return

    # Insert combined data into DB
    combined_df.columns = [col.strip().replace(" ", "_").lower() for col in combined_df.columns]
    insert_data_into_db(docker_compose, combined_df, 'wine_samples')

if __name__ == "__main__":
    main()

    

