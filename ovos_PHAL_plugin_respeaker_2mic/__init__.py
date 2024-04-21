from os.path import exists

from ovos_bus_client.message import Message
from ovos_plugin_manager.phal import PHALPlugin
from ovos_plugin_manager.templates.phal import PHALValidator
from ovos_PHAL_plugin_respeaker_2mic.drivers import get_led # TODO fix for kernel 6.6 , get_button
from ovos_utils.log import LOG

class Respeaker2MicValidator(PHALValidator):
    @staticmethod
    def validate(config=None):
        i2c_platform_dir = config.get("i2c_platform", "/home/ovos/.config/mycroft/i2c_platform")
        LOG.debug(f"i2c_platform_dir is {i2c_platform_dir}")
        if exists(i2c_platform_dir):
            with open(i2c_platform_dir, "r") as f:
                platform = f.readline()
            LOG.debug(f"2mic platform {platform}")
            if platform.strip() == "wm8960":
                return True
        return False


class Respeaker2MicControlPlugin(PHALPlugin):
    validator = Respeaker2MicValidator

    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="ovos-PHAL-plugin-respeaker-2mic", config=config)
        # TODO: Fix for kernel 6.6
        # self.button = get_button()
        # self.button.on_press(self.handle_button_press)
        # self.button.on_button_down(self.handle_button_down)
        # self.button.on_button_up(self.handle_button_up)
        self.led = get_led()
        self.led.wakeup()

    def handle_button_press(self, press_time=0):
        self.bus.emit(Message("ovos.PHAL.button.press",
                              {"press_time": press_time},
                              {"skill_id": self.name}))

    def handle_button_down(self):
        self.bus.emit(Message("ovos.PHAL.button.down",
                              {"skill_id": self.name}))

    def handle_button_up(self):
        self.bus.emit(Message("ovos.PHAL.button.up",
                              {"skill_id": self.name}))

    def on_record_begin(self, message=None):
        self.led.listen()

    def on_record_end(self, message=None):
        self.on_reset(message)

    def on_audio_output_start(self, message=None):
        self.led.speak()

    def on_audio_output_end(self, message=None):
        self.on_reset(message)

    def on_think(self, message=None):
        self.led.think()

    def on_reset(self, message=None):
        self.led.off()

    def on_system_reset(self, message=None):
        self.on_reset(message)

    def shutdown(self):
        self.led.off()
        super().shutdown()
