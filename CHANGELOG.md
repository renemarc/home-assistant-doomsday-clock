# Changelog [![Keep a Changelog v1.0.0][badge-keepachangelog]][link-keepachangelog] [![Semantic Versioning v2.0.0][badge-semver]][link-semver]

All notable changes to the [Doomsday Clock sensor][link-repo] will be documented
in this list. The format is based on [Keep a Changelog][link-keepachangelog],
and this project adheres to [Semantic Versioning][link-semver].


## [Unreleased][Unreleased] [![Commits to be deployed][badge-unreleased]][Unreleased]

### Added

- This changelog based on [Keep a Changelog][link-keepachangelog].


## [v2.1.0] — 2019-06-15

More polished version with support for HACS, improved documentation, better
community health files, and GitHub bots.

### Added

- Highlighted section for all contributors.
- Support for [HACS (Home Assistant Community Store)](https://custom-components.github.io/hacs/).
- Support for [All Contributors](https://allcontributors.org/).
- Support for [Probot's No Response](https://probot.github.io/apps/no-response/) issue closing service app.
- Support for [Probot's Stale](https://probot.github.io/apps/stale/) auto-closing service app.
- [Code of Conduct](./CODE_OF_CONDUCT.md).

### Changed

- Improve general documentation.
- Simplify contributors documentation
- Expand issues and pull request templates.
- Move Github resources into [dedicated folder](./.github).

## [v2.0.1] — 2019-06-03

### Fixed

- Tracker issue

## [v2.0.0] — 2019-06-03

Updated version for easier integration.

### Added

- Support for [Custom Updater](https://github.com/custom-components/custom_updater).

### Changed

- **BREAKING:** Reorganize component file structure to comply with [Home Assistant's Great Migration initiative](https://developers.home-assistant.io/blog/2019/02/19/the-great-migration.html).


## [v1.0.0] — 2018-07-17

Production-level version.

### Added

- Employ defensive design in case resource changes unexpectedly.

### Changed

- **BREAKING:** Dedicate repo to a single sensor.
- Increase delay between updates.
- Improve code styling and comments.

### Fixed

- Update resource URL and selector to match new site design.

## [v0.1.0] — 2018-01-26

Inital release.

### Added

- Extraction of minutes to midnight from [TheBulletin.org](https://thebulletin.org).
- Documentation.


[Unreleased]: https://github.com/renemarc/home-assistant-doomsday-clock/compare/2.1.0...master
[v2.1.0]: https://github.com/renemarc/home-assistant-doomsday-clock/releases/tag/2.1.0
[v2.0.1]: https://github.com/renemarc/home-assistant-doomsday-clock/releases/tag/2.0.1
[v2.0.0]: https://github.com/renemarc/home-assistant-doomsday-clock/releases/tag/2.0.0
[v1.0.0]: https://github.com/renemarc/home-assistant-doomsday-clock/releases/tag/1.0.0
[v0.1.0]: https://github.com/renemarc/home-assistant-doomsday-clock/releases/tag/0.1.0


[badge-keepachangelog]:https://img.shields.io/badge/keep%20a%20changelog-v1.0.0-%23E05735?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiICB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+CiAgIDxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik01LDE1LjVMNy41LDIwSDIuNUw1LDE1LjVNOSwxOUgyMVYxN0g5VjE5TTUsOS41TDcuNSwxNEgyLjVMNSw5LjVNOSwxM0gyMVYxMUg5VjEzTTUsMy41TDcuNSw4SDIuNUw1LDMuNU05LDdIMjFWNUg5VjdaIiAvPgo8L3N2Zz4=&cacheSeconds=86400

[badge-unreleased]:https://img.shields.io/github/commits-since/renemarc/home-assistant-doomsday-clock/latest.svg?label=commits%20to%20be%20deployed&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0Ij4KCTxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik0xMy41LDhIMTJWMTNMMTYuMjgsMTUuNTRMMTcsMTQuMzNMMTMuNSwxMi4yNVY4TTEzLDNBOSw5IDAgMCwwIDQsMTJIMUw0Ljk2LDE2LjAzTDksMTJINkE3LDcgMCAwLDEgMTMsNUE3LDcgMCAwLDEgMjAsMTJBNyw3IDAgMCwxIDEzLDE5QzExLjA3LDE5IDkuMzIsMTguMjEgOC4wNiwxNi45NEw2LjY0LDE4LjM2QzguMjcsMjAgMTAuNSwyMSAxMywyMUE5LDkgMCAwLDAgMjIsMTJBOSw5IDAgMCwwIDEzLDMiIC8+Cjwvc3ZnPgo=&cacheSeconds=300

[badge-semver]:https://img.shields.io/badge/semver-v2.0.0-black?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiICB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCI+CiAgIDxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik0xNC42LDE2LjZMMTkuMiwxMkwxNC42LDcuNEwxNiw2TDIyLDEyTDE2LDE4TDE0LjYsMTYuNk05LjQsMTYuNkw0LjgsMTJMOS40LDcuNEw4LDZMMiwxMkw4LDE4TDkuNCwxNi42WiIgLz4KPC9zdmc+&cacheSeconds=86400


[link-repo]:https://github.com/renemarc/home-assistant-doomsday-clock
[link-keepachangelog]:https://keepachangelog.com/en/1.0.0/
[link-semver]:https://semver.org/spec/v2.0.0.html
