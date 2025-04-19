import smbus2


class INA3221:

    # Registers
    CONFIGURATION = 0x00
    SHUNT_VOLTAGE = lambda self, x: 0x01 + (x * 2)
    BUS_VOLTAGE = lambda self, x: 0x02 + (x * 2)
    CRITICAL_ALERT = lambda self, x: 0x07 + (x * 2)
    WARNING_ALERT = lambda self, x: 0x08 + (x * 2)
    SHUNT_VOLTAGE_SUM = 0x0D
    SHUNT_VOLTAGE_LIMIT = 0x0E
    MASK_ENABLE = 0x0F
    POWER_VALID_UPPER = 0x10
    POWER_VALID_LOWER = 0x11
    MANUFACTURER = 0xFE
    DIE_ID = 0xFF

    AVERAGE_1 = 0x00
    AVERAGE_4 = 0x01
    AVERAGE_16 = 0x02
    AVERAGE_64 = 0x03
    AVERAGE_128 = 0x04
    AVERAGE_256 = 0x05
    AVERAGE_512 = 0x06
    AVERAGE_1024 = 0x07

    TIME_140_US = 0x00
    TIME_204_US = 0x01
    TIME_332_US = 0x02
    TIME_588_US = 0x03
    TIME_1_1_MS = 0x04
    TIME_2_1_MS = 0x05
    TIME_4_2_MS = 0x06
    TIME_8_2_MS = 0x07

    MODE_POWER_DOWN = 0x00
    MODE_SHUNT_SINGLE = 0x01
    MODE_BUS_SINGLE = 0x02
    MODE_ALL_SINGLE = 0x03
    MODE_SHUNT_CONTINUOUS = 0x05
    MODE_BUS_CONTINUOUS = 0x06
    MODE_ALL_CONTINUOUS = 0x07

    MASK_CVRF = 0x0000
    MASK_TCF = 0x0002
    MASK_PVF = 0x0004
    MASK_WF_0 = 0x0008
    MASK_WF_1 = 0x0010
    MASK_WF_2 = 0x0020
    MASK_SF = 0x0040
    MASK_CF_0 = 0x0080
    MASK_CF_1 = 0x0100
    MASK_CF_2 = 0x0200
    MASK_CEN = 0x0400
    MASK_WEN = 0x0800
    MASK_SCC_0 = 0x1000
    MASK_SCC_1 = 0x2000
    MASK_SCC_2 = 0x4000

    def __init__(self, address=0x40, bus=1):
        self._address = address
        self._bus = bus
        self._smbus = smbus2.SMBus()
        self._shunt = [0.1, 0.1, 0.1]  # Ohms
        self._error = 0

    def begin(self):
        self._smbus.open(self._bus)
        return self.is_connected()

    def end(self):
        self._smbus.close()

    def is_connected(self):
        if not 0x40 <= self._address <= 0x43:
            return False
        try:
            self._smbus.read_byte(self._address)
            return True
        except:
            return False

    def get_address(self):
        return self._address

    def get_bus_voltage(self, channel):
        if channel > 2:
            return -1
        value = self._read_register(self.BUS_VOLTAGE(channel))
        return (value >> 3) * 8.0e-3

    def get_shunt_voltage(self, channel):
        if channel > 2:
            return -1
        value = self._read_register(self.SHUNT_VOLTAGE(channel))
        return self._to_signed(value >> 3) * 40e-6

    def get_current(self, channel):
        if channel > 2:
            return -1
        return self.get_shunt_voltage(channel) / self._shunt[channel]

    def get_power(self, channel):
        if channel > 2:
            return -1
        return self.get_bus_voltage(channel) * self.get_current(channel)

    def get_bus_voltage_mv(self, channel):
        return self.get_bus_voltage(channel) * 1000

    def get_shunt_voltage_mv(self, channel):
        return self.get_shunt_voltage(channel) * 1000

    def get_current_ma(self, channel):
        return self.get_current(channel) * 1000

    def get_power_mw(self, channel):
        return self.get_power(channel) * 1000

    def get_bus_voltage_uv(self, channel):
        return self.get_bus_voltage(channel) * 1000000

    def get_shunt_voltage_uv(self, channel):
        return self.get_shunt_voltage(channel) * 1000000

    def get_current_ua(self, channel):
        return self.get_current(channel) * 1000000

    def get_power_uw(self, channel):
        return self.get_power(channel) * 1000000

    def set_shunt_resistor(self, channel, ohm):
        if channel > 2:
            return -1
        self._shunt[channel] = ohm
        return 0

    def get_shunt_resistor(self, channel):
        if channel > 2:
            return -1
        return self._shunt[channel]

    def set_critical_alert(self, channel, microvolt):
        if channel > 2 or microvolt > 163800:
            return -1
        value = (microvolt // 40) << 3
        return self._write_register(self.CRITICAL_ALERT(channel), value)

    def get_critical_alert(self, channel):
        if channel > 2:
            return -1
        value = self._read_register(self.CRITICAL_ALERT(channel))
        return (value >> 3) * 40

    def set_warning_alert(self, channel, microvolt):
        if channel > 2 or microvolt > 163800:
            return -1
        value = (microvolt // 40) << 3
        return self._write_register(self.WARNING_ALERT(channel), value)

    def get_warning_alert(self, channel):
        if channel > 2:
            return -1
        value = self._read_register(self.WARNING_ALERT(channel))
        return (value >> 3) * 40

    def set_critical_current(self, channel, milliamp):
        return self.set_critical_alert(channel, int(1000.0 * milliamp * self._shunt[channel]))

    def get_critical_current(self, channel):
        return self.get_critical_alert(channel) * 0.001 / self._shunt[channel]

    def set_warning_current(self, channel, milliamp):
        return self.set_warning_alert(channel, int(1000.0 * milliamp * self._shunt[channel]))

    def get_warning_current(self, channel):
        return self.get_warning_alert(channel) * 0.001 / self._shunt[channel]

    def get_shunt_voltage_sum(self):
        value = self._read_register(self.SHUNT_VOLTAGE_SUM)
        return self._to_signed(value >> 1) * 40

    def set_shunt_voltage_sum_limit(self, microvolt):
        if abs(microvolt) > (16383 * 40):
            return -10
        value = (microvolt // 40) << 1
        return self._write_register(self.SHUNT_VOLTAGE_LIMIT, value)

    def get_shunt_voltage_sum_limit(self):
        value = self._read_register(self.SHUNT_VOLTAGE_LIMIT)
        return self._to_signed(value >> 1) * 40

    def set_configuration(self, mask):
        return self._write_register(self.CONFIGURATION, mask)

    def get_configuration(self):
        return self._read_register(self.CONFIGURATION)

    def reset(self):
        return self._write_register(self.CONFIGURATION, 0xF127)

    def enable_channel(self, channel):
        if channel > 2:
            return -1
        mask = self._read_register(self.CONFIGURATION)
        mask |= (1 << (14 - channel))
        return self._write_register(self.CONFIGURATION, mask)

    def disable_channel(self, channel):
        if channel > 2:
            return -1
        mask = self._read_register(self.CONFIGURATION)
        mask &= ~(1 << (14 - channel))
        return self._write_register(self.CONFIGURATION, mask)

    def get_enable_channel(self, channel):
        if channel > 2:
            return -1
        mask = self._read_register(self.CONFIGURATION)
        return (mask & (1 << (14 - channel))) > 0

    def set_average(self, avg):
        if avg > 7:
            return -10
        mask = self._read_register(self.CONFIGURATION)
        mask = (mask & ~(7 << 9)) | (avg << 9)
        return self._write_register(self.CONFIGURATION, mask)

    def get_average(self):
        mask = self._read_register(self.CONFIGURATION)
        return (mask >> 9) & 7

    def set_bus_voltage_conversion_time(self, bvct):
        if bvct > 7:
            return -10
        mask = self._read_register(self.CONFIGURATION)
        mask = (mask & ~(7 << 6)) | (bvct << 6)
        return self._write_register(self.CONFIGURATION, mask)

    def get_bus_voltage_conversion_time(self):
        mask = self._read_register(self.CONFIGURATION)
        return (mask >> 6) & 7

    def set_shunt_voltage_conversion_time(self, svct):
        if svct > 7:
            return -10
        mask = self._read_register(self.CONFIGURATION)
        mask = (mask & ~(7 << 3)) | (svct << 3)
        return self._write_register(self.CONFIGURATION, mask)

    def get_shunt_voltage_conversion_time(self):
        mask = self._read_register(self.CONFIGURATION)
        return (mask >> 3) & 7

    def set_mode(self, mode):
        if mode > 7:
            return -10
        mask = self._read_register(self.CONFIGURATION)
        mask = (mask & ~7) | mode
        return self._write_register(self.CONFIGURATION, mask)

    def get_mode(self):
        mask = self._read_register(self.CONFIGURATION)
        return mask & 7

    def shutdown(self):
        return self.set_mode(0)

    def set_mode_shunt_trigger(self):
        return self.set_mode(1)

    def set_mode_bus_trigger(self):
        return self.set_mode(2)

    def set_mode_shunt_bus_trigger(self):
        return self.set_mode(3)

    def set_mode_shunt_continuous(self):
        return self.set_mode(5)

    def set_mode_bus_continuous(self):
        return self.set_mode(6)

    def set_mode_shunt_bus_continuous(self):
        return self.set_mode(7)

    def set_mask_enable(self, mask):
        return self._write_register(self.MASK_ENABLE, mask)

    def get_mask_enable(self):
        return self._read_register(self.MASK_ENABLE)

    def set_power_upper_limit(self, millivolt):
        value = millivolt & 0xFFF8
        return self._write_register(self.POWER_VALID_UPPER, value)

    def get_power_upper_limit(self):
        return self._read_register(self.POWER_VALID_UPPER)

    def set_power_lower_limit(self, millivolt):
        value = millivolt & 0xFFF8
        return self._write_register(self.POWER_VALID_LOWER, value)

    def get_power_lower_limit(self):
        return self._read_register(self.POWER_VALID_LOWER)

    def get_manufacturer_id(self):
        return self._read_register(self.MANUFACTURER)

    def get_die_id(self):
        return self._read_register(self.DIE_ID)

    def get_last_error(self):
        e = self._error
        self._error = 0
        return e

    def _read_register(self, reg):
        try:
            data = self._smbus.read_i2c_block_data(self._address, reg, 2)
            return (data[0] << 8) | data[1]
        except:
            self._error = -1
            return 0

    def _write_register(self, reg, value):
        try:
            self._smbus.write_i2c_block_data(self._address, reg, [(value >> 8) & 0xFF, value & 0xFF])
            return 0
        except:
            self._error = -1
            return -1

    def _to_signed(self, val):
        if val & 0x1000:
            return val - 0x2000
        return val
