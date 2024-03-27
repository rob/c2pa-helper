from dotenv import load_dotenv
import os
import argparse
from lib.c2pa import sign_file

load_dotenv()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sign a media file with content credentials.')

    parser.add_argument('media_path', type=str, help='Path to the media file to be signed')

    parser.add_argument('output_path', type=str, help='Output path for the signed media file')

    args = parser.parse_args()

    media_path = args.media_path
    output_path = args.output_path

    data_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'temp')

    try:
        sign_file(media_path, output_path, data_path)
        print(f"Signed media file saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
