# Custom components for Home Assistant

Collection of my custom components for the [Home Assistant](https://home-assistant.io/) open-source home automation platform.

## Doomsday Clock Component

Support for the [Doomsday Clock](https://en.wikipedia.org/wiki/Doomsday_Clock) from the [Bulletin of the Atomic Scientists](https://thebulletin.org/).

Helps monitor how close humanity is a man-made global catastrophe, its own destruction if you will, either through nuclear war or climate change. Useful in case egocentric psychopaths keep on playing Russian roulette with humanity's future. Makes a great addition to your fallout shelter's Home Assistant build!

The clock doesn't change often, at most once a year, and offers no API. Since we rely on web scraping of their web site the component has a goodwill throttle of 1-hour, but it would be best to set the scan interval for the sensor to 1 day (86400 seconds) or more.

Code inspired by [mattbierner's Node Doomsday Clock API](https://github.com/mattbierner/MinutesToMidnight).

### Screenshots

![Sensor state](./screenshots/doomsday_clock_state.png "Sensor state")

### Installation

To enable the Doomsday Clock sensor in your installation:

1. Copy file `sensor/doomsday_clock.py` to `your_config_dir/custom_components/sensor` directory (create folder if necessary). 
1. Add the sensor to your `configuration.yaml` (see below).
1. Restart Home Assistant.

```yaml
# Example configuration.yaml entry
sensor:
  - platform: doomsday_clock
    name: Doomsday
    scan_interval: 86400
```

### Configuration variables

- **name** _(string) (optional)_ Name of sensor. (default = "Doomsday Clock")
- **scan_interval** _(number) (optional)_ Number of seconds between polls. (minimum = 3600 seconds).
- **unit_of_measurement** _(string) (optional)_ Defines the units of measurement of the sensor. (default = "min").
- **value_template** _([template](https://home-assistant.io/docs/configuration/templating/)) (optional)_ Defines a template to manipulate the state of the sensor.






