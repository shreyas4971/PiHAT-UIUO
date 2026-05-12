import time

# -------- I2C SETUP (MCP4728) --------
import smbus
bus = smbus.SMBus(1)

DAC1 = 0x60
DAC2 = 0x61

def write_i2c(addr, ch, value):
    value &= 0xFFF # 12-bit
    cmd = 0x40 | (ch << 1)
    high = (value >> 8) & 0x0F
    low = value & 0xFF
    bus.write_i2c_block_data(addr, cmd, [high, low])

# -------- SPI SETUP (DAC8564) --------
import spidev

spi0 = spidev.SpiDev()
spi1 = spidev.SpiDev()

spi0.open(0, 0) # DAC1 (AO1–AO4)
spi1.open(0, 1) # DAC2 (AO5–AO8)

spi0.max_speed_hz = 1000000
spi1.max_speed_hz = 1000000

spi0.mode = 1
spi1.mode = 1

def write_spi(spi, ch, value):
    value &= 0xFFFF # 16-bit
    cmd = 0x30 | (ch << 1)
    data = [cmd, (value >> 8) & 0xFF, value & 0xFF]
    spi.xfer2(data)

# -------- MAIN LOOP --------

while True:

    #  UP RAMP
    for step in range(0, 11): # 0 to 10 steps

        # Map step to DAC values
        v16 = int((step / 10) * 65535) # SPI
        v12 = int((step / 10) * 4095) # I2C

        print(f"Step {step} → Voltage Level")

        # --- I2C (12-bit DACs) ---
        for ch in range(4):
            write_i2c(DAC1, ch, v12)
            write_i2c(DAC2, ch, v12)

        # --- SPI (16-bit DACs) ---
        for ch in range(4):
            write_spi(spi0, ch, v16)
            write_spi(spi1, ch, v16)

        time.sleep(1)

    #  DOWN RAMP
    for step in range(10, -1, -1):

        v16 = int((step / 10) * 65535)
        v12 = int((step / 10) * 4095)

        print(f"Step {step} → Voltage Level")

        for ch in range(4):
            write_i2c(DAC1, ch, v12)
            write_i2c(DAC2, ch, v12)

        for ch in range(4):
            write_spi(spi0, ch, v16)
            write_spi(spi1, ch, v16)

        time.sleep(1)
