# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

import os

from SCons.Script import DefaultEnvironment


env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
core = board.get("build.core")

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinoasrmicro650x")
assert os.path.isdir(FRAMEWORK_DIR)

env.Append(
    CPPDEFINES=[
        ("ARDUINO", 10813),
        "__ASR6501__",
        ("CONFIG_MANUFACTURER", '\\"ASR\\"'),
        ("CONFIG_DEVICE_MODEL", '\\"6501\\"'),
        ("CONFIG_VERSION", '\\"v4.0\\"'),
        ("CY_CORE_ID", 0),
        "CONFIG_LORA_USE_TCXO"
    ],

    CCFLAGS=[
        "-w",
        "-Wall",
        "-Os",
        "-mcpu=%s" % board.get("build.cpu"),
        "-mthumb",
        "-mthumb-interwork",
        "-mapcs-frame",
        "-ffunction-sections",
        "-ffat-lto-objects",
        "-fno-common",
        "-fno-builtin-printf",
        "-fno-builtin-fflush",
        "-fno-builtin-sprintf",
        "-fno-builtin-snprintf",
        "-Wno-strict-aliasing",
    ],

    CXXFLAGS=[
        "-fno-exceptions",
        "-fno-rtti",
    ],

    LINKFLAGS=[
        "-Os",
        "-Wl,--gc-sections",
        "-mcpu=%s" % board.get("build.cpu"),
        "-Wl,--wrap=printf",
        "-Wl,--wrap=fflush",
        "-Wl,--wrap=sprintf",
        "-Wl,--wrap=snprintf",
        "-Wl,-Map,pio.map",
        "-mthumb",
        "-mthumb-interwork",
        "-specs=nano.specs",
        "-ffat-lto-objects"
    ],

    CPPPATH=[
        os.path.join(FRAMEWORK_DIR, "cores", core),
        os.path.join(FRAMEWORK_DIR, "cores", core, "board"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "board", "src"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "board", "inc"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "device", "asr6501_lrwan"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "device", "sx126x"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "loramac", "mac"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "loramac", "mac", "region"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "loramac", "system"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "loramac", "system", "crypto"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "port"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "port", "include"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "projects"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "projects", "PSoC4"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "cores"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "Serial"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "Wire"),
        os.path.join(FRAMEWORK_DIR, "cores", core, "SPI"),
    ],

    LIBS=[
        "stdc++",
        "m"
    ],

    LIBSOURCE_DIRS=[
        os.path.join(FRAMEWORK_DIR, "libraries")
    ]
)

env.Prepend(
    ASFLAGS=env.get("CCFLAGS", [])[:],
    _LIBFLAGS='"%s" ' % os.path.join(
        FRAMEWORK_DIR, "cores", core, "projects", "CubeCellLib.a")
)

if not board.get("build.ldscript", ""):
    env.Append(
        LIBPATH=[
            os.path.join(FRAMEWORK_DIR, "cores", core, "projects", "PSoC4"),
        ]
    )
    env.Replace(
        LDSCRIPT_PATH=board.get("build.arduino.ldscript", "cm0plusgcc.ld")
    )

#
# Configure LoRaWAN
#

lorawan_config = board.get("build.arduino.lorawan", {})
region = lorawan_config.get("region", "AS923")
debug_level = lorawan_config.get("debug_level", "NONE")

env.Append(
    CPPDEFINES=[
        "REGION_%s" % region,
        ("ACTIVE_REGION", "LORAMAC_REGION_%s" % region),
        ("LORAWAN_CLASS", lorawan_config.get("class", "CLASS_A")),
        ("LORAWAN_NETMODE", "true" if lorawan_config.get(
            "netmode", "OTAA") == "OTAA" else "false"),
        ("LORAWAN_ADR", "true" if lorawan_config.get("adr", "ON") == "ON" else "false"),
        ("LORAWAN_UPLINKMODE", "true" if lorawan_config.get(
            "uplinkmode", "CONFIRMED") == "CONFIRMED" else "false"),
        ("LORAWAN_NET_RESERVE", "true" if lorawan_config.get(
            "net_reserve", "OFF") == "ON" else "false"),
        ("AT_SUPPORT", 1 if lorawan_config.get("at_support", "ON") == "ON" else 0),
        ("LoraWan_RGB", 1 if lorawan_config.get(
            "rgb", "ACTIVE") == "ACTIVE" else 0),
        ("LoRaWAN_DEBUG_LEVEL", 2 if debug_level == "FREQ_AND_DIO" else (
            1 if debug_level == "FREQ" else 0))
    ]
)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    variants_dir = os.path.join(
        "$PROJECT_DIR", board.get("build.variants_dir")) if board.get(
            "build.variants_dir", "") else os.path.join(FRAMEWORK_DIR, "variants")
    env.Append(
        CPPPATH=[
            os.path.join(variants_dir, board.get("build.variant"))
        ]
    )
    libs.append(env.BuildLibrary(
        os.path.join("$BUILD_DIR", "FrameworkArduinoVariant"),
        os.path.join(variants_dir, board.get("build.variant"))
    ))

libs.append(env.BuildLibrary(
    os.path.join("$BUILD_DIR", "FrameworkArduino"),
    os.path.join(FRAMEWORK_DIR, "cores"),
    src_filter=[
        "+<*>",
        "-<%s/projects/PSoC4/CyBootAsmIar.s>" % core,
        "-<%s/projects/PSoC4/CyBootAsmRv.s>" % core
    ]
))

env.Prepend(LIBS=libs)
