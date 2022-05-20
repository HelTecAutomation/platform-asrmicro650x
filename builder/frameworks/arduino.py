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
mcu = board.get("build.mcu", "")
is_asr6601 = mcu.startswith("asr6601")
arch = "asr6601" if is_asr6601 else "asr650x"

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinoasrmicro")
CORE_DIR = os.path.join(FRAMEWORK_DIR, "cores", core)
assert os.path.isdir(FRAMEWORK_DIR)

env.Append(
    ASPPFLAGS=["-x", "assembler-with-cpp"],

    CPPDEFINES=[
        ("ARDUINO", 10815),
        "ARDUINO_ARCH_%s" % arch.upper(),
        "__%s__" % mcu.upper(),
        "__%s__" % arch,
        ("CONFIG_MANUFACTURER", '\\"ASR\\"'),
        ("CONFIG_DEVICE_MODEL", '\\"%s\\"' % mcu),
        ("CONFIG_VERSION", '\\"v4.0\\"'),
        ("CY_CORE_ID", 0),
        "CONFIG_LORA_USE_TCXO",
        ("F_CPU", "$BOARD_F_CPU"),
        "SOFT_SE",
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
        "-fdata-sections",
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
        "-mthumb",
        "-mthumb-interwork",
        "-specs=nano.specs",
        "-specs=nosys.specs",
        "-ffat-lto-objects",
    ],
    LIBS=["stdc++", "m"],
    LIBSOURCE_DIRS=[os.path.join(FRAMEWORK_DIR, "libraries")],
)

env.Prepend(
    _LIBFLAGS='"%s" '
    % (
        os.path.join(CORE_DIR, "asr6601.a")
        if is_asr6601
        else os.path.join(CORE_DIR, "projects", "CubeCellLib.a")
    ),
)

if is_asr6601:
    env.Append(
        CPPPATH=[
            CORE_DIR,
            os.path.join(CORE_DIR, "drivers", "peripheral", "inc"),
            os.path.join(CORE_DIR, "drivers", "crypto", "inc"),
            os.path.join(CORE_DIR, "platform", "CMSIS"),
            os.path.join(CORE_DIR, "platform", "system"),
            os.path.join(CORE_DIR, "lora", "driver"),
            os.path.join(CORE_DIR, "lora", "radio"),
            os.path.join(CORE_DIR, "lora"),
            os.path.join(CORE_DIR, "lora", "radio", "sx126x"),
            os.path.join(CORE_DIR, "lora", "system"),
            os.path.join(CORE_DIR, "lora", "system", "crypto"),
            os.path.join(CORE_DIR, "base"),
            os.path.join(CORE_DIR, "peripheral"),
        ],
    )
else:
    env.Append(
        CPPPATH=[
            CORE_DIR,
            os.path.join(CORE_DIR, "board"),
            os.path.join(CORE_DIR, "board", "src"),
            os.path.join(CORE_DIR, "board", "inc"),
            os.path.join(CORE_DIR, "device", "sx126x"),
            os.path.join(CORE_DIR, "lora"),
            os.path.join(CORE_DIR, "lora", "system"),
            os.path.join(CORE_DIR, "lora", "system", "crypto"),
            os.path.join(CORE_DIR, "port"),
            os.path.join(CORE_DIR, "port", "include"),
            os.path.join(CORE_DIR, "projects"),
            os.path.join(CORE_DIR, "projects", "PSoC4"),
            os.path.join(CORE_DIR, "cores"),
            os.path.join(CORE_DIR, "Serial"),
            os.path.join(CORE_DIR, "Wire"),
            os.path.join(CORE_DIR, "SPI"),
        ],
    )


if not board.get("build.ldscript", ""):
    env.Append(
        LIBPATH=[
            CORE_DIR if is_asr6601 else os.path.join(CORE_DIR, "projects", "PSoC4"),
        ]
    )
    env.Replace(
        LDSCRIPT_PATH=board.get(
            "build.arduino.ldscript", "gcc.ld" if is_asr6601 else "cm0plusgcc.ld"
        )
    )

#
# Configure LoRaWAN
#

lorawan_config = board.get("build.arduino.lorawan", {})
region = lorawan_config.get("region", "US915")
debug_level = lorawan_config.get("debug_level", "NONE")

env.Append(
    CPPDEFINES=[
        "REGION_%s" % region,
        ("ACTIVE_REGION", "LORAMAC_REGION_%s" % region),
        ("LORAWAN_CLASS", lorawan_config.get("class", "CLASS_A")),
        (
            "LORAWAN_NETMODE",
            "true" if lorawan_config.get("netmode", "OTAA") == "OTAA" else "false",
        ),
        ("LORAWAN_ADR", "true" if lorawan_config.get("adr", "ON") == "ON" else "false"),
        (
            "LORAWAN_UPLINKMODE",
            "true"
            if lorawan_config.get("uplinkmode", "CONFIRMED") == "CONFIRMED"
            else "false",
        ),
        (
            "LORAWAN_NET_RESERVE",
            "true" if lorawan_config.get("net_reserve", "OFF") == "ON" else "false",
        ),
        ("AT_SUPPORT", 1 if lorawan_config.get("at_support", "ON") == "ON" else 0),
        (
            "LORAWAN_DEVEUI_AUTO",
            0 if lorawan_config.get("deveui", "CUSTOM") == "CUSTOM" else 1,
        ),
        ("LoraWan_RGB", 1 if lorawan_config.get("rgb", "ACTIVE") == "ACTIVE" else 0),
        ("LORAWAN_PREAMBLE_LENGTH", lorawan_config.get("preamble_length", 8)),
        (
            "LoRaWAN_DEBUG_LEVEL",
            2 if debug_level == "FREQ_AND_DIO" else (1 if debug_level == "FREQ" else 0),
        ),
    ]
)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in board:
    variants_dir = (
        os.path.join("$PROJECT_DIR", board.get("build.variants_dir"))
        if board.get("build.variants_dir", "")
        else os.path.join(FRAMEWORK_DIR, "variants")
    )
    env.Append(CPPPATH=[os.path.join(variants_dir, board.get("build.variant"))])
    libs.append(
        env.BuildLibrary(
            os.path.join("$BUILD_DIR", "FrameworkArduinoVariant"),
            os.path.join(variants_dir, board.get("build.variant")),
        )
    )

libs.append(
    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "FrameworkArduino"),
        CORE_DIR,
        # Only applicable to ASR6501
        src_filter=[
            "+<*>",
            "-<projects/PSoC4/CyBootAsmIar.s>",
            "-<projects/PSoC4/CyBootAsmRv.s>",
        ],
    )
)

env.Prepend(LIBS=libs)

# Duplicate preprocessor flags to the assembler
# for '.S', '.spp', '.SPP', '.sx' source files
env.Append(ASPPFLAGS=env.get("CCFLAGS", []))
