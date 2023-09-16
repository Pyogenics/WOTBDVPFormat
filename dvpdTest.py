'''
Quick reader to figure out how dvpd works
'''

from FileIO import FileBuffer
from sys import argv
from io import SEEK_END

class ReadError(RuntimeError): pass

def readDVPD(stream):
    stream.seek(-4, SEEK_END)
    if stream.readBytes(4) != b"DVPD":
        raise ReadError("Invalid magic string")
    stream.seek(-32, SEEK_END)

    for _ in range(4):
        print(stream.readInt32(False))
    
    size = stream.readInt64()
    print(stream.readInt32(False))

    print(f"data size: {size}")

with open(argv[1], "rb") as f:
    print("> Reading footer")
    stream = FileBuffer(f)
    readDVPD(stream)
