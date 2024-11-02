from __future__ import annotations

import json
import logging
import pprint
from datetime import datetime as dt, date, timedelta

from homeassistant.helpers import config_entry_oauth2_flow

from .const import MAX_NB_ACTIVITIES

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class CycleWeekStats:
    distance = 0
    distance_delta = 0
    time = 0
    time_delta = 0
    elevation = 0

    @property
    def climbing(self) -> float:
        climb = 0
        if self.distance > 0:
            climb = round(self.elevation / self.distance / 10, 1)
        return climb


class StravaAPI:
    """
    API to read data from Strava API
    """

    def __init__(
        self,
        oauth_websession: config_entry_oauth2_flow.OAuth2Session,
    ):
        """Init the Object."""
        self.oauth_websession = oauth_websession

    async def fetch_strava_data(self):
        """
        Fetches data for the latest activities from the Strava API
        """

        _LOGGER.debug("Fetching Data from Strava API")

        activities_response = await self.oauth_websession.async_request(
            method="GET",
            url=f"https://www.strava.com/api/v3/athlete/activities?per_page={MAX_NB_ACTIVITIES}",
        )

        if activities_response.status == 200:
            json_data = json.loads(await activities_response.text())
            athlete_id = None
            for activity in json_data:
                athlete_id = int(activity["athlete"]["id"])

            # Create a list of ride activities only
            activities = []
            for idx, activity in enumerate(json_data):

                if activity["type"] != "Ride":
                    continue

                activities.append(activity)

            self._weekly_data = dict()

            for mon_date in self._last_2years_mondays():
                self._weekly_data[mon_date] = {"distance": 0, "time": 0, "elevation": 0}
                for a in activities:
                    act_date = dt.strptime(a["start_date_local"], "%Y-%m-%dT%H:%M:%SZ")
                    act_date = date(act_date.year, act_date.month, act_date.day)
                    if act_date >= mon_date and act_date < mon_date + timedelta(7):
                        self._weekly_data[mon_date]["distance"] += round(
                            a["distance"] / 1000, 1
                        )
                        self._weekly_data[mon_date]["time"] += round(
                            a["moving_time"] / 3600, 2
                        )
                        self._weekly_data[mon_date]["elevation"] += int(
                            a["total_elevation_gain"]
                        )

            weekly_stats = self._calc_weekly_strava_stats()

            # fetch summary stats
            summary_stats_url = (
                f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats"
            )

            summary_stats_response = await self.oauth_websession.async_request(
                method="GET",
                url=summary_stats_url,
            )

            sumary_stats = json.loads(await summary_stats_response.text())

            # Create a single dictionary of key:value pairs
            summary_stats = {}
            for (k, v) in sumary_stats.items():
                if isinstance(v, dict):
                    for (k2, v2) in v.items():
                        summary_stats[k + "_" + k2] = v2
                else:
                    summary_stats[k] = v

            # Change units, from strava to our units
            # time = strava:seconds; we want:hours
            # distance = strava:meters; we want:km
            for (k, v) in summary_stats.items():
                if "distance" in k:
                    summary_stats[k] = round(v / 1000, 1)
                if "time" in k:
                    summary_stats[k] = round(v / 3600, 2)
                if "elevation" in k:
                    summary_stats[k] = int(v)

        elif activities_response.status == 429:
            _LOGGER.warn("Strava API rate limit has been reached")
            return

        else:
            _LOGGER.error(
                f"Could not fetch strava activities (response code: {activities_response.status}): {await activities_response.text()}"
            )
            return

        _LOGGER.debug(f"Strava statistics updated from API")

        data = {
            # "activities": activities,
            "summary_stats": summary_stats,
            "weekly_stats": weekly_stats,
        }

        return data

    def _calc_weekly_strava_stats(self):

        # Weekly data not available
        if self._weekly_data is None:
            return None

        data = self._weekly_data
        mon_this_week = date.today() + timedelta(0 - date.today().weekday())
        mon_last_week = mon_this_week + timedelta(-7)
        mon_last_fnight = mon_last_week + timedelta(-7)

        last_week = CycleWeekStats()
        last_week.distance = data[mon_last_week]["distance"]
        last_week.distance_delta = round(
            last_week.distance / data[mon_last_fnight]["distance"] * 100, 1
        )
        last_week.time = data[mon_last_week]["time"]
        last_week.time_delta = round(
            last_week.time / data[mon_last_fnight]["time"] * 100, 1
        )
        last_week.elevation = data[mon_last_week]["elevation"]

        this_week = CycleWeekStats()
        this_week.distance = data[mon_this_week]["distance"]
        this_week.distance_delta = round(
            this_week.distance / data[mon_last_week]["distance"] * 100, 1
        )
        this_week.time = data[mon_this_week]["time"]
        this_week.time_delta = round(
            this_week.time / data[mon_last_week]["time"] * 100, 1
        )
        this_week.elevation = data[mon_this_week]["elevation"]

        return {"last_week": last_week, "this_week": this_week}

    def _last_2years_mondays(self):
        d = date(date.today().year - 1, 1, 1)
        d += timedelta(7 - d.weekday())
        while d <= date.today():
            yield d
            d += timedelta(7)
