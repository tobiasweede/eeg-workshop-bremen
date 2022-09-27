"""
Provides some methods to read data from a xdf file.
"""

def load_stream_data(streams, stream_name='ActiChamp-0'):
    """
    Loads the recorded data, timestamps and channel information of a specific
    stream in a xdf file.

    Args:
        streams :
            Streams which should be used, has to be loaded before with _load_stream()
        stream_name (str):
            Name of the stream in the xdf file to be loaded

    Returns:
        data_matrix, data_timestamps, channel_labels

    """
    # find all stream names in the file
    streamToPosMapping = {}
    for pos in range(0, len(streams)):
        stream = streams[pos]['info']['name']
        streamToPosMapping[stream[0]] = pos

    # raise an error if the searched stream_name is not existing
    if stream_name not in streamToPosMapping.keys():
        raise ValueError(
            'Stream ' + str(stream_name) + ' not found in xdf file. '
                                           'Found streams are: '
                                           '\n' + str(
                streamToPosMapping.keys()))

    # Read the channel labels of the stream
    channel_labels = []
    try:
        for channel in \
                streams[streamToPosMapping[stream_name]]['info']['desc'][0][
                    'channels'][0]['channel']:
            channel_labels.append(channel['label'][0])
    except TypeError:
        # no channel information could be found!
        pass

    # Read the data and timestamps
    data_matrix = streams[streamToPosMapping[stream_name]]['time_series']
    data_timestamps = streams[streamToPosMapping[stream_name]]['time_stamps']
    return data_matrix, data_timestamps, channel_labels