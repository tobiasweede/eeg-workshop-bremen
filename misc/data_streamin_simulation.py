from pylsl import StreamInlet, resolve_stream


streams = resolve_stream('type','NIRS')

stream = StreamInlet(streams[0])

while True:
    data , timestamp = stream.pull_sample()
    print(data)