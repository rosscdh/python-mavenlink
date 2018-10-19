import os
import shutil

from glob import glob


class PathNotExistsException(Exception): pass
class ConfigExistsException(Exception): pass


class MavenlinkService:
    conf = None
    default_settings = """
auth:
    username: {username}
    password: {password}
    token: null
defaults:
    # NWOT
    workspace_id: 17277765
    role_id: ftux_participant
    story_id: 348530265
    """
    def __init__(self, conf):
        self.conf = conf

    def initialize_project(self, path: str, **kwargs: dict):
        """
        Create a new .mavenlink.yml at a specific path
        """
        output_dir = path
        filename = os.path.join(output_dir, '.mavenlink.yml')

        # if os.path.exists(output_dir):
        #     raise PathNotExistsException(output_dir)

        if os.path.exists(filename):
            raise ConfigExistsException(output_dir)

        template_config = self.default_settings.format(**kwargs)

        with open(filename, 'w') as f:
            f.write(template_config)

        return template_config

    def login(self, username: str, password: str):
        return {}

    def consume(self, input: str):
        return {}

    def preview(self):
        return {}

    def send(self):
        return {}