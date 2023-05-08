from enum import Enum
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

from PIL import Image, ImageFilter

from rich.progress import track

class EnhanceOptions(str, Enum):
    UNSHARP_MASK = 'unsharp_mask'
    SMOOTH = 'smooth'

class ImageEnhancer:
    def __init__(self, input_folder: Path, output_folder: Path) -> None:
        self.output_folder = output_folder
        self.input_files = list(input_folder.glob('*.png'))

    def convert(self) -> None:
        # Create output folder if it doesn't exist
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # Create a process pool
        with ProcessPoolExecutor() as executor:
            jobs = []
            for input_file in track(self.input_files, description='Submitting jobs...'):
                # print(f'Submitting {input_file.name}...')
                jobs.append(executor.submit(self._convert_image, input_file))

            # Wait for all jobs to finish
            for job in track(jobs, description='Waiting for jobs to finish...'):
                job.result()

    def _convert_image(self, input_file: Path) -> bool:
        # Open image
        image = Image.open(input_file)

        # Unsharp mask
        image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

        # Smooth
        image = image.filter(ImageFilter.SMOOTH)

        # Save to output folder
        output_file = self.output_folder / input_file.name
        image.save(output_file)

        return True
