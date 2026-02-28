from flask import Flask, request, send_file
import subprocess, uuid

app = Flask(__name__)

@app.route("/download")
def download():
    video = request.args.get("video")
    start = request.args.get("start")
    end = request.args.get("end")

    uid = str(uuid.uuid4())
    video_file = f"{uid}.mp4"
    clip_file = f"clip_{uid}.mp4"

    subprocess.run([
        "yt-dlp",
        f"https://www.youtube.com/watch?v={video}",
        "-o", video_file
    ])

    subprocess.run([
        "ffmpeg", "-y",
        "-ss", start, "-to", end,
        "-i", video_file,
        "-c", "copy",
        clip_file
    ])

    return send_file(clip_file, as_attachment=True)

app.run(host="0.0.0.0", port=10000)
