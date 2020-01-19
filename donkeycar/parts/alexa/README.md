# Alexa Support
## Overview
Technically this is a part that allow you to override the `user_mode` and `AI_THROTTLE_MULT` by an external url, which is supposed to be altered by an Alexa in our case.

This part will send an POST request every 0.25 second to an url and expect to receive the data in the following format:

```
{
  "statusCode": 200,
  "body": {
    "target": "DonkeyCar",
    "command": "speed up"
  }
}
```

## Command Supported
The command supported are:
- auto pilot
- slow down
- speed up
- stop/manual

## Installation
To install this part, add the following lines to `manage.py`, before the `DriveMode()` part.

```python
from donkeycar.parts.alexa.alexa import AlexaController
V.add(AlexaController(ctr), inputs=['throttle'], outputs=['throttle'], threaded=True)

from donkeycar.parts.alexa.alexa import AlexaController
V.add(AlexaController(ctr, cfg), inputs=['pilot/throttle'], threaded=True)

```

## Commands
Autopilot
===
If you use this command, it is expected that the donkey car is started with a model. This command will set the variable `mode` of the controller to `local`

Slow Down / Speed Up
===
This command alter the `cfg.AI_THROTTLE_MULT` variable passed from the constructor. Each time this command is received, the `AI_THROTTLE_MULT` is increased/decreased by 0.05.

Note: Since this command alter `AI_THROTTLE_MULT`, it won't speed up when you are running in `user` or `local_angle` mode.


Stop/Manual
===
This command will set the variable `mode` of the controller to `user`

## License
AGPL