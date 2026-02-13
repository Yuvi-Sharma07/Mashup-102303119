

import sys
import os
import re
from pytubefix import YouTube, Search
from moviepy import AudioFileClip, concatenate_audioclips
import tempfile
import shutil


def validate_inputs(singer_name, num_videos, audio_duration, output_file):
    """Validate all input parameters"""
    errors = []
    
    if not singer_name or not singer_name.strip():
        errors.append("Singer name cannot be empty")
    
    try:
        num_videos = int(num_videos)
        if num_videos <= 10:
            errors.append("Number of videos must be greater than 10")
    except ValueError:
        errors.append("Number of videos must be a valid integer")
    
    try:
        audio_duration = int(audio_duration)
        if audio_duration < 20:
            errors.append("Audio duration must be greater than 20 seconds")
    except ValueError:
        errors.append("Audio duration must be a valid integer")
    
    if not output_file or not output_file.strip():
        errors.append("Output file name cannot be empty")
    elif not output_file.endswith('.mp3'):
        errors.append("Output file must have .mp3 extension")
    
    return errors


def sanitize_filename(filename):
    """Remove special characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)


def download_videos(singer_name, num_videos, temp_dir):
    """Download N videos of the specified singer from YouTube"""
    print(f"\n[1/4] Searching for {singer_name} videos on YouTube...")
    
    try:
        search = Search(singer_name)
        downloaded_files = []
        count = 0
        
        for video in search.results:
            if count >= num_videos:
                break
            
            try:
                print(f"\nDownloading video {count + 1}/{num_videos}: {video.title}")
                
                
                audio_stream = video.streams.filter(only_audio=True).first()
                
                if audio_stream:
                    
                    output_path = audio_stream.download(
                        output_path=temp_dir,
                        filename=f"video_{count}.mp4"
                    )
                    downloaded_files.append(output_path)
                    count += 1
                    print(f" Downloaded successfully")
                else:
                    print(f" No audio stream available")
                    
            except Exception as e:
                print(f" Error downloading video: {str(e)}")
                continue
        
        if count < num_videos:
            print(f"\n Warning: Only {count} videos were downloaded (requested {num_videos})")
        
        return downloaded_files
        
    except Exception as e:
        raise Exception(f"Error searching for videos: {str(e)}")


def convert_to_audio(video_files, temp_dir):
    """Convert video files to audio files"""
    print(f"\n[2/4] Converting videos to audio...")
    audio_files = []
    
    for i, video_file in enumerate(video_files):
        try:
            print(f"Converting {i + 1}/{len(video_files)}...")
            
            
            audio = AudioFileClip(video_file)
            audio_path = os.path.join(temp_dir, f"audio_{i}.mp3")
            audio.write_audiofile(audio_path, logger=None)
            audio.close()
            
            audio_files.append(audio_path)
            print(f"Converted successfully")
            
        except Exception as e:
            print(f" Error converting video {i + 1}: {str(e)}")
            continue
    
    return audio_files


def cut_audio(audio_files, duration, temp_dir):
    """Cut first Y seconds from each audio file"""
    print(f"\n[3/4] Cutting first {duration} seconds from each audio...")
    cut_files = []
    
    for i, audio_file in enumerate(audio_files):
        try:
            print(f"Processing {i + 1}/{len(audio_files)}...")
            
            audio = AudioFileClip(audio_file)
            
            
            cut_duration = min(duration, audio.duration)
            cut_audio_clip = audio.subclipped(0, cut_duration)
            
            cut_path = os.path.join(temp_dir, f"cut_{i}.mp3")
            cut_audio_clip.write_audiofile(cut_path, logger=None)
            
            audio.close()
            cut_audio_clip.close()
            
            cut_files.append(cut_path)
            print(f" Cut to {cut_duration} seconds")
            
        except Exception as e:
            print(f" Error cutting audio {i + 1}: {str(e)}")
            continue
    
    return cut_files


def merge_audio(audio_files, output_file):
    """Merge all audio files into a single output file"""
    print(f"\n[4/4] Merging {len(audio_files)} audio clips into mashup...")
    
    try:
        
        clips = [AudioFileClip(audio_file) for audio_file in audio_files]
        
        
        final_clip = concatenate_audioclips(clips)
        
        
        final_clip.write_audiofile(output_file, logger=None)
        
        
        for clip in clips:
            clip.close()
        final_clip.close()
        
        print(f" Mashup created successfully: {output_file}")
        
    except Exception as e:
        raise Exception(f"Error merging audio files: {str(e)}")


def main():
    """Main function to orchestrate the mashup creation"""
    
    
    if len(sys.argv) != 5:
        print("Error: Incorrect number of parameters")
        print("\nUsage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)
    
    
    singer_name = sys.argv[1]
    num_videos = sys.argv[2]
    audio_duration = sys.argv[3]
    output_file = sys.argv[4]
    
    
    errors = validate_inputs(singer_name, num_videos, audio_duration, output_file)
    if errors:
        print("Error: Invalid inputs detected:")
        for error in errors:
            print(f"  - {error}")
        print("\nUsage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
    
        sys.exit(1)
    
    
    num_videos = int(num_videos)
    audio_duration = int(audio_duration)
    
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        print("=" * 60)
        print("MASHUP CREATOR")
        print("=" * 60)
        print(f"Singer: {singer_name}")
        print(f"Videos to download: {num_videos}")
        print(f"Audio duration: {audio_duration} seconds")
        print(f"Output file: {output_file}")
        print("=" * 60)
        
        
        video_files = download_videos(singer_name, num_videos, temp_dir)
        
        if not video_files:
            raise Exception("No videos were downloaded successfully")
        
        
        audio_files = convert_to_audio(video_files, temp_dir)
        
        if not audio_files:
            raise Exception("No audio files were created")
        
        
        cut_files = cut_audio(audio_files, audio_duration, temp_dir)
        
        if not cut_files:
            raise Exception("No audio files were cut successfully")
        
        
        merge_audio(cut_files, output_file)
        
        print("\n" + "=" * 60)
        print(" MASHUP COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n Error: {str(e)}")
        sys.exit(1)
        
    finally:
        
        try:
            shutil.rmtree(temp_dir)
            print(f"\n Temporary files cleaned up")
        except Exception as e:
            print(f"\nCould not clean up temporary files: {str(e)}")


if __name__ == "__main__":
    main()
