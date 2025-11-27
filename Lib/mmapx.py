#!/usr/bin/env python3
"""
mmapx.py
-------------
This library allows you to modify your application's memory (similar to C, but even easier).
This is a fork; it's not the original repository, just a fork created by NopAngel.
"""

class mmapx:
    def __init__(self, size=4096):
        self._memory = bytearray(size)
        self._pos = 0
        self._size = size

    def write(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        data_len = len(data)
        if self._pos + data_len > self._size:
            raise MemoryError("Out of memory")
        
        for i in range(data_len):
            self._memory[self._pos + i] = data[i]
        
        self._pos += data_len
        return data_len

    def read(self, size=None):
        if size is None:
            size = self._size - self._pos
        
        if self._pos + size > self._size:
            size = self._size - self._pos
        
        data = bytes(self._memory[self._pos:self._pos + size])
        self._pos += size
        return data

    def seek(self, pos):
        if pos < 0 or pos >= self._size:
            raise ValueError("Invalid position")
        self._pos = pos
        return pos

    def peek(self, addr, size=1):
        if addr + size > self._size:
            raise MemoryError("Address out of range")
        return bytes(self._memory[addr:addr + size])

    def poke(self, addr, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if addr + len(data) > self._size:
            raise MemoryError("Address out of range")
        
        for i in range(len(data)):
            self._memory[addr + i] = data[i]
        return len(data)

    def hexdump(self, start=0, size=32):
        result = []
        result.append("HEXDUMP @ 0x%08x:" % start)
        for i in range(start, min(start + size, self._size), 16):
            hex_bytes = ' '.join('%02x' % self._memory[j] for j in range(i, min(i + 16, self._size)))
            ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in self._memory[i:min(i + 16, self._size)])
            result.append("0x%08x: %-48s %s" % (i, hex_bytes, ascii_str))
        return '\n'.join(result)

    def memset(self, value, size=None, start=None):
        if start is None:
            start = self._pos
        if size is None:
            size = self._size - start
        
        for i in range(start, start + size):
            self._memory[i] = value & 0xFF
        return size

    def memcpy(self, dest, src, size):
        for i in range(size):
            self._memory[dest + i] = self._memory[src + i]
        return size

    def get_size(self):
        return self._size

    def get_pos(self):
        return self._pos
