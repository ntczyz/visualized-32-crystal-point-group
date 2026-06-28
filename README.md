# Visualized 32 Crystal Point Groups

This project uses [3b1b/manim](https://github.com/3b1b/manim), also known as ManimGL, to visualize the symmetry operations of the 32 crystallographic point groups.

Each animation traverses the full point group, orders operations by conjugacy class, and displays the corresponding operation label and matrix. Proper operations keep the original probe colors, while improper operations briefly recolor the low-symmetry probe to make orientation-reversing operations easier to recognize.

## Gallery

- [32 point group GIF catalog](docs/pointgroup_32_gif_catalog.md)
- [Development notes in Chinese](docs/pointgroup_manim_zhihu_blog.md)

Final rendered outputs are stored in:

- `outputs/gifs_full/`
- `outputs/videos_full/`

## Project Layout

```text
pointgroup/
  data.py          Point group metadata
  geometry.py      Geometry helpers
  operations.py    Rotation, reflection, inversion, and rotoinversion matrices
  styles.py        Shared visual constants
scenes/
  point_groups.py  ManimGL scenes and full-operation animation logic
scripts/
  check_env.ps1
  render_one.ps1
  render_all_point_groups.py
  render_all_point_groups.ps1
  convert_gif.ps1
docs/
  pointgroup_32_gif_catalog.md
  pointgroup_32_gif_catalog_local.md
  pointgroup_manim_zhihu_blog.md
outputs/
  gifs_full/
  videos_full/
```

Local virtual environments, TeX toolchains, caches, and prototype render outputs are intentionally excluded from Git.

## Requirements

- Python 3.11 recommended
- ManimGL
- NumPy
- SciPy
- FFmpeg
- A LaTeX distribution capable of compiling the ManimGL `Tex` labels

Install Python dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Render

Check the environment:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_env.ps1
```

Render one point group scene:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\render_one.ps1 -SceneName PointGroup4 -Quality -l
```

Render all 32 point groups and create GIFs:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\render_all_point_groups.ps1
```

The batch renderer writes full outputs to `outputs/videos_full/` and `outputs/gifs_full/`.

## Notes

The project focuses on educational visualization rather than physically realistic occlusion. The low-symmetry probe is kept visually legible even when it moves behind the crystal frame, so that the effect of each symmetry operation remains clear.

