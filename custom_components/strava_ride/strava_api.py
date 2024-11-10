"""Read data from Strava API for cycling."""

from __future__ import annotations

from datetime import date, datetime, timedelta
import json
import logging

from dateutil.parser import parse as dt_parse

from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.util import dt as dt_util

from .const import MAX_GEAR_SERVICE_ITEMS, MAX_NB_ACTIVITIES

_LOGGER = logging.getLogger(__name__)


class CycleGearService:
    """Represents a serviceable item on a bike."""

    distance: int = 0
    time: int = 0
    service_date: datetime = datetime.now(tz=dt_util.get_default_time_zone())

    def clear_counters(self):
        """Clear all service counters."""
        self.distance = 0
        self.time = 0

    def process_activity(self, act_date: datetime, act_dist: int, act_time: int):
        """Add an activities distance time to this service, dependant on date."""
        if act_date >= self.service_date:
            self.distance += act_dist
            self.time += act_time

    def __repr__(self) -> str:
        """Create string representation."""
        return f"CycleGearService time:{self.time}; distance:{self.distance}; service_date:{self.service_date}"


class CycleGear:
    """Represents a bike (Strava Gear item)."""

    name: str = "Unknown Name"
    ha_id: str = None
    distance: int = 0
    service = [CycleGearService]

    def __init__(self) -> None:
        """Create a cycle gear object."""
        self.service = []
        for idx in range(MAX_GEAR_SERVICE_ITEMS):
            self.service.insert(idx, CycleGearService())

    def clear_counters(self):
        """Clear all service counters."""
        for idx in range(MAX_GEAR_SERVICE_ITEMS):
            self.service[idx].clear_counters()

    def process_activity(self, act_date: datetime, act_dist: int, act_time: int):
        """Add an activities distance time to service items, dependant on date."""
        for idx in range(MAX_GEAR_SERVICE_ITEMS):
            self.service[idx].process_activity(act_date, act_dist, act_time)

    def __repr__(self) -> str:
        """Create string representation."""
        return f"CycleGear {self.name} {self.service}"


class CycleWeekStats:
    """Weekly summary cycling stats."""

    distance = 0
    distance_delta = 0
    time = 0
    time_delta = 0
    elevation = 0

    @property
    def climbing(self) -> float:
        """Return climbing in percentage (elevation on distance)."""
        climb = 0
        if self.distance > 0:
            climb = round(self.elevation / self.distance / 10, 1)
        return climb


class StravaAPI:
    """API to read data from Strava API."""

    _strava_ride_activities: list = []
    _strava_ride_gear: dict[str, CycleGear] = {}
    _strava_athlete_id: int = None

    def __init__(
        self,
        oauth_websession: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Init the Object."""
        self.oauth_websession = oauth_websession

    async def set_gear_service_date(
        self, strava_id: str, service_index: int, service_date: datetime
    ):
        """Set the service date of the strava_id gear for the given service attribute."""
        gear_service: CycleGearService = self._strava_ride_gear[strava_id].service[
            service_index
        ]
        gear_service.service_date = service_date

        # Calculate gear service time/distance with updated date
        self.recalc_gear_service()

    async def fetch_ride_activities(self):
        """Fetch ride activities from the Strava API, using adding found gear to the list."""

        _LOGGER.debug("Fetching Data from Strava API")

        activities_response = await self.oauth_websession.async_request(
            method="GET",
            url=f"https://www.strava.com/api/v3/athlete/activities?per_page={MAX_NB_ACTIVITIES}",
        )

        # Exit on rate limit, cannot update data
        if activities_response.status == 429:
            _LOGGER.warning(
                "Strava API rate limit has been reached why requesting activities."
            )
            return

        # Otherwise, existing logging message if not a good response
        if activities_response.status != 200:
            _LOGGER.error(
                f"Could not fetch strava activities (response code: {activities_response.status}): {await activities_response.text()}."
            )
            return

        json_data = json.loads(await activities_response.text())
        for activity in json_data:
            self._strava_athlete_id = int(activity["athlete"]["id"])

        # start with an empty list of activities
        self._strava_ride_activities = []

        # Create a list of ride activities only
        for idx, activity in enumerate(json_data):
            if activity["type"] != "Ride":
                continue
            self._strava_ride_activities.append(activity)

        # Make sure the gear dict contains all gear from ride activities
        for a in self._strava_ride_activities:
            gear_id = a["gear_id"]

            # Skip when gear no defined in strava
            if gear_id is None:
                continue

            # Check if this gear id has been found already, if not setup
            if gear_id not in self._strava_ride_gear:
                self._strava_ride_gear[gear_id] = CycleGear()

    async def fetch_gear_information(self):
        """Retrieve all gear information based on known id's from strava API."""

        # Load the name and overall distance of all gear
        for gear_id, gear in self._strava_ride_gear.items():
            api_response = await self.oauth_websession.async_request(
                method="GET",
                url=f"https://www.strava.com/api/v3/gear/{gear_id}",
            )

            # Exit on rate limit, cannot update data
            if api_response.status == 429:
                _LOGGER.warning(
                    f"Strava API rate limit has been reached when requesting gear {gear_id}."
                )
                return

            # Otherwise, existing logging message if not a good response
            if api_response.status != 200:
                _LOGGER.error(
                    f"Could not fetch strava gear (response code: {api_response.status}): {await api_response.text()}."
                )
                return

            json_gear = json.loads(await api_response.text())
            gear.name = json_gear["name"]
            name = json_gear["name"]
            name = name.replace(" ", "_")
            name = name.lower()
            gear.ha_id = name
            gear.distance = int(json_gear["distance"] / 1000)

    def recalc_gear_service(self):
        """Calculate gear service times and distances from loaded activities."""

        # Clear all service counters ready to reload from activities
        for gear_id in self._strava_ride_gear:
            self._strava_ride_gear[gear_id].clear_counters()

        # For every activity, ask the gear to process the usage
        for a in self._strava_ride_activities:
            gear_id = a["gear_id"]

            # Skip when no gear defined
            if gear_id is None:
                continue

            # activity date and time
            act_date = dt_parse(a["start_date"])
            distance = round(a["distance"] / 1000, 1)
            moving_time = round(a["moving_time"] / 3600, 2)

            # Add the activity distance and time to the gear
            self._strava_ride_gear[gear_id].process_activity(
                act_date, distance, moving_time
            )

    def create_gear_data(self):
        """Create a dictionary of gear data including service for HA entities."""

        # Create a single dictionary of key:value pairs for gear
        stats = {}
        ids = {}
        for strava_id, gear in self._strava_ride_gear.items():
            ha_id = gear.ha_id
            ids[ha_id] = {"name": gear.name, "strava_id": strava_id}
            stats[ha_id + "_distance"] = {"distance": gear.distance}
            for idx in range(MAX_GEAR_SERVICE_ITEMS):
                prefix = f"{ha_id}_service_gear_{idx}"
                # service: CycleGearService = getattr(gear, key)
                service: CycleGearService = gear.service[idx]
                stats[prefix] = {
                    "time": int(round(service.time, 0)),
                    "distance": int(round(service.distance, 0)),
                    "service_date": service.service_date,
                }

        return {"ids": ids, "stats": stats}

    def create_weekly_data(self):
        """Create a dictionary of weekly strava stats for HA entities."""
        weekly_data: dict = {}

        for mon_date in self._last_2years_mondays():
            weekly_data[mon_date] = {"distance": 0, "time": 0, "elevation": 0}
            for a in self._strava_ride_activities:
                # activity date and time, use the local date because we dont want year, month, day to be in local time (not utc)
                act_date = dt_parse(a["start_date_local"])
                act_date = date(act_date.year, act_date.month, act_date.day)
                distance = round(a["distance"] / 1000, 1)
                moving_time = round(a["moving_time"] / 3600, 2)

                #  increment weekly info
                if act_date >= mon_date and act_date < mon_date + timedelta(7):
                    weekly_data[mon_date]["distance"] += distance
                    weekly_data[mon_date]["time"] += moving_time
                    weekly_data[mon_date]["elevation"] += int(a["total_elevation_gain"])

        mon_this_week = date.today() + timedelta(0 - date.today().weekday())
        mon_last_week = mon_this_week + timedelta(-7)
        mon_last_fnight = mon_last_week + timedelta(-7)

        last_week = CycleWeekStats()
        last_week.distance = weekly_data[mon_last_week]["distance"]
        last_week.distance_delta = round(
            last_week.distance / weekly_data[mon_last_fnight]["distance"] * 100, 1
        )
        last_week.time = weekly_data[mon_last_week]["time"]
        last_week.time_delta = round(
            last_week.time / weekly_data[mon_last_fnight]["time"] * 100, 1
        )
        last_week.elevation = weekly_data[mon_last_week]["elevation"]

        this_week = CycleWeekStats()
        this_week.distance = weekly_data[mon_this_week]["distance"]
        this_week.distance_delta = round(
            this_week.distance / weekly_data[mon_last_week]["distance"] * 100, 1
        )
        this_week.time = weekly_data[mon_this_week]["time"]
        this_week.time_delta = round(
            this_week.time / weekly_data[mon_last_week]["time"] * 100, 1
        )
        this_week.elevation = weekly_data[mon_this_week]["elevation"]

        return {"last_week": last_week, "this_week": this_week}

    async def fetch_strava_data(self):
        """Fetch data for the latest activities from the Strava API."""

        # Fetch activity and gear from strava api
        await self.fetch_ride_activities()
        await self.fetch_gear_information()

        # Clear and recalculate gear service counters
        self.recalc_gear_service()

        # Create weekly data for entities
        weekly_stats = self.create_weekly_data()

        # Create gear data for entities
        gear_data = self.create_gear_data()

        # fetch summary stats
        summary_stats_url = (
            f"https://www.strava.com/api/v3/athletes/{self._strava_athlete_id}/stats"
        )

        summary_stats_response = await self.oauth_websession.async_request(
            method="GET",
            url=summary_stats_url,
        )

        sumary_stats = json.loads(await summary_stats_response.text())

        # Create a single dictionary of key:value pairs
        summary_stats = {}
        for k, v in sumary_stats.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    summary_stats[k + "_" + k2] = v2
            else:
                summary_stats[k] = v

        # Change units, from strava to our units
        # time = strava:seconds; we want:hours
        # distance = strava:meters; we want:km
        for k, v in summary_stats.items():
            if "distance" in k:
                summary_stats[k] = round(v / 1000, 1)
            if "time" in k:
                summary_stats[k] = round(v / 3600, 2)
            if "elevation" in k:
                summary_stats[k] = int(v)

        _LOGGER.debug("Strava statistics updated from API")

        return {
            "summary_stats": summary_stats,
            "weekly_stats": weekly_stats,
            "gear_ids": gear_data["ids"],
            "gear_stats": gear_data["stats"],
        }

    def _last_2years_mondays(self):
        d = date(date.today().year - 1, 1, 1)
        d += timedelta(7 - d.weekday())
        while d <= date.today():
            yield d
            d += timedelta(7)
