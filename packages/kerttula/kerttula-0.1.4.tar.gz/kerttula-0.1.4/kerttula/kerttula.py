from typing_extensions import override

from masterpiece import Application

# from juham.web import HomeWizardWaterMeter

from juham_shelly import (
    ShellyPlus1,
    ShellyDS18B20,
    ShellyPro3EM,
    ShellyMotion,
    ShellyPro3,
    ShellyDHT22,
)

from juham_automation import HeatingOptimizer, WaterCirculator, JApp
from juham_watermeter import WaterMeterImgDiff, WaterMeterTs, LeakDetector


class Kerttula(JApp):
    """Kerttula home automation application."""

    shelly_temperature = "shellyplus1-a0a3b3c309c4"  # 4 temp  sensors, circulator relay
    shelly_mainboilerradiator = "shellyplus1-alakerta"  # hot water heating relay
    shelly_sunboilerradiator = "shellypro3-alakerta"  # sun pre-heating relay

    def __init__(self, name: str = "kerttula") -> None:
        """Creates home automation application with the given name.
        If --enable_plugins is False create hard coded configuration
        by calling instantiate_classes() method.

        Args:
            name (str): name for the application
        """
        super().__init__(name)
        self.instantiate_classes()

    @override
    def instantiate_classes(self) -> None:
        super().instantiate_classes()

        #
        # Create sensors
        #

        # Note: commented out, because the sensor is not compatible with the current watermeter
        # self.add(HomeWizardWaterMeter())

        # sensors upstairs, attached to hot water boilers
        self.add(ShellyDS18B20("boiler", self.shelly_temperature))

        # main boiler heating in MDB relay, no sensors attached
        self.add(ShellyDS18B20("mdb", self.shelly_mainboilerradiator))

        # ShellyDHT22 with attached shellyplusaddon, upstairs, with attached humidity sensor
        self.add(ShellyDHT22("ylakerta_humidity", "shelly1g3-humidity"))

        # ShellyDHT22 alapohja
        self.add(ShellyDHT22("laatta_humidity", "shellyplus1-laatta"))

        # ShellyDHT22 with attached shellyplusaddon
        self.add(ShellyDHT22("lapio_humidity", "shelly1g3-laipio"))

        # ShellyDHT22 with attached shellyplusaddon
        self.add(ShellyDHT22("kotilampo_humidity", "shellyplus1-kotilampo"))

        # energy meter in MDB measuring current consumption
        self.add(ShellyPro3EM())  # energy meter

        # living room, shelly motion sensor with temperature and more
        self.add(ShellyMotion("livingroom"))

        # watermeters
        # self.add("WaterMeterOCR"))
        self.add(WaterMeterImgDiff("watermeter_imgdiff"))
        self.add(WaterMeterTs("watermeter_ts"))
        self.add(LeakDetector("leakdetector"))

        #
        # Automation objects regulating energy consumption
        #

        # power plans for the both heating boiler radiators
        main_boiler: HeatingOptimizer = HeatingOptimizer(
            "main_boiler", "temperature/shellyplus1-a0a3b3c309c4/102", 0, 3, 0.15
        )
        self.add(main_boiler)

        # sun boiler heating constrained to night time only!
        sun_boiler: HeatingOptimizer = HeatingOptimizer(
            "sun_boiler", "temperature/shellyplus1-a0a3b3c309c4/101", 3, 2, 0.02
        )
        sun_boiler.schedule_start_hour = 22
        sun_boiler.schedule_stop_hour = 6
        self.add(sun_boiler)

        # water circulator logic, based on the temperature of the circulating water
        # and motion sensor data
        self.add(
            WaterCirculator(
                "watercirculator", "temperature/shellyplus1-a0a3b3c309c4/103"
            )
        )

        #
        # Relay controllers acting on Juham MQTT messages.
        # Important: if these are commented out no automation is applied
        #

        self.add(
            ShellyPlus1(
                "main_boiler_relay", "main_boiler", self.shelly_mainboilerradiator
            )
        )

        self.add(
            ShellyPro3(
                "sun_boiler_relay",
                "sun_boiler",
                self.shelly_sunboilerradiator,
                True,  # L1
                False,  # L2 unused
                False,  # L3 unused
            )
        )
        self.add(
            ShellyPlus1("circulator_relay", "watercirculator", self.shelly_temperature)
        )

        # show the instance hierarchy
        self.print()


def main() -> None:
    id: str = "kerttula"
    Kerttula.init_app_id(id)
    Application.register_plugin_group(id)
    Kerttula.load_plugins()
    Application.load_configuration()

    app = Kerttula(id)
    app.install_plugins()

    # app.serialize()

    # start the network loops
    app.run_forever()


if __name__ == "__main__":
    main()
