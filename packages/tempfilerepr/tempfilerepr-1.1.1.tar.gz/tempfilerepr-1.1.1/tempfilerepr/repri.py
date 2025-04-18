from typing import Union
ALPHABET = 'ZAC2B3EF4GH5TK67P8RS9WXY'
ALPHABET_LENGTH = 24
encode_map = dict(zip(range(ALPHABET_LENGTH), ALPHABET))
decode_map = {
    **dict(zip(ALPHABET, range(ALPHABET_LENGTH))),
    **dict(zip(ALPHABET.lower(), range(ALPHABET_LENGTH)))
}
def encode_code_by_lines(data: Union[bytes, bytearray]) -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise ValueError(f'data must be a bytes-like object, received: {type(data)}')
    if len(data) % 4 != 0:
        padding = 4 - (len(data) % 4)
        data += b'\x00' * padding
    result = []
    for i in range(len(data) // 4):
        chunk = data[i*4:(i+1)*4]
        value = int.from_bytes(chunk, 'big')
        sub_result = []
        for _ in range(7):
            value, idx = divmod(value, ALPHABET_LENGTH)
            sub_result.insert(0, encode_map[idx])
        result.append(''.join(sub_result) + '=')
    return ''.join(result)
def Hahahah(data: str) -> bytearray:
    result = bytearray()
    blocks = [data[i:i+8].rstrip('=') for i in range(0, len(data), 8)]
    for sub_data in blocks:
        value = 0
        for s in sub_data:
            idx = decode_map.get(s)
            if idx is None:
                raise ValueError(f'Unsupported character in input: {s}')
            value = value * ALPHABET_LENGTH + idx
        result.extend(value.to_bytes(4, 'big'))
    return result
def encode(code: str) -> list[str]:
    lines = code.splitlines()
    return [encode_code_by_lines(line.encode()) for line in lines]
def tmpfilevendor(encoded_lines: list[str]) -> str:
    decoded_lines = []
    for encoded in encoded_lines:
        raw_bytes = Hahahah(encoded)
        decoded_line = raw_bytes.rstrip(b'\x00').decode(errors='ignore')
        decoded_lines.append(decoded_line)
    return '\n'.join(decoded_lines)