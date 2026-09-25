"""Video provider registry and orchestration.

Every provider renders one fixed 15-second part. A longer video passes one
prompt per part: each part starts from the previous part's last frame, and
ffmpeg merges the parts into a single MP4.
"""

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile

from common import discover_providers, local_path, MEDIA_CACHE

PROVIDERS = discover_providers("video")

VIDEO_EXTS = (".mp4", ".mov", ".m4v", ".webm", ".mkv")


def run_video(args):
    if not args.prompt:
        sys.exit("Error: --prompt is required.")
    if not args.image:
        sys.exit("Error: --image is required.")

    api_key = args.api or os.environ.get("CLAWDESS_VIDEO_API", "")
    if not api_key:
        sys.exit("Error: --api or CLAWDESS_VIDEO_API required.")

    provider_name = (args.provider or "FAL").upper()
    if provider_name not in PROVIDERS:
        sys.exit(f"Unknown video provider: {provider_name}. Available: {', '.join(PROVIDERS)}")

    total = len(args.prompt)
    if total > 1 and not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        sys.exit("Error: ffmpeg and ffprobe are required for videos with more than one part.")

    os.makedirs(MEDIA_CACHE, exist_ok=True)
    stem = os.path.join(MEDIA_CACHE, time.strftime("video-%Y%m%d-%H%M%S"))

    image = args.image
    parts = []
    for n, prompt in enumerate(args.prompt, 1):
        print(f"\nGenerating video part {n}/{total} with provider={provider_name}, prompt={prompt}")
        video_result = PROVIDERS[provider_name].generate(api_key, prompt, image)
        if not video_result:
            sys.exit(f"Error generating video part {n}/{total}.")

        dest = f"{stem}.mp4" if total == 1 else f"{stem}-part{n}.mp4"
        parts.append(save_video(video_result, dest))
        print(f"Video part {n}/{total} ready: {dest}")

        if n < total:
            image = last_frame(dest, f"{stem}-part{n}-last.png")

    if total > 1:
        merge_videos(parts, f"{stem}.mp4")

    print(f"Video on the way. MEDIA: {stem}.mp4")


def save_video(result, dest):
    """Save a provider result (URL or local file, possibly zipped) as *dest*."""
    tmp = dest + ".download"
    if result.startswith(("http://", "https://")):
        req = urllib.request.Request(result, headers={"User-Agent": "curl/8.0"})
        with urllib.request.urlopen(req, timeout=300) as resp, open(tmp, "wb") as out:
            shutil.copyfileobj(resp, out)
    else:
        shutil.copyfile(local_path(result), tmp)

    with open(tmp, "rb") as handle:
        zipped = handle.read(4) == b"PK\x03\x04"
    if not zipped:
        os.replace(tmp, dest)
        return dest

    # ComfyUI-style apps (e.g. RunningHub) deliver the video inside a zip.
    with zipfile.ZipFile(tmp) as archive:
        videos = [m for m in archive.infolist() if m.filename.lower().endswith(VIDEO_EXTS)]
        if not videos:
            sys.exit(f"Error: no video file inside {result}")
        with archive.open(max(videos, key=lambda m: m.file_size)) as src, open(dest, "wb") as out:
            shutil.copyfileobj(src, out)
    os.remove(tmp)
    return dest


def last_frame(video, dest):
    """Write the final frame of *video* to *dest*; it becomes the next part's first frame."""
    run_ffmpeg(["-sseof", "-1", "-i", video, "-map", "0:V:0", "-update", "1", dest])
    return dest


def merge_videos(parts, dest):
    """Concatenate *parts* into *dest* at the first part's size and frame rate."""
    infos = [probe(path) for path in parts]
    width, height = infos[0]["width"] // 2 * 2, infos[0]["height"] // 2 * 2
    fps = infos[0]["fps"]
    with_audio = any(info["audio"] for info in infos)

    inputs, graph, streams = [], [], ""
    for i, (path, info) in enumerate(zip(parts, infos)):
        inputs += ["-i", path]
        graph.append(
            f"[{i}:V:0]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},"
            f"format=yuv420p,setpts=PTS-STARTPTS[v{i}]"
        )
        streams += f"[v{i}]"
        if with_audio:
            # Silence stands in for a part without audio; every track is cut to its video length.
            source = f"[{i}:a:0]" if info["audio"] else "anullsrc=r=48000:cl=stereo,"
            graph.append(
                f"{source}aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
                f"apad,atrim=duration={info['duration']},asetpts=PTS-STARTPTS[a{i}]"
            )
            streams += f"[a{i}]"
    graph.append(f"{streams}concat=n={len(parts)}:v=1:a={int(with_audio)}[v]" + ("[a]" if with_audio else ""))

    args = inputs + ["-filter_complex", ";".join(graph), "-map", "[v]"]
    if with_audio:
        args += ["-map", "[a]", "-c:a", "aac", "-b:a", "160k"]
    args += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-movflags", "+faststart", dest]
    print(f"\nMerging {len(parts)} parts into {dest}")
    run_ffmpeg(args)


def probe(path):
    """Return the size, frame rate, duration, and audio presence of a video file."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f"ffprobe failed on {path}: {result.stderr.strip()[-1000:]}")
    info = json.loads(result.stdout)
    video = next(
        (s for s in info["streams"]
         if s["codec_type"] == "video" and not s.get("disposition", {}).get("attached_pic")),
        None,
    )
    if not video:
        sys.exit(f"Error: no video stream in {path}")
    rates = [video.get(key, "0/0") for key in ("r_frame_rate", "avg_frame_rate")]
    return {
        "width": video["width"],
        "height": video["height"],
        "fps": next((rate for rate in rates if not rate.startswith("0/")), "24"),
        "duration": float(video.get("duration") or info["format"]["duration"]),
        "audio": any(s["codec_type"] == "audio" for s in info["streams"]),
    }


def run_ffmpeg(args):
    result = subprocess.run(["ffmpeg", "-v", "error", "-y", *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"ffmpeg failed: {result.stderr.strip()[-1000:]}")
