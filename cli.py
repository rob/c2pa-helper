import argparse

from dotenv import load_dotenv

from lib.c2pa import sign_file

load_dotenv()


if __name__ == "__main__":

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description='Sign a media file with content credentials.')

    parser.add_argument('media_path', type=str, help='Path to the media file to be signed')

    parser.add_argument('output_path', type=str, help='Output path for the signed media file')

    args: argparse.Namespace = parser.parse_args()

    media_path: str = args.media_path
    output_path: str = args.output_path

    try:
        sign_file(media_path, output_path)
        print(f"Signed media file saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
