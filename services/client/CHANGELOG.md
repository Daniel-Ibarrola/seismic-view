# Changelog

## v0.2.1
- Fixed conversion factor to convert counts to gals. Now each station
has its own conversion factor.
- Changed accelerations slider range to smaller values.


## v0.2.0
Updated and styled UI, added new options.

### Features
- New style for charts: removed grid, lines slimmer and points
aren't shown.
- Station list component restyled and uses scrolling instead of
displaying a very long list.
- Options menu redone: channel and units selector changed from dropdown to radio buttons.
- Sliders for time and acceleration range.

### Dependencies
- Use MaterialUI 

### Development
- Button to skip login. Only appears in dev mode.

## v0.1.0

First release of earthworm grapher website.

### Features

- Can visualize each station data individually and can select
between the three channels of each station.
- Can choose between gals and counts for the units of the acceleration.
- Can select the following stats for acceleration: min, max and mean.
- Website is protected with authentication

### Tests
- Unit tests for react components.
- CI GitHub action
- Server program simulates data in real time for developing.
