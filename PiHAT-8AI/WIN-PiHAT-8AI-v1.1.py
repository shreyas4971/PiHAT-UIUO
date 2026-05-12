import spidev
import smbus2
import time

# --- Calibration Constants ---
# The RAW register value the ADC produces at exactly 20mA (5V)
CALIBRATED_MAX_RAW = 26560 

# ===== SPI Setup (MCP3208 - 12-bit) =====
spi = spidev.SpiDev()
spi.open(0, 1)  # CE1
spi.max_speed_hz = 1350000

def read_12bit_spi(ch_index):
    """Proper 3-byte transfer to read all 12 bits (0-4095)"""
    # Byte 0: Start bit (1), SGL (1), D2 
    byte0 = 0x06 | ((ch_index >> 2) & 0x01)
    # Byte 1: D1, D0, followed by 0s
    byte1 = (ch_index & 0x03) << 6
    # Byte 2: 0x00 (padding to keep clock running)
    cmd = [byte0, byte1, 0x00]
    
    r = spi.xfer2(cmd)
    
    # Extract the 12 bits: lower 4 bits of r[1] and all 8 bits of r[2]
    return ((r[1] & 0x0F) << 8) | r[2]

# ===== I2C Setup (ADS1115 - 16-bit) =====
bus = smbus2.SMBus(1)

def read_16bit_i2c(addr, ch):
    """Reads and maps raw voltage to 0-65535"""
    mux = (0x4 + ch) << 12
    # Config: ±6.144V Range (000 PGA), Single-Shot, 128 SPS
    config = 0x8183 | mux 
    
    try:
        bus.write_i2c_block_data(addr, 0x01, [(config >> 8) & 0xFF, config & 0xFF])
        time.sleep(0.01)
        data = bus.read_i2c_block_data(addr, 0x00, 2)
        
        raw_reg = (data[0] << 8) | data[1]
        
        # Convert to signed 
        signed_val = raw_reg
        if signed_val > 32767: 
            signed_val -= 65536
        
        # Map directly using the RAW expected value
        if signed_val <= 0:
            unsigned_mapped = 0
        else:
            unsigned_mapped = (signed_val / CALIBRATED_MAX_RAW) * 65535
            
        return max(0, min(65535, int(unsigned_mapped)))
    except OSError:
        return "ERROR"

# ===== MAIN EXECUTION LOOP =====
try:
    while True:
        print("\033c", end="") # Clear terminal
        print(f"{'Channel':<10} | {'16-bit (0-65535)':<18} | {'12-bit (0-4095)'}")
        print("-" * 50)
        
        for ai_ch in range(1, 9):
            # Address logic: U2 (0x48) for AI 1-4, U3 (0x49) for AI 5-8
            i2c_addr = 0x48 if ai_ch <= 4 else 0x49
            i2c_internal_ch = (ai_ch - 1) % 4
            
            # Fetch values
            i2c_val = read_16bit_i2c(i2c_addr, i2c_internal_ch)
            spi_val = read_12bit_spi(ai_ch - 1)
            
            # Format and print
            print(f"AI {ai_ch:<7} | {str(i2c_val):<18} | {spi_val}")
            
            # Visual separator between U2 and U3
            if ai_ch == 4:
                print("-" * 50)
                
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nDiagnostic safely stopped. Closing buses.")
    bus.close()
    spi.close()