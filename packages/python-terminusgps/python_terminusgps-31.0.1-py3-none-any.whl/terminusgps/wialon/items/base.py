from abc import abstractmethod
from typing import Type

from terminusgps.wialon import flags
from terminusgps.wialon.session import WialonSession


class WialonBase:
    def __init__(
        self, id: str | int | None, session: WialonSession, *args, **kwargs
    ) -> None:
        if isinstance(id, str) and not id.isdigit():
            raise ValueError(f"'id' must be a digit. Got '{id}'.")

        self._session = session
        self._id = str(id if id else self.create(*args, **kwargs))
        self._name = None
        self._hw_type = None
        self._access_lvl = None

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id}, session={self.session.id})"

    def populate(self) -> None:
        """Retrieves and saves the latest data for the item from Wialon."""
        response = self.session.wialon_api.core_search_item(
            **{"id": str(self.id), "flags": flags.DataFlag.UNIT_BASE}
        )
        if response is not None:
            item = response.get("item", {})
            self._name = item.get("nm")
            self._hw_type = item.get("cls")
            self._access_lvl = item.get("uacl")

    @property
    def name(self) -> str:
        """Name of the Wialon object."""
        if self._name is None:
            self.populate()
        return str(self._name)

    @property
    def hw_type(self) -> str:
        """Hardware type of the Wialon object."""
        if self._hw_type is None:
            self.populate()
        return str(self._hw_type)

    @property
    def access_lvl(self) -> str:
        """Access level of the Wialon object."""
        if self._access_lvl is None:
            self.populate()
        return str(self._access_lvl)

    @property
    def session(self) -> WialonSession:
        """
        A valid Wialon API session.

        :type: :py:obj:`~terminusgps.wialon.session.WialonSession`

        """

        return self._session

    @property
    def id(self) -> int | None:
        """
        A unique Wialon ID.

        :type: :py:obj:`int` | :py:obj:`None`

        """

        return int(self._id) if self._id else None

    def has_access(self, other: Type["WialonBase"]) -> bool:
        """
        Checks if this Wialon object has access to ``other``.

        :type: :py:obj:`bool`

        """
        response = self.session.wialon_api.core_check_accessors(
            **{"items": [other.id], "flags": False}
        )
        return True if self.id in response.keys() else False

    @abstractmethod
    def create(self, *args, **kwargs) -> int | None:
        """Creates a Wialon object and returns its id."""
        raise NotImplementedError("Subclasses must implement this method.")

    def rename(self, new_name: str) -> None:
        """
        Renames the Wialon object to the new name.

        :param new_name: A new name.
        :type new_name: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.item_update_name(
            **{"itemId": self.id, "name": new_name}
        )
        self._name = new_name

    def add_afield(self, key: str, value: str) -> None:
        """
        Adds an admin field to the Wialon object.

        :param key: A key (name) for the admin field.
        :type key: :py:obj:`str`
        :param value: A value for the admin field.
        :type value: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.item_update_admin_field(
            **{"itemId": self.id, "id": 0, "callMode": "create", "n": key, "v": value}
        )

    def update_afield(self, id: int, key: str, value: str) -> None:
        """
        Updates an admin field by id.

        :param id: The admin field id.
        :type id: :py:obj:`int`
        :param key: A key (name) for the admin field.
        :type key: :py:obj:`str`
        :param value: A value for the admin field.
        :type value: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.item_update_admin_field(
            **{"itemId": self.id, "id": id, "callMode": "update", "n": key, "v": value}
        )

    def add_cfield(self, key: str, value: str) -> None:
        """
        Adds a custom field to the Wialon object.

        :param key: A key (name) for the custom field.
        :type key: :py:obj:`str`
        :param value: A value for the custom field.
        :type value: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.item_update_custom_field(
            **{"itemId": self.id, "id": 0, "callMode": "create", "n": key, "v": value}
        )

    def update_cfield(self, id: int, key: str, value: str) -> None:
        """
        Updates a custom field by id.

        :param id: The admin field id.
        :type id: :py:obj:`int`
        :param field: A key (name) for the custom field.
        :type field: :py:obj:`str`
        :param field: A value for the custom field.
        :type field: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.item_update_custom_field(
            **{"itemId": self.id, "id": id, "callMode": "update", "n": key, "v": value}
        )

    def add_cproperty(self, key: str, value: str) -> None:
        """
        Adds a custom property to the Wialon object.

        :param key: A key (name) for the custom property.
        :type key: :py:obj:`str`
        :param value: A value for the custom property.
        :type value: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.item_update_custom_property(
            **{"itemId": self.id, "name": key, "value": value}
        )

    def add_profile_field(self, key: str, value: str) -> None:
        """
        Adds a profile field to the Wialon object.

        :param key: A key (name) for the profile field.
        :type key: :py:obj:`str`
        :param value: A value for the profile field.
        :type value: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.item_update_profile_field(
            **{"itemId": self.id, "n": key, "v": value}
        )

    def delete(self) -> None:
        """
        Deletes the Wialon object.

        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.item_delete_item(**{"itemId": self.id})

    @property
    def cfields(self) -> dict[str, str]:
        """Custom fields for the Wialon object."""
        response = self.session.wialon_api.core_search_item(
            **{"id": self.id, "flags": flags.DataFlag.UNIT_CUSTOM_FIELDS}
        )
        fields = response.get("item", {}).get("flds") if response is not None else {}
        return {field["n"]: field["v"] for field in fields.values()} if fields else {}

    @property
    def afields(self) -> dict[str, str]:
        """Admin fields for the Wialon object."""
        response = self.session.wialon_api.core_search_item(
            **{"id": self.id, "flags": flags.DataFlag.UNIT_ADMIN_FIELDS}
        )
        fields = response.get("item", {}).get("aflds") if response is not None else {}
        return {field["n"]: field["v"] for field in fields.values()} if fields else {}
