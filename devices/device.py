class WinkDevice(object):
    def __init__(self, device_type, device_id, name):
        self.device_type = device_type
        self.device_id = device_id
        self.name = name

    def __repr__(self):
        return "<WinkDevice id:%s name:%s>" % (self.device_id, self.name)

    def url(self):
        return "/%s/%s" % (self.device_type, self.device_id)

    def configuration(self):
        #The dictionary of configurable params
        return {"name": self.name}
