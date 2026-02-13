import sys
import os
import re
from pytubefix import YouTube, Search
from moviepy import AudioFileClip, concatenate_audioclips
import tempfile
import shutil


def validate_inputs(singer_name, num_videos, audio_duration, output_file):
    errors = []

    if not singer_name or not singer_name.strip():
        errors.append("Singer name cannot be empty")

    try:
        num_videos = int(num_videos)
        if num_videos <= 0:
            errors.append("Number of videos must be greater than 0")
    except ValueError:
        errors.append("Number of videos must be a valid integer")

    try:
        audio_duration = int(audio_duration)
        if audio_duration <= 0:
            errors.append("Audio duration must be greater than 0 seconds")
    except ValueError:
        errors.append("Audio duration must be a valid integer")

    if not output_file or not output_file.strip():
        errors.append("Output file name cannot be empty")
    elif not output_file.endswith('.mp3'):
        errors.append("Output file must have .mp3 extension")

    return errors


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)


def download_videos(singer_name, num_videos, temp_dir):
    try:
        search = Search(singer_name)
        downloaded_files = []
        count = 0

        if not search.results:
            return []

        for video in search.results:
            if count >= num_videos:
                break

            try:
                audio_stream = video.streams.filter(only_audio=True).first()

                if audio_stream:
                    output_path = audio_stream.download(
                        output_path=temp_dir,
                        filename=f"video_{count}.mp4"
                    )
                    downloaded_files.append(output_path)
                    count += 1
            except:
                continue

        return downloaded_files

    except Exception:
        return []


def convert_to_audio(video_files, temp_dir):
    audio_files = []

    for i, video_file in enumerate(video_files):
        try:
            audio = AudioFileClip(video_file)
            audio_path = os.path.join(temp_dir, f"audio_{i}.mp3")
            audio.write_audiofile(audio_path, logger=None)
            audio.close()
            audio_files.append(audio_path)
        except:
            continue

    return audio_files


def cut_audio(audio_files, duration, temp_dir):
    cut_files = []

    for i, audio_file in enumerate(audio_files):
        try:
            audio = AudioFileClip(audio_file)

            if audio.duration <= 0:
                audio.close()
                continue

            cut_duration = min(duration, audio.duration)

            clip = audio.subclip(0, cut_duration)

            cut_path = os.path.join(temp_dir, f"cut_{i}.mp3")
            clip.write_audiofile(cut_path, logger=None)

            audio.close()
            clip.close()

            cut_files.append(cut_path)

        except:
            continue

    return cut_files


def merge_audio(audio_files, output_file):
    if not audio_files:
        raise Exception("No audio files available to merge.")

    clips = []

    for file in audio_files:
        try:
            clips.append(AudioFileClip(file))
        except:
            continue

    if not clips:
        raise Exception("All audio clips failed to load.")

    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_file, logger=None)

    for clip in clips:
        clip.close()

    final_clip.close()


def main():
    if len(sys.argv) != 5:
        print("Usage: python program.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer_name = sys.argv[1]
    num_videos = sys.argv[2]
    audio_duration = sys.argv[3]
    output_file = sys.argv[4]

    errors = validate_inputs(singer_name, num_videos, audio_duration, output_file)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    num_videos = int(num_videos)
    audio_duration = int(audio_duration)

    temp_dir = tempfile.mkdtemp()

    try:
        video_files = download_videos(singer_name, num_videos, temp_dir)
        if not video_files:
            raise Exception("No videos downloaded.")

        audio_files = convert_to_audio(video_files, temp_dir)
        if not audio_files:
            raise Exception("No audio files created.")

        cut_files = cut_audio(audio_files, audio_duration, temp_dir)
        if not cut_files:
            raise Exception("No audio files cut.")

        merge_audio(cut_files, output_file)

        print("Mashup created successfully.")

    except Exception as e:
        print(str(e))
        sys.exit(1)

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def run_from_web(singer_name, num_videos, duration, output_file):
    num_videos = int(num_videos)
    duration = int(duration)

    temp_dir = tempfile.mkdtemp()

    try:
        video_files = download_videos(singer_name, num_videos, temp_dir)
        if not video_files:
            raise Exception("No videos downloaded from YouTube.")

        audio_files = convert_to_audio(video_files, temp_dir)
        if not audio_files:
            raise Exception("Audio conversion failed.")

        cut_files = cut_audio(audio_files, duration, temp_dir)
        if not cut_files:
            raise Exception("Audio cutting failed.")

        merge_audio(cut_files, output_file)

        return output_file, temp_dir

    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e


if __name__ == "__main__":
    main()
