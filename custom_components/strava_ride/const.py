"""Constants for the Strava integration."""
from datetime import timedelta

from homeassistant.components.sensor import SensorDeviceClass, SensorEntityDescription
from homeassistant.const import (
    LENGTH_KILOMETERS,
    PERCENTAGE,
    TIME_HOURS,
    LENGTH_METERS,
)

DOMAIN = "strava_ride"

SCAN_INTERVAL = timedelta(minutes=10)

# OAuth Specs
OAUTH2_AUTHORIZE = "https://www.strava.com/oauth/authorize"
OAUTH2_TOKEN = "https://www.strava.com/oauth/token"

MAX_NB_ACTIVITIES = 200

WEEKLY_ENTITIES: tuple[SensorEntityDescription] = (
    SensorEntityDescription(
        key="distance",
        name="Distance",
        native_unit_of_measurement=LENGTH_KILOMETERS,
        icon="mdi:ruler",
    ),
    SensorEntityDescription(
        key="distance_delta",
        name="Distance Delta",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:ruler-square-compass",
    ),
    SensorEntityDescription(
        key="time",
        name="Moving Time",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:timer",
    ),
    SensorEntityDescription(
        key="time_delta",
        name="Moving Time Delta",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:clock-start",
    ),
    SensorEntityDescription(
        key="elevation",
        name="Elevation Gain",
        native_unit_of_measurement=LENGTH_METERS,
        icon="mdi:elevation-rise",
    ),
    SensorEntityDescription(
        key="climbing",
        name="Climbing",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:slope-uphill",
    ),
)

SUMMARY_ENTITIES: tuple[SensorEntityDescription] = (
    SensorEntityDescription(
        key="all_ride_totals_count", name="Ride All Time Count", icon="mdi:numeric"
    ),
    SensorEntityDescription(
        key="all_ride_totals_distance",
        name="Ride All Time Distance",
        native_unit_of_measurement=LENGTH_KILOMETERS,
        icon="mdi:ruler",
    ),
    SensorEntityDescription(
        key="all_ride_totals_elapsed_time",
        name="Ride All-Time Elapsed Time",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:timer",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="all_ride_totals_elevation_gain",
        name="Ride All-Time Elevation Gain",
        native_unit_of_measurement=LENGTH_METERS,
        icon="mdi:elevation-rise",
    ),
    SensorEntityDescription(
        key="all_ride_totals_moving_time",
        name="Ride All-Time Moving Time",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:timer",
    ),
    SensorEntityDescription(
        key="biggest_climb_elevation_gain",
        name="Ride Biggest Elevation Gain",
        native_unit_of_measurement=LENGTH_METERS,
        icon="mdi:elevation-rise",
    ),
    SensorEntityDescription(
        key="biggest_ride_distance",
        name="Ride Biggest Distance",
        native_unit_of_measurement=LENGTH_KILOMETERS,
        icon="mdi:ruler",
    ),
    SensorEntityDescription(
        key="ytd_ride_totals_count", name="Ride YTD Count", icon="mdi:numeric"
    ),
    SensorEntityDescription(
        key="ytd_ride_totals_distance",
        name="Ride YTD Distance",
        native_unit_of_measurement=LENGTH_KILOMETERS,
        icon="mdi:ruler",
    ),
    SensorEntityDescription(
        key="ytd_ride_totals_elapsed_time",
        name="Ride YTD Elapsed Time",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:timer",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="ytd_ride_totals_elevation_gain",
        name="Ride YTD Elevation Gain",
        native_unit_of_measurement=LENGTH_METERS,
    ),
    SensorEntityDescription(
        key="ytd_ride_totals_moving_time",
        name="Ride YTD Moving Time",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:timer",
    ),
    SensorEntityDescription(
        key="recent_ride_totals_count",
        name="Ride Last 4 Weeks Count",
        icon="mdi:numeric",
    ),
    SensorEntityDescription(
        key="recent_ride_totals_distance",
        name="Ride Last 4 Weeks Distance",
        native_unit_of_measurement=LENGTH_KILOMETERS,
        icon="mdi:ruler",
    ),
    SensorEntityDescription(
        key="recent_ride_totals_elapsed_time",
        name="Ride Last 4 Weeks Elapsed Time",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:timer",
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="recent_ride_totals_elevation_gain",
        name="Ride Last 4 Weeks Elevation Gain",
        native_unit_of_measurement=LENGTH_METERS,
        icon="mdi:elevation-rise",
    ),
    SensorEntityDescription(
        key="recent_ride_totals_moving_time",
        name="Ride Last 4 Weeks Moving Time",
        native_unit_of_measurement=TIME_HOURS,
        icon="mdi:timer",
    ),
)
