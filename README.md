# ASR Microelectronics ASR605x (ASR6501, ASR6502): development platform for [PlatformIO](http://platformio.org)

[![Build Status](https://github.com/HelTecAutomation/platform-asrmicro650x/workflows/Examples/badge.svg)](https://github.com/HelTecAutomation/platform-asrmicro650x/actions)

ASR Microelectronics ASR605x series is highly integrated and ultra low power SoC based on the PSoC 4000 series MCU (ARM Cortex M0+ Core) and Semtech SX1262 transceiver.

* [Home](https://registry.platformio.org/platforms/heltecautomation/asrmicro650x) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/asrmicro650x.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = asrmicro650x
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/HelTecAutomation/platform-asrmicro650x.git
board = ...
...
```

# Configuration

Please navigate to [documentation](https://docs.platformio.org/page/platforms/asrmicro650x.html).
