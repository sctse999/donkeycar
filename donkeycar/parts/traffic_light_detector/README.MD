### Before you begin

Follow [this instruction on medium](https://medium.com/@jonathantse/setting-up-google-coral-usb-accelerator-on-raspberry-pi-4-for-donkey-car-706f33e575a9) to install and setup Google Coral on Pi 4

### Install this part

Add the following code to `manage.py`
```python
from donkeycar.parts.traffic_light_detector.traffic_light_detector import TrafficLightDetector
V.add(TrafficLightDetector(), inputs=['cam/image_array', 'throttle'], outputs=['throttle', 'cam/image_array'])

```

After this line:
```
V.add(DriveMode(),
          inputs=['user/mode', 'user/angle', 'user/throttle',
                  'pilot/angle', 'pilot/throttle'],
          outputs=['angle', 'throttle'])
```

So the traffic light detector could override the throttle value if it detects a red light. By default, this part will annotate bounding box on the image. If you are setting `USE_FPV=True` you might want to move the line under this part.

```
if cfg.USE_FPV:
        V.add(WebFpv(), inputs=['cam/image_array'], threaded=True)
```
