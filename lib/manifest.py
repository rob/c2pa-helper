import json
import os
from typing import Dict, List, Optional

from lib.actions import get_c2pa_published_action
from lib.assertions import (get_author_assertion,
                            get_exif_datetime_original_assertion,
                            get_exif_gps_assertion,
                            get_exif_make_model_assertion,
                            get_training_mining_assertion)
from lib.media import get_media_metadata, get_mime_type


def generate_manifest(media_path: str) -> Optional[str]:
    mime_type: Optional[str] = get_mime_type(media_path)

    if not mime_type:
        raise RuntimeError("The mime type could not be determined.")

    image_metadata: Optional[Dict] = get_media_metadata(media_path)

    if not image_metadata:
        raise RuntimeError("The image metadata could not be retrieved.")

    manifest: Dict = {
        "title": _get_title(media_path, image_metadata),
        "format": mime_type
    }

    potential_assertions_actions: List[Optional[Dict]] = [
        get_training_mining_assertion(),
        # get_c2pa_created_action(image_metadata, type='minorHumanEdits'),
        get_c2pa_published_action(),
        get_author_assertion(image_metadata),
        get_exif_make_model_assertion(image_metadata),
        get_exif_gps_assertion(image_metadata),
        get_exif_datetime_original_assertion(image_metadata)
    ]

    valid_assertions_actions: List[Dict] = [assertion_or_action
                                            for assertion_or_action in potential_assertions_actions
                                            if isinstance(assertion_or_action, dict)]

    if not valid_assertions_actions:
        raise RuntimeError("No valid assertions could be generated.")

    manifest['assertions'] = valid_assertions_actions

    claim_generator: Optional[str] = os.environ.get('CLAIM_GENERATOR')

    if claim_generator:
        manifest['claim_generator'] = claim_generator

    return json.dumps(manifest)


def _get_title(media_path: str, metadata: dict) -> str:
    if 'XMP:Title' in metadata:
        return metadata['XMP:Title']

    return os.path.basename(media_path)
