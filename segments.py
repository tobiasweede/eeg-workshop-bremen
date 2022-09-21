import numpy as np


def level_difficulty(level: dict):
    if level["Balls"] and level["Numbers"] and level["Wheel"]:
        return 2
    if level["Balls"] and level["Numbers"]:
        return 1
    if level["Balls"]:
        return 0
    raise RuntimeError("Unreachable code")


def find_nearst_index(a: np.ndarray, value: float):
    return (np.abs(a - value)).argmin()


def do_create_segments(levels, streams):
    timestamps = streams["time_stamps"]
    eeg_data = streams["time_series"]

    timestamps_out = []
    channels_out = []
    labels = []

    for level in levels:
        start_idx, end_idx = level["start_idx"], level["end_idx"]
        timestamps_out.append(timestamps[start_idx:end_idx])
        channels_out.append(eeg_data[start_idx:end_idx])
        labels.append(level["class_id"])

    return timestamps_out, channels_out, labels


def create_segments(xdf_data):
    streams = []

    for stream_idx, stream in enumerate(xdf_data):
        y = stream['time_series']
        level = None
        levels = []
        segments = []
        if isinstance(y, list):
            # list of strings, draw one vertical line for each marker
            for timestamp, marker in zip(stream['time_stamps'], y):

                if marker[0].split()[0] == "Starting":
                    if level is None:
                        level = {"start_timestamp": timestamp}
                    for task in marker[0].split("Tasks:")[1].split(","):
                        task = task.split()
                        name, activated = task[0], task[1]
                        level[name] = eval(activated)

                else:
                    level["stop_timestamp"] = timestamp
                    level["class_id"] = level_difficulty(level)

                    level.pop("Numbers")
                    level.pop("Balls")
                    level.pop("Wheel")

                    levels.append(level)
                    level = None
                print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
            streams.append(levels)
        elif isinstance(y, np.ndarray):
            streams.append({"time_stamps": stream["time_stamps"],
                            "time_series": stream["time_series"]})

        else:
            raise RuntimeError('Unknown stream format')

    levels = streams[0]
    stream = streams[1]

    for level in levels:
        time_stamps = stream["time_stamps"]
        start, end = level["start_timestamp"], level["stop_timestamp"]

        start_idx = find_nearst_index(time_stamps, start)
        end_idx = find_nearst_index(time_stamps, end)

        level["start_idx"] = start_idx
        level["end_idx"] = end_idx

    timestamps, eeg_data, labels = do_create_segments(levels, stream)
    return timestamps, eeg_data, labels
