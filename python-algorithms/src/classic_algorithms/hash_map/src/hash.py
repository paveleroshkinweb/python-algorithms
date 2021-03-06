import math


def hash1(key, size):
    return key % size


def hash2(constant):
    def inner(key, size):
        return int(size * math.modf(key * constant)[0])
    return inner


def hash3(key, size):
    return int(size * math.modf(key * (math.sqrt(5) - 1) / 2)[0])


def double_hash(key, size, hash1, hash2, i=0):
    return (hash1(key, size) + i * hash2(key, size)) % size
