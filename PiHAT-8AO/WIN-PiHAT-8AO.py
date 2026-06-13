"""
8-Channel Selectable Isolated Analog Output Board - Calibration & Test Script
Supports: 
- TPC112S8 (12-bit, 8-Channel SPI DAC)
- TPC116S8 (16-bit, 8-Channel SPI DAC)

This script drives a 0V to 10V ramp across all 8 channels simultaneously.
It includes a universal calibration multiplier to compensate for physical 
hardware tolerances (e.g., protection diode drops and Op-Amp scaling).
"""

import time
import spidev

# =========================================================
# UNIVERSAL CALIBRATION VARIABLES 
# =========================================================
# To calibrate: Measure the voltage on the DAC VREFIN pin (after any 
# protection diodes) and enter it below. The software will automatically 
# scale the 12-bit and 16-bit math to output perfect voltages.
ACTUAL_5V_RAIL = 5.25

# Hardware multiplier (Op-Amp gain stage)
OPAMP_GAIN = 2.0 

# The theoretical maximum voltage the hardware can output
SYSTEM_MAX_VOLTS = ACTUAL_5V_RAIL * OPAMP_GAIN 

# =========================================================
# SPI BUS SETUP
# =========================================================
# Initialize SPI for TPC112S8 (Connected to SPI CE0)
spi0 = spidev.SpiDev()
spi0.open(0, 0)
spi0.max_speed_hz = 1000000
spi0.mode = 1

# Initialize SPI for TPC116S8 (Connected to SPI CE1)
spi1 = spidev.SpiDev()
spi1.open(0, 1)
spi1.max_speed_hz = 1000000
spi1.mode = 1

# =========================================================
# DAC WRITE FUNCTIONS
# =========================================================

def write_tpc112s8(spi, ch, target_volts):
    """
    Translates a target voltage into a 12-bit SPI command for the TPC112S8.
    Requires a 16-bit data frame: [A2, A1, A0, PD, D11...D0]
    """
    # Clamp voltage to prevent hardware limits overflow
    if target_volts > SYSTEM_MAX_VOLTS:
        target_volts = SYSTEM_MAX_VOLTS
    if target_volts < 0:
        target_volts = 0

    # Calculate 12-bit hex value (0-4095)
    val_12bit = int((target_volts / SYSTEM_MAX_VOLTS) * 4095)

    # Pack bits into 2 bytes for SPI transfer
    # Byte 0: 3 bits for channel address, 1 bit for Power Down (0), 4 highest bits of data
    byte0 = (ch << 5) | ((val_12bit >> 8) & 0x0F)
    # Byte 1: 8 lowest bits of data
    byte1 = val_12bit & 0xFF

    spi.xfer2([byte0, byte1])


def write_tpc116s8(spi, ch, target_volts):
    """
    Translates a target voltage into a 16-bit SPI command for the TPC116S8.
    Requires a 24-bit data frame: [X, X, X, X, A2, A1, A0, PD, D15...D0]
    """
    # Clamp voltage to prevent hardware limits overflow
    if target_volts > SYSTEM_MAX_VOLTS:
        target_volts = SYSTEM_MAX_VOLTS
    if target_volts < 0:
        target_volts = 0

    # Calculate 16-bit hex value (0-65535)
    val_16bit = int((target_volts / SYSTEM_MAX_VOLTS) * 65535)

    # Pack bits into 3 bytes for SPI transfer
    # Byte 0: 4 dummy bits (0), 3 bits for channel address, 1 bit for Power Down (0)
    byte0 = (ch << 1)
    # Byte 1: 8 highest bits of data
    byte1 = (val_16bit >> 8) & 0xFF
    # Byte 2: 8 lowest bits of data
    byte2 = val_16bit & 0xFF

    spi.xfer2([byte0, byte1, byte2])

# =========================================================
# MAIN EXECUTION LOOP
# =========================================================

if __name__ == "__main__":
    print("Starting V2.0 SPI Analog Output Sequence...")
    print(f"Calibrated Max Output Ceiling: {SYSTEM_MAX_VOLTS:.2f}V\n")

    try:
        while True:
            
            # --- UP RAMP TEST (0V to 10V) ---
            # Steps output by 1.0V increments and holds for multimeter verification
            for step in range(0, 11): 
                target_v = step * 1.0 
                
                print(f"Ramping UP: Setting all 8 channels to {target_v:.1f}V")
                
                # Iterate through all 8 channels on both DACs
                for ch in range(8):
                    write_tpc112s8(spi0, ch, target_v) # Update U5
                    write_tpc116s8(spi1, ch, target_v) # Update U6
                    
                time.sleep(3) 

            # --- DOWN RAMP TEST (10V to 0V) ---
            for step in range(10, -1, -1):
                target_v = step * 1.0
                
                print(f"Ramping DOWN: Setting all 8 channels to {target_v:.1f}V")
                
                for ch in range(8):
                    write_tpc112s8(spi0, ch, target_v)
                    write_tpc116s8(spi1, ch, target_v)
                    
                time.sleep(3) 

    except KeyboardInterrupt:
        # --- SAFE SHUTDOWN PROCEDURE ---
        print("\nProgram interrupted by user. Shutting down DACs to 0V...")
        for ch in range(8):
            write_tpc112s8(spi0, ch, 0.0)
            write_tpc116s8(spi1, ch, 0.0)
        
        spi0.close()
        spi1.close()
        print("Hardware safely disabled. Cleanup complete.")
