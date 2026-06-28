# 32 Crystallographic Point Groups with 3b1b Manim

This project uses 3b1b's ManimGL (`manimgl`) to generate GIF animations for
the rotational/symmetry operations of the 32 crystallographic point groups.

## Target Directory

`E:\Codex\pointgroup`

## Phase 0 - Environment Probe

Goal: confirm which required tools already exist on this machine.

Checks:

```powershell
python --version
py --version
git --version
ffmpeg -version
where python
where py
where git
where ffmpeg
```

Expected tools:

- Python 3.10 or 3.11 is preferred for ManimGL compatibility.
- Git is useful for cloning `3b1b/manim` if pip installation is insufficient.
- FFmpeg is required for video/GIF conversion.
- A working OpenGL-capable environment is required for ManimGL previews/renders.
- LaTeX is optional, but recommended for clean crystallographic symbols.

Permission note:

- Installing missing tools may require network access and administrator actions.
- If installation is needed, ask the user before running package managers.

## Phase 1 - Project Skeleton

Create this structure:

```text
E:\Codex\pointgroup
  README.md
  PROJECT_PLAN.md
  requirements.txt
  scenes/
    point_groups.py
  pointgroup/
    __init__.py
    data.py
    operations.py
    geometry.py
    styles.py
  scripts/
    render_one.ps1
    render_all.ps1
    convert_gif.ps1
  notes/
    point_groups.md
    references.md
  outputs/
    videos/
    gifs/
    stills/
```

Initial `requirements.txt`:

```text
manimgl
numpy
scipy
imageio
imageio-ffmpeg
```

Optional later:

```text
spglib
```

`spglib` can help cross-check crystallographic operations, but the first version
should keep a transparent hand-authored point group table.

## Phase 2 - Define Scope Precisely

Important distinction:

- Some of the 32 point groups are pure proper-rotation groups.
- Many include mirror planes, inversion, rotoinversion, or improper rotations.

Recommended animation scope:

1. Always show the main rotational content: axes, rotation order, and animated
   rotation of a reference object.
2. For non-rotational symmetry elements, show visual markers:
   - mirror plane: translucent plane
   - inversion center: central dot/pulse
   - rotoinversion: rotation plus inversion marker
   - improper axes: distinct dashed axis style
3. Export one GIF per point group.

This keeps the project faithful to crystallography while still matching the
user-facing goal of "rotation operation GIFs".

## Phase 3 - Point Group Data Model

Create `pointgroup/data.py` containing a list of 32 point groups.

Each entry:

```python
{
    "hm": "4mm",
    "schoenflies": "C4v",
    "crystal_system": "tetragonal",
    "family": "polar",
    "generators": [...],
    "display_operations": [...],
}
```

Operation schema:

```python
{
    "kind": "rotation",
    "axis": [0, 0, 1],
    "order": 4,
    "angle_degrees": 90,
    "label": "C4 z",
}
```

Other operation kinds:

- `mirror`
- `inversion`
- `rotoinversion`
- `identity`

Canonical 32 Hermann-Mauguin symbols:

```text
1, -1,
2, m, 2/m,
222, mm2, mmm,
4, -4, 4/m, 422, 4mm, -42m, 4/mmm,
3, -3, 32, 3m, -3m,
6, -6, 6/m, 622, 6mm, -6m2, 6/mmm,
23, m-3, 432, -43m, m-3m
```

## Phase 4 - Math Layer

Create `pointgroup/operations.py`.

Functions:

- `normalize_axis(axis)`
- `rotation_matrix(axis, angle)`
- `axis_angle_for_order(axis, order, step=1)`
- `apply_matrix(points, matrix)`
- `generate_cyclic_rotations(axis, order)`
- `operation_label(operation)`

Use `numpy` for matrices. Use `scipy.spatial.transform.Rotation` if convenient,
but keep the matrix functions simple enough to inspect.

## Phase 5 - Visual Language

Create `pointgroup/styles.py`.

Suggested conventions:

- x axis: red
- y axis: green
- z axis: blue
- 2-fold axis: yellow/orange
- 3-fold axis: purple
- 4-fold axis: cyan
- 6-fold axis: magenta
- mirror plane: translucent silver
- inversion center: bright white/black pulse depending on background

Use consistent camera position, frame rate, and duration so all 32 GIFs feel
like a coherent set.

## Phase 6 - ManimGL Prototype

Start with three representative groups:

- `4`: simple principal rotation
- `mmm`: orthorhombic mirrors plus 2-fold axes
- `432`: cubic high-symmetry rotation group

Build `scenes/point_groups.py` with:

- `PointGroupScene`
- `PointGroup4`
- `PointGroupMMM`
- `PointGroup432`

Prototype success criteria:

- Can render a video for each scene.
- Camera framing is stable.
- Axis labels are readable.
- The reference object visibly rotates.
- Generated MP4 can be converted into GIF.

## Phase 7 - GIF Pipeline

Use ManimGL to render MP4, then FFmpeg to create GIF.

Example commands:

```powershell
manimgl scenes/point_groups.py PointGroup4 -w
ffmpeg -i path\to\input.mp4 -vf "fps=15,scale=720:-1:flags=lanczos" outputs\gifs\4.gif
```

Better GIF quality can use a palette pass:

```powershell
ffmpeg -i input.mp4 -vf "fps=15,scale=720:-1:flags=lanczos,palettegen" palette.png
ffmpeg -i input.mp4 -i palette.png -lavfi "fps=15,scale=720:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
```

## Phase 8 - Expand to All 32 Groups

After prototype passes:

1. Add all 32 entries to `data.py`.
2. Create a dynamic scene class or one scene that accepts a point-group key.
3. Add batch rendering scripts.
4. Render all MP4s.
5. Convert all MP4s to GIFs.
6. Review visual consistency.
7. Fix labels/framing for dense cubic and hexagonal groups.

## Phase 9 - Quality Control

For every output GIF, check:

- Symbol and group name correct.
- Rotation order matches label.
- Axis direction visually clear.
- Non-rotation elements are not confused with proper rotations.
- Loop timing is smooth.
- GIF dimensions and file sizes are acceptable.

Suggested output target:

- 720 px width
- 10-15 fps
- 3-6 seconds per GIF
- One clean loop per featured operation or operation sequence

## Permission Checkpoints

Ask the user before:

- Installing Python, Git, FFmpeg, LaTeX, or package managers.
- Running commands that need network access.
- Writing outside the approved workspace.
- Creating or replacing files in `E:\Codex\pointgroup`.
- Launching GUI apps or browser previews.

## Immediate Next Steps

1. Create the directory skeleton in `E:\Codex\pointgroup`.
2. Add `PROJECT_PLAN.md`, `README.md`, and `requirements.txt`.
3. Probe `py`, `python`, `git`, and `ffmpeg` again with full path checks.
4. If Python exists as `py`, create `.venv`.
5. If not, ask the user how they prefer to install Python.
6. Install dependencies only after approval.
7. Implement the three-scene prototype.
