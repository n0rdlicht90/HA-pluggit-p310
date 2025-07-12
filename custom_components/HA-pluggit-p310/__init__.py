import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_HOST, CONF_PORT
from .modbus import PluggitModbus

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """
    Wird beim Start von Home Assistant aufgerufen.
    Stellt sicher, dass der Domain-Key existiert.
    """
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """
    Wird aufgerufen, wenn der User die Integration über die UI bestätigt hat.
    Hier bauen wir die Modbus-Verbindung auf und laden die Sensor-Plattform.
    """
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    _LOGGER.debug("Setup Pluggit P310 auf %s:%s", host, port)

    # Modbus-Client initialisieren und verbinden
    client = PluggitModbus(host, port)
    await client.connect()

    # Client-Instanz merken
    hass.data[DOMAIN][entry.entry_id] = client

    # Sensor-Plattform laden
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """
    Säubert die Integration, wenn sie in Home Assistant wieder entfernt wird.
    """
    # Sensor-Plattform entladen
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        # Modbus-Verbindung schließen
        client = hass.data[DOMAIN].pop(entry.entry_id)
        await client.close()
    return unload_ok
