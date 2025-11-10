"""Home Assistant integration for the DingTalk gateway service."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .client import DingTalkGatewayClient
from .const import (
    CONF_ACCESS_TOKEN,
    CONF_BASE_URL,
    DATA_CLIENT,
    DOMAIN,
    PLATFORMS,
    SERVICE_SEND_MARKDOWN,
    SERVICE_SEND_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)

# Service schemas
SEND_MESSAGE_SCHEMA = vol.Schema(
    {
        vol.Required("target"): cv.string,
        vol.Required("message"): cv.string,
        vol.Optional("at_list"): vol.All(cv.ensure_list, [cv.string]),
    }
)

SEND_MARKDOWN_SCHEMA = vol.Schema(
    {
        vol.Required("target"): cv.string,
        vol.Optional("title", default="通知"): cv.string,
        vol.Required("content"): cv.string,
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the DingTalk Gateway integration from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    base_url: str = entry.data[CONF_BASE_URL]
    token: str | None = entry.data.get(CONF_ACCESS_TOKEN)

    client = DingTalkGatewayClient(hass, base_url, token)
    await client.async_start()

    hass.data[DOMAIN][entry.entry_id] = {DATA_CLIENT: client, "remove_listener": None}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    async def handle_send_message(call: ServiceCall) -> None:
        """Handle the send_message service call."""
        target = call.data["target"]
        message = call.data["message"]
        at_list = call.data.get("at_list")
        
        try:
            await client.async_send_text(target, message, at_list)
        except Exception as err:
            _LOGGER.error("Error sending message: %s", err)
            raise

    async def handle_send_markdown(call: ServiceCall) -> None:
        """Handle the send_markdown service call."""
        target = call.data["target"]
        title = call.data.get("title", "通知")
        content = call.data["content"]
        
        try:
            await client.async_send_markdown(target, title, content)
        except Exception as err:
            _LOGGER.error("Error sending markdown: %s", err)
            raise

    hass.services.async_register(
        DOMAIN, SERVICE_SEND_MESSAGE, handle_send_message, schema=SEND_MESSAGE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SEND_MARKDOWN, handle_send_markdown, schema=SEND_MARKDOWN_SCHEMA
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    data = hass.data[DOMAIN].pop(entry.entry_id, None)

    if data:
        remove_listener = data.get("remove_listener")
        if remove_listener:
            await remove_listener()
            data["remove_listener"] = None
        client: DingTalkGatewayClient = data[DATA_CLIENT]
        await client.async_stop()

    # Unregister services if this was the last entry
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)
        hass.services.async_remove(DOMAIN, SERVICE_SEND_MESSAGE)
        hass.services.async_remove(DOMAIN, SERVICE_SEND_MARKDOWN)

    return unload_ok
