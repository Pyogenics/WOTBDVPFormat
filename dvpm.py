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
from io import SEEK_END, BytesIO

from sys import argv

class ReadError(RuntimeError): pass

def reverseByteArray(array):
    for arrayI in range(0, len(array), 4):
        print(arrayI)

def readFromBuffer(stream):
    # Read footer
    stream.seek(-44, SEEK_END)
    unk1 = stream.readBytes(8)
    unk2 = stream.readInt32(False)

    metaSize = stream.readInt32(False)

    unk3 = stream.readBytes(16)

    fileTableSize = stream.readInt32(False)

    unk4 = stream.readInt32(False)

    if stream.readBytes(4) != b"DVPM":
        raise ReadError("Invalid footer magic")

    print(f"meta section size: {metaSize}, file table section size: {fileTableSize}")

if __name__ == "__main__":
    filepath = argv[1]

    with open(filepath, "rb") as f:
        stream = FileBuffer(f)
        readFromBuffer(stream)
