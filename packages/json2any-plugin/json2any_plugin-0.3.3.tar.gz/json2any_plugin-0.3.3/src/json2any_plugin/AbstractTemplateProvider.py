from abc import abstractmethod
from typing import Optional

from jinja2 import BaseLoader

from json2any_plugin.AbstractProvider import AbstractProvider


class AbstractTemplateProvider(AbstractProvider):
    """
    Provides jinja2 template loader.
    """

    def init(self, template_location: str) -> None:
        """
        Initialise the loader with overall template location
        :param template_location:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def get_loader(self, templates_path: Optional[str]) -> BaseLoader:
        """
        Returns Template loader
        :param templates_path: template_location passed in init() along with optional templates_path
        provide hints where to find templates. The format of those is specific to the implementation.
        :return: BaseLoader: instance of jinja2.BaseLoader
        """
        raise NotImplementedError()
