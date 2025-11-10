"""Config flow for DingTalk Gateway integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import CONF_ACCESS_TOKEN, CONF_BASE_URL, DOMAIN


class DingTalkGatewayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DingTalk Gateway."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="DingTalk Gateway",
                data=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_BASE_URL, default="http://localhost:8099"): cv.string,
                vol.Optional(CONF_ACCESS_TOKEN): cv.string,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
