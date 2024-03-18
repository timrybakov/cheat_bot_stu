from functools import cached_property

from cheat_bot import config
from .repository_container import RepositoryContainer


class Container:
    @cached_property
    def settings(self) -> config.Settings:
        return config.Settings()

    @cached_property
    def repository_container(self) -> RepositoryContainer:
        return RepositoryContainer(self.settings)
