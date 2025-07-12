import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT

class PluggitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config-Flow für Pluggit Avent P310 über Modbus."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """
        Erster Schritt im UI: Holt Host und Port vom Nutzer ab.
        """
        errors = {}

        if user_input is not None:
            # Eingaben validieren (z.B. Erreichbarkeit könnte man hier später prüfen)
            return self.async_create_entry(
                title=f"{user_input[CONF_HOST]}:{user_input[CONF_PORT]}",
                data=user_input
            )

        # Formular anzeigen
        data_schema = vol.Schema({
            vol.Required(CONF_HOST, description="IP-Adresse der Pluggit Avent P310"): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT, description="Modbus-Port, meist 502"): int,
        })
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )
