'''
Copyright (c) 2023 Pyogenics, <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from FileIO import FileBuffer

from io import SEEK_END, SEEK_SET, BytesIO
from sys import argv

class ReadError(RuntimeError): pass

def readFromBuffer(stream):
    # Read footer
    print(">> Reading footer")
    stream.seek(-4, SEEK_END)
    if stream.readBytes(4) != b"DVPM":
        raise ReadError("Invalid magic stream")
    stream.seek(-44, SEEK_END)

    stream.readBytes(8)
    metaCRC = stream.readInt32(False)
    metaSize = stream.readInt32(False)
    stream.readBytes(4)
    metaUnknown = stream.readInt32(False)
    stream.readBytes(8)

    fileTableSize = stream.readInt32(False)
    fileTableCRC = stream.readInt32(False)

    print(f"\tmeta size: {metaSize}\n\tmeta crc: {metaCRC}\n\tmeta unknown: {metaUnknown}\n\n\tfile table size: {fileTableSize}\n\tfile table crc: {fileTableCRC}")

if __name__ == "__main__":
    filepath = argv[1]

    print(f"> Reading {filepath}")
    with open(filepath, "rb") as f:
        stream = FileBuffer(f)
        readFromBuffer(stream)
