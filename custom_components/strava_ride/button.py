"""Support for Strava buttons."""

from datetime import datetime
import logging

from homeassistant.components.button import (
    ENTITY_ID_FORMAT,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util

from .const import DOMAIN, GEAR_RESET_ENTITIES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Strava button platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    for ha_id, gear in coordinator.data["gear_ids"].items():
        async_add_entities(
            [
                GearServiceResetCommand(
                    coordinator,
                    gear["name"],
                    ha_id,
                    async_generate_entity_id(
                        ENTITY_ID_FORMAT, f"{ha_id}_{description.key}_reset", hass=hass
                    ),
                    gear["strava_id"],
                    description,
                )
                for description in GEAR_RESET_ENTITIES
            ],
            False,
        )


class GearServiceResetCommand(CoordinatorEntity, ButtonEntity):
    """Strava Gear Service Reset Command."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        name: str,
        device_id: str,
        entity_id: str,
        strava_id: str,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize the Strava sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self.entity_id = entity_id
        self.object_name = f"{device_id}_{description.key}_reset"
        self._attr_name = f"{name} {description.name}"
        self._attr_unique_id = f"{device_id}_{description.key}_reset"
        self._attr_device_info = self.coordinator.get_device(device_id)

        # Get last character as index in gear service list
        self.gear_service_index = int(description.key[-1])
        self.gear_strava_id = strava_id

    async def async_press(self):
        """Handle the button press."""
        await self.coordinator.set_gear_service_date(
            self.gear_strava_id,
            self.gear_service_index,
            datetime.now(tz=dt_util.get_default_time_zone()),
        )
