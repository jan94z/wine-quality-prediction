from data.data_preparation import parse_docker_compose


DATABASE_URL = parse_docker_compose("docker-compose.yml")