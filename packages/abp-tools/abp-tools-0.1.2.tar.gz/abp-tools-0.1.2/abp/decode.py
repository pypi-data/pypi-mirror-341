def decode(ciphertext: bytes, patterns: list[list[int]], return_bytes=False) -> str | bytes:
    data = list(ciphertext)

    for pattern in reversed(patterns):
        for i in range(len(data)):
            data[i] = (data[i] - pattern[i % len(pattern)]) % 256

    result = bytes(data)
    return result if return_bytes else result.decode()
