from .project import Project


def create_empty_project():
    json = {
        "Toolbox": {
            "Spaces": [],
            "Blocks": [],
        },
        "Workbench": {
            "Processors": [],
            "Wires": [],
            "Systems": [],
        },
    }
    return Project(json)
