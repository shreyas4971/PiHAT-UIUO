import time
import spidev

# =========================================================
# UNIVERSAL CALIBRATION VARIABLES (Adjust these anytime!)
# =========================================================

ACTUAL_5V_RAIL = 5.04  

OPAMP_GAIN = 2.0
SYSTEM_MAX_VOLTS = ACTUAL_5V_RAIL * OPAMP_GAIN

# =========================================================
# SPI SETUP
# =========================================================
# U5: TPC112S8 (12-bit, 8-Channel) connected to CE0
spi0 = spidev.SpiDev()
spi0.open(0, 0)
spi0.max_speed_hz = 1000000
spi0.mode = 1

# U6: TPC116S8 (16-bit, 8-Channel) connected to CE1
spi1 = spidev.SpiDev()
spi1.open(0, 1)
spi1.max_speed_hz = 1000000
spi1.mode = 1

# =========================================================
# DAC WRITE FUNCTIONS
# =========================================================

def write_tpc112s8(spi, ch, target_volts):
    """
    Writes to the 12-bit TPC112S8.
    Requires a 16-bit frame: [A2, A1, A0, PD, D11...D0]
    """
    # Clamp voltage to physical limits
    if target_volts > SYSTEM_MAX_VOLTS:
        target_volts = SYSTEM_MAX_VOLTS
    if target_volts < 0:
        target_volts = 0

    # Calculate 12-bit value (0-4095)
    val_12bit = int((target_volts / SYSTEM_MAX_VOLTS) * 4095)

    # Pack into 2 bytes
    # Byte 0: 3 bits channel, 1 bit PD (0), 4 highest bits of data
    byte0 = (ch << 5) | ((val_12bit >> 8) & 0x0F)
    # Byte 1: 8 lowest bits of data
    byte1 = val_12bit & 0xFF

    spi.xfer2([byte0, byte1])


def write_tpc116s8(spi, ch, target_volts):
    """
    Writes to the 16-bit TPC116S8.
    Requires a 24-bit frame: [X, X, X, X, A2, A1, A0, PD, D15...D0]
    """
    # Clamp voltage to physical limits
    if target_volts > SYSTEM_MAX_VOLTS:
        target_volts = SYSTEM_MAX_VOLTS
    if target_volts < 0:
        target_volts = 0

    # Calculate 16-bit value (0-65535)
    val_16bit = int((target_volts / SYSTEM_MAX_VOLTS) * 65535)

    # Pack into 3 bytes
    # Byte 0: 4 dummy bits (0), 3 bits channel, 1 bit PD (0)
    byte0 = (ch << 1)
    # Byte 1: 8 highest bits of data
    byte1 = (val_16bit >> 8) & 0xFF
    # Byte 2: 8 lowest bits of data
    byte2 = val_16bit & 0xFF

    spi.xfer2([byte0, byte1, byte2])

# =========================================================
# MAIN LOOP
# =========================================================

print("Starting V2.0 SPI Analog Output Sequence...")
print(f"Calibrated Max Output Ceiling: {SYSTEM_MAX_VOLTS:.2f}V")

try:
    while True:
        
        # --- UP RAMP (0V to 10V) ---
        for step in range(0, 11): 
            target_v = step * 1.0 # 0.0V, 1.0V, 2.0V ... 10.0V
            
            print(f"Ramping UP: Setting all 16 channels to {target_v:.1f}V")
            
            # Loop through all 8 channels (0 to 7) on both chips
            for ch in range(8):
                write_tpc112s8(spi0, ch, target_v) # Update U5 (12-bit)
                write_tpc116s8(spi1, ch, target_v) # Update U6 (16-bit)
                
            time.sleep(1)

        # --- DOWN RAMP (10V to 0V) ---
        for step in range(10, -1, -1):
            target_v = step * 1.0
            
            print(f"Ramping DOWN: Setting all 16 channels to {target_v:.1f}V")
            
            for ch in range(8):
                write_tpc112s8(spi0, ch, target_v)
                write_tpc116s8(spi1, ch, target_v)
                
            time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram interrupted by user. Shutting down DACs to 0V...")
    # Safe shutdown: Set all channels back to 0V before exiting
    for ch in range(8):
        write_tpc112s8(spi0, ch, 0.0)
        write_tpc116s8(spi1, ch, 0.0)
    spi0.close()
    spi1.close()
    print("Cleanup complete.")
