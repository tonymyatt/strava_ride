# Strava Ride

[![version](https://img.shields.io/github/manifest-json/v/tonymyatt/strava_ride?filename=custom_components%2Fstrava_ride%2Fmanifest.json&label=latest&plastic)](https://github.com/tonymyatt/strava_ride/releases/latest)
![GitHub all releases](https://img.shields.io/github/downloads/tonymyatt/strava_ride/total)
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

_Integration to integrate with [strava_ride][strava_ride]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Sensors showing weekly statistics and bike servicing durations and kilometers.
`button` | Provides ability to reset servicing durations for bikes to current date time.
`datetime` | Access to bike last serviced date and time.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `integration_blueprint`.
1. Download _all_ the files from the `custom_components/integration_blueprint/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

## Configuration is done in the UI

<!---->

***

[strava_ride]: https://github.com/tonymyatt/strava_ride
[commits-shield]: https://img.shields.io/github/commit-activity/y/tonymyatt/strava_ride.svg?plastic
[commits]: https://github.com/tonymyatt/strava_ride/commits/main
[license-shield]: https://img.shields.io/github/license/tonymyatt/strava_ride.svg?plastic
[maintenance-shield]: https://img.shields.io/badge/maintainer-tonymyatt-blue.svg?plastic
[releases-shield]: https://img.shields.io/github/release/tonymyatt/strava_ride.svg?plastic
[releases]: https://github.com/tonymyatt/strava_ride/releases
