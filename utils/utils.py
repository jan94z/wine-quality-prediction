import yaml

def parse_docker_compose(docker_compose: yaml) -> str:
    """
    Function to create a SQLAlchemy engine.
    Args:
        docker_compose (yaml): The docker-compose configuration.
    Returns:
        str: The database URL.
    """
    user = docker_compose["services"]["postgres"]["environment"]["POSTGRES_USER"]
    password = docker_compose["services"]["postgres"]["environment"]["POSTGRES_PASSWORD"]
    host = "localhost"
    port = docker_compose["services"]["postgres"]["ports"][0].split(':')[0]
    database = docker_compose["services"]["postgres"]["environment"]["POSTGRES_DB"]
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"