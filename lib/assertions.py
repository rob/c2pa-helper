import os
from typing import Dict, Optional


def get_training_mining_assertion() -> Dict:
    """
    Returns the assertion for training and mining data.

    Returns:
        Dict: The assertion for training and mining data.
    """
    return {
        "label": "c2pa.training-mining",
        "data": {
            "entries": {
                # AI generative training is not allowed
                "c2pa.ai_generative_training": {"use": "notAllowed"},
                "c2pa.ai_inference": {"use": "notAllowed"},  # AI inference is not allowed
                "c2pa.ai_training": {"use": "notAllowed"},  # AI training is not allowed
                "c2pa.data_mining": {"use": "notAllowed"}  # Data mining is not allowed
            }
        }
    }


def get_c2pa_created_assertion(metadata: Dict, type: str = "minorHumanEdits") -> Dict:
    """
    Returns the assertion for a created action in c2pa.

    Args:
        metadata (Dict): The metadata associated with the created action.
        type (str, optional): The type of digital source. Defaults to "minorHumanEdits".

    Returns:
        Dict: The assertion for the created action.
    """
    assertion = {"label": "c2pa.actions",
                 "data": {"actions": [{"action": "c2pa.created",
                                       "digitalSourceType": f"http://cv.iptc.org/newscodes/digitalsourcetype/{type}"}]}}

    if "XMP:HistorySoftwareAgent" in metadata:
        software_agent = metadata["XMP:HistorySoftwareAgent"]
        if isinstance(software_agent, list):
            software_agent = software_agent[0]

        assertion["data"]["actions"][0]["softwareAgent"] = software_agent

    return assertion


def get_c2pa_published_assertion() -> Dict:
    """
    Returns the assertion for a published action in c2pa.

    Returns:
        Dict: The assertion for the published action.
    """
    return {"label": "c2pa.actions",
            "data": {"actions": [{"action": "c2pa.published"}]}}


def get_author_assertion(metadata: Dict) -> Optional[Dict]:
    """
    Returns the assertion for the author of the content.

    Args:
        metadata (Dict): The metadata associated with the content.

    Returns:
        Optional[Dict]: The assertion for the author.
    """
    author = None
    author_keys = ['EXIF:Artist', 'XMP:Creator', 'XMP:Credit']
    organization_url = os.environ.get('ORGANIZATION_URL')
    instagram_name = os.environ.get('INSTAGRAM_NAME')
    instagram_url = os.environ.get('INSTAGRAM_URL')
    linkedin_name = os.environ.get('LINKEDIN_NAME')
    linkedin_url = os.environ.get('LINKEDIN_URL')

    # Find the author from the metadata
    for key in author_keys:
        if key in metadata:
            author = metadata[key]
            break

    # If no author and no additional information, return None
    if not author and not organization_url and not instagram_name and not instagram_url and not linkedin_name and not linkedin_url:
        return None

    # Create the assertion dictionary
    assertion = {"label": "stds.schema-org.CreativeWork",
                 "data": {"@context": "https://schema.org",
                          "@type": "CreativeWork"},
                 "kind": "Json"}

    # Add the author information to the assertion
    if author:
        assertion["data"].setdefault("author", []).append({"@type": "Person", "name": author})

    # Add the organization URL to the assertion
    if organization_url:
        assertion["data"]["url"] = organization_url

    # Add the Instagram information to the assertion
    if instagram_url and instagram_name:
        assertion["data"].setdefault("author", []).append({"@id": instagram_url,
                                                           "@type": "Organization",
                                                           "name": instagram_name})

    # Add the LinkedIn information to the assertion
    if linkedin_url and linkedin_name:
        assertion["data"].setdefault("author", []).append({"@id": linkedin_url,
                                                           "@type": "Organization",
                                                           "name": linkedin_name})

    return assertion


def get_exif_gps_assertion(metadata: Dict) -> Optional[Dict]:
    """
    Returns the assertion for the GPS metadata in the EXIF data.

    Args:
        metadata (Dict): The metadata associated with the content.

    Returns:
        Optional[Dict]: The assertion for the GPS metadata.
    """
    if 'EXIF:GPSLatitude' not in metadata or 'EXIF:GPSLongitude' not in metadata:
        return None

    exif_wrapper = _get_exif_wrapper()

    if 'EXIF:GPSLatitude' in metadata:
        exif_wrapper["data"]["EXIF:GPSLatitude"] = metadata['EXIF:GPSLatitude']

    if 'EXIF:GPSLongitude' in metadata:
        exif_wrapper["data"]["EXIF:GPSLongitude"] = metadata['EXIF:GPSLongitude']

    if 'EXIF:GPSAltitude' in metadata:
        exif_wrapper["data"]["EXIF:GPSAltitude"] = metadata['EXIF:GPSAltitude']

    if 'EXIF:GPSTimeStamp' in metadata:
        exif_wrapper["data"]["EXIF:GPSTimeStamp"] = metadata['EXIF:GPSTimeStamp']

    if 'EXIF:GPSHorizontalAccuracy' in metadata:
        exif_wrapper["data"]["EXIF:GPSHorizontalAccuracy"] = metadata['EXIF:GPSHorizontalAccuracy']

    return exif_wrapper


def get_exif_make_model_assertion(metadata: Dict) -> Optional[Dict]:
    """
    Returns the assertion for the make and model metadata in the EXIF data.

    Args:
        metadata (Dict): The metadata associated with the content.

    Returns:
        Optional[Dict]: The assertion for the make and model metadata.
    """
    # Check if 'EXIF:Make' and 'EXIF:Model' are present in the metadata
    if 'EXIF:Make' not in metadata or 'EXIF:Model' not in metadata:
        return None

    # Create the EXIF wrapper dictionary
    exif_wrapper = _get_exif_wrapper()

    # Add 'EXIF:Make' and 'EXIF:Model' to the EXIF wrapper data
    if 'EXIF:Make' in metadata:
        exif_wrapper["data"]["EXIF:Make"] = metadata['EXIF:Make']
    if 'EXIF:Model' in metadata:
        exif_wrapper["data"]["EXIF:Model"] = metadata['EXIF:Model']

    return exif_wrapper


def get_exif_datetime_original_assertion(metadata: Dict) -> Optional[Dict]:
    """
    Returns the assertion for the DateTimeOriginal metadata in the EXIF data.

    Args:
        metadata (Dict): The metadata associated with the content.

    Returns:
        Optional[Dict]: The assertion for the DateTimeOriginal metadata.
    """
    # Check if 'EXIF:DateTimeOriginal' is present in the metadata
    if 'EXIF:DateTimeOriginal' not in metadata:
        return None

    # Create the EXIF wrapper dictionary
    exif_wrapper = _get_exif_wrapper()

    # Add 'EXIF:DateTimeOriginal' to the EXIF wrapper data
    exif_wrapper["data"]["EXIF:DateTimeOriginal"] = metadata['EXIF:DateTimeOriginal']

    return exif_wrapper


def _get_exif_wrapper() -> Dict:
    """
    Returns the EXIF wrapper dictionary.

    Returns:
        Dict: The EXIF wrapper dictionary.
    """
    return {
        "label": "stds.exif",
        "data": {
            "@context": {
                "EXIF": "http://ns.adobe.com/EXIF/1.0/",
                "EXIFEX": "http://cipa.jp/EXIF/2.32/",
                "dc": "http://purl.org/dc/elements/1.1/",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "tiff": "http://ns.adobe.com/tiff/1.0/",
                "xmp": "http://ns.adobe.com/xap/1.0/"
            }
        },
        "kind": "Json"
    }
