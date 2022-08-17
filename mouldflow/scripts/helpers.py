import json
from collections import OrderedDict
import paho.mqtt.client as mqtt

extension = R"_docker"

# Christophe has a more bug-free version of this class (implement once he is 'done')
class Mqtt():
    def __init__(self, clientid):
        # read config files
        # cnf_version = self.config_version()
        self.config = self.read_jsonconfig("_docker")

        # define Paho Mqtt client:
        self.client = mqtt.Client(
            client_id=clientid,
            clean_session=True,
            userdata=None,
            protocol=mqtt.MQTTv311,
            transport="tcp"
            )


    def read_jsonconfig(self, extension):
            with open(Rf"mqtt_config{extension}.json") as jsonfile:
                return json.load(jsonfile, object_pairs_hook=OrderedDict)


    # def config_version(self):
    #     with open(Rf"{local_string}config.ini") as f:
    #         line = f.readline()
    #         return line


    def make_connection(self):
        # make connection
        if self.config['broker_login'] != "":
            self.client.username_pw_set(username=self.config['broker_login'], password=self.config['broker_password'])
        
        self.client.connect(
            host=self.config['broker_ip'], 
            port=self.config['broker_port'],
            # keepalive=6000
            )

