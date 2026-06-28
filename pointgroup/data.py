from __future__ import annotations


def rotation(axis, order, label=None, step=1):
    return {
        "kind": "rotation",
        "axis": axis,
        "order": order,
        "angle_degrees": 360 * step / order,
        "label": label or f"C{order}",
    }


def mirror(normal, label="mirror"):
    return {"kind": "mirror", "normal": normal, "label": label}


def inversion():
    return {"kind": "inversion", "label": "inversion"}


def rotoinversion(axis, order, label=None, step=1):
    return {
        "kind": "rotoinversion",
        "axis": axis,
        "order": order,
        "angle_degrees": 360 * step / order,
        "label": label or f"bar {order}",
    }


POINT_GROUPS = {
    "1": {
        "hm": "1",
        "schoenflies": "C1",
        "crystal_system": "triclinic",
        "display_operations": [{"kind": "identity", "label": "E"}],
    },
    "-1": {
        "hm": "-1",
        "schoenflies": "Ci",
        "crystal_system": "triclinic",
        "display_operations": [inversion()],
    },
    "2": {
        "hm": "2",
        "schoenflies": "C2",
        "crystal_system": "monoclinic",
        "display_operations": [rotation([0, 1, 0], 2, "C2 b")],
    },
    "m": {
        "hm": "m",
        "schoenflies": "Cs",
        "crystal_system": "monoclinic",
        "display_operations": [mirror([0, 1, 0], "mirror")],
    },
    "2/m": {
        "hm": "2/m",
        "schoenflies": "C2h",
        "crystal_system": "monoclinic",
        "display_operations": [rotation([0, 1, 0], 2, "C2 b"), mirror([0, 1, 0], "m perp b"), inversion()],
    },
    "222": {
        "hm": "222",
        "schoenflies": "D2",
        "crystal_system": "orthorhombic",
        "display_operations": [rotation([1, 0, 0], 2, "C2 a"), rotation([0, 1, 0], 2, "C2 b"), rotation([0, 0, 1], 2, "C2 c")],
    },
    "mm2": {
        "hm": "mm2",
        "schoenflies": "C2v",
        "crystal_system": "orthorhombic",
        "display_operations": [rotation([0, 0, 1], 2, "C2 c"), mirror([1, 0, 0], "m yz"), mirror([0, 1, 0], "m xz")],
    },
    "mmm": {
        "hm": "mmm",
        "schoenflies": "D2h",
        "crystal_system": "orthorhombic",
        "display_operations": [rotation([1, 0, 0], 2, "C2 a"), rotation([0, 1, 0], 2, "C2 b"), rotation([0, 0, 1], 2, "C2 c"), mirror([1, 0, 0], "m yz"), mirror([0, 1, 0], "m xz"), mirror([0, 0, 1], "m xy"), inversion()],
    },
    "4": {
        "hm": "4",
        "schoenflies": "C4",
        "crystal_system": "tetragonal",
        "display_operations": [rotation([0, 0, 1], 4, "C4 c")],
    },
    "-4": {
        "hm": "-4",
        "schoenflies": "S4",
        "crystal_system": "tetragonal",
        "display_operations": [rotoinversion([0, 0, 1], 4, "bar 4 c")],
    },
    "4/m": {
        "hm": "4/m",
        "schoenflies": "C4h",
        "crystal_system": "tetragonal",
        "display_operations": [rotation([0, 0, 1], 4, "C4 c"), mirror([0, 0, 1], "m xy"), inversion()],
    },
    "422": {
        "hm": "422",
        "schoenflies": "D4",
        "crystal_system": "tetragonal",
        "display_operations": [rotation([0, 0, 1], 4, "C4 c"), rotation([1, 0, 0], 2, "C2 a"), rotation([0, 1, 0], 2, "C2 b")],
    },
    "4mm": {
        "hm": "4mm",
        "schoenflies": "C4v",
        "crystal_system": "tetragonal",
        "display_operations": [rotation([0, 0, 1], 4, "C4 c"), mirror([1, 0, 0], "m yz"), mirror([0, 1, 0], "m xz")],
    },
    "-42m": {
        "hm": "-42m",
        "schoenflies": "D2d",
        "crystal_system": "tetragonal",
        "display_operations": [rotoinversion([0, 0, 1], 4, "bar 4 c"), rotation([1, 0, 0], 2, "C2 a"), mirror([1, 1, 0], "diagonal m")],
    },
    "4/mmm": {
        "hm": "4/mmm",
        "schoenflies": "D4h",
        "crystal_system": "tetragonal",
        "display_operations": [rotation([0, 0, 1], 4, "C4 c"), rotation([1, 0, 0], 2, "C2 a"), mirror([0, 0, 1], "m xy"), inversion()],
    },
    "3": {
        "hm": "3",
        "schoenflies": "C3",
        "crystal_system": "trigonal",
        "display_operations": [rotation([0, 0, 1], 3, "C3 c")],
    },
    "-3": {
        "hm": "-3",
        "schoenflies": "C3i",
        "crystal_system": "trigonal",
        "display_operations": [rotation([0, 0, 1], 3, "C3 c"), inversion()],
    },
    "32": {
        "hm": "32",
        "schoenflies": "D3",
        "crystal_system": "trigonal",
        "display_operations": [rotation([0, 0, 1], 3, "C3 c"), rotation([1, 0, 0], 2, "C2 a")],
    },
    "3m": {
        "hm": "3m",
        "schoenflies": "C3v",
        "crystal_system": "trigonal",
        "display_operations": [rotation([0, 0, 1], 3, "C3 c"), mirror([1, 0, 0], "vertical m")],
    },
    "-3m": {
        "hm": "-3m",
        "schoenflies": "D3d",
        "crystal_system": "trigonal",
        "display_operations": [rotation([0, 0, 1], 3, "C3 c"), mirror([1, 0, 0], "vertical m"), inversion()],
    },
    "6": {
        "hm": "6",
        "schoenflies": "C6",
        "crystal_system": "hexagonal",
        "display_operations": [rotation([0, 0, 1], 6, "C6 c")],
    },
    "-6": {
        "hm": "-6",
        "schoenflies": "C3h",
        "crystal_system": "hexagonal",
        "display_operations": [rotoinversion([0, 0, 1], 6, "bar 6 c"), mirror([0, 0, 1], "m xy")],
    },
    "6/m": {
        "hm": "6/m",
        "schoenflies": "C6h",
        "crystal_system": "hexagonal",
        "display_operations": [rotation([0, 0, 1], 6, "C6 c"), mirror([0, 0, 1], "m xy"), inversion()],
    },
    "622": {
        "hm": "622",
        "schoenflies": "D6",
        "crystal_system": "hexagonal",
        "display_operations": [rotation([0, 0, 1], 6, "C6 c"), rotation([1, 0, 0], 2, "C2 a")],
    },
    "6mm": {
        "hm": "6mm",
        "schoenflies": "C6v",
        "crystal_system": "hexagonal",
        "display_operations": [rotation([0, 0, 1], 6, "C6 c"), mirror([1, 0, 0], "vertical m")],
    },
    "-6m2": {
        "hm": "-6m2",
        "schoenflies": "D3h",
        "crystal_system": "hexagonal",
        "display_operations": [rotation([0, 0, 1], 3, "C3 c"), mirror([0, 0, 1], "horizontal m"), rotation([1, 0, 0], 2, "C2 a")],
    },
    "6/mmm": {
        "hm": "6/mmm",
        "schoenflies": "D6h",
        "crystal_system": "hexagonal",
        "display_operations": [rotation([0, 0, 1], 6, "C6 c"), rotation([1, 0, 0], 2, "C2 a"), mirror([0, 0, 1], "m xy"), inversion()],
    },
    "23": {
        "hm": "23",
        "schoenflies": "T",
        "crystal_system": "cubic",
        "display_operations": [rotation([1, 1, 1], 3, "C3 body diagonal"), rotation([1, 0, 0], 2, "C2 edge")],
    },
    "m-3": {
        "hm": "m-3",
        "schoenflies": "Th",
        "crystal_system": "cubic",
        "display_operations": [rotation([1, 1, 1], 3, "C3 body diagonal"), rotation([1, 0, 0], 2, "C2 edge"), inversion()],
    },
    "432": {
        "hm": "432",
        "schoenflies": "O",
        "crystal_system": "cubic",
        "display_operations": [rotation([0, 0, 1], 4, "C4 face axis"), rotation([1, 1, 1], 3, "C3 body diagonal"), rotation([1, 1, 0], 2, "C2 edge axis")],
    },
    "-43m": {
        "hm": "-43m",
        "schoenflies": "Td",
        "crystal_system": "cubic",
        "display_operations": [rotation([1, 1, 1], 3, "C3 body diagonal"), rotoinversion([0, 0, 1], 4, "bar 4 face axis"), mirror([1, 1, 0], "diagonal m")],
    },
    "m-3m": {
        "hm": "m-3m",
        "schoenflies": "Oh",
        "crystal_system": "cubic",
        "display_operations": [rotation([0, 0, 1], 4, "C4 face axis"), rotation([1, 1, 1], 3, "C3 body diagonal"), rotation([1, 1, 0], 2, "C2 edge axis"), inversion()],
    },
}


def get_point_group(symbol: str) -> dict:
    try:
        return POINT_GROUPS[symbol]
    except KeyError as exc:
        raise KeyError(f"Unknown point group: {symbol}") from exc


def all_point_group_symbols() -> list[str]:
    return list(POINT_GROUPS.keys())
