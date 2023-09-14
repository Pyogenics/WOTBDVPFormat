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
    uint32_t footerUnknown; // Unknown value that is also present in the footer (metaSectionUnknown)
    uint32_t unknownArray[footerUnknown*2];
    uint32_t dvpdCount;
    uint32_t unknownArray1[dvpdCount*4]; // For every dvpd there are 16 bytes of unknown data
    uint32_t filePathStringLength;
    char filePathString[]; // Null seperated filepath strings
}
```
### file table
```c
struct DVPMFileTable
{
    struct {
        uint32_t unknown1;
        uint32_t unknown2;
        uint32_t compressedSize;
        uint32_t uncompressedSize;
        uint32_t unknown3;
        uint32_t compressionType;
        uint32_t unknown4;
        uint32_t metaSectionReference;
    } FileEntries[];
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
The footer is 44 bytes large and the last 4 bytes are a magic big endian string that reads "DVPM".

```c
struct DVPMFooter
{
    byte unknown1[8];
    uint32_t metaSectionCRC32;
    uint32_t metaSectionSize;
    byte unknown2[4];
    uint32_t metaSectionUnknown; // Unknown value that is also present in the meta section
    byte unknown3[8];
    uint32_t fileTableSize;
    uint32_t fileTableCRC32;
    char magic[4]; // "DVPM"
}
```
