# wotb-dvp
WOTB dvp type file specification.

## Research materials
- [DVPL file tool](https://github.com/Maddoxkkm/dvpl_converter) by Maddoxkkm 

## .dvpm
DVPM files are split into 3 sections: meta, file table and footer.
### meta
This section is at the very start of the file and has a magic string of "met3".
```c
struct DVPMMeta
{
    char magic[4]; // "met3"
    uint32_t fileCount;
    uint32_t unknownArray[fileCount];
    uint32_t dvpdCount;
    struct {
        uint32_t dvpdUnknown1;
        uint32_t dvpdUnknown2;
        uint32_t dvpdUnknown3;
        uint32_t dvpdUnknown4;
    } dvpdInfo[dvpdCount]; // For every dvpd there are 16 bytes of unknown data
    uint32_t filePathStringLength;
    char filePathString[]; // Null seperated filepath strings
    uint32_t packStringsRawSize;
    uint32_t packStringCompressedSize;
    byte packStrings[]; // lz4 encoded "pack" strings
}
```
### file table
```c
struct DVPMFileTable
{
    struct {
        uint64_t fileOffset; // Offset to the file inside the dvpd data block
        uint32_t compressedSize;
        uint32_t uncompressedSize;
        uint32_t compressedCRC32;
        uint32_t compressionType;
        uint32_t uncompressedCRC32;
        uint32_t metaSectionReference;
    } FileEntries[];
    byte filePaths[]; // lz4 encoded file paths string (separated by null bytes), see footer "fileTableFilepaths"
}
```
#### Compression types
```
0 none
1 LZ4
2 LZ4_HC
3 RFC1951
```
### footer
The footer is 44 bytes large and the last 4 bytes are a magic string that reads "DVPM".

```c
struct DVPMFooter
{
    byte unknown1[8];
    uint32_t metaSectionCRC32;
    uint32_t metaSectionSize;
    byte unknown2[4];
    uint32_t fileCount;
    uint32_t fileTableFilepathsCompressedSize;
    uint32_t fileTableFilepathsRawSize;
    uint32_t fileTableSize;
    uint32_t fileTableCRC32;
    char magic[4]; // "DVPM"
}
```

## .dvpd
TODO
### footer
The footer is 32 bytes large and the last four bytes are a magic string that read "DVPD".
```c
struct DVPDFooter
{
    struct {
        uint32_t dvpdUnknown1;
        uint32_t dvpdUnknown2;
        uint32_t dvpdUnknown3;
        uint32_t dvpdUnknown4;
    } dvpdInfo; // Matches with dvpdInfo in DVPM meta section
    uint64_t dataSize; // File size - header size (file size - 32)
    uint32_t dataCRC32;
    char magic[4]; // "DVPD"
}
```
