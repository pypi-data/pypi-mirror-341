# -*- encoding: utf-8 -*-
import time

from .taskflux import *

from .abcglobal import *
from .management import Management


class AiMaestro:

    def __init__(self, config_file: str):
        GlobalVar(config_file=config_file)

        initialization_taskflux(config=GlobalVar().taskflux_config)

    @staticmethod
    def registry_services(services: list):
        from aimaestro.workflows.web_automation import web_automation
        _services = [web_automation]
        for service in services:
            _services.append(service)

        services_registry(services=_services)

    @staticmethod
    def start_management():
        Management(config=GlobalVar().taskflux_config).run()

    def start_services(self):
        services_start()
        time.sleep(10)
        self.start_management()
