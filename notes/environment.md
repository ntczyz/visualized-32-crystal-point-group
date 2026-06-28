# Environment Configuration

Project root:

```text
E:\Codex\pointgroup
```

Configured tools:

```text
Python base: E:\VSCode\Conda\python.exe
Project Python: E:\Codex\pointgroup\.venv\Scripts\python.exe
ManimGL: E:\Codex\pointgroup\.venv\Scripts\manimgl.exe
Conda FFmpeg: E:\VSCode\Conda\Library\bin\ffmpeg.exe
Git: E:\Git\cmd\git.exe
```

Installed Python package highlights:

```text
manimgl==1.7.2
setuptools==80.10.2
numpy==2.4.6
scipy==1.17.1
imageio==2.37.3
imageio-ffmpeg==0.6.0
```

`setuptools<81` is intentionally pinned because ManimGL 1.7.2 imports
`pkg_resources`, which is no longer available in the newest setuptools line.

To activate the project environment in PowerShell:

```powershell
cd E:\Codex\pointgroup
.\scripts\activate_env.ps1
```

To verify the environment:

```powershell
cd E:\Codex\pointgroup
.\scripts\check_env.ps1
```

Notes:

- The system PATH visible to Codex does not currently expose Python, Git, or
  FFmpeg directly, so project scripts prepend the known working directories.
- ManimGL import succeeds after pinning `setuptools<81`.
- `manimgl --help` succeeds.
- LaTeX has not been configured yet. The first animation prototype should avoid
  TeX-only labels until a TeX distribution is confirmed.
