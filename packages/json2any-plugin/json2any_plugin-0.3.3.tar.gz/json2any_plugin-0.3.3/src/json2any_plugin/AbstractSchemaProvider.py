from abc import abstractmethod
from typing import Dict, Optional, Type

from json2any_plugin.AbstractProvider import AbstractProvider


class AbstractSchemaProvider(AbstractProvider):
    """
    JSON Schema provider
    By implementing this interface you can provide JSON schema for data validation in json2any
    """

    @abstractmethod
    def get_schema(self, schema_id: str) -> Optional[Dict[str, Dict]]:
        """
        returns schema as a dictionary or None if schema id is not available
        """
        raise NotImplementedError()

    @abstractmethod
    def get_schema_class(self, schema_id: str) -> Optional[Type]:
        """
        returns schema root class
        """
        raise NotImplementedError()

    @abstractmethod
    def get_schema_metadata(self, schema_id: str) -> Optional[Dict[str, str]]:
        """
        returns schema metadata like $id, title, description, ...
        """
        raise NotImplementedError()

    @abstractmethod
    def get_available_schemas(self) -> Dict[str, str]:
        """
        returns available schemas as a dictionary mapping of 'schema_id' to 'title' string
        schema_id is the $id property of schema
        """
        raise NotImplementedError()
