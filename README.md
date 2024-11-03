# Strava Ride

[![version](https://img.shields.io/github/manifest-json/v/tonymyatt/strava_ride?filename=custom_components%2Fstrava_ride%2Fmanifest.json&label=latest&color=slateblue)](https://github.com/tonymyatt/strava_ride/releases/latest)
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]

_Integration to integrate with [Strava][strava_ride], for ride statistics and bike gear data to create insights for cyclists._

## Installation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Installation is easiest via the [Home Assistant Community Store (HACS)](https://hacs.xyz/), which is the best place to get third-party integrations for Home Assistant. Once you have HACS set up, simply click the button below (requires My Homeassistant configured) or follow the [instructions for adding a custom
repository](https://hacs.xyz/docs/faq/custom_repositories) and then the integration will be available to install like any other.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tonymyatt&repository=strava_ride&category=integration)

## Configuration

### Remote Access to your Home Assistant
To use the Strava Ride integration, your Home Assistant must be accessible from an External URL (i.e. Remote Access). Without remote access, the integration won't be able to authenicate with Strava. To learn how to set up Remote Access for Home Assistant, please visit the Official Documentation. Two popular options are: 
- Nabu Casa. You can find this under Configuration -> "Home Assistant Cloud"
- Cloudflare. I use [addon-cloudflared](https://github.com/brenner-tobias/addon-cloudflared) by [@brenner-tobias](https://github.com/brenner-tobias).

### Obtain your Strava API credentials
Open your Strava Profile and go to Settings > My API Application.
- Follow the steps in the configuration wizard, and obtain your Strava API credentials (ID + secret).

### Add the integration to home assistant
Go to Settings / Devices & Services and press the Add Integration button, or click the shortcut button below (requires My Homeassistant configured).
During the setup, use your ID and secret from step 2
[![Add Integration to your Home Assistant
instance.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=strava_ride)

## How to Use

*Coming Soon*

## To Do

- Option to select which gear item are imported
- Custom number of gear service/maintenance items
- Custom names of gear service/maintenance items

## Contributing

To submit your changes please fork this repository and open a pull request. 

## Thanks To

 - [xiaomi_vacuum](https://github.com/pooyashahidi/xiaomi_vacuum) by [@pooyashahidi](https://github.com/pooyashahidi)


[strava_ride]: https://www.strava.com/login
[commits-shield]: https://img.shields.io/github/commit-activity/y/tonymyatt/strava_ride.svg?plastic
[commits]: https://github.com/tonymyatt/strava_ride/commits/main
[license-shield]: https://img.shields.io/github/license/tonymyatt/strava_ride.svg?plastic
[maintenance-shield]: https://img.shields.io/badge/maintainer-tonymyatt-blue.svg?plastic
