"""Constants for the DingTalk Gateway integration."""

DOMAIN = "dingtalk_gateway"

# Configuration
CONF_BASE_URL = "base_url"
CONF_ACCESS_TOKEN = "access_token"

# Data keys
DATA_CLIENT = "client"

# Platforms
PLATFORMS = ["sensor"]

# Services
SERVICE_SEND_MESSAGE = "send_message"
SERVICE_SEND_MARKDOWN = "send_markdown"

# Events and signals
EVENT_MESSAGE = "dingtalk_gateway_message"
SIGNAL_NEW_MESSAGE = f"{DOMAIN}_new_message"
