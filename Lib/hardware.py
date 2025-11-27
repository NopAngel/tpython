import ctypes
import os
import fcntl
import struct
import mmap
import array

class Hardware:
    def __init__(self):
        self._mem_fd = None
        self._mem_map = None
        
    def init(self):
        try:
            self._mem_fd = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
            return True
        except:
            return False
            
    def map_physical_memory(self, phys_addr, size=4096):
        if not self._mem_fd:
            return None
            
        offset = phys_addr & ~(4096 - 1)
        page_offset = phys_addr - offset
        
        try:
            self._mem_map = mmap.mmap(
                self._mem_fd, 
                size + page_offset,
                mmap.MAP_SHARED,
                mmap.PROT_READ | mmap.PROT_WRITE,
                offset=offset
            )
            return self._mem_map[page_offset:page_offset + size]
        except:
            return None
            
    def port_inb(self, port):
        libc = ctypes.CDLL("libc.so.6")
        result = libc.ioperm(port, 1, 1)
        if result == 0:
            libc = ctypes.CDLL(None)
            return libc.inb(port)
        return 0
        
    def port_outb(self, port, value):
        libc = ctypes.CDLL("libc.so.6")
        result = libc.ioperm(port, 1, 1)
        if result == 0:
            libc = ctypes.CDLL(None)
            libc.outb(value, port)
            return True
        return False
        
    def i2c_read(self, bus, address, register, length):
        try:
            import smbus
            bus_obj = smbus.SMBus(bus)
            data = []
            for i in range(length):
                data.append(bus_obj.read_byte_data(address, register + i))
            return bytes(data)
        except:
            return bytes([0xFF] * length)
            
    def i2c_write(self, bus, address, register, data):
        try:
            import smbus
            bus_obj = smbus.SMBus(bus)
            for i, byte in enumerate(data):
                bus_obj.write_byte_data(address, register + i, byte)
            return True
        except:
            return False
            
    def gpio_setup(self, pin, direction):
        try:
            export_path = f"/sys/class/gpio/gpio{pin}"
            if not os.path.exists(export_path):
                with open("/sys/class/gpio/export", "w") as f:
                    f.write(str(pin))
            
            with open(f"{export_path}/direction", "w") as f:
                f.write("out" if direction else "in")
            return True
        except:
            return False
            
    def gpio_write(self, pin, value):
        try:
            with open(f"/sys/class/gpio/gpio{pin}/value", "w") as f:
                f.write("1" if value else "0")
            return True
        except:
            return False
            
    def gpio_read(self, pin):
        try:
            with open(f"/sys/class/gpio/gpio{pin}/value", "r") as f:
                return int(f.read().strip())
        except:
            return 0
            
    def spi_transfer(self, bus, data):
        try:
            with open(f"/dev/spidev{bus}.0", "wb") as spi:
                spi.write(data)
                return True
        except:
            return False
            
    def pwm_set(self, chip, channel, duty_cycle, period):
        try:
            pwm_path = f"/sys/class/pwm/pwmchip{chip}/pwm{channel}"
            
            if not os.path.exists(pwm_path):
                with open(f"/sys/class/pwm/pwmchip{chip}/export", "w") as f:
                    f.write(str(channel))
            
            with open(f"{pwm_path}/period", "w") as f:
                f.write(str(period))
                
            with open(f"{pwm_path}/duty_cycle", "w") as f:
                f.write(str(duty_cycle))
                
            with open(f"{pwm_path}/enable", "w") as f:
                f.write("1")
                
            return True
        except:
            return False
            
    def read_temp(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return int(f.read().strip()) / 1000.0
        except:
            return 0.0
            
    def read_voltage(self):
        try:
            with open("/sys/class/power_supply/BAT0/voltage_now", "r") as f:
                return int(f.read().strip()) / 1000000.0
        except:
            return 0.0
            
    def beep(self, frequency=1000, duration=100):
        try:
            os.system(f"play -n synth {duration/1000} sin {frequency} >/dev/null 2>&1")
            return True
        except:
            return False
            
    def led_control(self, led, state):
        leds = {
            "caps": "/sys/class/leds/input0::capslock/brightness",
            "num": "/sys/class/leds/input0::numlock/brightness", 
            "scroll": "/sys/class/leds/input0::scrolllock/brightness"
        }
        
        if led in leds and os.path.exists(leds[led]):
            try:
                with open(leds[led], "w") as f:
                    f.write("1" if state else "0")
                return True
            except:
                pass
        return False
        
    def read_accelerometer(self):
        try:
            with open("/sys/bus/iio/devices/iio:device0/in_accel_x_raw", "r") as f:
                x = int(f.read().strip())
            with open("/sys/bus/iio/devices/iio:device0/in_accel_y_raw", "r") as f:
                y = int(f.read().strip())
            with open("/sys/bus/iio/devices/iio:device0/in_accel_z_raw", "r") as f:
                z = int(f.read().strip())
            return (x, y, z)
        except:
            return (0, 0, 0)
