"""Support for Strava sensor."""

from homeassistant.components.sensor import (
    ENTITY_ID_FORMAT,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, GEAR_SENSOR_ENTITIES, SUMMARY_ENTITIES, WEEKLY_ENTITIES


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Strava sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            StravaSummarySensor(coordinator, description)
            for description in SUMMARY_ENTITIES
        ],
        False,
    )

    for ha_id, gear in coordinator.data["gear_ids"].items():
        async_add_entities(
            [
                StravaGearSensor(
                    coordinator,
                    gear["name"],
                    ha_id,
                    async_generate_entity_id(
                        ENTITY_ID_FORMAT, f"{ha_id}_{description.key}", hass=hass
                    ),
                    description,
                )
                for description in GEAR_SENSOR_ENTITIES
            ],
            False,
        )

    async_add_entities(
        [
            StravaWeeklySensor(coordinator, "This Week", "this_week", description)
            for description in WEEKLY_ENTITIES
        ],
        False,
    )

    async_add_entities(
        [
            StravaWeeklySensor(coordinator, "Last Week", "last_week", description)
            for description in WEEKLY_ENTITIES
        ],
        False,
    )


class StravaSummarySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Strava sensor."""

    def __init__(
        self, coordinator: DataUpdateCoordinator, description: SensorEntityDescription
    ) -> None:
        """Initialize the Strava sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"{description.name}"
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = self.coordinator.get_device()

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return (
            self.coordinator.data["summary_stats"][self.entity_description.key]
            if self.coordinator.data
            else None
        )


class StravaWeeklySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Strava sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        name: str,
        device_id: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Strava sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self.object_name = device_id
        self._attr_name = f"{name} {description.name}"
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_device_info = self.coordinator.get_device()

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return (
            getattr(
                self.coordinator.data["weekly_stats"][self.object_name],
                self.entity_description.key,
            )
            if self.coordinator.data
            else None
        )


class StravaGearSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Strava gear sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        name: str,
        device_id: str,
        entity_id: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Strava sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self.entity_id = entity_id
        self.object_name = f"{device_id}_{description.key}"
        self._attr_name = f"{name} {description.name}"
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_device_info = self.coordinator.get_device(device_id)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        key = "time"
        if self.device_class == SensorDeviceClass.DISTANCE:
            key = "distance"

        return (
            self.coordinator.data["gear_stats"][self.object_name][key]
            if self.coordinator.data
            else None
        )

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return attributes if more than one defined."""
        attributes: dict = self.coordinator.data["gear_stats"][self.object_name].copy()
        if "distance" in attributes:
            attributes["distance"] = f"{attributes["distance"]} km"
        if "time" in attributes:
            attributes["time"] = f"{attributes["time"]} h"

        if len(attributes) > 1:
            return attributes

        return None
