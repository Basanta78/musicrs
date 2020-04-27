import io
import json
import numpy


def serialize(numpy_obj):
    memfile = io.BytesIO()
    numpy.save(memfile, numpy_obj)
    memfile.seek(0)
    serialized = json.dumps(memfile.read().decode("latin-1"))
    return serialized


def de_serialize(serialized_obj):
    memfile = io.BytesIO()
    memfile.write(json.loads(serialized_obj).encode("utf-8"))
    memfile.seek(0)
    numpy_obj = numpy.load(memfile)
    return numpy_obj
