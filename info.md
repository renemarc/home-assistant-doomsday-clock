[![GitHub Release][img-release]][link-release]
[![Maintainer][img-maintainer]][link-maintainer]
[![All Contributors][img-contributors]][link-contributors]

[![Community Forum][img-forum]][link-forum]
[![PRs Welcome][img-contribute]][link-contribute]
[![Open issues][img-issues]][link-issues]
[![Stargazers][img-stars]][link-stars]

<br/>

Add support for the [Doomsday Clock](https://en.wikipedia.org/wiki/Doomsday_Clock) world threat assessment index from the [Bulletin of the Atomic Scientists](https://thebulletin.org/doomsday-clock/).

<br/>

<div align="center">
    <figure>
        <div>
            <img src="https://raw.githubusercontent.com/renemarc/home-assistant-doomsday-clock/master/.github/screenshot-card.png" alt="Sensor state card" title="Sensor state card" width="325">
            <img src="https://raw.githubusercontent.com/renemarc/home-assistant-doomsday-clock/master/.github/screenshot-details.png" alt="Sensor details" title="Sensor details" width="325">
        </div>
        <figcaption>
            <p><strong>Sensor state card and details popup.</strong></p>
        </figcaption>
    </figure>
</div>

## Description 🕚

The [Doomsday Clock](https://thebulletin.org/doomsday-clock/current-time/) helps monitor how close humanity is to a man-made global catastrophe, its own destruction if you will, either through nuclear war or climate change. Useful in case egocentric psychopaths keep on playing Russian roulette with humanity's future. Makes a great addition to your fallout shelter's Home Assistant build! 😱

<br/>

<div align="center">
    <figure>
        <div>
            <a href="https://www.youtube.com/watch?v=jCnWPbn-ZKo"><img src="http://img.youtube.com/vi/jCnWPbn-ZKo/maxresdefault.jpg" alt="Doomsday Clock description video by Vox" title="Doomsday Clock description video by Vox" width="400"></a>
        </div>
        <figcaption>
            <p><strong><a href="https://www.youtube.com/watch?v=jCnWPbn-ZKo">Doomsday Clock description video by <em>Vox</em>.</a></strong></strong></p>
        </figcaption>
    </figure>
</div>

<br/>

The clock doesn't change often, at most once a year, and offers no API. Since we rely on web scraping of [TheBulletin.org](https://thebulletin.org) the component has a goodwill throttle of 6 hours (21,600 seconds), but it would be best to set the scan interval for the sensor to 1 day (86,400 seconds) or more.

## Configuration ⚙

```yaml
# Example configuration.yaml entry
sensor:
  - platform: doomsday_clock
    scan_interval: 86400
```

> **`icon`** _(string) (optional)_  
> [Material Design Icon](https://materialdesignicons.com) that illustrates the sensor. (default = [`mdi:nuke`](https://materialdesignicons.com/icon/nuke))  
> <br/>
> **`name`** _(string) (optional)_  
> Custom name of sensor. (default = `Doomsday Clock`)  
> <br/>
> **`scan_interval`** _(integer) (optional)_  
> Number of seconds between polls. (minimum = `21600` seconds [6 hours])  
> <br/>
> **`unit_of_measurement`** _(string) (optional)_  
> Custom unit of measurement for the value. (default = `min`)  
> <br/>
> **`value_template`** _([template](https://home-assistant.io/docs/configuration/templating/)) (optional)_  
> Custom template to manipulate the state of the sensor.

## Contributing ✨

This project follows the [all-contributors](https://allcontributors.org) specification. Found a bug, want to suggest an idea or share some improvements? [Contributions of any kind are welcome!][link-contribute] 😃

<div align="center">
    <figure>
        <div>
            <a href="https://www.youtube.com/watch?v=JxN70DYuPuA"><img src="https://media.giphy.com/media/xUOxfg0ESyhKOv4Vva/giphy.gif" alt="Bethesda's Fallout Vault Boy" title="Bethesda's Fallout Vault Boy in &quot;Atomics for Peace&quot;" width="200"></a>
        </div>
        <figcaption>
            <p><strong><a href="https://www.youtube.com/watch?v=JxN70DYuPuA" title="Bethesda's Fallout Vault Boy in &quot;Atomics for Peace&quot;">🕊️ Make the world a better place! 🌱</a></strong></p>
        </figcaption>
    </figure>
</div>


[img-contribute]:https://img.shields.io/badge/pull_requests-welcome-brightgreen.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48IURPQ1RZUEUgc3ZnIFBVQkxJQyAiLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4iICJodHRwOi8vd3d3LnczLm9yZy9HcmFwaGljcy9TVkcvMS4xL0RURC9zdmcxMS5kdGQiPjxzdmcgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgdmVyc2lvbj0iMS4xIiB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTYsM0EzLDMgMCAwLDEgOSw2QzksNy4zMSA4LjE3LDguNDIgNyw4LjgzVjE1LjE3QzguMTcsMTUuNTggOSwxNi42OSA5LDE4QTMsMyAwIDAsMSA2LDIxQTMsMyAwIDAsMSAzLDE4QzMsMTYuNjkgMy44MywxNS41OCA1LDE1LjE3VjguODNDMy44Myw4LjQyIDMsNy4zMSAzLDZBMywzIDAgMCwxIDYsM002LDVBMSwxIDAgMCwwIDUsNkExLDEgMCAwLDAgNiw3QTEsMSAwIDAsMCA3LDZBMSwxIDAgMCwwIDYsNU02LDE3QTEsMSAwIDAsMCA1LDE4QTEsMSAwIDAsMCA2LDE5QTEsMSAwIDAsMCA3LDE4QTEsMSAwIDAsMCA2LDE3TTIxLDE4QTMsMyAwIDAsMSAxOCwyMUEzLDMgMCAwLDEgMTUsMThDMTUsMTYuNjkgMTUuODMsMTUuNTggMTcsMTUuMTdWN0gxNVYxMC4yNUwxMC43NSw2TDE1LDEuNzVWNUgxN0EyLDIgMCAwLDEgMTksN1YxNS4xN0MyMC4xNywxNS41OCAyMSwxNi42OSAyMSwxOE0xOCwxN0ExLDEgMCAwLDAgMTcsMThBMSwxIDAgMCwwIDE4LDE5QTEsMSAwIDAsMCAxOSwxOEExLDEgMCAwLDAgMTgsMTdaIiBmaWxsPSIjZmZmZmZmIiAvPjwvc3ZnPgo=&style=for-the-badge&maxAge=86400
[img-contributors]:https://img.shields.io/badge/all_contributors-3-orange.svg?logo=github&style=for-the-badge&maxAge=21600
[img-forum]:https://img.shields.io/badge/community-forum-brightgreen.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiICB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+CiAgIDxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik0xNywxMlYzQTEsMSAwIDAsMCAxNiwySDNBMSwxIDAgMCwwIDIsM1YxN0w2LDEzSDE2QTEsMSAwIDAsMCAxNywxMk0yMSw2SDE5VjE1SDZWMTdBMSwxIDAgMCwwIDcsMThIMThMMjIsMjJWN0ExLDEgMCAwLDAgMjEsNloiIC8+Cjwvc3ZnPg==&style=for-the-badge&maxAge=86400
[img-issues]:https://img.shields.io/github/issues/renemarc/home-assistant-doomsday-clock.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiICB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+CiAgIDxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik0xMSwxNUgxM1YxN0gxMVYxNU0xMSw3SDEzVjEzSDExVjdNMTIsMkM2LjQ3LDIgMiw2LjUgMiwxMkExMCwxMCAwIDAsMCAxMiwyMkExMCwxMCAwIDAsMCAyMiwxMkExMCwxMCAwIDAsMCAxMiwyTTEyLDIwQTgsOCAwIDAsMSA0LDEyQTgsOCAwIDAsMSAxMiw0QTgsOCAwIDAsMSAyMCwxMkE4LDggMCAwLDEgMTIsMjBaIiAvPgo8L3N2Zz4=&style=for-the-badge&maxAge=21600
[img-maintainer]:https://img.shields.io/badge/maintainer-René--Marc_Simard_(@renemarc)-blue.svg?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiICB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+CiAgIDxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik0xMiwyQTEwLDEwIDAgMCwwIDIsMTJBMTAsMTAgMCAwLDAgMTIsMjJBMTAsMTAgMCAwLDAgMjIsMTJBMTAsMTAgMCAwLDAgMTIsMk0xMSwxNC40MVYxOS45M0M5LjU4LDE5Ljc1IDguMjMsMTkuMTkgNy4xLDE4LjMxTDExLDE0LjQxTTEzLDE0LjQxTDE2LjksMTguMzFDMTUuNzcsMTkuMTkgMTQuNDIsMTkuNzUgMTMsMTkuOTNWMTQuNDFNNCwxMkM0LDcuOTcgNyw0LjU3IDExLDQuMDdWMTEuNTlMNS42OSwxNi45QzQuNTksMTUuNSA0LDEzLjc4IDQsMTJNMTguMzEsMTYuOUwxMywxMS41OVY0LjA3QzE3LDQuNTcgMjAsNy45NyAyMCwxMkMyMCwxMy43OCAxOS40MSwxNS41IDE4LjMxLDE2LjlaIiAvPgo8L3N2Zz4=&style=for-the-badge&maxAge=86400
[img-release]:https://img.shields.io/github/release/renemarc/home-assistant-doomsday-clock/all.svg?logo=git&logoColor=white&style=for-the-badge&maxAge=21600
[img-stars]:https://img.shields.io/github/stars/renemarc/home-assistant-doomsday-clock.svg?label=Stargazers&logo=github&style=for-the-badge&maxAge=21600

[link-contribute]:https://github.com/renemarc/home-assistant-doomsday-clock/blob/master/CONTRIBUTING.md
[link-contributors]:https://github.com/renemarc/home-assistant-doomsday-clock/#contributors-
[link-forum]:https://community.home-assistant.io/t/doomsday-clock-custom-sensor/40758
[link-issues]:https://github.com/renemarc/home-assistant-doomsday-clock/issues
[link-maintainer]:https://github.com/renemarc/
[link-release]:https://github.com/renemarc/home-assistant-doomsday-clock/releases
[link-stars]:https://github.com/renemarc/home-assistant-doomsday-clock/stargazers
