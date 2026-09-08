"""
===============================================================
Industrial I/O HAT
2AI + 2AO + 4DI + 4DO Test & Demonstration Program
===============================================================

Description:
------------
This program demonstrates the operation of the Industrial I/O HAT
using a Raspberry Pi.

I/O Configuration:
------------------
Analog Inputs:
    AI1 -> ADS1015 AIN0
    AI2 -> ADS1015 AIN1
    Input type: 4-20 mA
    Shunt resistor: 249 ohm

Analog Outputs:
    AO1 -> MCP4728 Channel A
    AO2 -> MCP4728 Channel B
    Output range: 0-10 V
    Test sequence: 0 V -> 10 V -> 0 V
    Step size: 1 V
    Step interval: 2 seconds

Digital Inputs:
    DI1 -> GPIO5
    DI2 -> GPIO6
    DI3 -> GPIO16
    DI4 -> GPIO26

    Input logic:
        LOW  = ON
        HIGH = OFF

Digital Outputs:
    DO1 -> GPIO22
    DO2 -> GPIO23
    DO3 -> GPIO24
    DO4 -> GPIO25

    Output sequence:
        DO1 -> DO2 -> DO3 -> DO4
    Each output remains ON for 2 seconds.

I2C Devices:
------------
    ADS1015  -> Address 0x48
    MCP4728  -> Address 0x60

Analog Output Calibration:
--------------------------
The MCP4728 is configured using its internal 2.048 V reference
with gain = 2, giving an approximately 0-4.096 V DAC output.

The external AO amplifier stage is calibrated so that the complete
AO output stage produces approximately 0-10 V.

Calibration is based on the measured hardware transfer:

    DAC full-scale  = 4.095 V
    AO full-scale   = 10.42 V

The software uses this measured transfer to calculate the DAC
value required for the requested 0-10 V output.

Terminal Display:
-----------------
The display is continuously refreshed in a fixed terminal position
so that the output does not continuously scroll.

Safety:
-------
On program termination:
    - All digital outputs are switched OFF.
    - Both analog outputs are returned to 0 V.
    - GPIO pins are cleaned up.

===============================================================
"""

import time
import board
import busio
import RPi.GPIO as GPIO

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15 import ads1x15
from adafruit_ads1x15.analog_in import AnalogIn

import adafruit_mcp4728


# ===============================================================
# GPIO CONFIGURATION
# ===============================================================

# Digital Outputs
DO1 = 22
DO2 = 23
DO3 = 24
DO4 = 25

DO_PINS = {
    "DO1": DO1,
    "DO2": DO2,
    "DO3": DO3,
    "DO4": DO4,
}


# Digital Inputs
DI1 = 5
DI2 = 6
DI3 = 16
DI4 = 26

DI_PINS = {
    "DI1": DI1,
    "DI2": DI2,
    "DI3": DI3,
    "DI4": DI4,
}


# ===============================================================
# HARDWARE CONSTANTS
# ===============================================================

ADS1015_ADDRESS = 0x48
MCP4728_ADDRESS = 0x60

AI_SHUNT_RESISTOR = 249.0


# ===============================================================
# AO CALIBRATION
# ===============================================================

# Measured MCP4728 maximum output
DAC_FULL_SCALE = 4.095

# Measured complete AO stage maximum output
AO_FULL_SCALE = 10.42

# Calculated measured gain of complete AO stage
AO_GAIN = AO_FULL_SCALE / DAC_FULL_SCALE


# ===============================================================
# AO TEST PARAMETERS
# ===============================================================

AO_MIN_VOLTAGE = 0
AO_MAX_VOLTAGE = 10
AO_STEP_VOLTAGE = 1

AO_STEP_TIME = 2.0


# ===============================================================
# DO TEST PARAMETERS
# ===============================================================

DO_STEP_TIME = 2.0

DO_SEQUENCE = [
    "DO1",
    "DO2",
    "DO3",
    "DO4",
]


# ===============================================================
# INITIALIZE GPIO
# ===============================================================

GPIO.setmode(GPIO.BCM)

# Digital outputs
for pin in DO_PINS.values():
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

# Digital inputs
for pin in DI_PINS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# ===============================================================
# INITIALIZE I2C
# ===============================================================

i2c = busio.I2C(
    board.SCL,
    board.SDA
)


# ===============================================================
# INITIALIZE ADS1015
# ===============================================================

ads = ADS.ADS1015(
    i2c,
    address=ADS1015_ADDRESS
)

# Gain = 2/3 gives ±6.144 V input range
# Suitable for approximately 0-4.98 V generated
# by the 4-20 mA / 249 ohm input circuit.
ads.gain = 2 / 3

AI1 = AnalogIn(
    ads,
    ads1x15.Pin.A0
)

AI2 = AnalogIn(
    ads,
    ads1x15.Pin.A1
)


# ===============================================================
# INITIALIZE MCP4728
# ===============================================================

dac = adafruit_mcp4728.MCP4728(
    i2c,
    address=MCP4728_ADDRESS
)


# Configure channels for internal 2.048 V reference
# with gain = 2.
#
# DAC output range:
# approximately 0 V to 4.096 V
#
# This matches the measured hardware behavior.

dac.channel_a.vref = adafruit_mcp4728.Vref.INTERNAL
dac.channel_a.gain = 2

dac.channel_b.vref = adafruit_mcp4728.Vref.INTERNAL
dac.channel_b.gain = 2


# ===============================================================
# FUNCTIONS
# ===============================================================

def set_all_digital_outputs_off():
    """Switch all digital outputs OFF."""
    
    for pin in DO_PINS.values():
        GPIO.output(pin, GPIO.LOW)


def set_digital_output(output_name):
    """
    Switch ON the selected digital output.
    All other digital outputs remain OFF.
    """

    set_all_digital_outputs_off()

    GPIO.output(
        DO_PINS[output_name],
        GPIO.HIGH
    )


def set_analog_output(channel, voltage):
    """
    Set the requested 0-10 V analog output.

    The MCP4728 generates approximately 0-4.095 V.
    The external analog output stage is calibrated using
    the measured DAC-to-AO transfer.
    """

    # Limit requested voltage
    voltage = max(
        AO_MIN_VOLTAGE,
        min(AO_MAX_VOLTAGE, voltage)
    )

    # Calculate required DAC voltage
    required_dac_voltage = voltage / AO_GAIN

    # Convert DAC voltage to 12-bit DAC code
    raw_value = round(
        (required_dac_voltage / DAC_FULL_SCALE) * 4095
    )

    # Safety limits
    raw_value = max(
        0,
        min(4095, raw_value)
    )

    if channel == "AO1":
        dac.channel_a.raw_value = raw_value

    elif channel == "AO2":
        dac.channel_b.raw_value = raw_value


def set_both_analog_outputs(voltage):
    """Set AO1 and AO2 to the same requested voltage."""

    set_analog_output(
        "AO1",
        voltage
    )

    set_analog_output(
        "AO2",
        voltage
    )


def read_analog_inputs():
    """Read both analog inputs and convert voltage to current."""

    ai1_voltage = AI1.voltage
    ai2_voltage = AI2.voltage

    # I = V / R
    ai1_current = (
        ai1_voltage / AI_SHUNT_RESISTOR
    ) * 1000.0

    ai2_current = (
        ai2_voltage / AI_SHUNT_RESISTOR
    ) * 1000.0

    return (
        ai1_voltage,
        ai1_current,
        ai2_voltage,
        ai2_current
    )


def read_digital_inputs():
    """Read all digital inputs."""

    states = {}

    for name, pin in DI_PINS.items():

        # LOW = ON
        states[name] = (
            GPIO.input(pin) == GPIO.LOW
        )

    return states


def get_do_states():
    """Read current digital output states."""

    states = {}

    for name, pin in DO_PINS.items():

        states[name] = (
            GPIO.input(pin) == GPIO.HIGH
        )

    return states


def display_status(
    ao_voltage,
    active_do,
    ai_data,
    di_states
):
    """Display all I/O information."""

    (
        ai1_voltage,
        ai1_current,
        ai2_voltage,
        ai2_current
    ) = ai_data

    # Clear terminal and move cursor to top
    print(
        "\033[2J\033[H",
        end=""
    )

    print("=" * 62)
    print("              INDUSTRIAL I/O HAT")
    print("          2AI + 2AO + 4DI + 4DO")
    print("=" * 62)

    print()
    print("ANALOG INPUTS")
    print("-" * 62)

    print(
        f"AI1 : {ai1_voltage:7.3f} V    "
        f"{ai1_current:7.2f} mA"
    )

    print(
        f"AI2 : {ai2_voltage:7.3f} V    "
        f"{ai2_current:7.2f} mA"
    )

    print()
    print("ANALOG OUTPUTS")
    print("-" * 62)

    print(
        f"AO1 : {ao_voltage:7.2f} V"
    )

    print(
        f"AO2 : {ao_voltage:7.2f} V"
    )

    print()
    print("DIGITAL INPUTS")
    print("-" * 62)

    for name in DI_PINS:

        state = "ON " if di_states[name] else "OFF"

        print(
            f"{name} : {state}"
        )

    print()
    print("DIGITAL OUTPUTS")
    print("-" * 62)

    for name in DO_PINS:

        state = "ON " if name == active_do else "OFF"

        print(
            f"{name} : {state}"
        )

    print()
    print("-" * 62)

    print(
        f"AO Test Voltage : {ao_voltage:5.1f} V"
    )

    print(
        f"Active DO       : {active_do}"
    )

    print("-" * 62)

    print()
    print(
        "AO sequence: 0 V -> 10 V -> 0 V"
    )

    print(
        "DO sequence: DO1 -> DO2 -> DO3 -> DO4"
    )

    print()
    print("Press Ctrl+C to stop.")


# ===============================================================
# MAIN PROGRAM
# ===============================================================

try:

    # Start with everything OFF
    set_all_digital_outputs_off()

    set_both_analog_outputs(
        0
    )

    # AO sequence:
    #
    # 0,1,2,...,10,9,8,...,0
    #
    ao_sequence = (
        list(
            range(
                AO_MIN_VOLTAGE,
                AO_MAX_VOLTAGE + 1,
                AO_STEP_VOLTAGE
            )
        )
        +
        list(
            range(
                AO_MAX_VOLTAGE - AO_STEP_VOLTAGE,
                AO_MIN_VOLTAGE - 1,
                -AO_STEP_VOLTAGE
            )
        )
    )

    ao_index = 0
    do_index = 0

    current_ao_voltage = ao_sequence[ao_index]
    current_do = DO_SEQUENCE[do_index]

    set_both_analog_outputs(
        current_ao_voltage
    )

    set_digital_output(
        current_do
    )

    next_ao_update = time.monotonic()
    next_do_update = time.monotonic()

    while True:

        now = time.monotonic()

        # -------------------------------------------------------
        # Update AO
        # -------------------------------------------------------

        if now >= next_ao_update:

            current_ao_voltage = (
                ao_sequence[ao_index]
            )

            set_both_analog_outputs(
                current_ao_voltage
            )

            ao_index += 1

            if ao_index >= len(ao_sequence):
                ao_index = 0

            next_ao_update += AO_STEP_TIME

        # -------------------------------------------------------
        # Update DO
        # -------------------------------------------------------

        if now >= next_do_update:

            current_do = DO_SEQUENCE[do_index]

            set_digital_output(
                current_do
            )

            do_index += 1

            if do_index >= len(DO_SEQUENCE):
                do_index = 0

            next_do_update += DO_STEP_TIME

        # -------------------------------------------------------
        # Read inputs
        # -------------------------------------------------------

        ai_data = read_analog_inputs()

        di_states = read_digital_inputs()

        # -------------------------------------------------------
        # Display
        # -------------------------------------------------------

        display_status(
            current_ao_voltage,
            current_do,
            ai_data,
            di_states
        )

        # Small delay to prevent excessive CPU usage
        time.sleep(0.1)


# ===============================================================
# SAFE SHUTDOWN
# ===============================================================

except KeyboardInterrupt:

    print("\n\nStopping program...")


except Exception as error:

    print(
        f"\n\nERROR: {error}"
    )


finally:

    # Switch all digital outputs OFF
    set_all_digital_outputs_off()

    # Return both analog outputs to 0 V
    try:
        dac.channel_a.raw_value = 0
        dac.channel_b.raw_value = 0
    except Exception:
        pass

    # Release GPIO
    GPIO.cleanup()

    print(
        "All outputs switched OFF."
    )

    print(
        "GPIO cleanup completed."
    )