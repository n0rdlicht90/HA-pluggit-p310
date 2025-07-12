import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT

class PluggitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config-Flow für Pluggit Avent P310 über Modbus."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Hier könnten wir später schon die Erreichbarkeit prüfen
            return self.async_create_entry(
                title=f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}",
                data=user_input
            )

        data_schema = vol.Schema({
            vol.Required(CONF_HOST): cv.string,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
        })
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )