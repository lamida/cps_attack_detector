import sys
import time
from enum import Enum


"""
State of a valve.
"""


class StateValve(Enum):
    CLOSE = 0
    OPEN = 1


"""
Valve allows water flow when it opens and stop the flow when it closes.
"""


class Valve:

    """
    Create a valve with a name and initial state. 
    """

    def __init__(self, name: str, state: StateValve = StateValve.CLOSE):
        self.name = name
        self.state = state

    """
    Check whether the valve is open.
    """

    def is_open(self) -> bool:
        return self.state == StateValve.OPEN

    """
    Check whether the valve is close.
    """

    def is_close(self) -> bool:
        return not self.is_open()

    def __change_state(self, new_state: StateValve):
        if new_state != self.state:
            print("Change Valve state", self.name, "to", new_state)
            self.state = new_state

    """
    Open the valve.
    """

    def open(self):
        self.__change_state(StateValve.OPEN)

    """
    Close the valve.
    """

    def close(self):
        self.__change_state(StateValve.CLOSE)


"""
State of a pump.
"""


class StatePump(Enum):
    OFF = 0
    ON = 1


"""
Pump will suck the water out from a tank when it is on and will do nothing when it is off.
"""


class Pump:

    """
    Create a pump using a name and an initial state.
    """

    def __init__(self, name: str, state: StatePump = StatePump.OFF):
        self.name = name
        self.state = state

    """
    Check whether the pump is on.
    """

    def is_on(self) -> bool:
        return self.state == StatePump.ON

    """
    Check whether the pump is off.
    """

    def is_off(self) -> bool:
        return not self.is_on()

    def __change_state(self, new_state: StatePump):
        if new_state != self.state:
            print("Change Pump state", self.name, "to", new_state)
            self.state = new_state

    """
    Turn on the pump.
    """

    def turn_on(self):
        self.__change_state(StatePump.ON)

    """
    Turn off the pump.
    """

    def turn_off(self):
        self.__change_state(StatePump.ON)


"""
Level sensor.
"""


class LevelSensor:

    def __init__(self, name: str, high: float, low: float):
        self.name = name
        self.high = high
        self.low = low


"""
Tank is a water container. It maintain a water level. It connects to an inlet valve and sink to a pump out. 
The water level in a tank must never goes to zero.
"""


class Tank:
    """
    Create a tank.
    """

    def __init__(self, name: str, current_level: float, level_sensor: LevelSensor, inlet_valve: Valve, pump_out: Pump):
        self.name = name
        self.current_level = current_level
        self.level_sensor = level_sensor
        self.inlet_valve = inlet_valve
        self.pump_out = pump_out

    """
    Return water change rate in the tank.

    If it is positive it means water level is rising.
    If it is negative it means water level is falling.

    speed_factor can be set to speed up the simulation. speed_factor = 1 means the water_level change
    rate will be in real actual time. speed_factor = x will speed up the simulation to the x factor.
    """

    def water_level_rate(self, speed_factor: float = 1) -> float:
        seconds_in_minute = 60
        if self.inlet_valve.is_open() and self.pump_out.is_on():
            return speed_factor * 1.11857 / seconds_in_minute
        elif self.inlet_valve.is_open() and self.pump_out.is_off():
            return speed_factor * 28.5234 / seconds_in_minute
        elif self.inlet_valve.is_close() and self.pump_out.is_on():
            return speed_factor * -27.40 / seconds_in_minute
        else:
            return 0

    """
    Update the state of tank. A speed_factor can be passed to speed up the simulation.
    """

    def update_state(self, speed_factor: float):
        new_level = self.current_level + self.water_level_rate(speed_factor)
        if new_level >= 0:
            self.current_level = new_level
        else:
            self.current_level = 0

        if new_level > self.level_sensor.high:
            print("Warning! The water is overflowing!")

        if self.current_level <= self.level_sensor.low:
            self.inlet_valve.open()
            self.pump_out.turn_off()

        if self.current_level >= self.level_sensor.high:
            self.inlet_valve.close()
            self.pump_out.turn_on()

        if self.current_level > self.level_sensor.low and self.current_level < self.level_sensor.high:
            self.inlet_valve.open()
            self.pump_out.turn_on()


class Simulator:
    def __init__(self, tick_time: float = 1, speed_factor: float = 1):
        self.p101 = Pump("P101")
        self.mv101 = Valve("MV101")
        self.lit101 = LevelSensor(name="LIT101", low=500, high=800)
        self.t101 = Tank(name="T101", current_level=600, level_sensor=self.lit101,
                         inlet_valve=self.mv101, pump_out=self.p101)
        self.tick_time = tick_time
        self.speed_factor = speed_factor

    def run(self):
        print("=========================================================================================")
        print(
            f"Running simulator with tick time: {self.tick_time} and speed factor: {self.speed_factor}")
        print("Press CTRL + C or CTRL + Z to stop")
        print("=========================================================================================")
        print()
        c = 0
        while(True):
            self.t101.update_state(self.speed_factor)
            print("Tank water level:", self.t101.current_level)
            time.sleep(self.tick_time)


if __name__ == "__main__":
    simulator = Simulator(tick_time=1, speed_factor=500)
    simulator.run()
