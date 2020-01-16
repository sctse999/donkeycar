## Installation

To use this part, go to
```
cd donkeycar/donkeycar/parts/

git submodule add https://github.com/sctse999/donkeypart_traffic_light_detector.git
```


### Install Coral TPU on Pi

Follow [this instruction on medium](https://medium.com/@jonathantse/setting-up-google-coral-usb-accelerator-on-raspberry-pi-4-for-donkey-car-706f33e575a9) to install and setup Google Coral on Pi 4


### Testing this part


### Add code to manage.py

Add the following code
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

So the traffic light detector could override the throttle value if it detects a red light


### More info
Additionally, you need to config ImageResizer


```
from donkeycar.parts.traffic_light_detector.image_resizer import ImageResizer
V.add(ImageResizer(), inputs=['cam/image_array'], outputs=[inf_input, 'cam/image_array'])
```

After this line:

```
if "coral" in model_type:
        inf_input = 'cam/image_array'
    else:
        inf_input = 'cam/normalized/cropped'
        V.add(ImgPreProcess(cfg),
            inputs=['cam/image_array'],
            outputs=[inf_input],
            run_condition='run_pilot')
```