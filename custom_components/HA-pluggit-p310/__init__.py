import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_HOST, CONF_PORT
from .modbus import PluggitModbus

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    _LOGGER.debug("Setting up Pluggit P310 at %s:%s", host, port)

    client = PluggitModbus(host, port)
    await client.connect()
    hass.data[DOMAIN][entry.entry_id] = client

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        client = hass.data[DOMAIN].pop(entry.entry_id)
        await client.close()
    return unload_ok
