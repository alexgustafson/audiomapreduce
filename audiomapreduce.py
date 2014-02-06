import mincemeat
import wave
from struct import unpack


def get_sample_data(path_to_audiofile, start_pos=0, num_of_samples=44100, skip=1000):

    audioData = wave.open(path_to_audiofile, 'r')
    audioData.setpos(start_pos)
    samples = audioData.readframes(num_of_samples)
    number_of_channels = audioData.getnchannels()

    npts=len(num_of_samples)
    formatstr = '%ih' % (npts/2)
    int_data = unpack(formatstr, samples)

    format_data = []
    i = 0
    skip *= number_of_channels

    for sample in int_data:
        i += number_of_channels
        if i % skip != 0:
            continue
        format_data.append(sample)

    return format_data


datasource = dict(enumerate(get_sample_data('test_data/OsBorges-EuSouComoVoceE.wav', num_of_samples=1000, skip=0)))

def mapfn(k, v):
    for w in v:
        yield abs(w), 1


def reducefn(k, vs):
    result = sum(vs)
    return result

s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
print results