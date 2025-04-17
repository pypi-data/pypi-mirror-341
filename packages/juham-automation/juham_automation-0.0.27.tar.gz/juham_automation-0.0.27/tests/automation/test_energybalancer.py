import unittest
from typing import List, Any
from juham_automation.automation.energybalancer import EnergyBalancer
from juham_core.timeutils import (
    quantize,
    timestamp,
    timestamp_hour,
    timestampstr,
    is_hour_within_schedule,
    timestamp_hour_local,
)
from masterpiece.mqtt import MqttMsg
from juham_automation.automation.heatingoptimizer import HeatingOptimizer


class SimpleMqttMsg(MqttMsg):
    def __init__(self, topic: str, payload: Any):
        self._topic = topic
        self._payload = payload

    @property
    def payload(self) -> Any:
        return self._payload

    @payload.setter
    def payload(self, value: Any) -> None:
        self._payload = value

    @property
    def topic(self) -> str:
        return self._topic

    @topic.setter
    def topic(self, value: str) -> None:
        self._topic = value


class TestEnergyBalancing(unittest.TestCase):

    balancing_interval: int = EnergyBalancer.energy_balancing_interval
    power: int = 3000  # Power of the radiator (in watts )

    def setUp(self) -> None:
        self.optimizer = EnergyBalancer("test_optimizer")
        self.optimizer.radiator_power = 3000  # Set the radiator power

    def test_initial_state(self) -> None:
        self.assertEqual(
            self.optimizer.net_energy_balance, 0, "Initial energy balance should be 0"
        )
        self.assertEqual(
            self.balancing_interval, self.optimizer.energy_balancing_interval
        )
        self.assertFalse(self.optimizer.net_energy_balancing_mode)

        self.assertEqual(
            self.optimizer.needed_energy, self.balancing_interval * self.power
        )

        #  time within the interval should be zero
        self.assertEqual(-1, self.optimizer.net_energy_balance_ts)

    def test_set_power(self) -> None:
        """Test setting power consumption and check if the energy balance is updated."""
        step: int = 60
        for ts in range(0, self.balancing_interval, step):
            self.optimizer.update_energy_balance(self.power, ts)
            self.assertEqual(ts * self.power, self.optimizer.net_energy_balance)
            self.assertEqual(ts, self.optimizer.net_energy_balance_ts)

        self.optimizer.update_energy_balance(self.power, ts + step)
        self.assertEqual(0, self.optimizer.net_energy_balance)

    def test_consider_net_energy_balance(self) -> None:
        """Test case to simulate passing time and check energy balancing behavior.
        Pass power consumption self.power, which should switch the heating on just
        in the middle of the interval."""

        balancing_interval: int = self.balancing_interval
        energy: float = 0
        step: int = balancing_interval // 10
        for ts in range(0, self.balancing_interval, step):
            energy = self.power * ts  # in watt-seconds
            self.optimizer.update_energy_balance(self.power, ts)

            # make sure the optimizer is in the right state
            self.assertEqual(energy, self.optimizer.net_energy_balance)

            # Call the method to check if balancing mode should be activated
            heating_on: bool = self.optimizer.consider_net_energy_balance(ts)

            # Calculate the remaining energy needed to power the radiator for the rest of the time slot
            remaining_time: float = self.optimizer.energy_balancing_interval - ts
            required_energy: float = self.optimizer.radiator_power * remaining_time

            # Check if heating was enabled or not based on energy balance
            if energy >= required_energy and remaining_time > 0:
                self.assertTrue(heating_on, f"At time {ts}, heating should be ON")
            else:
                self.assertFalse(heating_on, f"At time {ts}, heating should be OFF")

            # Ensure heating state is correct
            if energy >= required_energy and remaining_time > 0:
                self.assertTrue(self.optimizer.net_energy_balancing_mode)
            else:
                self.assertFalse(self.optimizer.net_energy_balancing_mode)

        # Step 2: Testing energy balancing reset at the end of the interval
        # self.optimizer.net_energy_balance = 0  # Reset energy before boundary test
        self.optimizer.update_energy_balance(self.power, self.balancing_interval)
        heating_on = self.optimizer.consider_net_energy_balance(ts)
        self.assertFalse(heating_on, "Heating should be OFF after interval reset")
        self.assertEqual(
            self.optimizer.net_energy_balance,
            0,
            "Energy balance should be reset to 0 at the end of the interval",
        )
        self.assertFalse(
            self.optimizer.net_energy_balancing_mode,
            "Balancing mode should be OFF after interval reset",
        )

        # Step 3: Testing activation when energy is sufficient
        self.optimizer.update_energy_balance(
            self.power * 1800, self.balancing_interval // 10
        )

        ts = 3600 + 60  # Start of a new interval
        heating_on = self.optimizer.consider_net_energy_balance(ts)
        self.assertTrue(
            heating_on, "Heating should be ON when enough energy is available"
        )
        self.assertTrue(
            self.optimizer.net_energy_balancing_mode,
            "Balancing mode should be ON when enough energy is available",
        )

    def test_consider_net_energy_balance_start_middle(self) -> None:
        """Start from the middle of the interval."""

        balancing_interval: int = self.balancing_interval
        energy: float = 0
        step: int = balancing_interval // 10
        for ts in range(self.balancing_interval // 2, self.balancing_interval, step):

            self.optimizer.update_energy_balance(self.power, ts)

            # make sure the optimizer is in the right state
            self.assertEqual(energy, self.optimizer.net_energy_balance)

            # Call the method to check if balancing mode should be activated
            heating_on: bool = self.optimizer.consider_net_energy_balance(ts)

            # Calculate the remaining energy needed to power the radiator for the rest of the time slot
            remaining_time: float = self.optimizer.energy_balancing_interval - ts
            required_energy: float = self.optimizer.radiator_power * remaining_time

            # Check if heating was enabled or not based on energy balance
            if energy >= required_energy and remaining_time > 0:
                self.assertTrue(heating_on, f"At time {ts}, heating should be ON")
            else:
                self.assertFalse(heating_on, f"At time {ts}, heating should be OFF")

            # Ensure heating state is correct
            if energy >= required_energy and remaining_time > 0:
                self.assertTrue(self.optimizer.net_energy_balancing_mode)
            else:
                self.assertFalse(self.optimizer.net_energy_balancing_mode)
            energy = energy + self.power * step  # in watt-seconds

    def test_quantization(self) -> None:
        """Test that timestamps are quantized to the interval boundaries correctly."""
        test_times: List[int] = [3601, 7200, 10800]  # Slightly over boundaries
        for ts in test_times:
            quantized_ts = quantize(self.optimizer.energy_balancing_interval, ts)
            expected_quantized_ts = (
                ts // self.optimizer.energy_balancing_interval
            ) * self.optimizer.energy_balancing_interval
            self.assertEqual(
                quantized_ts,
                expected_quantized_ts,
                f"Timestamp {ts} should be quantized to {expected_quantized_ts}",
            )
