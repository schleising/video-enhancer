from pathlib import Path
import shutil

from ffmpeg import FFmpeg, Progress
from ffmpeg.types import Option

from . import ImageEnhancer

class VideoProcessor:
    def __init__(self, input_file: Path, output_file: Path) -> None:
        # Set input and output files
        self.input_file = input_file
        self.output_file = output_file

        # Create a temporary folder
        self.input_temp_folder = Path('.temp_input')

        # Create a temporary folder for the output
        self.output_temp_folder = Path('.temp_output')

    def enhance(self):
        # Create the temporary folders if they don't exist
        self.input_temp_folder.mkdir(parents=True, exist_ok=True)
        self.output_temp_folder.mkdir(parents=True, exist_ok=True)

        # Extract the audio
        self._extract_audio()

        # Extract the frames
        self._extract_frames()

        # Enhance the frames
        image_enhancer = ImageEnhancer(self.input_temp_folder, self.output_temp_folder)
        image_enhancer.convert()

        # Create a video from the frames
        self._create_video()

        # Add the audio to the video
        self._add_audio()

        # Delete the temporary folders
        shutil.rmtree(self.input_temp_folder)
        shutil.rmtree(self.output_temp_folder)

    def _extract_audio(self) -> None:
        # Create a temporary file for the audio
        temp_audio_file = self.output_temp_folder / 'audio.aac'

        # Extract the audio
        ffmpeg = (
            FFmpeg
            .option(FFmpeg(), 'vn')
            .option('y')
            .input(self.input_file)
            .output(temp_audio_file,
                    {'c:v': 'copy'})
        )
    
        @ffmpeg.on('progress')
        def _on_progress(progress: Progress) -> None:
            print(progress)

        ffmpeg.execute()

    def _extract_frames(self) -> None:
        # Extract the frames
        ffmpeg = (
            FFmpeg
            .input(FFmpeg(), self.input_file)
            .output(f'{self.input_temp_folder}/%05d.png')
        )

        @ffmpeg.on('progress')
        def _on_progress(progress: Progress) -> None:
            print(progress)

        ffmpeg.execute()

    def _create_video(self) -> None:
        # Create a temporary file for the video
        temp_video_file = self.output_temp_folder / 'video.mp4'

        # Create the video from the enhanced frames
        ffmpeg = (
            FFmpeg
            .option(FFmpeg(), 'framerate', 30)
            .option('pattern_type', 'glob')
            .option('y')
            .input(self.output_temp_folder / '*.png')
            .output(temp_video_file,
                {
                    'c:v': 'libx264',
                    'b': '4000k',
                }
            )
        )

        @ffmpeg.on('progress')
        def _on_progress(progress: Progress) -> None:
            print(progress)

        ffmpeg.execute()

    def _add_audio(self) -> None:
        # Add the audio to the video
        ffmpeg = (
            FFmpeg
            .option(FFmpeg(), 'y')
            .input(self.output_temp_folder / 'video.mp4')
            .input(self.output_temp_folder / 'audio.aac')
            .output(self.output_file,
                {
                    'c': 'copy',
                }
            )
        )

        @ffmpeg.on('progress')
        def _on_progress(progress: Progress) -> None:
            print(progress)

        ffmpeg.execute()