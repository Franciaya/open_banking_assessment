from injector import Binder, inject, Module
from configparser import ConfigParser

class DependencyModule(Module):
    def configure(self,binder: Binder) -> None:
        binder.bind(ConfigParser)