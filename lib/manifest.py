import json
import os
from typing import Dict, List, Optional

from lib.assertions import (get_author_assertion, get_c2pa_created_assertion,
                            get_c2pa_published_assertion,
                            get_exif_datetime_original_assertion,
                            get_exif_gps_assertion,
                            get_exif_make_model_assertion,
                            get_training_mining_assertion)
from lib.image import get_image_metadata, get_mime_type, get_title


def generate_manifest(media_path: str) -> Optional[str]:
    mime_type: Optional[str] = get_mime_type(media_path)

    if not mime_type:
        raise RuntimeError("The mime type could not be determined.")

    image_metadata: Optional[Dict] = get_image_metadata(media_path)

    if not image_metadata:
        raise RuntimeError("The image metadata could not be retrieved.")

    manifest: Dict = {
        "title": get_title(media_path, image_metadata),
        "format": mime_type
    }

    potential_assertions: List[Optional[Dict]] = [
        get_training_mining_assertion(),
        # get_c2pa_created_assertion(image_metadata, type='minorHumanEdits'),
        get_c2pa_published_assertion(),
        get_author_assertion(image_metadata),
        get_exif_make_model_assertion(image_metadata),
        get_exif_gps_assertion(image_metadata),
        get_exif_datetime_original_assertion(image_metadata)
    ]

    valid_assertions: List[Dict] = [assertion for assertion in potential_assertions
                                    if isinstance(assertion, dict)]

    if not valid_assertions:
        raise RuntimeError("No valid assertions could be generated.")

    manifest['assertions'] = valid_assertions

    claim_generator: Optional[str] = os.environ.get('CLAIM_GENERATOR')

    if claim_generator:
        manifest['claim_generator'] = claim_generator

    return json.dumps(manifest)
