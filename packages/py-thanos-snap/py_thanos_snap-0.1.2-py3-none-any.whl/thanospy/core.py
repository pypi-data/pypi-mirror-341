# thanospy/core.py

import math
import random
import struct
from typing import Any, Dict, List, Sequence, Set, TypeVar

# Define a generic type variable
T = TypeVar("T")


def _snap_sequence(data: Sequence[T]) -> List[T]:
    """Snaps a sequence (list, tuple, string, bytes). Returns a list."""
    n = len(data)
    if n == 0:
        return []
    k = math.ceil(n / 2)  # Number of items to keep
    indices_to_keep = sorted(random.sample(range(n), k))
    return [data[i] for i in indices_to_keep]


def _snap_set(data: Set[T]) -> Set[T]:
    """Snaps a set."""
    n = len(data)
    if n == 0:
        return set()
    k = math.ceil(n / 2)  # Number of items to keep
    # Convert to list for sampling, then back to set
    return set(random.sample(list(data), k))


def _snap_dict(data: Dict[Any, Any]) -> Dict[Any, Any]:
    """Snaps a dictionary."""
    n = len(data)
    if n == 0:
        return {}
    k = math.ceil(n / 2)  # Number of keys to keep
    keys_to_keep = random.sample(list(data.keys()), k)
    return {key: data[key] for key in keys_to_keep}


def _snap_int(data: int) -> int:
    """Snaps an integer by removing half its bits."""
    if data == 0:
        return 0

    is_negative = data < 0
    if is_negative:
        data = -data

    binary_repr = bin(data)[2:]  # Get binary string without '0b'
    n = len(binary_repr)

    if n <= 1:  # Cannot remove half if only 0 or 1 bits
        return -data if is_negative else data

    k = math.ceil(n / 2)  # Number of bits to keep
    indices_to_keep = sorted(random.sample(range(n), k))
    snapped_binary = "".join(binary_repr[i] for i in indices_to_keep)

    if not snapped_binary:  # Should not happen if k >= 1, but safety check
        return 0

    snapped_int = int(snapped_binary, 2)

    return -snapped_int if is_negative else snapped_int


def _snap_float(data: float) -> float:
    """
    Snaps a float by manipulating its underlying bits (IEEE 754 double).
    Warning: This can produce unusual results, NaN, or infinities.
    """
    if math.isnan(data) or math.isinf(data) or data == 0.0:
        return data  # Keep special values or zero as is

    # Pack float into 8 bytes (double precision)
    try:
        packed = struct.pack(">d", data)  # Use big-endian for consistency
    except struct.error:
        return data  # Cannot pack, return original

    # Convert bytes to integer
    int_repr = int.from_bytes(packed, "big")

    # Snap the integer representation (sign bit might be affected)
    snapped_int_repr = _snap_int(int_repr)  # Reuse int snapping logic

    # Convert snapped integer back to bytes (must be 8 bytes)
    try:
        snapped_packed = snapped_int_repr.to_bytes(
            8, "big", signed=True
        )  # Use signed=True as sign bit is part of int_repr
    except OverflowError:
        # Snapped int might be too large/small after bit removal
        # Return something plausible? Maybe 0.0 or original? Let's return 0.0
        return 0.0

    # Unpack bytes back to float
    try:
        snapped_float = struct.unpack(">d", snapped_packed)[0]
    except struct.error:
        return 0.0  # Could not unpack

    # If snapping resulted in Inf/NaN where original wasn't, maybe return 0?
    # Let's allow Inf/NaN results for now as it's inherent to bit manipulation.
    return snapped_float


def snap(data: T) -> T:
    """
    Randomly removes approximately half the content of a built-in Python
    data structure or type, returning the same type.

    Supports: list, tuple, set, dict, str, int, float, bytes, bytearray,
              bool, NoneType.

    - Sequences (list, tuple, str, bytes, bytearray): Removes elements/chars/bytes.
    - Sets: Removes elements.
    - Dicts: Removes key-value pairs.
    - Ints: Converts to binary, removes bits, converts back.
    - Floats: Manipulates underlying bits (can yield NaN/Inf).
    - Bool/None: Returned unchanged.

    Args:
        data: The input data structure or value.

    Returns:
        A new object of the same type as the input, with roughly half the
        content removed randomly, or the original value for types where
        snapping is not applicable (bool, None).

    Raises:
        TypeError: If the input data type is not supported.
    """
    if isinstance(data, list):
        # Type checker needs help understanding the return type matches T
        return _snap_sequence(data)  # type: ignore[return-value]
    elif isinstance(data, tuple):
        return tuple(_snap_sequence(data))  # type: ignore[return-value]
    elif isinstance(data, set):
        return _snap_set(data)  # type: ignore[return-value]
    elif isinstance(data, dict):
        # Dictionary keys/values might not match T directly
        return _snap_dict(data)  # type: ignore[return-value]
    elif isinstance(data, str):
        return "".join(_snap_sequence(data))  # type: ignore[return-value]
    elif isinstance(data, bytes):
        # Convert list of ints back to bytes
        return bytes(_snap_sequence(list(data)))  # type: ignore[return-value]
    elif isinstance(data, bytearray):
        # bytearray is mutable, modify in place based on snapped list
        snapped_list = _snap_sequence(list(data))
        # Create a new bytearray, as modifying length during iteration is tricky
        return bytearray(snapped_list)  # type: ignore[return-value]
    elif isinstance(data, int) and not isinstance(data, bool):  # Exclude bool
        return _snap_int(data)  # type: ignore[return-value]
    elif isinstance(data, float):
        return _snap_float(data)  # type: ignore[return-value]
    elif isinstance(data, (bool, type(None))):
        return data  # Return booleans and None unchanged
    else:
        raise TypeError(f"Unsupported data type for snap: {type(data).__name__}")
