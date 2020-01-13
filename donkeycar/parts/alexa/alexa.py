import time

class AlexaController(object):
    '''
    Accept simple command from alexa. For the command supported, please refer to the README.md

    I have defined the following commands: "engine on", "engine off", "stop", "auto pilot", "manual", "speed up", "slow down"
    '''

    def __init__(self, ctr):
        self.running = True
        self.user_mode = "user"
        self.speed_factor = 1
        self.throttle = 0
        self.ctr = ctr

    def get_command(self):
        import requests

        # api-endpoint
        API_ENDPOINT = "https://r4s41gawe7.execute-api.us-east-2.amazonaws.com/dev"

        # sending get request and saving the response as response object
        data = {
            'caller': 'Alexa',
            'apikey': 'zQ8ieCMQuE5L693hUX0lioDL2crgNtuyreyGVUkbLeA'
        }

        # data = {
        #     'caller': 'DonkeyCar',
        #     'apikey': 'srEZiM59dCqFu6ZRjPjMa7H4oMMHpDVmzthipiTAb8w'
        # }

        r = requests.post(url = API_ENDPOINT, json = data)

        result = r.json()
        print(result)
        command = (result['body']['command'])
        return command


    def update(self):
        while (self.running):
            command = self.get_command()
            print("command = {}".format(command))

            if command == "auto pilot":
                self.ctr.mode = "local"
            elif command == "speed up":
                self.speed_factor += 0.1
            elif command == "slow down":
                self.speed_factor -= 0.1
            elif command == "stop" or command == "manual":
                self.ctr.mode = "user"
                self.speed_factor = 1

            print("mode = {}, speed_factor = {}".format(self.ctr.mode, self.speed_factor))
            time.sleep(0.25)


    def run_threaded(self, throttle):
        return self.throttle * self.speed_factor


    def shutdown(self):
        self.running = False
