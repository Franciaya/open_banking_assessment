from injector import Binder, Injector, inject, Module
from configparser import ConfigParser

class DependencyModule(Module):
    def configure(self,binder: Binder) -> None:
        binder.bind(ConfigParser,to= ConfigParser())