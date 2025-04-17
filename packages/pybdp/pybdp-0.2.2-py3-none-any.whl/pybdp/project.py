from jsonschema import validate
from .schema import schema
from .toolbox import load_toolbox
from .workbench import load_workbench
from .convenience import find_duplicates
from copy import deepcopy
import json


class Project:
    def __init__(self, json: dict):
        self.raw_data = json

        # Load toolbox
        self.toolbox = load_toolbox(json["Toolbox"])

        # Bring in mapping and objects to the project level
        self.blocks = self.toolbox.blocks
        self.spaces = self.toolbox.spaces
        self.blocks_map = self.toolbox.blocks_map
        self.spaces_map = self.toolbox.spaces_map
        self.toolbox_map = self.toolbox.toolbox_map

        # Load workbench
        self.workbench = load_workbench(
            json["Workbench"], self.blocks_map, self.spaces_map
        )

        self.processors = self.workbench.processors
        self.wires = self.workbench.wires
        self.systems = self.workbench.systems

        self.processors_map = self.workbench.processors_map
        self.wires_map = self.workbench.wires_map
        self.systems_map = self.workbench.systems_map

        self._validate_unique_ids()

        # Build out composite processors
        for processor in self.processors:
            processor._load_subsytem(self.systems_map, self.processors_map)

    def _validate_unique_ids(self):
        duplicates = find_duplicates(
            self.blocks + self.spaces + self.processors + self.wires + self.systems
        )
        assert (
            len(duplicates) == 0
        ), f"Overlapping IDs between the toolbox and workbench found: {duplicates}"

    def __repr__(self):
        return """< Project
Toolbox:

{}

Workbench:

{} >""".format(
            self.toolbox, self.workbench
        )

    def add_to_spec(
        self, spaces=None, blocks=None, processors=None, wires=None, systems=None
    ):
        new = deepcopy(self.raw_data)
        if spaces is not None:
            new["Toolbox"]["Spaces"].extend(spaces)
        if blocks is not None:
            new["Toolbox"]["Blocks"].extend(blocks)
        if processors is not None:
            new["Workbench"]["Processors"].extend(processors)
        if wires is not None:
            new["Workbench"]["Wires"].extend(wires)
        if systems is not None:
            new["Workbench"]["Systems"].extend(systems)

        new = Project(new)
        self.__dict__.clear()  # Clears the existing instance's attributes
        self.__dict__.update(new.__dict__)  # Copies attributes from the new instance

    def add_space(self, id, name=None, description=None):
        new = {
            "ID": id,
            "Name": name,
            "Description": description,
        }
        if name is None:
            new["Name"] = id
        self.add_to_spec(spaces=[new])

    def add_block(self, id, name=None, description=None, codomain=None, domain=None):
        new = {
            "ID": id,
            "Name": name,
            "Description": description,
            "Codomain": codomain,
            "Domain": domain,
        }
        if name is None:
            new["Name"] = id
        if codomain is None:
            new["Codomain"] = []
        if domain is None:
            new["Domain"] = []
        self.add_to_spec(blocks=[new])

    def add_processor(
        self,
        id,
        parent_id,
        name=None,
        description=None,
        subsystem=None,
        ports=None,
        terminals=None,
    ):
        new = {
            "ID": id,
            "Parent": parent_id,
            "Name": name,
            "Description": description,
            "Subsystem": subsystem,
            "Ports": ports,
            "Terminals": terminals,
        }
        assert parent_id in self.blocks_map, f"Parent Block ID {parent_id} not found"
        if name is None:
            new["Name"] = id
        if ports is None:
            new["Ports"] = [x.id for x in self.blocks_map[parent_id].domain]
        if terminals is None:
            new["Terminals"] = [x.id for x in self.blocks_map[parent_id].codomain]
        self.add_to_spec(processors=[new])

    def add_wire(self, id, parent, source, target):
        new = {
            "ID": id,
            "Parent": parent,
            "Source": source,
            "Target": target,
        }
        self.add_to_spec(wires=[new])

    def add_system(
        self,
        id,
        name=None,
        processors=None,
        wires=None,
        description=None,
        subsystem=None,
    ):
        new = {
            "ID": id,
            "Name": name,
            "Processors": processors,
            "Wires": wires,
            "Description": description,
            "Subsystem": subsystem,
        }
        if name is None:
            new["Name"] = id
        if processors is None:
            new["Processors"] = []
        if wires is None:
            new["Wires"] = []
        self.add_to_spec(systems=[new])

    def copy_add_wire(self, wire, update_dict):
        new = deepcopy(wire.raw_data)
        assert "ID" in update_dict, "New ID is required to update wire"
        new["ID"] = update_dict["ID"]
        if "Parent" in update_dict:
            new["Parent"] = update_dict["Parent"]
        if "Source" in update_dict:
            new["Source"] = update_dict["Source"]
        if "Target" in update_dict:
            new["Target"] = update_dict["Target"]
        self.add_to_spec(wires=[new])

    def add_wires(self, wires, auto_increment=False):
        if auto_increment:
            mx = 0
            for wire in self.wires:
                w_id = wire.id
                if w_id.startswith("W"):
                    try:
                        mx = max(mx, int(w_id[1:]))
                    except ValueError:
                        pass
            mx += 1
            for wire in wires:
                wire["ID"] = "W" + str(mx)
                mx += 1
        self.add_to_spec(wires=wires)

    def update_spec(self, processors=None):
        new = deepcopy(self.raw_data)
        if processors is not None:
            for p in processors:
                record = [x for x in new["Workbench"]["Processors"] if x["ID"] == p][0]
                d = processors[p]
                for key in d:
                    record[key] = d[key]

        new = Project(new)
        self.__dict__.clear()  # Clears the existing instance's attributes
        self.__dict__.update(new.__dict__)  # Copies attributes from the new instance

    def attach_subsystem(self, processor, system, port_mappings, terminal_mappings):
        assert (
            processor.is_primitive()
        ), f"Processor {processor.id} is not a primitive processor"

        self.update_spec(
            processors={
                processor.id: {
                    "Subsystem": {
                        "System ID": system.id,
                        "Port Mappings": port_mappings,
                        "Terminal Mappings": terminal_mappings,
                    }
                }
            }
        )

    def save(self, path):
        """
        Save the project to a JSON file.
        """

        with open(path, "w") as f:
            json.dump(self.raw_data, f, indent=4)


def load_project(json: dict):
    validate(json, schema)
    return Project(json)
