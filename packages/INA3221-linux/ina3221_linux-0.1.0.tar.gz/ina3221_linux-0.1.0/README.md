[![PyPI - Downloads](https://img.shields.io/pypi/dm/LoRaRF)](https://pypi.org/project/LoRaRF/)
[![PyPI](https://img.shields.io/pypi/v/LoRaRF)](https://pypi.org/project/LoRaRF/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/chandrawi/INA3221_linux/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/chandrawi/INA3221_linux.svg)](https://github.com/chandrawi/INA3221_linux/issues)
[![GitHub release](https://img.shields.io/github/release/chandrawi/INA3221_linux.svg?maxAge=3600)](https://github.com/chandrawi/INA3221_linux/releases)

# INA3221

Python library for the INA3221 3-channel voltage and current sensor that works on linux OS using I2C or SMBus interface.


## Description

**Experimental** **USE WITH CARE**

The INA3221 is a 3 channel voltage and current sensor, which work with I2C or SMBus interface. The INA3221 monitors both shunt voltage drops and bus supply voltages, in addition to having programmable conversion times and averaging modes for these signals. The INA3221 offers both critical and warning alerts to detect multiple programmable out-of-range conditions for each channel.

The INA3221 performs two measurements on up to three power supplies of interest. The voltage developed from the load current passing through a shunt resistor creates a shunt voltage that is measured between the IN+ and IN– pins. The device also measures the power-supply bus voltage at the IN– pin with respect to ground for each channel.

The device has two operating modes, continuous and single-shot (triggered). In continuous mode, the device continues to cycle through all enabled channels until a new configuration setting is programmed. In single-shot mode, setting any single-shot convert mode to the configuration register triggers a single-shot conversion.

Some important maximum ratings are follows, see datasheet for all details.

|  description  |  max   |  unit  |  notes  |
|:--------------|-------:|-------:|:--------|
| channels      |     3  |        |  |
| bus voltage   |    26  |   Volt |  unclear for how long |
| shunt voltage |   163  |  mVolt |  at 0.1 Ohm |
| shunt R       |   100  |   mOhm |  typical |
| current       |  1.63  | Ampere |  I = V/R |


### Tests

Still experimental so use with care.

The library is only tested partially with an Orange Pi 3B and Raspberry Pi 4B.
So not all functionality is tested and verified with hardware yet. 
This is an ongoing process.

One point of attention to be tested and verified is the behaviour 
around negative values in registers.

As always feedback is welcome, please open an issue on GitHub.


### Installation

### Using pip

Using terminal run following command.
```sh
pip3 install INA3221_linux
```

### Using Git and Build Package

To using latest update of the library, you can clone then build python package manually. Using this method require **build** module.
```sh
git clone https://github.com/chandrawi/INA3221_linux
cd INA3221_linux
python3 -m build
pip3 install dist/INA3221_linux-0.0.1-py3-none-any.whl
```

### Enabling I2C Interface

Before using the library, I2C interface must be enabled. For Raspberry pi OS, this is done by set I2C interface enable using raspi-config or edit **/boot/config.txt** by adding following line.
```txt
dtparam=i2c_arm=on
```


### Related

- https://www.ti.com/product/INA3221#tech-docs
- https://www.ti.com/product/INA3221#params
- https://www.ti.com/document-viewer/INA3221/datasheet
- https://github.com/RobTillaart/INA219  26 Volt, I2C, 12 bit
- https://github.com/RobTillaart/INA226  36 Volt, I2C, 16 bit
- https://github.com/RobTillaart/INA228  85 Volt, I2C, 20 bit
- https://github.com/RobTillaart/INA236  48 Volt, I2C, 16 bit
- https://github.com/RobTillaart/INA239  85 Volt, SPI, 16 bit
- https://github.com/RobTillaart/INA3221_RT  26 Volt, I2C, 13 bits (3 channel)
- https://github.com/chandrawi/INA3221_linux  26 Volt, I2C, 13 bits (3 channel)
- https://www.adafruit.com/product/5832
- https://www.mateksys.com/?portfolio=i2c-ina-bm
- https://github.com/RobTillaart/printHelpers  (for scientific notation)



## I2C

### Address

The INA3221 sensor can have 4 different I2C addresses, depending on how
the A0 address line is connected, to the SCL, SDA, GND or VCC pin.

|  A0   |  DEC  |  HEX   |  Notes  |
|:-----:|:-----:|:------:|:-------:|
|  GND  |   64  |  0x40  |  A0 not connected seems to choose this one too. |
|  VS   |   65  |  0x41  |  |
|  SDA  |   66  |  0x42  |  |
|  SCL  |   67  |  0x43  |  |

See datasheet - table 1 + page 20


## Interface

```python
from INA3221_linux import INA3221
```

All parameters channels are zero based => so numbered 0 , 1 or 2.
Using channels > 2 are not handled (correctly).

### Constructor

- **INA3221(address, bus)** Constructor to set the address and optional SMBus number or path (ex. "/dev/i2c-1").
- **begin()** initializes the class.
Returns true if the INA3221 address is valid and on the I2C bus.
- **is_connected()** returns true if the INA3221 address is valid and on the I2C bus.
- **get_address()** returns the I2C address set in the constructor.


### Core Functions

Note the power and the current are not meaningful without calibrating the sensor.
Also the value is not meaningful if there is no shunt connected.

The parameter **channel** should always be 0..2. 
The functions return -1 if channel is out of range.

- **get_bus_voltage(channel)** idem. in volts. Max 26 Volt.
- **get_shunt_voltage(channel)** idem, in volts.
- **get_current(channel)** is the current through the shunt in Ampere.
- **get_power(channel)** is the current x BusVoltage in Watt.

The library has wrapper functions to convert above output to a more appropriate scale of units.

Wrapper functions for the milli scale.

- **get_bus_voltage_mv(channel)** idem, in milliVolts.
- **get_shunt_voltage_mv(channel)** idem, in milliVolts.
- **get_current_ma(channel)** idem, in milliAmpere.
- **get_power_mw(channel)** idem, in milliWatt.

Wrapper functions for the micro scale.

- **get_bus_voltage_uv(channel)** idem, in microVolts.
- **get_shunt_voltage_uv(channel)** idem, in microVolts.
- **get_current_ua(channel)** idem, in microAmpere.
- **get_power_uw(channel)** idem, in microWatt.


### Shunt Resistor

The shunt resistor is typical in the order of 0.100 Ohm.

- **set_shunt_resistor(channel, ohm)** sets value in Ohm.
- **get_shunt_resistor(channel)** returns value in Ohm.


### Shunt Alerts, warning and critical

(not tested)
Read datasheet!

The user is responsible to be sure that the critical value >= warning value
if he decides to use both.
If only one of the two is used, critical might be less than warning.

The parameter **channel** should always be 0..2
The parameter **microVolt** should not exceed 163800 µV, will return error -2.
NOTE: LSB = 40 uV so microVolt should be >= 40uV

- **set_critical_alert(channel, microVolt)**
sets the critical alert level in microvolts.
- **get_critical_alert(channel)** returns microVolt
- **set_warning_alert(channel, uint32_t microVolt)**
sets the warning alert level in microvolts.
- **get_warning_alert(channel)** returns microVolt

Wrappers using milliAmpere (assuming Shunt is set correctly!).
These are often more intuitive from user perspective.
NOTE: LSB = 40 uV so milliAmpere should be >= 0.4 mA (assume Shunt = 0.1 Ohm)

- **set_critical_current(channel, milliAmpere)**
sets the critical alert level in milliAmpere.
- **get_critical_current(channel)** returns milliAmpere
- **set_warning_current(channel, milliAmpere)**
sets the warning alert level in milliAmpere.
- **get_warning_current(channel)** returns milliAmpere


### Shunt voltage sum

(not tested)
Read datasheet!

- **get_shunt_voltage_sum()** returns microVolt
- **set_shunt_voltage_sum_limit(microVolt)** idem.
- **get_shunt_voltage_sum_limit()** returns set value in microVolt.


### Configuration

(partially tested)
Read datasheet for bit pattern of the mask.

Setting all bits at once with a mask is faster, atomic and uses less code.

- **set_configuration(mask = 0x7127)**  0x7127 = power on default.
- **get_configuration()** returns bit mask.

The library also provides getters and setters per field.

- **reset()** triggers software power on reset.
- **enable_channel(channel)** add a channel to the background measurements loop.
- **disable_channel(channel)** remove a channel to the background measurements loop.
- **get_enable_channel(channel)** check if a channel is enabled.


### Average

Datasheet, section 8.4.1

The average does not make multiple measurements and then return the average, 
one should think of it as a low pass filter that reduces noise.

in code:
```cpp
value = value + (measurement - value) * (1/samples);

e.g. (1/samples) == (1/128) 
```

The higher the average number of samples the less noise you have. 
Higher values for average cause the measurements take more time to stabilize.
Therefor it reacts slower on changes in voltage and current. 
So choose the level of averaging with care.


- **set_average(avg = 0)** see table below.
(avg 0 = default ==> 1 read)
  - return 0 is OK.
  - return -10 if parameter > 7.
  - other is I2C error.
- **get_average()** returns the value set. See table below.
Note this is not the count of samples.


| Average | # samples | Constant     |  notes  |
|:-------:|----------:|:-------------|:-------:|
|    0    |       1   | AVERAGE_1    | default |
|    1    |       4   | AVERAGE_4    |  |
|    2    |      16   | AVERAGE_16   |  |
|    3    |      64   | AVERAGE_64   |  |
|    4    |     128   | AVERAGE_128  |  |
|    5    |     256   | AVERAGE_256  |  |
|    6    |     512   | AVERAGE_512  |  |
|    7    |    1024   | AVERAGE_1024 |  |


### Conversion time

- **set_bus_voltage_conversion_time(bvct = 4)** see table below.
(4 = default ==> 1.1 ms), 
  - return 0 is OK.
  - return -10 if parameter > 7.
  - other is I2C error.
- **get_bus_voltage_conversion_time()** return the value set 0..7.
See table below. Note the value returned is not a unit of time.
- **set_shunt_voltage_conversion_time(svct = 4)** see table below.
(4 = default ==> 1.1 ms), 
  - return 0 is OK.
  - return -10 if parameter > 7.
  - other is I2C error.
- **get_shunt_voltage_conversion_time()** return the value set 0..7.
Note the value returned is not a unit of time.


| BVCT SVCT |   time    | Constant    |  notes  |
|:---------:|:---------:|:------------|:-------:|
|    0      |  140 us   | TIME_140_US |  |
|    1      |  204 us   | TIME_204_US |  |
|    2      |  332 us   | TIME_332_US |  |
|    3      |  588 us   | TIME_588_US |  |
|    4      |  1.1 ms   | TIME_1_1_MS | default |
|    5      |  2.116 ms | TIME_2_1_MS |  |
|    6      |  4.156 ms | TIME_4_2_MS |  |
|    7      |  8.244 ms | TIME_8_2_MS |  |

Note: times are typical, check datasheet for operational range.
The maximum time can be up to ~10% higher than typical!


### Operating mode

(not tested)
See datasheet!

- **setMode(mode = 7)** mode = 0..7. see table below. Default = 7 ==> ShuntBusContinuous mode.
  - return 0 is OK.
  - return -10 if parameter > 7.
  - other is I2C error.
- **getMode()** returns the mode (0..7). see table below.

| Mode  | Description                | Constant              |  notes  |
|:-----:|:---------------------------|:----------------------|:-------:|
|   0   | Power-down                 | MODE_POWER_DOWN       | default |
|   1   | Shunt voltage, single-shot | MODE_SHUNT_SINGLE     |  |
|   2   | Bus voltage, single-shot   | MODE_BUS_SINGLE       |  |
|   3   | Shunt and bus, single-shot | MODE_ALL_SINGLE       |  |
|   4   | Power-down                 |                       |  |
|   5   | Shunt voltage, continuous  | MODE_SHUNT_CONTINUOUS |  |
|   6   | Bus voltage, continuous    | MODE_BUS_CONTINUOUS   |  |
|   7   | Shunt and bus, continuous  | MODE_ALL_CONTINUOUS   |  |

Descriptive mode functions (convenience wrappers).
These have the same return value as **setMode()**.

- **shutDown()** mode 0
- **setModeShuntTrigger()** mode 1
- **setModeBusTrigger()** mode 2
- **setModeShuntBusTrigger()** mode 3
- **setModeShuntContinuous()** mode 5
- **setModeBusContinuous()** mode 6
- **setModeShuntBusContinuous()** mode 7 - default - (only one tested)


### Mask / enable register

(not tested)
See datasheet!

Setting all bits at once with a mask is faster, atomic and uses less code.

- **set_mask_enable(mask)** (0..14). see table below.
  - return 0 is OK.
  - other is I2C error.
- **get_mask_enable()** (0..14). see table below.

|  bit  | Description               | Constant   |
|:-----:|:--------------------------|:-----------|
|   0   | Conversion-ready flag     | MASK_CVRF  |
|   1   | Timing-control-alert flag | MASK_TCF   |
|   2   | Power-valid-alert flag    | MASK_PVF   |
|   3   | Warning-alert flag 0      | MASK_WF_0  |
|   4   | Warning-alert flag 1      | MASK_WF_1  |
|   5   | Warning-alert flag 2      | MASK_WF_2  |
|   6   | Summation-alert flag      | MASK_SF    |
|   7   | Critical-alert flag 0     | MASK_CF_0  |
|   8   | Critical-alert flag 1     | MASK_CF_1  |
|   9   | Critical-alert flag 2     | MASK_CF_2  |
|  10   |Critical alert latch enable| MASK_CEN   |
|  11   |Warning alert latch enable | MASK_WEN   |
|  12   |Summation channel control 0| MASK_SCC_0 |
|  13   |Summation channel control 1| MASK_SCC_1 |
|  14   |Summation channel control 2| MASK_SCC_2 |
|  15   | Reserved                  |            |

### Power Limit

(not tested)
See datasheet!

To guard the BUS voltage, max value 32760

- **set_power_upper_limit(milliVolt)**
  - return 0 is OK.
  - other is I2C error.
- **get_power_upper_limit()** returns limit in mV.
- **set_power_lower_limit(milliVolt)**
  - return 0 is OK.
  - other is I2C error.
- **get_power_lower_limit()** returns limit in mV.


### Meta information

(tested)

- **get_manufacturer_id()** should return 0x5449, mine returns 0x5449.
- **get_die_id()** should return 0x2260, mine returns 0x3220.

If your device returns other ManufacturerID or DieID, please let me know.


### Debugging

- **_read_register(reg)** fetch registers directly, for debugging only.
- **_write_register(reg, value)** load registers directly, for debugging only.


### Error Handling

- **get_last_error()** returns last (I2C) error.


## Future


#### Must

- update documentation.
  - return values
- test all functionality
  - negative values = two complements - does it work?


#### Should

- keep in sync with INA219/226 where possible.
- do error codes conflict with results (negative numbers). 
  - getBusVoltage() returns -1 to indicate channel error.
    would be a problem if VBus can be < 0. Others idem.
- error handling
  - parameter error
  - I2C error
  - documentation

#### Could

- convenience wrappers MASK/ENABLE register.
  - 9 x getters  9 x setters (quite a lot)
- clean up magic numbers in the code (e.g. 40 uV and 8 mV)
  - comments?


#### Won't


## Support

If you appreciate my libraries, you can support the development and maintenance.
Improve the quality of the libraries by providing issues and Pull Requests, or
donate through PayPal or GitHub sponsors.

Thank you,
