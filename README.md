# Strava Ride

[![version](https://img.shields.io/github/manifest-json/v/tonymyatt/strava_ride?filename=custom_components%2Fstrava_ride%2Fmanifest.json&label=latest&color=slateblue)](https://github.com/tonymyatt/strava_ride/releases/latest)
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]

_Integration to integrate with [Strava][strava_ride], for ride statistics and bike gear data to create insights for cyclists._

<img src="https://raw.githubusercontent.com/tonymyatt/strava_ride/main/image/statistics-sensors.PNG"><img src="https://raw.githubusercontent.com/tonymyatt/strava_ride/main/image/gear-sensors.PNG">

## Installation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Installation is via the [Home Assistant Community Store (HACS)](https://hacs.xyz/). Once you have HACS set up, simply click the button below (requires My Homeassistant configured) or follow the [instructions for adding a custom
repository](https://hacs.xyz/docs/faq/custom_repositories) and then the integration will be available to install like any other.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tonymyatt&repository=strava_ride&category=integration)

## Configuration

### Remote Access to your Home Assistant
To use the Strava Ride integration, your Home Assistant must be accessible from an External URL (i.e. Remote Access), allowing authentication with Strava. To learn how to set up Remote Access for Home Assistant, please visit the Official Documentation. Two popular options are: 
- Nabu Casa. You can find this under Configuration -> "Home Assistant Cloud".
- Cloudflare. I use [addon-cloudflared](https://github.com/brenner-tobias/addon-cloudflared) by [@brenner-tobias](https://github.com/brenner-tobias).

### Obtain your Strava API credentials
Open your Strava Profile and go to Settings > My API Application.
- Follow the steps in the configuration wizard, and obtain your Strava API credentials. Use the following when prompted:
  - Application Name: *Any name you like*
  - Category: *Any category you like*
  - Club: *Blank or any you like*
  - Website: *Blank or any you like*
  - Application Description: *Blank or any you like*
  - Authorisation Callback Domain: my.home-assistant.io
- You will need both Client ID + Client Secret in the next step.

### Add the integration to home assistant
Go to Settings / Devices & Services and press the Add Integration button, or click the shortcut button below (requires My Homeassistant configured).
During the setup, use your ID and secret from the previous step.
[![Add Integration to your Home Assistant
instance.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=strava_ride)

## How to Use

*Coming Soon*

## Example Cards

### Bike Service Card
Requires custom card [multiple-entity-row](https://github.com/benct/lovelace-multiple-entity-row). Replace bike_a with your bike gear entity name.

<img src="https://raw.githubusercontent.com/tonymyatt/strava_ride/main/image/gear-bike-example.PNG">

```yaml
type: entities
entities:
  - entity: sensor.bike_a_distance
    name: Total Distance
  - type: custom:multiple-entity-row
    entity: sensor.bike_a_service_gear_0
    name: Chain
    state_color: true
    show_state: false
    entities:
      - icon: mdi:restore-alert
        state_color: false
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.bike_a_service_gear_0_reset
          confirmation:
            text: Confirm Chain Lubed?
      - entity: datetime.bike_a_service_gear_0_date
        name: Last Lubed
        format: date
      - entity: sensor.bike_a_service_gear_0
        name: Distance
  - type: custom:multiple-entity-row
    entity: sensor.bike_a_service_gear_5
    name: Wash & Polish
    state_color: true
    show_state: false
    entities:
      - icon: mdi:restore-alert
        state_color: false
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.bike_a_service_gear_5_reset
          confirmation:
            text: Wash and Polish Complete?
      - entity: datetime.bike_a_service_gear_5_date
        name: Last Washed
        format: date
      - entity: sensor.bike_a_service_gear_5
        name: Distance
  - type: custom:multiple-entity-row
    entity: sensor.bike_a_service_gear_1
    name: Front Tyre
    state_color: true
    show_state: false
    entities:
      - icon: mdi:restore-alert
        state_color: false
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.bike_a_service_gear_1_reset
          confirmation:
            text: Confirm Front Tyre Changed?
      - entity: datetime.bike_a_service_gear_1_date
        name: Last Changed
        format: date
      - entity: sensor.bike_a_service_gear_1
        name: Distance
  - type: custom:multiple-entity-row
    entity: sensor.bike_a_service_gear_2
    name: Rear Tyre
    state_color: true
    show_state: false
    entities:
      - icon: mdi:restore-alert
        state_color: false
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.bike_a_service_gear_2_reset
          confirmation:
            text: Confirm Rear Tyre Changed?
      - entity: datetime.bike_a_service_gear_2_date
        name: Last Changed
        format: date
      - entity: sensor.bike_a_service_gear_2
        name: Distance
  - type: custom:multiple-entity-row
    entity: sensor.bike_a_service_gear_7
    name: Bar Tape
    state_color: true
    show_state: false
    entities:
      - icon: mdi:restore-alert
        state_color: false
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.bike_a_service_gear_7_reset
          confirmation:
            text: Confirm Bar Tape Changed?
      - entity: datetime.bike_a_service_gear_7_date
        name: Last Changed
        format: date
      - entity: sensor.bike_a_service_gear_7
        name: Time
  - type: custom:multiple-entity-row
    entity: sensor.bike_a_service_gear_6
    name: Major Service
    state_color: true
    show_state: false
    entities:
      - icon: mdi:restore-alert
        state_color: false
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.bike_a_service_gear_6_reset
          confirmation:
            text: Confirm Major Service Completed?
      - entity: datetime.bike_a_service_gear_6_date
        name: Last Serviced
        format: date
      - entity: sensor.bike_a_service_gear_6
        name: Distance
  - type: custom:multiple-entity-row
    entity: sensor.bike_a_service_gear_3
    name: Shop Service
    state_color: true
    show_state: false
    entities:
      - icon: mdi:restore-alert
        state_color: false
        tap_action:
          action: call-service
          service: button.press
          service_data:
            entity_id: button.bike_a_service_gear_3_reset
          confirmation:
            text: Confirm Shop Serviced?
      - entity: datetime.bike_a_service_gear_3_date
        name: Last Serviced
        format: date
      - entity: sensor.bike_a_service_gear_3
        name: Distance
title: Bike A

```

## To Do

- Option to select which gear (bikes) are imported
- Custom number of gear (bike) service/maintenance items
- Custom names of gear (bike) service/maintenance items

## Contributing

To submit your changes please fork this repository and open a pull request. 

## Thanks To

Forked from [ha_strava](https://github.com/craibo/ha_strava) by [@craibo](https://github.com/craibo)

[strava_ride]: https://www.strava.com/login
[commits-shield]: https://img.shields.io/github/commit-activity/y/tonymyatt/strava_ride.svg?plastic
[commits]: https://github.com/tonymyatt/strava_ride/commits/main
[license-shield]: https://img.shields.io/github/license/tonymyatt/strava_ride.svg?plastic
[maintenance-shield]: https://img.shields.io/badge/maintainer-tonymyatt-blue.svg?plastic
