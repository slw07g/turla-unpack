#/usr/bin/env python3


import struct
import argparse
import pefile
import os
from ctypes import *
import lzma2 as lzma
import traceback
import platform
import sys

def find_packed_header(filedata, pe):
    # look for the size of the scratch workspace (0xc1cd8) - this is hardcoded in the decompression algo
    for i in range(10):
        off = 0x1000 * i
        #print(hex(off))
        pi = get_packed_info(filedata, off)
        #print(pi)
        if pe.OPTIONAL_HEADER.Magic != 0x20B:
            for field in pi:
                if pi[field] == 0xc1cd8:
                    return off
        else:
            if not (pi['packedSize'] or pi['chunk2Offset'] or pi['headerSize'] or pi['scratchSize']):
                if pi['field0'] and pi['field4'] and pi['packedOffset']:
                    return off

    return None

def do_xor(arr, sz, xorKey):
    j = 0
    while j < (sz >> 2):
        xor =  xorKey ^ struct.unpack_from('<I', arr, j * 4)[0]
        for i in range(4):
            arr[j * 4 + i] = (xor >> (8 * i)) & 0xFF
        j += 1

    return arr

def do_xor_check(packed : bytearray, xorKey):
    #print("checking xor")
    ret = do_xor(packed[:4], 4, xorKey)
    #print(bytearray(ret))
    if str(ret) == "\x00&\x96\x8e":
        return 1
    if ret[0] == 0 and ret[2] == ord('&') and ret[3] == 0x96:
        return 2

    return False

def decompress(compressedBuf, decompressedSize, scratchSize=0x30736*4):
    decompressedBuf = bytearray(str('\x00' * decompressedSize).encode('utf-8'))
    lzma.decompress(decompressedBuf, compressedBuf, bytearray(struct.pack('<I', 0x400) * 0x30736) )
    return decompressedBuf

def unpack64(pe, filedata, header_offset):
    # It's not really packed, just obfuscated
    pi = get_packed_info(filedata, header_offset)
    if not pi['packedSize'] and not pi['field8']:
        packedSize = pi['packedOffset']
        xorKey = pi['field4']
        unpackedSize = pi['field0']
        packed = filedata[header_offset + 0x28: header_offset + 0x28 + packedSize]

    else:
        raise Exception("Shouldn't get to this point!")
    j = 0
    k = 0
    newpacked = bytearray(str('\x00' * packedSize).encode('utf-8'))
    while k < packedSize:
        newpacked[j] = packed[k]
        if not (j % 0xF):
            k += 1
        k += 1
        j += 1
    packed = newpacked
    i = packedSize - 1
    while i >= j:
        packed[i] = 0
        i -= 1

    j = 0
    while j < packedSize >> 2:
        xor =  xorKey ^ struct.unpack_from('<I', packed, j * 4)[0]
        for i in range(4):
            packed[j * 4 + i] = (xor >> (8 * i)) & 0xFF
        j += 1

    return packed


def unpack2(pe, filedata, header_offset):
    print("Trying unpack2")
    packed_info = get_packed_info(filedata, header_offset)

    if not packed_info['packedSize']:
        packedSize = packed_info['packedOffset']
        packed = bytearray(filedata[header_offset + 0x28: header_offset + 0x28 + packedSize])
        xorKey = packed_info['field4']
        unpackedSize = packed_info['field0']
        scratchSize = packed_info['field8']
    else:
        raise(Exception("Shouldn't be here!!!"))

    j = 0
    k = 0
    newpacked = bytearray(str('\x00' * packedSize).encode('utf-8'))
    decoded = False
    if do_xor_check(packed, xorKey) == 2:
        do_xor(packed, packedSize, xorKey)
        decoded = True
    while k < packedSize:
        newpacked[j] = packed[k]
        if not (j % 0xF):
            k += 1
        k += 1
        j += 1
    packed = newpacked
    i = packedSize - 1

    while i >= j:
        packed[i] = 0
        i -= 1
    if not decoded:
        do_xor(packed, packedSize, xorKey)

    unpacked = decompress(packed, unpackedSize, scratchSize)

    #print('XOR Key: {0}'.format(hex(xorKey)))
    return unpacked


def unpack1(packed_info, filedata, header_offset):
    print('trying to unpack....')
    packed = (filedata[header_offset:header_offset + packed_info['headerSize']] +
              filedata[packed_info['chunk2Offset'] : packed_info['chunk2Offset'] + packed_info['headerSize']])
    packed = packed[0x28:]

    if packed_info['packedSize']:
        packed = packed[packed_info['packedOffset']:]
        packedSize = packed_info['packedSize']
        unpackedSize = packed_info['unpackedSize']
        scratchSize = packed_info['scratchSize']
        xorKey = packed_info['xor']
    else:
        packedSize = packed_info['packedOffset']
        unpackedSize = packed_info['field0']
        scratchSize = packed_info['field8']
        xorKey = packed_info['field4']

    packed = bytearray(packed)
    decodedCompressed = bytearray(str('\x00' * packedSize).encode('utf-8'))
    i = decodedCompressedLen = 0
    decoded = False
    if  do_xor_check(packed, xorKey) == 2:
        decoded = True
        packed == do_xor(packed, packedSize, xorKey)
    while i < packedSize:
        decodedCompressed[decodedCompressedLen] = packed[i]
        if not (decodedCompressedLen % 0xF):
            i += 1
        i += 1
        decodedCompressedLen += 1

    k = packedSize - 1
    while k >= decodedCompressedLen:
        decodedCompressed[k] = 0
        k -= 1
    if not decoded:
        do_xor(decodedCompressed, decodedCompressedLen, xorKey)
        #print(l)

    print(decodedCompressed[:10])
    return decompress(decodedCompressed, unpackedSize, scratchSize)


def get_packed_info(filedata, start=0x5000):
    #unpack_info = vfile[start:start + 0x28]
    (f0, f1, f2, f3, f4, f5, f6, f7, f8, f9) = struct.unpack_from('<IIIIIIIIII', filedata, start)
    d = {'field0': f0,
         'field4': f1,
         'field8': f2,
         'packedOffset': f3,
         'unpackedSize': f4,
         'xor': f5,
         'scratchSize': f6,
         'packedSize': f7,
         'chunk2Offset': f8,
         'headerSize': f9
         }
    return d

def deflate_pe(filedata):
    pe = pefile.PE(data=filedata)
    ret = filedata[:pe.OPTIONAL_HEADER.SizeOfHeaders]
    for section in pe.sections:
        ret += filedata[section.VirtualAddress:section.VirtualAddress + section.SizeOfRawData]
        if section.SizeOfRawData % pe.OPTIONAL_HEADER.FileAlignment:
            ret += bytearray(str('\x00') * (pe.OPTIONAL_HEADER.FileAlignment -
                                            (section.SizeOfRawData % pe.OPTIONAL_HEADER.FileAlignment)))

    pe = pefile.PE(data=ret)
    #print(pe)
    return ret

def expand_pe(filedata, pe):
    ret = str('\x00' * pe.OPTIONAL_HEADER.SizeOfImage).encode('utf-8')
    ret = filedata[:pe.OPTIONAL_HEADER.SizeOfHeaders]  + ret[pe.OPTIONAL_HEADER.SizeOfHeaders:]
    for section in pe.sections:
        if section.SizeOfRawData == 0:
            #print('skipping section')
            continue

        ret = (ret[:section.VirtualAddress] +
               section.get_data() +
               ret[section.VirtualAddress + section.SizeOfRawData:])

        #print(ret[0x1000:0x1008])

    return ret

def attempt_unpack(filedata, filename=None):
    pe = pefile.PE(data=filedata, fast_load=False)
    expanded = expand_pe(str(filedata).encode('utf-8'), pe)
    header_offset = find_packed_header(expanded, pe)
    if header_offset is None:
        return None
    else:
        print(filename)
        print(hex(pe.OPTIONAL_HEADER.Magic))
    packed_info = get_packed_info(expanded, header_offset)
    print(packed_info)

    if pe.OPTIONAL_HEADER.Magic == 0x20B: # if x64:
        unpacked = unpack64(pe, expanded, header_offset)
    elif packed_info['chunk2Offset'] == 0 and (packed_info['field8'] == 0xc1cd8):
        unpacked = unpack2(pe, expanded, header_offset)
    elif packed_info['field8'] == 0xc1cd8:
        print("Trying unpack1")
        unpacked = unpack1(packed_info, expanded, header_offset)

    return unpacked


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="file to unpack", required=False)
    group.add_argument("-F", "--folder", help='path to recursively unpack', required=False)
    try:
        args = parser.parse_args()
        file = args.file
        folder = args.folder
    except:
        print(traceback.format_exc())
        pass
    finally:
        pass


    if file:
        fh = open(file, 'rb')
        filename = fh.name
        filedata = fh.read()
        unpacked = attempt_unpack(filedata, filename)
        if unpacked:
            deflated = deflate_pe(unpacked)
            open('{0}.unpacked'.format(filename), 'wb').write(deflated)
            pe = pefile.PE(data=deflated)
            for rsrc in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                for r in rsrc.directory.entries:
                    for e in r.directory.entries:
                        print(dir(e))
                        print(r.id)
                        fh2 = open('{0}.unpacked.{1}_{2}'.format(filename, rsrc.name, r.id), 'wb')
                        fh2.write(unpacked[e.data.struct.OffsetToData:e.data.struct.OffsetToData + e.data.struct.Size])


    if folder:
        for r, _, files in os.walk(folder):
            for f in files:
                unpacked = None
                currfile = os.path.join(r, f)
                filedata = open(currfile, 'rb').read()
                try:
                    unpacked = attempt_unpack(filedata, currfile)
                except:
                    continue
                if unpacked:
                    deflated = deflate_pe(unpacked)
                    open('{0}.unpacked'.format(currfile), 'wb').write(deflated)
                    pe = pefile.PE(data=deflated)
                    try:
                        for rsrc in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                            for rsrcEntry in rsrc.directory.entries:
                                for e in rsrcEntry.directory.entries:
                                    rsrcName = '{0}_{1}'.format(rsrc.name, rsrcEntry.id)
                                    print('Extracting resource: {0}'.format(rsrcName))
                                    fh2 = open('{0}.unpacked.{1}'.format(currfile, rsrcName), 'wb')
                                    fh2.write(unpacked[e.data.struct.OffsetToData:e.data.struct.OffsetToData + e.data.struct.Size ])
                    except Exception:
                        continue
        return


if __name__ == '__main__':
    main()