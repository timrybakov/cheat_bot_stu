from functools import cached_property


from cheat_bot.di.repository_container import RepositoryContainer
from cheat_bot.config.config import DBSettings
from cheat_bot.utils.singleton_meta import SingletonMeta


class Container(metaclass=SingletonMeta):
    @cached_property
    def settings(self):
        return DBSettings()

    @cached_property
    def repository_container(self):
        return RepositoryContainer(self.settings)
