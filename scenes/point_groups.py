from __future__ import annotations

import numpy as np

from manimlib import *

from pointgroup.data import all_point_group_symbols, get_point_group
from pointgroup.geometry import axis_endpoints, mirror_plane_rotation
from pointgroup.operations import (
    inversion_matrix,
    operation_label,
    reflection_matrix,
    rotation_matrix,
    rotoinversion_matrix,
)
from pointgroup.styles import (
    AXIS_COLORS,
    BACKGROUND_COLOR,
    CRYSTAL_COLOR,
    INVERSION_COLOR,
    MIRROR_COLOR,
    TEXT_COLOR,
)


PROBE_ROD_COLORS = (YELLOW, ORANGE)
PROBE_BEAD_COLORS = (YELLOW, ORANGE, RED)
IMPROPER_ROD_COLORS = ("#38bdf8", "#818cf8")
IMPROPER_BEAD_COLORS = ("#22d3ee", "#38bdf8", "#a78bfa")
LATEX_PREAMBLE = "\\usepackage{amsmath}\n\\usepackage{xcolor}"

HM_TEX = {
    "1": r"1",
    "-1": r"\bar{1}",
    "2": r"2",
    "m": r"\mathrm{m}",
    "2/m": r"2/\mathrm{m}",
    "222": r"222",
    "mm2": r"\mathrm{mm}2",
    "mmm": r"\mathrm{mmm}",
    "4": r"4",
    "-4": r"\bar{4}",
    "4/m": r"4/\mathrm{m}",
    "422": r"422",
    "4mm": r"4\mathrm{mm}",
    "-42m": r"\bar{4}2\mathrm{m}",
    "4/mmm": r"4/\mathrm{mmm}",
    "3": r"3",
    "-3": r"\bar{3}",
    "32": r"32",
    "3m": r"3\mathrm{m}",
    "-3m": r"\bar{3}\mathrm{m}",
    "6": r"6",
    "-6": r"\bar{6}",
    "6/m": r"6/\mathrm{m}",
    "622": r"622",
    "6mm": r"6\mathrm{mm}",
    "-6m2": r"\bar{6}\mathrm{m}2",
    "6/mmm": r"6/\mathrm{mmm}",
    "23": r"23",
    "m-3": r"\mathrm{m}\bar{3}",
    "432": r"432",
    "-43m": r"\bar{4}3\mathrm{m}",
    "m-3m": r"\mathrm{m}\bar{3}\mathrm{m}",
}

SCHOENFLIES_TEX = {
    "C1": r"\mathrm{C}_{1}",
    "Ci": r"\mathrm{C}_{i}",
    "C2": r"\mathrm{C}_{2}",
    "Cs": r"\mathrm{C}_{s}",
    "C2h": r"\mathrm{C}_{2h}",
    "D2": r"\mathrm{D}_{2}",
    "C2v": r"\mathrm{C}_{2v}",
    "D2h": r"\mathrm{D}_{2h}",
    "C4": r"\mathrm{C}_{4}",
    "S4": r"\mathrm{S}_{4}",
    "C4h": r"\mathrm{C}_{4h}",
    "D4": r"\mathrm{D}_{4}",
    "C4v": r"\mathrm{C}_{4v}",
    "D2d": r"\mathrm{D}_{2d}",
    "D4h": r"\mathrm{D}_{4h}",
    "C3": r"\mathrm{C}_{3}",
    "C3i": r"\mathrm{C}_{3i}",
    "D3": r"\mathrm{D}_{3}",
    "C3v": r"\mathrm{C}_{3v}",
    "D3d": r"\mathrm{D}_{3d}",
    "C6": r"\mathrm{C}_{6}",
    "C3h": r"\mathrm{C}_{3h}",
    "C6h": r"\mathrm{C}_{6h}",
    "D6": r"\mathrm{D}_{6}",
    "C6v": r"\mathrm{C}_{6v}",
    "D3h": r"\mathrm{D}_{3h}",
    "D6h": r"\mathrm{D}_{6h}",
    "T": r"\mathrm{T}",
    "Th": r"\mathrm{T}_{h}",
    "O": r"\mathrm{O}",
    "Td": r"\mathrm{T}_{d}",
    "Oh": r"\mathrm{O}_{h}",
}


def operation_matrix_from_dict(operation):
    kind = operation.get("kind")
    if kind == "rotation":
        return rotation_matrix(operation["axis"], operation["angle_degrees"])
    if kind == "mirror":
        return reflection_matrix(operation["normal"])
    if kind == "inversion":
        return inversion_matrix()
    if kind == "rotoinversion":
        return rotoinversion_matrix(operation["axis"], operation["angle_degrees"])
    return np.identity(3)


class PointGroupScene(ThreeDScene):
    point_group_symbol = "4"
    crystal_shape = "prism"
    latex_matrix_available = True
    latex_title_available = True

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.frame.reorient(35, 65, 0, height=7)

        group = get_point_group(self.point_group_symbol)
        crystal_body, probe = self.make_crystal_parts()
        operated_object = Group(crystal_body, probe)
        axes = self.make_reference_axes()
        title = self.make_title(group)
        title.fix_in_frame()

        self.add(axes, crystal_body, title)
        self.add(probe, set_depth_test=False)
        probe.deactivate_depth_test()
        self.wait(0.4)

        for operation in group["display_operations"]:
            label = self.make_operation_label(operation)
            label.fix_in_frame()
            self.play(FadeIn(label, shift=0.15 * UP), run_time=0.4)
            self.show_operation(operation, operated_object)
            self.play(FadeOut(label, shift=0.15 * DOWN), run_time=0.25)

        self.wait(0.5)

    def make_title(self, group, detail_text=None):
        hm_tex = HM_TEX.get(group["hm"], group["hm"])
        schoenflies_tex = SCHOENFLIES_TEX.get(group["schoenflies"], group["schoenflies"])
        detail = detail_text or group["crystal_system"]
        title = VGroup(
            self.make_title_tex(
                rf"{hm_tex}\quad|\quad{schoenflies_tex}",
                fallback=f"{group['hm']} | {group['schoenflies']}",
            ),
            Text(detail, font_size=18, color=TEXT_COLOR),
        )
        title.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        title.to_corner(UL, buff=0.18)
        return title

    def make_title_tex(self, tex_string, fallback):
        if self.__class__.latex_title_available:
            try:
                return Tex(
                    tex_string,
                    font_size=30,
                    color=TEXT_COLOR,
                    template="empty_ctex",
                    additional_preamble=LATEX_PREAMBLE,
                )
            except Exception:
                self.__class__.latex_title_available = False
        return Text(fallback, font_size=30, color=TEXT_COLOR)

    def make_operation_label(self, operation):
        label = self.make_matrix_label(
            operation_label(operation),
            self.operation_matrix(operation),
            label_font_size=24,
            matrix_font_size=17,
        )
        return label

    def operation_matrix(self, operation):
        return operation_matrix_from_dict(operation)

    def make_matrix_label(self, label_text, matrix, label_font_size=24, matrix_font_size=17):
        label = Text(label_text, font_size=label_font_size, color=TEXT_COLOR)
        matrix_mobject = self.make_matrix_mobject(matrix, matrix_font_size)
        group = VGroup(label, matrix_mobject)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        if group.get_width() > 4.45:
            group.set_width(4.45)
        group.to_corner(UR, buff=0.18)
        return group

    def make_matrix_mobject(self, matrix, matrix_font_size):
        if self.__class__.latex_matrix_available:
            try:
                return Tex(
                    self.matrix_tex_string(matrix),
                    font_size=matrix_font_size * 1.35,
                    color=TEXT_COLOR,
                    template="empty_ctex",
                    additional_preamble=LATEX_PREAMBLE,
                )
            except Exception:
                self.__class__.latex_matrix_available = False
        return self.make_matrix_fallback(matrix, matrix_font_size)

    def make_matrix_fallback(self, matrix, matrix_font_size):
        entries = VGroup()
        cell_width = 0.42
        cell_height = 0.28
        for row_index, row in enumerate(np.asarray(matrix)):
            for col_index, value in enumerate(row):
                entry = Text(
                    self.matrix_entry_plain_text(value),
                    font_size=matrix_font_size,
                    color=TEXT_COLOR,
                    font="Consolas",
                )
                entry.move_to(
                    (col_index - 1) * cell_width * RIGHT
                    + (1 - row_index) * cell_height * UP
                )
                entries.add(entry)

        left_bracket = Text("[", font_size=matrix_font_size * 4.0, color=TEXT_COLOR)
        right_bracket = Text("]", font_size=matrix_font_size * 4.0, color=TEXT_COLOR)
        left_bracket.next_to(entries, LEFT, buff=0.03)
        right_bracket.next_to(entries, RIGHT, buff=0.03)
        return VGroup(left_bracket, entries, right_bracket)

    def matrix_tex_string(self, matrix):
        rows = [
            " & ".join(self.matrix_entry_tex(value) for value in row)
            for row in np.asarray(matrix)
        ]
        return r"\begin{bmatrix}" + r" \\ ".join(rows) + r"\end{bmatrix}"

    def matrix_entry_tex(self, value):
        if abs(value) < 1e-8:
            return "0"
        rounded = round(value)
        if abs(value - rounded) < 1e-8:
            return str(int(rounded))
        for target, expression in [
            (np.sqrt(3) / 2, r"\frac{\sqrt{3}}{2}"),
            (np.sqrt(2) / 2, r"\frac{\sqrt{2}}{2}"),
            (1 / 2, r"\frac{1}{2}"),
            (1 / 3, r"\frac{1}{3}"),
            (2 / 3, r"\frac{2}{3}"),
            (np.sqrt(3) / 3, r"\frac{\sqrt{3}}{3}"),
            (np.sqrt(6) / 3, r"\frac{\sqrt{6}}{3}"),
        ]:
            if abs(value - target) < 1e-8:
                return expression
            if abs(value + target) < 1e-8:
                return "-" + expression
        return f"{value:.2f}"

    def matrix_entry_plain_text(self, value):
        tex = self.matrix_entry_tex(value)
        replacements = {
            r"\frac{\sqrt{3}}{2}": "sqrt(3)/2",
            r"\frac{\sqrt{2}}{2}": "sqrt(2)/2",
            r"\frac{1}{2}": "1/2",
            r"\frac{1}{3}": "1/3",
            r"\frac{2}{3}": "2/3",
            r"\frac{\sqrt{3}}{3}": "sqrt(3)/3",
            r"\frac{\sqrt{6}}{3}": "sqrt(6)/3",
        }
        for source, target in replacements.items():
            tex = tex.replace(source, target)
        return tex

    def make_reference_axes(self):
        items = Group()
        for axis, color, label, offset in [
            ([1, 0, 0], RED, "x", RIGHT),
            ([0, 1, 0], GREEN, "y", UP),
            ([0, 0, 1], BLUE, "z", OUT),
        ]:
            start, end = axis_endpoints(axis, 5.0)
            line = Line3D(start, end, width=0.025, color=color)
            text = Text(label, font_size=18, color=color)
            text.move_to(end + 0.25 * np.array(offset))
            items.add(line, text)
        return items

    def make_crystal_parts(self):
        if self.crystal_shape == "cube":
            crystal = self.make_wireframe_box(1.7, 1.7, 1.7)
        elif self.crystal_shape == "hex":
            crystal = self.make_wireframe_hex_prism(radius=1.0, depth=2.0)
        else:
            crystal = self.make_wireframe_box(1.35, 1.8, 2.2)
        probe = self.make_asymmetric_probe()
        probe.add_updater(lambda mob: mob.deactivate_depth_test())
        return crystal, probe

    def make_wireframe_box(self, width, height, depth):
        x = width / 2
        y = height / 2
        z = depth / 2
        vertices = [
            np.array([sx * x, sy * y, sz * z])
            for sx in (-1, 1)
            for sy in (-1, 1)
            for sz in (-1, 1)
        ]
        edges = []
        for i, start in enumerate(vertices):
            for j, end in enumerate(vertices):
                if j <= i:
                    continue
                if np.sum(np.abs(np.sign(start) - np.sign(end)) > 0) == 1:
                    edge = Line3D(start, end, width=0.025, color=CRYSTAL_COLOR)
                    edge.set_opacity(0.38)
                    edges.append(edge)
        return Group(*edges)

    def make_wireframe_hex_prism(self, radius=1.0, depth=2.0):
        angles = [k * TAU / 6 for k in range(6)]
        top = [
            np.array([radius * np.cos(angle), radius * np.sin(angle), depth / 2])
            for angle in angles
        ]
        bottom = [
            np.array([radius * np.cos(angle), radius * np.sin(angle), -depth / 2])
            for angle in angles
        ]
        edges = []
        for layer in (top, bottom):
            for index in range(6):
                edge = Line3D(layer[index], layer[(index + 1) % 6], width=0.025, color=CRYSTAL_COLOR)
                edge.set_opacity(0.38)
                edges.append(edge)
        for index in range(6):
            edge = Line3D(bottom[index], top[index], width=0.025, color=CRYSTAL_COLOR)
            edge.set_opacity(0.38)
            edges.append(edge)
        return Group(*edges)

    def make_asymmetric_probe(self):
        base = 0.62 * RIGHT + 0.28 * UP + 0.42 * OUT
        points = [
            base,
            base + 0.34 * RIGHT + 0.11 * UP + 0.05 * OUT,
            base - 0.08 * RIGHT + 0.31 * UP + 0.24 * OUT,
        ]
        radii = [0.12, 0.085, 0.065]
        beads = Group(*[
            Sphere(radius=radius, color=color).move_to(point)
            for point, radius, color in zip(points, radii, PROBE_BEAD_COLORS)
        ])
        rods = Group(
            Line3D(points[0], points[1], width=0.035, color=PROBE_ROD_COLORS[0]),
            Line3D(points[0], points[2], width=0.025, color=PROBE_ROD_COLORS[1]),
        )
        return Group(rods, beads)

    def show_operation(self, operation, crystal):
        kind = operation.get("kind")
        if kind == "rotation":
            self.show_rotation(operation, crystal)
        elif kind == "mirror":
            self.show_mirror(operation, crystal)
        elif kind == "inversion":
            self.show_inversion(crystal)
        elif kind == "rotoinversion":
            self.show_rotoinversion(operation, crystal)
        else:
            self.wait(0.5)

    def show_rotation(self, operation, crystal):
        axis = np.array(operation["axis"], dtype=float)
        order = operation["order"]
        color = AXIS_COLORS.get(order, "#f8fafc")
        start, end = axis_endpoints(axis, 5.2)
        rotation_axis = Line3D(start, end, width=0.07, color=color)
        self.play(GrowFromCenter(rotation_axis), run_time=0.35)
        self.play(
            Rotate(
                crystal,
                angle=operation["angle_degrees"] * DEGREES,
                axis=axis,
                about_point=ORIGIN,
            ),
            run_time=1.3,
        )
        self.play(FadeOut(rotation_axis), run_time=0.25)

    def show_mirror(self, operation, crystal):
        angle, axis = mirror_plane_rotation(operation["normal"])
        plane = Square3D(side_length=3.3, color=MIRROR_COLOR, opacity=0.22)
        plane.rotate(angle, axis=axis, about_point=ORIGIN)
        self.play(FadeIn(plane), run_time=0.35)
        self.play(
            ApplyMatrix(reflection_matrix(operation["normal"]), crystal),
            Flash(ORIGIN, color=MIRROR_COLOR),
            run_time=1.0,
        )
        self.play(FadeOut(plane), run_time=0.35)

    def show_inversion(self, crystal):
        center = Sphere(radius=0.18, color=INVERSION_COLOR)
        self.play(FadeIn(center), run_time=0.25)
        self.play(
            ApplyMatrix(inversion_matrix(), crystal),
            Flash(ORIGIN, color=INVERSION_COLOR),
            run_time=1.0,
        )
        self.play(FadeOut(center), run_time=0.25)

    def show_rotoinversion(self, operation, crystal):
        axis = np.array(operation["axis"], dtype=float)
        order = operation["order"]
        color = AXIS_COLORS.get(order, "#f8fafc")
        start, end = axis_endpoints(axis, 5.2)
        improper_axis = Line3D(start, end, width=0.08, color=color)
        center = Sphere(radius=0.14, color=INVERSION_COLOR)
        self.play(GrowFromCenter(improper_axis), FadeIn(center), run_time=0.35)
        self.play(
            ApplyMatrix(
                rotoinversion_matrix(axis, operation["angle_degrees"]),
                crystal,
            ),
            Flash(ORIGIN, color=color),
            run_time=1.2,
        )
        self.play(FadeOut(improper_axis), FadeOut(center), run_time=0.25)


def rounded_matrix_key(matrix, decimals=6):
    rounded = np.round(np.asarray(matrix, dtype=float), decimals=decimals)
    rounded[np.abs(rounded) < 10 ** (-decimals)] = 0
    return tuple(rounded.flatten())


def matrix_order(matrix, max_order=48):
    current = np.identity(3)
    for order in range(1, max_order + 1):
        current = matrix @ current
        if np.allclose(current, np.identity(3), atol=1e-6):
            return order
    return None


def matrix_axis_for_eigenvalue(matrix, eigenvalue):
    values, vectors = np.linalg.eig(matrix)
    index = int(np.argmin(np.abs(values - eigenvalue)))
    vector = np.real(vectors[:, index])
    norm = np.linalg.norm(vector)
    if norm < 1e-8:
        return np.array([0, 0, 1], dtype=float)
    vector = vector / norm
    first_nonzero = np.flatnonzero(np.abs(vector) > 1e-6)
    if len(first_nonzero) and vector[first_nonzero[0]] < 0:
        vector = -vector
    return vector


def signed_rotation_angle_degrees(matrix, axis):
    matrix = np.asarray(matrix, dtype=float)
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    cosine = np.clip((np.trace(matrix) - 1) / 2, -1, 1)
    sine_vector = np.array([
        matrix[2, 1] - matrix[1, 2],
        matrix[0, 2] - matrix[2, 0],
        matrix[1, 0] - matrix[0, 1],
    ]) / 2
    sine = float(np.dot(sine_vector, axis))
    angle = np.degrees(np.arctan2(sine, cosine))
    if angle < 0:
        angle += 360
    if abs(angle - 360) < 1e-6:
        angle = 0
    return angle


def angle_text(angle):
    rounded = round(angle)
    if abs(angle - rounded) < 1e-6:
        return f"{int(rounded)} deg"
    return f"{angle:.1f} deg"


def direction_text(vector):
    vector = np.asarray(vector, dtype=float)
    if np.linalg.norm(vector) < 1e-8:
        return "(0, 0, 0)"
    scaled = vector / np.max(np.abs(vector))
    scaled[np.abs(scaled) < 1e-6] = 0
    integer = np.round(scaled).astype(int)
    if np.allclose(scaled, integer, atol=1e-6):
        return "(" + ", ".join(str(value) for value in integer) + ")"
    return "(" + ", ".join(f"{value:.2f}" if abs(value) > 1e-6 else "0" for value in scaled) + ")"


def generated_full_operations(group):
    generators = []
    for operation in group["display_operations"]:
        matrix = operation_matrix_from_dict(operation)
        if not np.allclose(matrix, np.identity(3), atol=1e-6):
            generators.append(matrix)

    identity = np.identity(3)
    operations = [identity]
    seen = {rounded_matrix_key(identity)}
    index = 0
    while index < len(operations):
        current = operations[index]
        for generator in generators:
            candidate = generator @ current
            key = rounded_matrix_key(candidate)
            if key not in seen:
                seen.add(key)
                operations.append(candidate)
        index += 1
        if len(operations) > 96:
            raise ValueError(f"Generated too many operations for {group['hm']}")
    return operations


def operation_metadata(matrix):
    det = round(float(np.linalg.det(matrix)))
    order = matrix_order(matrix)
    if np.allclose(matrix, np.identity(3), atol=1e-6):
        return {
            "class": "identity",
            "sort_key": (0, 0, 0, rounded_matrix_key(matrix)),
            "description": "identity operation E",
            "marker": {"kind": "identity"},
        }
    if np.allclose(matrix, -np.identity(3), atol=1e-6):
        return {
            "class": "inversion",
            "sort_key": (3, 0, 0, rounded_matrix_key(matrix)),
            "description": "inversion through center",
            "marker": {"kind": "center"},
        }
    if det == 1:
        axis = matrix_axis_for_eigenvalue(matrix, 1)
        angle = signed_rotation_angle_degrees(matrix, axis)
        return {
            "class": "rotation",
            "sort_key": (1, order or 99, round(angle, 6), direction_text(axis)),
            "description": f"C{order or '?'} rotation {angle_text(angle)}\naxis {direction_text(axis)}",
            "marker": {
                "kind": "axis",
                "axis": axis,
                "order": order or 2,
            },
        }
    if order == 2:
        normal = matrix_axis_for_eigenvalue(matrix, -1)
        return {
            "class": "mirror",
            "sort_key": (2, 0, 0, direction_text(normal)),
            "description": f"mirror plane\nnormal {direction_text(normal)}",
            "marker": {
                "kind": "plane",
                "normal": normal,
            },
        }
    axis = matrix_axis_for_eigenvalue(matrix, -1)
    rotation_part = -np.asarray(matrix, dtype=float)
    angle = signed_rotation_angle_degrees(rotation_part, axis)
    return {
        "class": "rotoinversion",
        "sort_key": (4, order or 99, round(angle, 6), direction_text(axis)),
        "description": f"rotoinversion bar {order or '?'}: rotate {angle_text(angle)}\naxis {direction_text(axis)}, then invert",
        "marker": {
            "kind": "rotoaxis",
            "axis": axis,
            "order": order or 4,
        },
    }


def operation_type_rank(metadata):
    ranks = {
        "identity": 0,
        "rotation": 1,
        "mirror": 2,
        "inversion": 3,
        "rotoinversion": 4,
    }
    return ranks.get(metadata["class"], 9)


def conjugacy_class_sort_key(class_items):
    metadata = class_items[0][1]
    return (
        operation_type_rank(metadata),
        metadata["sort_key"],
        len(class_items),
    )


def conjugacy_sorted_full_operations(group):
    operations = generated_full_operations(group)
    by_key = {rounded_matrix_key(matrix): matrix for matrix in operations}
    remaining = set(by_key)
    classes = []

    while remaining:
        seed_key = min(remaining)
        seed = by_key[seed_key]
        class_keys = set()
        for h in operations:
            conjugate = h @ seed @ np.linalg.inv(h)
            class_keys.add(rounded_matrix_key(conjugate))

        class_keys &= set(by_key)
        remaining -= class_keys
        class_items = []
        for key in class_keys:
            matrix = by_key[key]
            class_items.append((matrix, operation_metadata(matrix)))
        class_items.sort(key=lambda item: item[1]["sort_key"])
        classes.append(class_items)

    classes.sort(key=conjugacy_class_sort_key)
    flattened = []
    for class_index, class_items in enumerate(classes, start=1):
        class_size = len(class_items)
        for element_index, (matrix, metadata) in enumerate(class_items, start=1):
            enriched = dict(metadata)
            enriched["conjugacy_class_index"] = class_index
            enriched["conjugacy_class_count"] = len(classes)
            enriched["conjugacy_class_size"] = class_size
            enriched["class_element_index"] = element_index
            flattened.append((matrix, enriched))
    return flattened


def sorted_full_operations(group):
    items = []
    for matrix in generated_full_operations(group):
        metadata = operation_metadata(matrix)
        items.append((metadata["sort_key"], matrix, metadata))
    items.sort(key=lambda item: item[0])
    return [(matrix, metadata) for _, matrix, metadata in items]


def full_operation_label(index, total, metadata):
    prefix = f"{index:02d}/{total}"
    class_prefix = (
        f"Class {metadata['conjugacy_class_index']}/{metadata['conjugacy_class_count']} "
        f"elem {metadata['class_element_index']}/{metadata['conjugacy_class_size']}"
    )
    return f"{prefix}  {class_prefix}\n{metadata['description']}"


def full_operation_marker(matrix):
    return operation_metadata(matrix)["marker"]


class FullClosurePointGroupScene(PointGroupScene):
    point_group_symbol = "mmm"
    crystal_shape = "prism"

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.frame.reorient(35, 65, 0, height=7)

        group = get_point_group(self.point_group_symbol)
        operations = conjugacy_sorted_full_operations(group)
        total = len(operations)
        crystal_body, probe = self.make_crystal_parts()
        operated_object = Group(crystal_body, probe)
        axes = self.make_reference_axes()
        title = self.make_title(
            group,
            detail_text=f"{group['crystal_system']} full group | {total} elements",
        )
        title.fix_in_frame()

        self.add(axes, crystal_body, title)
        self.add(probe, set_depth_test=False)
        probe.deactivate_depth_test()
        self.wait(0.3)

        move_time = 0.8 if total <= 8 else 0.58 if total <= 24 else 0.42
        reset_time = 0.4 if total <= 8 else 0.28 if total <= 24 else 0.2
        label_font = 22
        matrix_font = 16

        for index, (target_matrix, metadata) in enumerate(operations, start=1):
            label = self.make_matrix_label(
                full_operation_label(index, total, metadata),
                target_matrix,
                label_font_size=label_font,
                matrix_font_size=matrix_font,
            )
            label.fix_in_frame()
            self.play(FadeIn(label, shift=0.15 * UP), run_time=0.15)
            self.show_full_operation_marker(metadata["marker"])
            self.play(ApplyMatrix(target_matrix, operated_object), run_time=move_time)
            is_improper = np.linalg.det(target_matrix) < -0.5
            if is_improper:
                self.set_probe_colors(probe, IMPROPER_BEAD_COLORS, IMPROPER_ROD_COLORS, run_time=0.18)
                self.wait(0.12)
            else:
                self.wait(0.08)
            self.play(ApplyMatrix(np.linalg.inv(target_matrix), operated_object), run_time=reset_time)
            if is_improper:
                self.set_probe_colors(probe, PROBE_BEAD_COLORS, PROBE_ROD_COLORS, run_time=0.14)
            self.play(FadeOut(label, shift=0.15 * DOWN), run_time=0.1)

        self.wait(0.35)

    def set_probe_colors(self, probe, bead_colors, rod_colors, run_time=0.16):
        rods, beads = probe
        animations = []
        for rod, color in zip(rods, rod_colors):
            animations.append(rod.animate.set_color(color))
        for bead, color in zip(beads, bead_colors):
            animations.append(bead.animate.set_color(color))
        self.play(*animations, run_time=run_time)

    def show_full_operation_marker(self, marker):
        kind = marker["kind"]
        if kind == "axis":
            order = marker.get("order", 2)
            color = AXIS_COLORS.get(order, "#f8fafc")
            start, end = axis_endpoints(marker["axis"], 5.2)
            axis = Line3D(start, end, width=0.07, color=color)
            self.play(GrowFromCenter(axis), run_time=0.14)
            self.play(FadeOut(axis), run_time=0.14)
        elif kind == "plane":
            angle, axis = mirror_plane_rotation(marker["normal"])
            plane = Square3D(side_length=3.3, color=MIRROR_COLOR, opacity=0.22)
            plane.rotate(angle, axis=axis, about_point=ORIGIN)
            self.play(FadeIn(plane), run_time=0.14)
            self.play(FadeOut(plane), run_time=0.14)
        elif kind == "center":
            center = Sphere(radius=0.18, color=INVERSION_COLOR)
            self.play(FadeIn(center), run_time=0.14)
            self.play(FadeOut(center), run_time=0.14)
        elif kind == "rotoaxis":
            order = marker.get("order", 4)
            color = AXIS_COLORS.get(order, "#f8fafc")
            start, end = axis_endpoints(marker["axis"], 5.2)
            axis = Line3D(start, end, width=0.08, color=color)
            center = Sphere(radius=0.14, color=INVERSION_COLOR)
            self.play(GrowFromCenter(axis), FadeIn(center), run_time=0.14)
            self.play(FadeOut(axis), FadeOut(center), run_time=0.14)
        else:
            self.wait(0.14)


class PointGroup4(PointGroupScene):
    point_group_symbol = "4"
    crystal_shape = "prism"


class PointGroupMMM(PointGroupScene):
    point_group_symbol = "mmm"
    crystal_shape = "prism"


class PointGroup432(PointGroupScene):
    point_group_symbol = "432"
    crystal_shape = "cube"


class PointGroupMinus4(PointGroupScene):
    point_group_symbol = "-4"
    crystal_shape = "prism"


class PointGroupMinus42M(PointGroupScene):
    point_group_symbol = "-42m"
    crystal_shape = "prism"


class PointGroupMinus43M(PointGroupScene):
    point_group_symbol = "-43m"
    crystal_shape = "cube"


class PointGroupMMMFullOperations(PointGroupScene):
    point_group_symbol = "mmm"
    crystal_shape = "prism"

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.frame.reorient(35, 65, 0, height=7)

        group = get_point_group(self.point_group_symbol)
        crystal_body, probe = self.make_crystal_parts()
        operated_object = Group(crystal_body, probe)
        axes = self.make_reference_axes()
        title = Text(
            f"{group['hm']} full operations  |  {group['schoenflies']}  |  8 elements",
            font_size=30,
            color=TEXT_COLOR,
        )
        title.to_corner(UL)
        title.fix_in_frame()

        self.add(axes, crystal_body, title)
        self.add(probe, set_depth_test=False)
        probe.deactivate_depth_test()
        self.wait(0.4)

        current_matrix = np.identity(3)
        for label_text, target_matrix, marker in self.mmm_full_operations():
            label = self.make_matrix_label(label_text, target_matrix, label_font_size=24, matrix_font_size=17)
            label.fix_in_frame()
            self.play(FadeIn(label, shift=0.15 * UP), run_time=0.25)
            self.show_full_operation_marker(marker)
            delta = target_matrix @ np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(delta, operated_object), run_time=0.8)
            current_matrix = target_matrix
            self.wait(0.25)
            reset = np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(reset, operated_object), run_time=0.45)
            current_matrix = np.identity(3)
            self.play(FadeOut(label, shift=0.15 * DOWN), run_time=0.2)

        self.wait(0.5)

    def mmm_full_operations(self):
        return [
            ("E", np.identity(3), {"kind": "identity"}),
            ("C2 about x", rotation_matrix([1, 0, 0], 180), {"kind": "axis", "axis": [1, 0, 0], "order": 2}),
            ("C2 about y", rotation_matrix([0, 1, 0], 180), {"kind": "axis", "axis": [0, 1, 0], "order": 2}),
            ("C2 about z", rotation_matrix([0, 0, 1], 180), {"kind": "axis", "axis": [0, 0, 1], "order": 2}),
            ("mirror yz", reflection_matrix([1, 0, 0]), {"kind": "plane", "normal": [1, 0, 0]}),
            ("mirror xz", reflection_matrix([0, 1, 0]), {"kind": "plane", "normal": [0, 1, 0]}),
            ("mirror xy", reflection_matrix([0, 0, 1]), {"kind": "plane", "normal": [0, 0, 1]}),
            ("inversion", inversion_matrix(), {"kind": "center"}),
        ]

    def show_full_operation_marker(self, marker):
        kind = marker["kind"]
        if kind == "axis":
            order = marker.get("order", 2)
            color = AXIS_COLORS.get(order, "#f8fafc")
            start, end = axis_endpoints(marker["axis"], 5.2)
            axis = Line3D(start, end, width=0.07, color=color)
            self.play(GrowFromCenter(axis), run_time=0.2)
            self.play(FadeOut(axis), run_time=0.2)
        elif kind == "plane":
            angle, axis = mirror_plane_rotation(marker["normal"])
            plane = Square3D(side_length=3.3, color=MIRROR_COLOR, opacity=0.22)
            plane.rotate(angle, axis=axis, about_point=ORIGIN)
            self.play(FadeIn(plane), run_time=0.2)
            self.play(FadeOut(plane), run_time=0.2)
        elif kind == "center":
            center = Sphere(radius=0.18, color=INVERSION_COLOR)
            self.play(FadeIn(center), run_time=0.2)
            self.play(FadeOut(center), run_time=0.2)
        else:
            self.wait(0.2)


class PointGroupMinus42MFullOperations(PointGroupMMMFullOperations):
    point_group_symbol = "-42m"
    crystal_shape = "prism"

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.frame.reorient(35, 65, 0, height=7)

        group = get_point_group(self.point_group_symbol)
        crystal_body, probe = self.make_crystal_parts()
        operated_object = Group(crystal_body, probe)
        axes = self.make_reference_axes()
        title = Text(
            f"{group['hm']} full operations  |  {group['schoenflies']}  |  8 elements",
            font_size=30,
            color=TEXT_COLOR,
        )
        title.to_corner(UL)
        title.fix_in_frame()

        self.add(axes, crystal_body, title)
        self.add(probe, set_depth_test=False)
        probe.deactivate_depth_test()
        self.wait(0.4)

        current_matrix = np.identity(3)
        for label_text, target_matrix, marker in self.minus42m_full_operations():
            label = self.make_matrix_label(label_text, target_matrix, label_font_size=24, matrix_font_size=17)
            label.fix_in_frame()
            self.play(FadeIn(label, shift=0.15 * UP), run_time=0.25)
            self.show_full_operation_marker(marker)
            delta = target_matrix @ np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(delta, operated_object), run_time=0.8)
            current_matrix = target_matrix
            self.wait(0.25)
            reset = np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(reset, operated_object), run_time=0.45)
            current_matrix = np.identity(3)
            self.play(FadeOut(label, shift=0.15 * DOWN), run_time=0.2)

        self.wait(0.5)

    def minus42m_full_operations(self):
        return [
            ("E", np.identity(3), {"kind": "identity"}),
            ("bar 4 +90 about z", rotoinversion_matrix([0, 0, 1], 90), {"kind": "rotoaxis", "axis": [0, 0, 1], "order": 4}),
            ("C2 about z", rotation_matrix([0, 0, 1], 180), {"kind": "axis", "axis": [0, 0, 1], "order": 2}),
            ("bar 4 -90 about z", rotoinversion_matrix([0, 0, 1], -90), {"kind": "rotoaxis", "axis": [0, 0, 1], "order": 4}),
            ("C2 about x", rotation_matrix([1, 0, 0], 180), {"kind": "axis", "axis": [1, 0, 0], "order": 2}),
            ("C2 about y", rotation_matrix([0, 1, 0], 180), {"kind": "axis", "axis": [0, 1, 0], "order": 2}),
            ("mirror x = y", reflection_matrix([1, -1, 0]), {"kind": "plane", "normal": [1, -1, 0]}),
            ("mirror x = -y", reflection_matrix([1, 1, 0]), {"kind": "plane", "normal": [1, 1, 0]}),
        ]

    def show_full_operation_marker(self, marker):
        if marker["kind"] == "rotoaxis":
            order = marker.get("order", 4)
            color = AXIS_COLORS.get(order, "#f8fafc")
            start, end = axis_endpoints(marker["axis"], 5.2)
            axis = Line3D(start, end, width=0.08, color=color)
            center = Sphere(radius=0.14, color=INVERSION_COLOR)
            self.play(GrowFromCenter(axis), FadeIn(center), run_time=0.2)
            self.play(FadeOut(axis), FadeOut(center), run_time=0.2)
        else:
            super().show_full_operation_marker(marker)


class PointGroupMinus3MFullOperations(PointGroupMMMFullOperations):
    point_group_symbol = "-3m"
    crystal_shape = "hex"

    def make_crystal_parts(self):
        crystal = self.make_wireframe_hex_prism(radius=1.0, depth=2.0)
        probe = self.make_asymmetric_probe()
        probe.add_updater(lambda mob: mob.deactivate_depth_test())
        return crystal, probe

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.frame.reorient(35, 65, 0, height=7)

        group = get_point_group(self.point_group_symbol)
        crystal_body, probe = self.make_crystal_parts()
        operated_object = Group(crystal_body, probe)
        axes = self.make_reference_axes()
        title = Text(
            f"{group['hm']} full operations  |  {group['schoenflies']}  |  12 elements",
            font_size=30,
            color=TEXT_COLOR,
        )
        title.to_corner(UL)
        title.fix_in_frame()

        self.add(axes, crystal_body, title)
        self.add(probe, set_depth_test=False)
        probe.deactivate_depth_test()
        self.wait(0.4)

        current_matrix = np.identity(3)
        for label_text, target_matrix, marker in self.minus3m_full_operations():
            label = self.make_matrix_label(label_text, target_matrix, label_font_size=24, matrix_font_size=17)
            label.fix_in_frame()
            self.play(FadeIn(label, shift=0.15 * UP), run_time=0.25)
            self.show_full_operation_marker(marker)
            delta = target_matrix @ np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(delta, operated_object), run_time=0.8)
            current_matrix = target_matrix
            self.wait(0.25)
            reset = np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(reset, operated_object), run_time=0.45)
            current_matrix = np.identity(3)
            self.play(FadeOut(label, shift=0.15 * DOWN), run_time=0.2)

        self.wait(0.5)

    def minus3m_full_operations(self):
        c2_axes = [
            [np.cos(k * TAU / 3), np.sin(k * TAU / 3), 0]
            for k in range(3)
        ]
        return [
            ("E", np.identity(3), {"kind": "identity"}),
            ("C3 +120 about z", rotation_matrix([0, 0, 1], 120), {"kind": "axis", "axis": [0, 0, 1], "order": 3}),
            ("C3 -120 about z", rotation_matrix([0, 0, 1], -120), {"kind": "axis", "axis": [0, 0, 1], "order": 3}),
            ("C2 axis 0 deg", rotation_matrix(c2_axes[0], 180), {"kind": "axis", "axis": c2_axes[0], "order": 2}),
            ("C2 axis 120 deg", rotation_matrix(c2_axes[1], 180), {"kind": "axis", "axis": c2_axes[1], "order": 2}),
            ("C2 axis 240 deg", rotation_matrix(c2_axes[2], 180), {"kind": "axis", "axis": c2_axes[2], "order": 2}),
            ("inversion", inversion_matrix(), {"kind": "center"}),
            ("bar 3 +120 about z", rotoinversion_matrix([0, 0, 1], 120), {"kind": "rotoaxis", "axis": [0, 0, 1], "order": 3}),
            ("bar 3 -120 about z", rotoinversion_matrix([0, 0, 1], -120), {"kind": "rotoaxis", "axis": [0, 0, 1], "order": 3}),
            ("mirror plane 0 deg", reflection_matrix(c2_axes[0]), {"kind": "plane", "normal": c2_axes[0]}),
            ("mirror plane 120 deg", reflection_matrix(c2_axes[1]), {"kind": "plane", "normal": c2_axes[1]}),
            ("mirror plane 240 deg", reflection_matrix(c2_axes[2]), {"kind": "plane", "normal": c2_axes[2]}),
        ]

    def show_full_operation_marker(self, marker):
        if marker["kind"] == "rotoaxis":
            order = marker.get("order", 3)
            color = AXIS_COLORS.get(order, "#f8fafc")
            start, end = axis_endpoints(marker["axis"], 5.2)
            axis = Line3D(start, end, width=0.08, color=color)
            center = Sphere(radius=0.14, color=INVERSION_COLOR)
            self.play(GrowFromCenter(axis), FadeIn(center), run_time=0.2)
            self.play(FadeOut(axis), FadeOut(center), run_time=0.2)
        else:
            super().show_full_operation_marker(marker)


class PointGroup6MMMFullOperations(PointGroupMMMFullOperations):
    point_group_symbol = "6/mmm"
    crystal_shape = "hex"

    def make_crystal_parts(self):
        crystal = self.make_wireframe_hex_prism(radius=1.0, depth=2.0)
        probe = self.make_asymmetric_probe()
        probe.add_updater(lambda mob: mob.deactivate_depth_test())
        return crystal, probe

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.frame.reorient(35, 65, 0, height=7)

        group = get_point_group(self.point_group_symbol)
        crystal_body, probe = self.make_crystal_parts()
        operated_object = Group(crystal_body, probe)
        axes = self.make_reference_axes()
        title = Text(
            f"{group['hm']} full operations  |  {group['schoenflies']}  |  24 elements",
            font_size=30,
            color=TEXT_COLOR,
        )
        title.to_corner(UL)
        title.fix_in_frame()

        self.add(axes, crystal_body, title)
        self.add(probe, set_depth_test=False)
        probe.deactivate_depth_test()
        self.wait(0.4)

        current_matrix = np.identity(3)
        for label_text, target_matrix, marker in self.six_mmm_full_operations():
            label = self.make_matrix_label(label_text, target_matrix, label_font_size=22, matrix_font_size=16)
            label.fix_in_frame()
            self.play(FadeIn(label, shift=0.15 * UP), run_time=0.2)
            self.show_full_operation_marker(marker)
            delta = target_matrix @ np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(delta, operated_object), run_time=0.65)
            current_matrix = target_matrix
            self.wait(0.15)
            reset = np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(reset, operated_object), run_time=0.35)
            current_matrix = np.identity(3)
            self.play(FadeOut(label, shift=0.15 * DOWN), run_time=0.15)

        self.wait(0.5)

    def six_mmm_full_operations(self):
        operations = []
        for step in range(6):
            angle = 60 * step
            label = "E" if step == 0 else f"C6^{step} about z"
            operations.append((
                label,
                rotation_matrix([0, 0, 1], angle),
                {"kind": "axis", "axis": [0, 0, 1], "order": 6},
            ))

        for index in range(6):
            angle = index * 30 * DEGREES
            axis = [np.cos(angle), np.sin(angle), 0]
            operations.append((
                f"C2 basal axis {index * 30} deg",
                rotation_matrix(axis, 180),
                {"kind": "axis", "axis": axis, "order": 2},
            ))

        for step in range(6):
            angle = 60 * step
            if step == 0:
                label = "inversion"
                marker = {"kind": "center"}
            else:
                label = f"inversion * C6^{step}"
                marker = {"kind": "rotoaxis", "axis": [0, 0, 1], "order": 6}
            operations.append((
                label,
                -rotation_matrix([0, 0, 1], angle),
                marker,
            ))

        for index in range(6):
            angle = index * 30 * DEGREES
            normal = [np.cos(angle), np.sin(angle), 0]
            operations.append((
                f"vertical mirror {index * 30} deg",
                reflection_matrix(normal),
                {"kind": "plane", "normal": normal},
            ))

        return operations

    def show_full_operation_marker(self, marker):
        if marker["kind"] == "rotoaxis":
            order = marker.get("order", 6)
            color = AXIS_COLORS.get(order, "#f8fafc")
            start, end = axis_endpoints(marker["axis"], 5.2)
            axis = Line3D(start, end, width=0.08, color=color)
            center = Sphere(radius=0.14, color=INVERSION_COLOR)
            self.play(GrowFromCenter(axis), FadeIn(center), run_time=0.18)
            self.play(FadeOut(axis), FadeOut(center), run_time=0.18)
        else:
            super().show_full_operation_marker(marker)


class PointGroup432FullOperations(PointGroupMMMFullOperations):
    point_group_symbol = "432"
    crystal_shape = "cube"

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.frame.reorient(35, 65, 0, height=7)

        group = get_point_group(self.point_group_symbol)
        crystal_body, probe = self.make_crystal_parts()
        operated_object = Group(crystal_body, probe)
        axes = self.make_reference_axes()
        title = Text(
            f"{group['hm']} full operations  |  {group['schoenflies']}  |  24 elements",
            font_size=30,
            color=TEXT_COLOR,
        )
        title.to_corner(UL)
        title.fix_in_frame()

        self.add(axes, crystal_body, title)
        self.add(probe, set_depth_test=False)
        probe.deactivate_depth_test()
        self.wait(0.4)

        current_matrix = np.identity(3)
        for label_text, target_matrix, marker in self.four_three_two_full_operations():
            label = self.make_matrix_label(label_text, target_matrix, label_font_size=22, matrix_font_size=16)
            label.fix_in_frame()
            self.play(FadeIn(label, shift=0.15 * UP), run_time=0.2)
            self.show_full_operation_marker(marker)
            delta = target_matrix @ np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(delta, operated_object), run_time=0.65)
            current_matrix = target_matrix
            self.wait(0.15)
            reset = np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(reset, operated_object), run_time=0.35)
            current_matrix = np.identity(3)
            self.play(FadeOut(label, shift=0.15 * DOWN), run_time=0.15)

        self.wait(0.5)

    def four_three_two_full_operations(self):
        operations = [("E", np.identity(3), {"kind": "identity"})]

        c4_axes = [
            ("x", [1, 0, 0]),
            ("y", [0, 1, 0]),
            ("z", [0, 0, 1]),
        ]
        for axis_name, axis in c4_axes:
            for angle in (90, 180, 270):
                order = 2 if angle == 180 else 4
                operations.append((
                    f"C{order} {angle} about {axis_name}",
                    rotation_matrix(axis, angle),
                    {"kind": "axis", "axis": axis, "order": order},
                ))

        c3_axes = [
            [1, 1, 1],
            [1, 1, -1],
            [1, -1, 1],
            [-1, 1, 1],
        ]
        for index, axis in enumerate(c3_axes, start=1):
            operations.append((
                f"C3 +120 body diagonal {index}",
                rotation_matrix(axis, 120),
                {"kind": "axis", "axis": axis, "order": 3},
            ))
            operations.append((
                f"C3 -120 body diagonal {index}",
                rotation_matrix(axis, -120),
                {"kind": "axis", "axis": axis, "order": 3},
            ))

        c2_axes = [
            [1, 1, 0],
            [1, -1, 0],
            [1, 0, 1],
            [1, 0, -1],
            [0, 1, 1],
            [0, 1, -1],
        ]
        for index, axis in enumerate(c2_axes, start=1):
            operations.append((
                f"C2 face-diagonal axis {index}",
                rotation_matrix(axis, 180),
                {"kind": "axis", "axis": axis, "order": 2},
            ))

        return operations


class PointGroupM3MFullOperations(PointGroup432FullOperations):
    point_group_symbol = "m-3m"
    crystal_shape = "cube"

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.frame.reorient(35, 65, 0, height=7)

        group = get_point_group(self.point_group_symbol)
        crystal_body, probe = self.make_crystal_parts()
        operated_object = Group(crystal_body, probe)
        axes = self.make_reference_axes()
        title = Text(
            f"{group['hm']} full operations  |  {group['schoenflies']}  |  48 elements",
            font_size=30,
            color=TEXT_COLOR,
        )
        title.to_corner(UL)
        title.fix_in_frame()

        self.add(axes, crystal_body, title)
        self.add(probe, set_depth_test=False)
        probe.deactivate_depth_test()
        self.wait(0.4)

        current_matrix = np.identity(3)
        for label_text, target_matrix, marker in self.m3m_full_operations():
            label = self.make_matrix_label(label_text, target_matrix, label_font_size=20, matrix_font_size=15)
            label.fix_in_frame()
            self.play(FadeIn(label, shift=0.15 * UP), run_time=0.16)
            self.show_full_operation_marker(marker)
            delta = target_matrix @ np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(delta, operated_object), run_time=0.46)
            current_matrix = target_matrix
            self.wait(0.08)
            reset = np.linalg.inv(current_matrix)
            self.play(ApplyMatrix(reset, operated_object), run_time=0.28)
            current_matrix = np.identity(3)
            self.play(FadeOut(label, shift=0.15 * DOWN), run_time=0.12)

        self.wait(0.5)

    def m3m_full_operations(self):
        rotations = self.four_three_two_full_operations()
        operations = list(rotations)

        for label, matrix, marker in rotations:
            inverted_matrix = -matrix
            if label == "E":
                inverted_label = "inversion"
                inverted_marker = {"kind": "center"}
            elif marker["kind"] == "axis" and marker.get("order") == 2:
                inverted_label = f"mirror normal to {label}"
                inverted_marker = {"kind": "plane", "normal": marker["axis"]}
            else:
                inverted_label = f"inversion * {label}"
                inverted_marker = {
                    "kind": "rotoaxis",
                    "axis": marker["axis"],
                    "order": marker.get("order", 3),
                }
            operations.append((inverted_label, inverted_matrix, inverted_marker))

        return operations

    def show_full_operation_marker(self, marker):
        if marker["kind"] == "rotoaxis":
            order = marker.get("order", 4)
            color = AXIS_COLORS.get(order, "#f8fafc")
            start, end = axis_endpoints(marker["axis"], 5.2)
            axis = Line3D(start, end, width=0.08, color=color)
            center = Sphere(radius=0.14, color=INVERSION_COLOR)
            self.play(GrowFromCenter(axis), FadeIn(center), run_time=0.14)
            self.play(FadeOut(axis), FadeOut(center), run_time=0.14)
        else:
            super().show_full_operation_marker(marker)


def point_group_scene_class_name(symbol):
    replacements = {
        "-": "Minus",
        "/": "Over",
        "m": "M",
    }
    pieces = []
    for character in symbol:
        pieces.append(replacements.get(character, character))
    return "PointGroup" + "".join(pieces)


def point_group_crystal_shape(symbol):
    system = get_point_group(symbol)["crystal_system"]
    if system == "cubic":
        return "cube"
    if system in ("trigonal", "hexagonal"):
        return "hex"
    return "prism"


for _symbol in all_point_group_symbols():
    _class_name = point_group_scene_class_name(_symbol)
    if _class_name not in globals():
        globals()[_class_name] = type(
            _class_name,
            (PointGroupScene,),
            {
                "point_group_symbol": _symbol,
                "crystal_shape": point_group_crystal_shape(_symbol),
            },
        )
    _full_class_name = _class_name + "FullClosure"
    if _full_class_name not in globals():
        globals()[_full_class_name] = type(
            _full_class_name,
            (FullClosurePointGroupScene,),
            {
                "point_group_symbol": _symbol,
                "crystal_shape": point_group_crystal_shape(_symbol),
            },
        )
