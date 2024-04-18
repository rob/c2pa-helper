import os
from typing import Optional

import exiftool


def get_media_metadata(media_path: str) -> Optional[dict]:
    metadata_values = {}

    with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata([media_path])

        if not metadata:
            raise ValueError("The 'metadata' parameter is missing or empty.")

        for d in metadata:
            for key, value in d.items():
                metadata_values[key] = value

    return metadata_values


def get_mime_type(media_path: str) -> Optional[str]:
    mime_types = {
        'avi': "video/msvideo",
        'avif': "image/avif",
        # 'c2pa': "application/x-c2pa-manifest-store",
        'dng': "image/x-adobe-dng",
        'heic': "image/heic",
        'heif': "image/heif",
        'jpg': "image/jpeg",
        'jpeg': "image/jpeg",
        # 'm4a': "audio/mp4",
        # 'mp3': "audio/mpeg",
        'mp4': "video/mp4",
        'mov': "video/quicktime",
        # 'pdf': "application/pdf",
        'png': "image/png",
        'svg': "image/svg+xml",
        'tif': "image/tiff",
        'tiff': "image/tiff",
        # 'wav': "audio/x-wav",
        'webp': "image/webp",
    }

    _, ext = os.path.splitext(media_path)
    ext = ext.lstrip('.').lower()

    return mime_types.get(ext, None)


def get_media_type(mime_type: Optional[str]) -> Optional[str]:
    if mime_type is None:
        return None

    if mime_type.startswith("image/"):
        return "image"
    elif mime_type.startswith("video/"):
        return "video"

    return None
