from pathlib import Path

import typer

from enhancer import VideoProcessor, VALID_VIDEO_FILE_EXTENSIONS

def main(input_file: Path, output_file: Path) -> None:
    # Check that the input file exists and is a video
    if not input_file.exists():
        raise typer.BadParameter(f'Input file {input_file} does not exist')
    if not input_file.is_file():
        raise typer.BadParameter(f'Input file {input_file} is not a file')
    if input_file.suffix not in VALID_VIDEO_FILE_EXTENSIONS:
        raise typer.BadParameter(f'Input file {input_file} is not a video')

    # Check that the output file does not exist and is a video
    if output_file.suffix not in VALID_VIDEO_FILE_EXTENSIONS:
        raise typer.BadParameter(f'Output file {output_file} is not a video')
    if output_file.exists():
        # Check whether the output file should be overwritten
        if not typer.confirm(f'Output file {output_file} already exists. Overwrite?'):
            # Print a message and exit
            typer.echo('File will not be overwritten, exiting...')
            raise typer.Exit(code=0)

    # Instantiate the converter
    video_processor = VideoProcessor(input_file, output_file)

    # Convert the images
    video_processor.enhance()

if __name__ == '__main__':
    typer.run(main)
