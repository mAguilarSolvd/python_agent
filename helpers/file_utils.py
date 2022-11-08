from os import getcwd, chdir, path, listdir


def search_resources_dir() -> str:
    absolute_path = getcwd()
    directories = absolute_path.split("/")
    current_directory = directories[len(directories) - 1]

    while current_directory != "resources":
        last_directory = getcwd()
        chdir("..")

        if last_directory == getcwd():
            raise AgentNotFound("Agent not found!")

        if path.exists('resources'):
            return getcwd() + "/resources"

        current_directory = getcwd()


def search_agent_file(agent_dir: str) -> str:
    for file in listdir(agent_dir):
        if file.startswith("agent."):
            match file:
                case "agent.yaml":
                    return "yaml"
                case "agent.yml":
                    return "yml"
                case "agent.toml":
                    return "toml"
                case "agent.properties":
                    return "properties"
                case _:
                    raise AgentNotFound("Agent not found!")


class AgentNotFound(Exception):
    pass


if __name__ == "__main__":
    agent_path = search_resources_dir()
    print(search_agent_file(agent_path))
