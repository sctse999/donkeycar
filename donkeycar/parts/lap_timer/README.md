# Lap Timer
## Overview
This part will record the lap time when a donkey completes a lap. The timer starts when the donkey cross the finish line and the lap ends when the donkey cross the finish line again. A lap.json file will be written to the tub folder storing the time of each lap.

## Finish line detector
The finish line detector shipped in this part detects a red line as the starting/finishing line. You can plug in any implementation you like.


## Installation
To install this part

1. Add the following lines to `manage.py`, preferably under the `TubHandler` part.

```python
if cfg.LAP_TIMER:
    from donkeycar.parts.lap_timer.finish_line_detector import FinishLineDetector
    V.add(FinishLineDetector(), inputs=['cam/image_array'], outputs=["finish_line_detected", "cam/image_array"])
    from donkeycar.parts.lap_timer.lap_timer import LapTimer
    print("tub_path", th.path)
    V.add(LapTimer(th.path), inputs=['finish_line_detected', 'tub/num_records'], outputs=["lap_counter", "lap_time", "lap_history"])
```

2. Add the following line in `myconfig.py`
```
LAP_TIMER=True
```

## Debugging
Use `debug=True` when you add the `FinishLineDetector()` in manage.py
```python
from donkeycar.parts.lap_timer.finish_line_detector import FinishLineDetector
    V.add(FinishLineDetector(), inputs=['cam/image_array', True], outputs=["finish_line_detected", "cam/image_array"])
```