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
from crc import Calculator, Crc32

class ReadError(RuntimeError): pass

def readMeta(data, checksum):
    print(">>> Checking CRC")
    if Calculator(Crc32.CRC32).checksum(data) != checksum:
        raise ReadError("Bad meta CRC")
    print("\tOK")

    stream = BytesIO(data)
    stream = FileBuffer(stream)

    if stream.readBytes(4) != b"met3":
        raise ReadError("Bad meta magic string")

    footerUnknown = stream.readInt32(False)
    unknowns = []
    for _ in range(footerUnknown):
        unknowns.append([stream.readInt32(False), stream.readInt32(False)])

    dvpdCount = stream.readInt32(False)

    print(f"\tdvpd count: {dvpdCount}")

def readFileTable(data, checksum):
    print(">>> Checking CRC")
    if Calculator(Crc32.CRC32).checksum(data) != checksum:
        raise ReadError("Bad file table CRC")
    print("\tOK")

def readFromBuffer(stream):
    # Read footer
    print(">> Reading footer")
    stream.seek(-4, SEEK_END)
    if stream.readBytes(4) != b"DVPM":
        raise ReadError("Invalid magic string")
    stream.seek(-44, SEEK_END)

    stream.readBytes(8)
    metaCRC = stream.readInt32(False)
    metaSize = stream.readInt32(False)
    stream.readBytes(4)
    metaUnknown = stream.readInt32(False)
    stream.readBytes(8)

    fileTableSize = stream.readInt32(False)
    fileTableCRC = stream.readInt32(False)

    stream.seek(0, SEEK_SET)
    print(f"\tmeta size: {metaSize}\n\tmeta crc: {metaCRC}\n\tmeta unknown: {metaUnknown}\n\n\tfile table size: {fileTableSize}\n\tfile table crc: {fileTableCRC}")
 
    # Read meta
    print(">> Reading meta")
    meta = stream.readBytes(metaSize)
    readMeta(meta, metaCRC)

    # Read file table
    print(">> Reading file table")
    fileTable = stream.readBytes(fileTableSize)
    readFileTable(fileTable, fileTableCRC)

    print("> All done")

if __name__ == "__main__":
    filepath = argv[1]

    print(f"> Reading {filepath}")
    with open(filepath, "rb") as f:
        stream = FileBuffer(f)
        readFromBuffer(stream)
