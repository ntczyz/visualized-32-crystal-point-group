from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


POINT_GROUPS = [
    ("PointGroup1", "\u4e09\u659c-1"),
    ("PointGroupMinus1", "\u4e09\u659c--1"),
    ("PointGroup2", "\u5355\u659c-2"),
    ("PointGroupM", "\u5355\u659c-m"),
    ("PointGroup2OverM", "\u5355\u659c-2\uff0fm"),
    ("PointGroup222", "\u6b63\u4ea4-222"),
    ("PointGroupMM2", "\u6b63\u4ea4-mm2"),
    ("PointGroupMMM", "\u6b63\u4ea4-mmm"),
    ("PointGroup4", "\u56db\u65b9-4"),
    ("PointGroupMinus4", "\u56db\u65b9--4"),
    ("PointGroup4OverM", "\u56db\u65b9-4\uff0fm"),
    ("PointGroup422", "\u56db\u65b9-422"),
    ("PointGroup4MM", "\u56db\u65b9-4mm"),
    ("PointGroupMinus42M", "\u56db\u65b9--42m"),
    ("PointGroup4OverMMM", "\u56db\u65b9-4\uff0fmmm"),
    ("PointGroup3", "\u4e09\u65b9-3"),
    ("PointGroupMinus3", "\u4e09\u65b9--3"),
    ("PointGroup32", "\u4e09\u65b9-32"),
    ("PointGroup3M", "\u4e09\u65b9-3m"),
    ("PointGroupMinus3M", "\u4e09\u65b9--3m"),
    ("PointGroup6", "\u516d\u65b9-6"),
    ("PointGroupMinus6", "\u516d\u65b9--6"),
    ("PointGroup6OverM", "\u516d\u65b9-6\uff0fm"),
    ("PointGroup622", "\u516d\u65b9-622"),
    ("PointGroup6MM", "\u516d\u65b9-6mm"),
    ("PointGroupMinus6M2", "\u516d\u65b9--6m2"),
    ("PointGroup6OverMMM", "\u516d\u65b9-6\uff0fmmm"),
    ("PointGroup23", "\u7acb\u65b9-23"),
    ("PointGroupMMinus3", "\u7acb\u65b9-m-3"),
    ("PointGroup432", "\u7acb\u65b9-432"),
    ("PointGroupMinus43M", "\u7acb\u65b9--43m"),
    ("PointGroupMMinus3M", "\u7acb\u65b9-m-3m"),
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def render_scene(
    root: Path,
    scene_name: str,
    file_base: str,
    quality: str,
    video_dir: Path,
) -> Path:
    scene_file = root / "scenes" / "point_groups.py"
    video_path = video_dir / f"{file_base}.mp4"
    command = [
        str(root / ".venv" / "Scripts" / "manimgl.exe"),
        str(scene_file),
        scene_name,
        "-w",
        quality,
        "--video_dir",
        str(video_dir),
        "--file_name",
        file_base,
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    print(f"Rendering {scene_name} -> {video_path}")
    subprocess.run(command, check=True, cwd=str(root), env=env)
    return video_path


def convert_gif(video_path: Path, file_base: str, gif_width: int, gif_dir: Path) -> Path:
    gif_path = gif_dir / f"{file_base}.gif"
    palette_path = Path(os.environ["TEMP"]) / f"pointgroup_palette_{video_path.stem}.png"
    ffmpeg = Path(r"E:\VSCode\Conda\Library\bin\ffmpeg.exe")

    print(f"Converting {video_path} -> {gif_path}")
    subprocess.run(
        [
            str(ffmpeg),
            "-y",
            "-i",
            str(video_path),
            "-vf",
            f"fps=15,scale={gif_width}:-1:flags=lanczos,palettegen",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(palette_path),
        ],
        check=True,
    )
    subprocess.run(
        [
            str(ffmpeg),
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(palette_path),
            "-lavfi",
            f"fps=15,scale={gif_width}:-1:flags=lanczos[x];[x][1:v]paletteuse",
            str(gif_path),
        ],
        check=True,
    )
    return gif_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quality", default="-l")
    parser.add_argument("--gif-width", type=int, default=720)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()

    root = project_root()
    video_dir = root / "outputs" / ("videos_full" if args.full else "videos")
    gif_dir = root / "outputs" / ("gifs_full" if args.full else "gifs")
    video_dir.mkdir(parents=True, exist_ok=True)
    gif_dir.mkdir(parents=True, exist_ok=True)

    for scene_name, file_base in POINT_GROUPS:
        render_name = scene_name + "FullClosure" if args.full else scene_name
        video_path = render_scene(root, render_name, file_base, args.quality, video_dir)
        convert_gif(video_path, file_base, args.gif_width, gif_dir)

    mode = "full point group" if args.full else "representative"
    print(f"Rendered {len(POINT_GROUPS)} {mode} videos and GIFs.")
    print(f"Videos: {video_dir}")
    print(f"GIFs: {gif_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
