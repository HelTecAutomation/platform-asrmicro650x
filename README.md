# ASR Microelectronics ASR605x (ASR6501, ASR6502): development platform for [PlatformIO](https://platformio.org)

[![Build Status](https://github.com/HelTecAutomation/platform-asrmicro650x/workflows/Examples/badge.svg)](https://github.com/HelTecAutomation/platform-asrmicro650x/actions)

ASR Microelectronics ASR605x series is highly integrated and ultra low power SoC based on the PSoC 4000 series MCU (ARM Cortex M0+ Core) and Semtech SX1262 transceiver.

* [Home](https://registry.platformio.org/platforms/heltecautomation/asrmicro650x) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/asrmicro650x.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](https://platformio.org)
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

## LoRaWAN

LoRaWAN protocol can be configured in https://docs.platformio.org/en/latest/projectconf/index.html using the following syntax
``board_build.arduino.lorawan.*`` where ``*`` is an option from the following list:

| Option      | Description | Possible values | Default |
| ----------- | ----------- | --------------- | ------- |
| ``region`` | Region definition | ``AS923_AS1``, ``AS923_AS2``, ``AU915``, ``CN470``, ``CN779``, ``EU433``, ``EU868``, ``KR920``, ``IN865``, ``US915``, ``US915_HYBRID`` | ``US915`` |
| ``class`` | Device class | ``CLASS_A``, ``CLASS_C`` | ``CLASS_A`` |
| ``netmode`` | Activation method | ``OTAA``, ``ABP`` | ``OTAA`` |
| ``adr`` | Adaptive Data Rate | ``ON``, ``OFF`` | ``ON`` |
| ``uplinkmode`` | Uplink confirmed/unconfirmed messages | ``CONFIRMED``, ``UNCONFIRMED`` | ``CONFIRMED`` |
| ``net_reserve`` | Don't rejoin after reset | ``ON``, ``OFF`` | ``OFF`` |
| ``at_support`` | AT commands support | ``ON``, ``OFF`` | ``ON`` |
| ``rgb`` | RGB light for LoRaWAN status | ``ACTIVE``, ``DEACTIVE`` | ``ACTIVE`` |
| ``preamble_length`` | Preamble length | ``8``, ``16`` (For M00 and M00L) | ``8`` |
| ``debug_level`` | Print LoRaWAN relevant messages print to serial port | ``NONE``, ``FREQ`` (Sending/receiving frequency), ``FREQ_AND_DIO`` (Sending/receiving frequency and DIO pin interrupt information) | ``NONE`` |


**Example**

```ini
[env:cubecell_board]
platform = asrmicro650x
framework = arduino
board = cubecell_board
board_build.arduino.lorawan.region = EU433
board_build.arduino.lorawan.adr = OFF
board_build.arduino.lorawan.debug_level = FREQ_AND_DIO
```

More information about LoRaWAN configuration can be found in
[the official CubeCell documentation](https://heltec-automation-docs.readthedocs.io/en/latest/cubecell/index.html).
