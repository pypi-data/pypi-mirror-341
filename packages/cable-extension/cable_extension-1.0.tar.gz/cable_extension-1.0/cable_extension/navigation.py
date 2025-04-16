"""
This file defines links in the plugin section for easy access to the plugin functions.
"""
from netbox.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link='plugins:cable_extension:cable_create',
        link_text='Cable create',
    ),
)
