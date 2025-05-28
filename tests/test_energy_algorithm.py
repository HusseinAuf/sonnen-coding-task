import pytest


@pytest.fixture(autouse=True)
def reset_dut(dut):
    dut.set("pv", None)
    dut.set("house", None)
    dut.set("storage", None)

    yield
    
    dut.set("pv", None)
    dut.set("house", None)
    dut.set("storage", None)

# --- Helpers ---
def set_photovoltaics(dut, power=5000, voltage=250):
    current = round(power / voltage, 2)
    dut.set("pv.power", power)
    dut.set("pv.voltage", voltage)
    dut.set("pv.current", current)

def set_house(dut, power=2000, voltage=230, frequency=50):
    current = round(power / voltage, 2)
    dut.set("house.power", power)
    dut.set("house.voltage", voltage)
    dut.set("house.frequency", frequency)
    dut.set("house.current", current)

def set_inverter(dut, power=1500, voltage=48, grid_voltage=230, grid_frequency=50):
    current = round(power / voltage, 2)
    dut.set("storage.inverter.max_power", 3000)
    dut.set("storage.inverter.battery_voltage", voltage)
    dut.set("storage.inverter.battery_current", current)
    dut.set("storage.inverter.power", power)
    dut.set("storage.inverter.grid_voltage", grid_voltage)
    dut.set("storage.inverter.grid_frequency", grid_frequency)

def set_storage_system_type(dut, batteries_count):
    batteries_types = {
        1: "basic",
        2: "standard",
        3: "pro",
    }
    dut.set("storage.system", batteries_types[batteries_count])

def set_batteries(dut, count=3, voltage=48, temperature=30, max_power=2000):
    set_storage_system_type(dut, count)
    for i in range(count):
        dut.set(f"storage.battery[{i}].voltage", voltage)
        dut.set(f"storage.battery[{i}].temperature", temperature)
        dut.set(f"storage.battery[{i}].max_power", max_power)

# --- Tests ---
def test_pv_exceeds_house_consumption_and_storage_not_full(dut):
    set_photovoltaics(dut, 5000) # power 5000 W
    set_house(dut, 2000) # power 2000 W
    
    set_inverter(dut)
    set_batteries(dut)
    
    # Trigger something (e.g. controller) to get the updated storage_power_command and grid_power
    # assuming storage is not full

    storage_power_command = float(dut.get("storage.power_command"))
    grid_power = float(dut.get("grid.power"))
    assert storage_power_command > 0, (
        f"Expected charging mode with positive storage command, "
        f"but got {storage_power_command} W"
    )
    assert grid_power == 0, f"Expected grid power to be 0 (no import/export), but got {grid_power} W"

def test_pv_exceeds_house_consumption_and_storage_full(dut):
    set_photovoltaics(dut, 5000) # power 5000 W
    set_house(dut, 2000) # power 2000 W
    
    set_inverter(dut)
    set_batteries(dut)
    
    # Trigger something (e.g. controller) to get the updated storage_power_command and grid_power
    # assuming storage is full

    storage_power_command = float(dut.get("storage.power_command"))
    grid_power = float(dut.get("grid.power"))
    assert storage_power_command == 0, (
        f"Expected storage power command to be 0 (no charge/discharge), "
        f"but got {storage_power_command} W"
    )
    assert grid_power > 0, f"Expected importing power to grid with positive value, but got {grid_power} W"

def test_house_consumption_exceeds_pv_and_storage_not_empty(dut):
    set_photovoltaics(dut, 1000) # power 1000 W
    set_house(dut, 2000) # power 2000 W
    
    set_inverter(dut)
    set_batteries(dut)
    
    # Trigger something (e.g. controller) to get the updated storage_power_command and grid_power
    # assuming storage is not empty

    storage_power_command = float(dut.get("storage.power_command"))
    grid_power = float(dut.get("grid.power"))
    assert storage_power_command < 0, (
        f"Expected discharging mode with negative storage command, "
        f"but got {storage_power_command} W"
    )
    assert grid_power == 0, f"Expected grid power to be 0 (no import/export), but got {grid_power} W"

def test_house_consumption_exceeds_pv_and_storage_empty(dut):
    set_photovoltaics(dut, 1000) # power 1000 W
    set_house(dut, 2000) # power 2000 W
    
    set_inverter(dut)
    set_batteries(dut)
    
    # Trigger something (e.g. controller) to get the updated storage_power_command and grid_power
    # assuming storage is empty

    storage_power_command = float(dut.get("storage.power_command"))
    grid_power = float(dut.get("grid.power"))
    assert storage_power_command == 0, (
        f"Expected discharging mode with negative storage command, "
        f"but got {storage_power_command} W"
    )
    assert grid_power < 0, f"Expected exporting power from grid with negative value, but got {grid_power} W"