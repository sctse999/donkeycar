import time
import os
import random
import json
from prettytable import PrettyTable

class LapTimer(object):
    '''
    Lap timer. Must be used together with finish line detector
    '''

    def __init__(self, tub_path):
        self.current_lap_start_time = time.time()
        self.lap_counter = 0
        self.lap_time = None
        self.lap_time_history = []
        self.finish_line_detected = None
        self.is_lap_started = None
        self.start_tub_num = None
        self.finish_tub_num = None
        if (tub_path is not None):
            self.lap_json_path = os.path.join(tub_path, 'lap.json')
        else:
            self.lap_json_path = None

    def write_lap_json_file(self):
        if (self.lap_json_path is not None):

            try:
                with open(self.lap_json_path, 'w') as fp:
                    json.dump(self.lap_time_history, fp)
            except TypeError:
                print('troubles with record:', self.lap_time_history)
            except FileNotFoundError:
                raise
            # except:
            #     print("Unexpected error:", sys.exc_info()[0])
            #     raise
        else:
            print("Not writing lap.json because tub_path is None")

    def is_lap_begin(self, finish_line_detected):
        if (self.finish_line_detected and (not finish_line_detected)):
            # If previous frame see a finish line and this frame does not see a finish line, the lap begins
            return True
        else:
            return False

    def is_lap_finished(self, finish_line_detected):

        if ((not self.finish_line_detected) and finish_line_detected and self.is_lap_started):
            # If previous frame does not see a finish line and this frame see a finish line, the lap ended
            # the lap can only finish after it was started
            return True
        else:
            return False

    def run(self, finish_line_detected , tub_num_records):
        if (self.finish_line_detected is not None):
            if self.is_lap_begin(finish_line_detected):
                print("Lap begin, tub num {}".format(tub_num_records))
                self.lap_counter += 1
                self.lap_start_time = time.time()
                self.is_lap_started = True
                self.start_tub_num = tub_num_records

            if self.is_lap_started:
                # Update the lap time per frame
                self.lap_time = time.time() - self.lap_start_time

            if self.is_lap_finished(finish_line_detected):

                print("Lap finished, tub num {}".format(tub_num_records))
                self.finish_tub_num = tub_num_records

                lap = dict()
                lap['counter'] = self.lap_counter
                lap['time'] = self.lap_time
                lap['start_tub_num'] = self.start_tub_num
                lap['finish_tub_num'] = self.finish_tub_num

                print("lap", lap)

                self.lap_time_history.append(lap)

                self.write_lap_json_file()

                self.is_lap_started = False

        # Update for next frame
        self.finish_line_detected = finish_line_detected

        # print("lap {}, time: {}, lap_history: {}".format(self.lap_counter, self.lap_time, self.lap_time_history))
        return self.lap_counter, self.lap_time, self.lap_time_history

    def shutdown(self):
        pt = PrettyTable()
        pt.field_names =["lap #", "time", "start", "finish"]
        for lap in self.lap_time_history:
            pt.add_row([lap['counter'],
                "%.2f" % lap['time'] ,
                lap['start_tub_num'],
                lap['finish_tub_num']])
        print(pt)
