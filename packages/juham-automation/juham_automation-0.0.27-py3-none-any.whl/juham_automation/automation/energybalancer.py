import json
from typing import Any, Dict
from typing_extensions import override

from juham_core import Juham, timestamp
from juham_core.timeutils import timestampstr, quantize
from masterpiece import MqttMsg


class EnergyBalancer(Juham):
    """The energy balancer monitors the balance between produced and consumed energy
    within the balancing interval to determine if there is enough energy available for
    a given energy-consuming device, such as heating radiators, to operate within the
    remaining time of the interval.

    Any number of energy-consuming devices can be connected to the energy balancer.
    The energy balancer is typically used in conjunction with a power meter that reads
    the total power consumption of the house. The energy balancer uses the power meter
    """

    #: Description of the attribute
    energy_balancing_interval: int = 3600
    radiator_power: float = 3000
    timezone: str = "Europe/Helsinki"

    def __init__(self, name: str = "energybalancer") -> None:
        """Initialize the energy balancer.

        Args:
            name (str): name of the heating radiator
            power (float): power of the consumer in watts
        """
        super().__init__(name)

        self.topic_in_powerconsumption = self.make_topic_name("powerconsumption")
        self.topic_in_net_energy_balance = self.make_topic_name("net_energy_balance")
        self.topic_out_energybalance = self.make_topic_name("energybalance")
        self.net_energy_balance: float = 0.0  # Energy balance in joules (watt-seconds)
        self.net_energy_balance_ts: float = -1
        self.needed_energy: float = self.energy_balancing_interval * self.radiator_power
        self.net_energy_balancing_mode: bool = False

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic_in_net_energy_balance)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        ts: float = timestamp()

        if msg.topic == self.topic_in_net_energy_balance:
            self.on_power(json.loads(msg.payload.decode()), ts)
        else:
            super().on_message(client, userdata, msg)

    def on_power(self, m: dict[str, Any], ts: float) -> None:
        """Handle the power consumption. Read the current power balance and accumulate
        to the net energy balance to reflect the  energy produced (or consumed) within the
        current time slot.
        Args:
            m (dict[str, Any]): power consumption message
            ts (float): current time
        """
        self.update_energy_balance(m["power"], ts)

    def update_energy_balance(self, power: float, ts: float) -> None:
        """Update the current net net energy balance. The change in the balance is calculate the
        energy balance, which the time elapsed since the last update, multiplied by the
        power. Positive energy balance means we have produced energy that can be consumed
        at the end of the interval. The target is to use all the energy produced during the
        balancing interval. This method is typically called  by the powermeter reading the
        total power consumption of the house

        Args:
            power (float): power reading from the powermeter. Positive value means
                energy produced, negative value means energy consumed. The value of 0 means
                the house is not consuming or producing energy.
            ts (float): current time in utc seconds
        """

        # regardless of the mode, if we hit the end of the interval, reset the balance
        quantized_ts: float = ts % self.energy_balancing_interval
        if self.net_energy_balance_ts < 0:
            self.net_energy_balance_ts = quantized_ts
            self.needed_energy = self.energy_balancing_interval - quantized_ts
        elif quantized_ts <= self.net_energy_balance_ts:
            self.reset_net_energy_balance()
        else:
            # update the energy balance with the elapsed time and the power
            elapsed_ts = quantized_ts - self.net_energy_balance_ts
            balance: float = elapsed_ts * power  # joules i.e. watt-seconds
            self.net_energy_balance = self.net_energy_balance + balance
            self.net_energy_balance_ts = quantized_ts
            self.needed_energy = (
                self.energy_balancing_interval - quantized_ts
            ) * self.radiator_power

            if self.net_energy_balancing_mode:
                if self.net_energy_balance <= 0:
                    # if we have used all the energy, disable the balancing mode
                    self.reset_net_energy_balance()
            else:
                if self.net_energy_balance >= self.needed_energy:
                    self.net_energy_balancing_mode = True
        self.publish_energybalance(ts)

    def consider_net_energy_balance(self, ts: float) -> bool:
        """Check if there is enough energy available for the consumer to heat
        the water in the remaining time within the balancing interval, and switch
        the balancing mode on if sufficient.

        Args:
            ts (float): current time

        Returns:
            bool: true if production exceeds the consumption
        """
        return self.net_energy_balancing_mode

    def reset_net_energy_balance(self) -> None:
        """Reset the net energy balance at the end of the interval."""
        self.net_energy_balance = 0.0
        self.needed_energy = self.energy_balancing_interval * self.radiator_power
        self.net_energy_balance_ts = 0
        self.net_energy_balancing_mode = False

    def activate_balancing_mode(self, ts: float) -> None:
        """Activate balancing mode when enough energy is available."""
        self.net_energy_balancing_mode = True
        self.info(
            f"{int(self.net_energy_balance/3600)} Wh is enough to supply the radiator, enable"
        )

    def deactivate_balancing_mode(self) -> None:
        """Deactivate balancing mode when energy is depleted or interval ends."""
        self.net_energy_balancing_mode = False
        self.info("Balance used, or the end of the interval reached, disable")
        self.net_energy_balance = 0.0  # Reset the energy balance at the interval's end

    def publish_energybalance(self, ts: float) -> None:
        """Publish energy balance information.

        Args:
            ts (float): current time
        Returns:
            dict: diagnostics information
        """
        m: dict[str, Any] = {
            "Unit": self.name,
            "Mode": self.net_energy_balancing_mode,
            "Rc": self.net_energy_balancing_mode,
            "CurrentBalance": self.net_energy_balance,
            "NeededBalance": self.needed_energy,
            "Timestamp": ts,
        }
        self.publish(self.topic_out_energybalance, json.dumps(m))
