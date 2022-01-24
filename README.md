# portable-air-logger
logging CO2, VOC, temperature, and humidity with an RP2040

This is basically just a fork of [@BlitzCityDIY](https://github.com/BlitzCityDIY)'s [Disconnected CO2 Data Logger](https://learn.adafruit.com/disconnected-co2-data-logger) with minor changes to support an [additional sensor for logging VOC info](https://www.adafruit.com/product/4829). 

I modified [the 3D case design](https://www.thingiverse.com/thing:5030874) a bit as well to support the sensor, add a slightly larger USB-C hole for the cable I use, add a hole for the MicroSD card, and adding some ventilation holes as well. Here is [my remix on Thingiverse](https://www.thingiverse.com/thing:5214475), and the two modified parts on TinkerCAD: [sensor-box](https://www.tinkercad.com/things/0YbBEU34PpT) and [sensor-lid](https://www.tinkercad.com/things/9p78jmuUmk7).

This was my first time working with RP2040, CircuitPython, and STEMMA QT connectors. It was a very refreshing weekend project compared to some previous electronics projects which required lots of soldering and C++.

![air-logger](https://user-images.githubusercontent.com/17863/150721770-ea3c41e4-5e17-4324-9afc-bd428591057b.jpg)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdieseltravis%2Fportable-air-logger.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fdieseltravis%2Fportable-air-logger?ref=badge_shield)


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdieseltravis%2Fportable-air-logger.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fdieseltravis%2Fportable-air-logger?ref=badge_large)