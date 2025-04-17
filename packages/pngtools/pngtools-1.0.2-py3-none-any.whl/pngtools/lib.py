"""pngtools library"""

from os import fstat
from os.path import exists
import zlib
from typing import List, Tuple

ERROR_CODE = {
    "WRONG_LENGTH": "Wrong length",
    "EOF": "End of file",
    "WRONG_CRC": "Wrong CRC",
    "WRONG_TYPE": "Wrong type",
}

CHUNKS_TYPES = {
    b"IHDR": "Image header",
    b"PLTE": "Palette",
    b"IDAT": "Image data",
    b"IEND": "Image trailer",
    b"eXIf": "Exif data",
    b"cHRM": "Primary chromaticities",
    b"gAMA": "Image gamma",
    b"iCCP": "Embedded ICC profile",
    b"sBIT": "Significant bits",
    b"sRGB": "Standard RGB color space",
    b"bKGD": "Background color",
    b"hIST": "Image histogram",
    b"tRNS": "Transparency",
    b"pHYs": "Physical pixel dimensions",
    b"sPLT": "Suggested palette",
    b"tIME": "Image last-modification time",
    b"iTXt": "International textual data",
    b"tEXt": "Textual data",
    b"zTXt": "Compressed textual data",
}

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


# chunk is a list of 5 elements (for now) -> can change in the future
# [length, chunk_type, data, crc, errors]
Chunk = Tuple[int, bytes, bytes, bytes, List[str]]


class ReaderHelper:
    """Helper class to read data from a file or buffer"""

    def __init__(self, fp):
        self.is_file = hasattr(fp, "read")
        self.fp = fp
        self.offset = 0

    def read(self, read_len):
        """Read data from file or buffer"""
        if self.is_file:
            return self.fp.read(read_len)
        else:
            data = self.fp[self.offset : self.offset + read_len]
            self.offset += read_len
            return data

    def size(self):
        """Get the size of the file or buffer"""
        if self.is_file:
            return fstat(self.fp.fileno()).st_size
        else:
            return len(self.fp)


def read_chunk(file: ReaderHelper, total_size):
    """Read a chunk from a file"""
    read = file.read(4)
    errors = []
    if read == "":
        errors.append(ERROR_CODE["EOF"])
        return None, None, None, None, errors
    data_length = int.from_bytes(read, byteorder="big")
    to_read = data_length
    if data_length > total_size:
        to_read = total_size - 3 * 4
        errors.append(ERROR_CODE["WRONG_LENGTH"])
    chunk_type = file.read(4)
    if chunk_type not in CHUNKS_TYPES:
        errors.append(ERROR_CODE["WRONG_TYPE"])
    data = file.read(to_read)
    crc = file.read(4)
    if crc != calculate_crc(chunk_type, data):
        errors.append(ERROR_CODE["WRONG_CRC"])
    return data_length, chunk_type, data, crc, errors


def try_dec(type_chunk):
    """Try to decode the type of chunk"""
    if type_chunk in CHUNKS_TYPES:
        return type_chunk.decode("utf-8")
    return "????"


def try_hex(a):
    """Try to decode a bytes object to hex, if it fails return ????"""
    try:
        return a.hex()
    except UnicodeDecodeError:
        return "????"


def get_by_type(chunks: List[Chunk], current_type="IDAT") -> List[Chunk]:
    """Get all chunks of a specific type"""
    return [
        one_chunk
        for one_chunk in chunks
        if get_type_of_chunk(one_chunk) == current_type
    ]


def _new_chunk(length, chunk_type, data, crc, errors) -> Chunk:
    """Create a new chunk"""
    return (length, chunk_type, data, crc, errors)


def get_length_of_chunk(one_chunk: Chunk):
    """Get the length of a chunk"""
    return one_chunk[0]


def get_type_of_chunk(one_chunk: Chunk):
    """Get the type of a chunk"""
    return one_chunk[1]


def get_data_of_chunk(one_chunk: Chunk):
    """Get the data of a chunk"""
    return one_chunk[2]


def get_crc_of_chunk(one_chunk: Chunk):
    """Get the CRC of a chunk"""
    return one_chunk[3]


def get_errors_of_chunk(one_chunk: Chunk):
    """Get the errors of a chunk"""
    return one_chunk[4]


def extract_idat(chunks: List[Chunk]):
    """Extract IDAT chunks from a list of chunks"""
    return [
        get_data_of_chunk(one_chunk)
        for one_chunk in chunks
        if get_type_of_chunk(one_chunk) == b"IDAT"
    ]


def decode_phy(chunk: Chunk):
    """Decode the pHYs chunk data"""
    phy_chunk_data = get_data_of_chunk(chunk)
    x_pixels_per_unit = int.from_bytes(phy_chunk_data[0:4], byteorder="big")
    y_pixels_per_unit = int.from_bytes(phy_chunk_data[4:8], byteorder="big")
    unit_specifier = int.from_bytes(phy_chunk_data[8:9], byteorder="big")
    if unit_specifier == 0:
        # Units are unspecified or in inches, using default
        x_pixels_per_unit = 2835
        y_pixels_per_unit = 2835
    return x_pixels_per_unit, y_pixels_per_unit, unit_specifier


def extract_data(chunks: List[Chunk]):
    """extract data from IDAT chunks and try to decompress it

    `chunks`: is a list of chunks
    """

    assert isinstance(chunks, list)
    data_idat = b"".join(extract_idat(chunks))
    return try_decompress(data_idat)


def read_broken_file(filename: str, force_idx=0):
    """Read a broken PNG file"""
    if exists(filename):
        with open(filename, "rb") as fp:
            file = fp.read()
        idxs = get_indices(file, PNG_MAGIC)
        if len(idxs) == 0:
            print("No PNG detected")
            return None, idxs
        print(f"PNG signatures detected at {idxs}")
        chosen_idx = force_idx if force_idx != 0 else idxs[0]
        file = ReaderHelper(file[chosen_idx:])
        return split_png_chunks(file), idxs
    print("File does not exist")
    return None, []


def read_file(filename: str, force_read=False):
    """Read a PNG file"""
    if exists(filename):
        with open(filename, "rb") as fp:
            if force_read:
                file = fp.read()
            else:
                file = fp
            file = ReaderHelper(file)
            data = split_png_chunks(file)
        return data
    print("File does not exist")
    return None


def split_png_chunks(fp: ReaderHelper):
    """Split PNG chunks from a file or buffer"""
    size = fp.size()
    print(f"Reading ({size} bytes)")
    remaining_size = size
    magic_len = len(PNG_MAGIC)
    signature = fp.read(magic_len)
    remaining_size -= magic_len
    if signature != PNG_MAGIC:
        raise ValueError("File is not a PNG")
    chunks = []
    idx = 0
    while True:
        if remaining_size <= 0:
            break
        length, chunk_type, data, crc, errors = read_chunk(fp, remaining_size)
        if ERROR_CODE["EOF"] in errors:
            break
        remaining_size -= length + 4 + len(chunk_type) + len(crc)
        if ERROR_CODE["WRONG_LENGTH"] in errors:
            if len(data) > 0 and data[-4:] == b"IEND":
                chunk1 = _new_chunk(
                    length, chunk_type, data[:-12], data[-12:-8], errors
                )
                print_chunks([chunk1], idx)
                chunks.append(chunk1)
                len_iend = int.from_bytes(data[-8:-4], byteorder="big")
                iend_errors = []
                if len_iend > 0:
                    iend_errors.append(ERROR_CODE["WRONG_LENGTH"])
                chunk2 = _new_chunk(len_iend, data[-4:], b"", crc, iend_errors)
                idx += 1
                print_chunks([chunk2], idx)
                chunks.append(chunk2)
        else:
            chunk_to_add = _new_chunk(length, chunk_type, data, crc, errors)
            print_chunks([chunk_to_add], idx)
            chunks.append(chunk_to_add)
        idx += 1
    return chunks


def write_png(chunks: List[Chunk], output_file: str):
    """Write a PNG file"""
    print(f"----> Writing {output_file}")
    print_chunks(chunks)
    with open(output_file, "wb") as file:
        file.write(PNG_MAGIC)
        for one_chunk in chunks:
            file.write(get_binary_chunk(one_chunk))


def print_chunks(chunks: List[Chunk], start_index=0):
    """Print chunks"""
    if len(chunks) == 0:
        return
    max_str = max(len(f"{get_length_of_chunk(one_chunk)}") for one_chunk in chunks)
    for i, one_chunk in enumerate(chunks):
        length_part = get_length_of_chunk(one_chunk)
        data_part = get_data_of_chunk(one_chunk)
        crc_part = get_crc_of_chunk(one_chunk)
        type_part = get_type_of_chunk(one_chunk)
        type_dec = try_dec(type_part)
        errors_part = get_errors_of_chunk(one_chunk)
        crc_hex = try_hex(crc_part)
        checksum = calculate_crc(type_part, data_part)
        is_correct = crc_part == checksum
        data_display = data_part[:5] + b"..." if len(data_part) > 10 else data_part
        errors = ""
        if len(errors_part) > 0:
            errors = f"Errors: {errors_part}"
        f_chunk = f"Length={length_part:{max_str}d}, Type={type_dec},"
        f_chunk = f"{f_chunk} CRC={crc_hex} ({is_correct}), data={data_display}"
        print(f"Chunk {start_index + i:2d}: {f_chunk} {errors}")


def calculate_crc(chunk_type, data):
    """Calculate the CRC of a chunk"""
    i = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return i.to_bytes(4, "big")


def create_ihdr_chunk(width, height):
    """Create an IHDR chunk"""
    chunk_type = b"IHDR"
    data = (
        width.to_bytes(4, byteorder="big")
        + height.to_bytes(4, byteorder="big")
        + b"\x08"  # 8 bits per channel
        + b"\x06"  # RGBA
        + b"\x00"  # Compression method
        + b"\x00"  # Filter method
        + b"\x00"  # Interlace method
    )
    crc = calculate_crc(chunk_type, data)
    return _new_chunk(len(data), chunk_type, data, crc, [])


def create_iend_chunk():
    """Create an IEND chunk"""
    chunk_type = b"IEND"
    data = b""
    crc = calculate_crc(chunk_type, data)
    return _new_chunk(len(data), chunk_type, data, crc, [])


def remove_chunk_by_type(chunks: List[Chunk], filter_type) -> List[Chunk]:
    """Remove chunks by type"""
    return [
        one_chunk for one_chunk in chunks if get_type_of_chunk(one_chunk) != filter_type
    ]


def fix_chunk(chunk: Chunk) -> Chunk:
    """Fix a chunk"""
    length = len(get_data_of_chunk(chunk))
    chunk_type = get_type_of_chunk(chunk)
    data = get_data_of_chunk(chunk)
    if chunk_type not in CHUNKS_TYPES:
        chunk_type = b"IDAT"
    crc = calculate_crc(chunk_type, data)
    errors = []
    return _new_chunk(length, chunk_type, data, crc, errors)


def get_indices(x: list, value: int) -> list:
    """Get the indices of a value in a list"""
    indices = []
    i = 0
    while True:
        try:
            # find an occurrence of value and update i to that index
            i = x.index(value, i)
            # add i to the list
            indices.append(i)
            # advance i by 1
            i += 1
        except ValueError as _e:
            break
    return indices


def get_binary_chunk(chunk: Chunk):
    """Get the binary representation of a chunk"""
    length_binary = get_length_of_chunk(chunk).to_bytes(4, byteorder="big")
    type_binary = get_type_of_chunk(chunk)
    data = get_data_of_chunk(chunk)
    crc = get_crc_of_chunk(chunk)
    return length_binary + type_binary + data + crc


def extract_sub_chunks(one_chunk: Chunk) -> List[Chunk]:
    """Extract sub chunks from a chunk"""
    chunked = get_binary_chunk(one_chunk)
    indices = get_indices(chunked, b"IDAT")
    if len(indices) > 1 and indices[0] > 4:
        indices.insert(0, 0)
    len_idat = len(b"IDAT")
    chunks = []
    for i, start_chunk in enumerate(indices):
        errors = []
        length_binary = chunked[start_chunk - 4 : start_chunk]
        real_length = int.from_bytes(length_binary, byteorder="big")
        if real_length <= 0:
            errors.append(ERROR_CODE["WRONG_LENGTH"])
            real_length = indices[i + 1] - start_chunk - len_idat
        type_idat = chunked[start_chunk : start_chunk + 4]
        if type_idat != b"IDAT":
            errors.append(ERROR_CODE["WRONG_TYPE"])
        data_start = start_chunk + len_idat
        data = chunked[data_start : data_start + real_length]
        if ERROR_CODE["WRONG_TYPE"] in errors:
            data = type_idat + data
        crc_start = data_start + real_length
        crc = chunked[crc_start : crc_start + 4]
        real_crc = calculate_crc(type_idat, data)
        if crc != real_crc:
            errors.append(ERROR_CODE["WRONG_CRC"])
        if ERROR_CODE["WRONG_LENGTH"] in errors:
            real_length = len(data)
        chunk = _new_chunk(
            real_length,
            type_idat,
            data,
            crc,
            errors,
        )
        chunks.append(chunk)
    return chunks


def try_decompress(data):
    """Try to decompress data"""
    try:
        return zlib.decompress(data)
    except zlib.error as e:
        print(e)
    return None


def decode_ihdr(data):
    """Decode IHDR chunk data"""
    width = int.from_bytes(data[0:4], byteorder="big")
    height = int.from_bytes(data[4:8], byteorder="big")
    bit_depth = data[8]
    color_type = data[9]
    compression_method = data[10]
    filter_method = data[11]
    interlace_method = data[12]
    return (
        width,
        height,
        bit_depth,
        color_type,
        compression_method,
        filter_method,
        interlace_method,
    )


def calculate_decompressed_length(width, height, bit_depth, color_type):
    """Calculate the total length of the decompressed image"""
    if color_type == 2:  # RGB
        samples_per_pixel = 3
    elif color_type == 6:  # RGBA
        samples_per_pixel = 4
    else:
        raise ValueError("Unsupported color type")

    # Calculate bytes per pixel
    bytes_per_pixel = (bit_depth * samples_per_pixel) // 8

    # Calculate bytes per scanline (including filter byte)
    bytes_per_scanline = (width * bytes_per_pixel) + 1

    # Calculate total decompressed length
    total_length = bytes_per_scanline * height
    return total_length


def paeth_predictor(a, b, c):
    """Paeth predictor function used in PNG filtering.

    Args:
        a: Left pixel.
        b: Above pixel.
        c: Upper-left pixel.

    Returns:
        The predicted pixel value.
    """
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    elif pb <= pc:
        return b
    else:
        return c


def unfilter_scanlines(data, width, height, bpp, raise_error=True):
    """Unfilter the scanlines of a PNG image."""
    scanline_length = width * bpp
    result = bytearray()
    prev_line = bytearray([0] * scanline_length)
    offset = 0

    for _ in range(height):
        filter_type = data[offset]
        offset += 1
        scanline = bytearray(data[offset : offset + scanline_length])
        offset += scanline_length

        if filter_type == 0:  # None
            pass
        elif filter_type == 1:  # Sub
            for i in range(bpp, len(scanline)):
                scanline[i] = (scanline[i] + scanline[i - bpp]) % 256
        elif filter_type == 2:  # Up
            for i, sc in enumerate(scanline):
                scanline[i] = (sc + prev_line[i]) % 256
        elif filter_type == 3:  # Average
            for i, sc in enumerate(scanline):
                left = scanline[i - bpp] if i >= bpp else 0
                up = prev_line[i]
                scanline[i] = (sc + ((left + up) // 2)) % 256
        elif filter_type == 4:  # Paeth
            for i, sc in enumerate(scanline):
                a = scanline[i - bpp] if i >= bpp else 0
                b = prev_line[i]
                c = prev_line[i - bpp] if i >= bpp else 0
                scanline[i] = (sc + paeth_predictor(a, b, c)) % 256
        else:
            if raise_error:
                raise ValueError(f"Unknown filter type: {filter_type}")

        result.extend(scanline)
        prev_line = scanline

    return result


def deinterlace_adam7(data, width, height, bpp, raise_error=True):
    """Deinterlace Adam7 interlaced PNG data."""
    # Adam7 pattern: (x_start, y_start, x_step, y_step)
    passes = [
        (0, 0, 8, 8),  # pass 1
        (4, 0, 8, 8),  # pass 2
        (0, 4, 4, 8),  # pass 3
        (2, 0, 4, 4),  # pass 4
        (0, 2, 2, 4),  # pass 5
        (1, 0, 2, 2),  # pass 6
        (0, 1, 1, 2),  # pass 7
    ]

    img = bytearray(width * height * bpp)
    offset = 0

    for x_start, y_start, x_step, y_step in passes:
        pass_width = (width - x_start + x_step - 1) // x_step
        pass_height = (height - y_start + y_step - 1) // y_step
        if pass_width == 0 or pass_height == 0:
            continue

        row_bytes = pass_width * bpp
        scanline_len = (row_bytes + 1) * pass_height
        pass_data = data[offset : offset + scanline_len]
        offset += scanline_len

        unfiltered = unfilter_scanlines(
            pass_data, pass_width, pass_height, bpp, raise_error
        )

        i = 0
        for y in range(pass_height):
            for x in range(pass_width):
                pixel_offset = (
                    (y_start + y * y_step) * width + (x_start + x * x_step)
                ) * bpp
                img[pixel_offset : pixel_offset + bpp] = unfiltered[i : i + bpp]
                i += bpp

    return img


def parse_idat(
    unzip_idat_data,
    width,
    height,
    bit_depth,
    color_type,
    interlace_method=0,
    raise_error=True,
):
    """Parse IDAT data and return pixel values."""
    if bit_depth != 8:
        raise NotImplementedError(
            "Only 8-bit depth is supported in this implementation"
        )

    if color_type == 2:  # RGB
        bpp = 3
    elif color_type == 6:  # RGBA
        bpp = 4
    else:
        raise NotImplementedError(f"Unsupported color type: {color_type}")

    if interlace_method == 0:
        raw = unfilter_scanlines(unzip_idat_data, width, height, bpp, raise_error)
    elif interlace_method == 1:
        raw = deinterlace_adam7(unzip_idat_data, width, height, bpp, raise_error)
    else:
        raise NotImplementedError(f"Unsupported interlace method: {interlace_method}")

    return raw


def acropalypse(chunks: List[Chunk], orig_width, orig_height, bit_depth, color_type):
    """Acropalypse function

    Args:
        chunks: List of chunks of IDAT
        orig_width: Original width of the image
        orig_height: Original height of the image
        bit_depth: Bit depth of the image
        color_type: Color type of the image

    Inspired from
    https://gist.github.com/DavidBuchanan314/93de9d07f7fab494bcdf17c2bd6cef02 (MIT License)
    """
    # keep only the IDAT chunks
    extracted = [get_data_of_chunk(one_chunk) for one_chunk in chunks]
    data_idat = b"".join(extracted)

    # remove the adler32 checksum at the end
    data_idat = data_idat[:-4]

    print(f"Extracted {len(data_idat)} bytes of idat!")

    bitstream = []
    for byte in data_idat:
        for bit in range(8):
            bitstream.append((byte >> bit) & 1)

    for _ in range(7):
        bitstream.append(0)

    byte_offsets = []
    for i in range(8):
        shifted_bytestream = []
        for j in range(i, len(bitstream) - 7, 8):
            val = 0
            for k in range(8):
                val |= bitstream[j + k] << k
            shifted_bytestream.append(val)
        byte_offsets.append(bytes(shifted_bytestream))

    # create new compression block
    prefix = (
        b"\x00"
        + (0x8000).to_bytes(2, "little")
        + (0x8000 ^ 0xFFFF).to_bytes(2, "little")
        + b"\x00" * 0x8000
    )
    for i in range(len(data_idat)):
        truncated = byte_offsets[i % 8][i // 8 :]

        # only bother looking if it's (maybe) the start of a non-final adaptive huffman coded block
        if truncated[0] & 7 != 0b100:
            continue
        d = zlib.decompressobj(wbits=-15)
        try:
            decompressed = d.decompress(prefix + truncated) + d.flush(zlib.Z_FINISH)
            if d.eof and d.unused_data in [
                b"",
                b"\x00",
            ]:  # there might be a null byte if we added too many padding bits
                print(f"Found viable parse at bit offset {i}!")
                decompressed = decompressed[0x8000:]  # remove leading padding
                break
        except zlib.error as _e:
            # print(_e)
            continue
    else:
        print("Failed to find viable parse :(")
        return None, None, None
    if color_type == 6:
        reconstructed_idat = bytearray(
            (b"\x00" + b"\xff\x00\xff\xff" * orig_width) * orig_height
        )
    else:
        reconstructed_idat = bytearray(
            (b"\x00" + b"\xff\x00\xff" * orig_width) * orig_height
        )

    # paste in the data we decompressed
    reconstructed_idat[-len(decompressed) :] = decompressed
    data = parse_idat(
        reconstructed_idat,
        orig_width,
        orig_height,
        bit_depth,
        color_type,
        raise_error=False,
    )
    return data


if __name__ == "__main__":
    print("pngtools package loaded")
