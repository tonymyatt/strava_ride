"""The Strava integration."""

from __future__ import annotations

from datetime import datetime
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow, config_validation as cv
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import config_flow
from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN, SCAN_INTERVAL
from .strava_api import StravaAPI

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

PLATFORMS: list[Platform] = [Platform.BUTTON, Platform.DATETIME, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Strava from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # OAuth Stuff
    try:
        implementation = (
            await config_entry_oauth2_flow.async_get_config_entry_implementation(
                hass, entry
            )
        )
    except ValueError:
        implementation = config_entry_oauth2_flow.LocalOAuth2Implementation(
            hass,
            DOMAIN,
            entry.data[CONF_CLIENT_ID],
            entry.data[CONF_CLIENT_SECRET],
            OAUTH2_AUTHORIZE,
            OAUTH2_TOKEN,
        )

        config_flow.OAuth2FlowHandler.async_register_implementation(
            hass, implementation
        )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)

    await session.async_ensure_token_valid()

    coordinator = StravaCoordinator(hass, session)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class StravaCoordinator(DataUpdateCoordinator):
    """Class to manage strava data fetching and gear management."""

    _gear_service_dates_restored = False
    _devices: dict[str, DeviceInfo]

    def __init__(
        self,
        hass: HomeAssistant,
        session: config_entry_oauth2_flow.AbstractOAuth2FlowHandler,
    ) -> None:
        """Initialize strava coorindator with oauth session."""

        super().__init__(
            hass,
            _LOGGER,
            name="Strava Ride",
            update_interval=SCAN_INTERVAL,
        )

        self._strava_api = StravaAPI(session)
        self._devices = {}
        self._devices["None"] = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, session.config_entry.data[CONF_CLIENT_ID])},
            manufacturer="Strava",
            model="Ride Statistics",
            name=self.name,
        )

    def get_device(self, gear_id: str = "None"):
        """Get the device for the given gear_id, if not found or none, return statistics device."""
        if gear_id in self._devices:
            return self._devices[gear_id]
        return self._devices["None"]

    def update_gear_devices(self, data: dict[str, list[str]]):
        """Make sure all the given gear id/names have devices loaded."""
        for k, v in data.items():
            if k in self._devices:
                continue
            self._devices[k] = DeviceInfo(
                entry_type=DeviceEntryType.SERVICE,
                identifiers={(DOMAIN, k)},
                manufacturer="Strava Gear",
                model=f"Bike: {v["name"]}",
                name=v["name"],
            )

    async def _async_update_data(self):
        data = await self._strava_api.fetch_strava_data()

        # Whenever we do an update, make sure all gear devices have been created,
        # this will be called once before entities are loaded, so entities
        # will get a device for each gear (bike)
        self.update_gear_devices(data["gear_ids"])
        return data

    async def set_gear_service_date(
        self, strava_id: str, service_index: int, value: datetime
    ):
        """Reset the gear service counters for the given strava_id and service attribute."""
        await self._strava_api.set_gear_service_date(strava_id, service_index, value)

        # Recalcualte and reload gear_stats into the data object for entities
        gear_data = self._strava_api.create_gear_data()
        self.data["gear_stats"] = gear_data["stats"]

        # Trigger a refesh of all entities as listeners of this coorindator
        self.async_update_listeners()
