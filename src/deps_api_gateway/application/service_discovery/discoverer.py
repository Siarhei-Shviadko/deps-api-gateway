import os
import re

__all__ = ["ServiceDiscoverer"]


class ServiceDiscoverer:
    PATTERN = r"^(\S*?)_SERVICE_HOST$"

    def find_services(self) -> set[str]:
        env_variable_names = os.environ.keys()
        services = set()

        for env_variable_name in env_variable_names:
            if match := re.match(self.PATTERN, env_variable_name):
                services.add(match.group(1).lower().replace("_", "-"))

        return services
