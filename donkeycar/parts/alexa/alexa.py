import time

class AlexaController(object):
    '''
    Accept simple command from alexa. For the command supported, please refer to the README.md
    '''

    def __init__(self, ctr, cfg):
        self.running = True
        self.user_mode = "user"
        self.ctr = ctr
        self.cfg = cfg  # Pass the config object for altering AI_THROTTLE_MULT

    def get_command(self):
        import requests

        # api-endpoint
        API_ENDPOINT = "https://r4s41gawe7.execute-api.us-east-2.amazonaws.com/dev"

        # sending get request and saving the response as response object
        data = {
            'caller': 'DonkeyCar',
            'apikey': 'srEZiM59dCqFu6ZRjPjMa7H4oMMHpDVmzthipiTAb8w'
        }

        r = requests.post(url = API_ENDPOINT, json = data)

        result = r.json()
        print(result)
        if ("command" in result['body']):
            command = result['body']['command']
        else:
            command = ""
        return command


    def update(self):
        while (self.running):
            command = self.get_command()
            print("command = {}".format(command))

            if command == "auto pilot":
                self.ctr.mode = "local"
            elif command == "speed up":
                self.cfg.AI_THROTTLE_MULT += 0.05
            elif command == "slow down":
                self.cfg.AI_THROTTLE_MULT -= 0.05
            elif command == "stop" or command == "manual":
                self.ctr.mode = "user"
                self.cfg.AI_THROTTLE_MULT = 1

            print("mode = {}, cfg.AI_THROTTLE_MULT={}".format(self.ctr.mode, self.cfg.AI_THROTTLE_MULT))
            time.sleep(0.25)


    def run_threaded(self):
        pass


    def shutdown(self):
        self.running = False
