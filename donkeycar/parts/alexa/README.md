# Alexa Support
## Overview
Technically this is a part that allow you to override the `user_mode` and `throttle` by an external url, which is supposed to be altered by an Alexa in our case.

This part will send an POST request every 0.25 second to an url and expect to receive the data in the following format:

```
{
  "StatusCode": 200,
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

## Input / Output
- Input - throttle
- Output - Adjusted throttle


## Installation
To install this part, add the following lines to `manage.py`, preferably under the `DriveMode()` part.

```python
from donkeycar.parts.alexa.alexa import AlexaController
V.add(AlexaController(ctr), inputs=['throttle'], outputs=['throttle'], threaded=True)
```

## Commands

Autopilot
===
If you use this command, it is expected that the donkey car is started with a model. This command will set the `user_mode` into `local` only

Slow Down / Speed Up
===
Internally there is a `speed_factor` variable in this part intialized at 1. Each time this command is received, the `speed_factor` is increased/decreased by 0.1.


Stop/Manual
===
This command set the `user_mode` to `user`

<Empty Command>
===
If no command is received from Alexa, this part will do nothing

