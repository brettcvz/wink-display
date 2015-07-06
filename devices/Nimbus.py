from device import WinkDevice
import json

#The "Device Template" id for manual configuration
MANUAL_CONFIGURATION_ID = "10"


class Nimbus(WinkDevice):
    TYPE = "cloud_clocks"

    def __init__(self, device_id, name):
        super(Nimbus, self).__init__(self.TYPE, device_id, name)
        self.dials = []

    @classmethod
    def from_json(cls, data):
        nimbus = cls(data["cloud_clock_id"], data["name"])
        nimbus.dials = map(lambda d: Dial.from_json(d), data['dials'])
        return nimbus

    def __repr__(self):
        return "<Nimbus: id:%s name:%s dials:%s>" % (self.device_id, self.name, str(self.dials))


class Dial(WinkDevice):
    TYPE = "dials"

    index = 0
    value = 0
    label = ""
    description = ""
    brightness = 0

    def __init__(self, device_id, name, index, value, label, description, brightness):
        super(Dial, self).__init__(self.TYPE, device_id, name)

        self.index = index
        self.value = value
        self.label = label
        self.description = description
        self.brightness = brightness

    @classmethod
    def from_json(cls, data):
        device = cls(data['dial_id'],
                data['name'],
                data['dial_index'],
                data['value'],
                data['labels'][0],
                data['labels'][1],
                data['brightness'])
        return device

    def __repr__(self):
        return "<Dial id:%s name:%s index:%d value:%d label:%s (%s) brightness:%d>" % (
                self.device_id, self.name, self.index, self.value, self.label, self.description, self.brightness)

    def configuration(self):
        config = super(Dial, self).configuration()
        #Assumes we always want manual control
        config["channel_configuration"] = {
            "channel_id": MANUAL_CONFIGURATION_ID
        }
        config["value"] = self.value
        config["labels"] = [self.label, self.description]
        config["brightness"] = self.brightness

        return config
