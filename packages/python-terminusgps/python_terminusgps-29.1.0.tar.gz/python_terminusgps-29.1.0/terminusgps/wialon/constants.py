import enum

from . import flags


class WialonItemsType(enum.StrEnum):
    HARDWARE = "avl_hw"
    RESOURCE = "avl_resource"
    RETRANSLATOR = "avl_retranslator"
    ROUTE = "avl_route"
    UNIT = "avl_unit"
    UNIT_GROUP = "avl_unit_group"
    USER = "user"


ACCESSMASK_RESOURCE_BASIC: int = (
    flags.AccessFlag.VIEW_ITEM_BASIC
    | flags.AccessFlag.VIEW_CUSTOM_FIELDS
    | flags.AccessFlag.MANAGE_CUSTOM_FIELDS
    | flags.AccessFlag.VIEW_ADMIN_FIELDS
    | flags.AccessFlag.RESOURCE_VIEW_NOTIFICATIONS
    | flags.AccessFlag.RESOURCE_MANAGE_NOTIFICATIONS
    | flags.AccessFlag.RESOURCE_VIEW_POIS
    | flags.AccessFlag.RESOURCE_VIEW_GEOFENCES
    | flags.AccessFlag.RESOURCE_MANAGE_GEOFENCES
    | flags.AccessFlag.RESOURCE_VIEW_DRIVERS
    | flags.AccessFlag.RESOURCE_MANAGE_DRIVERS
    | flags.AccessFlag.RESOURCE_VIEW_ORDERS
    | flags.AccessFlag.RESOURCE_VIEW_TRAILERS
)
"""Basic resource permissions"""

ACCESSMASK_UNIT_BASIC: int = (
    flags.AccessFlag.VIEW_ITEM_BASIC
    | flags.AccessFlag.VIEW_ITEM_DETAILED
    | flags.AccessFlag.RENAME_ITEM
    | flags.AccessFlag.VIEW_CUSTOM_FIELDS
    | flags.AccessFlag.MANAGE_CUSTOM_FIELDS
    | flags.AccessFlag.MANAGE_ICON
    | flags.AccessFlag.QUERY_REPORTS
    | flags.AccessFlag.VIEW_ATTACHED_FILES
    | flags.AccessFlag.UNIT_EXECUTE_COMMANDS
    | flags.AccessFlag.UNIT_VIEW_SERVICE_INTERVALS
    | flags.AccessFlag.UNIT_REGISTER_EVENTS
    | flags.AccessFlag.UNIT_IMPORT_MESSAGES
    | flags.AccessFlag.UNIT_EXPORT_MESSAGES
)
"""Basic unit permissions"""

ACCESSMASK_UNIT_MIGRATION: int = (
    flags.AccessFlag.DELETE_ITEM
    | flags.AccessFlag.MANAGE_ITEM_ACCESS
    | flags.AccessFlag.UNIT_DELETE_MESSAGES
    | flags.AccessFlag.UNIT_MANAGE_CONNECTIVITY
    | flags.AccessFlag.VIEW_ITEM_BASIC
)
"""Unit migration permissions"""
