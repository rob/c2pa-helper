import os
from typing import Dict, Optional


def get_training_mining_assertion() -> Dict:
    return {
        "label": "c2pa.training-mining",
        "data": {
            "entries": {
                "c2pa.ai_generative_training": {"use": "notAllowed"},
                "c2pa.ai_inference": {"use": "notAllowed"},
                "c2pa.ai_training": {"use": "notAllowed"},
                "c2pa.data_mining": {"use": "notAllowed"}
            }
        }
    }


def get_c2pa_created_assertion(metadata: Dict, type: str = "minorHumanEdits") -> Dict:
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
    return {"label": "c2pa.actions",
            "data": {"actions": [{"action": "c2pa.published"}]}}


def get_author_assertion(metadata: Dict) -> Optional[Dict]:
    author = None
    author_keys = ['EXIF:Artist', 'XMP:Creator', 'XMP:Credit']
    organization_url = os.environ.get('ORGANIZATION_URL')
    instagram_name = os.environ.get('INSTAGRAM_NAME')
    instagram_url = os.environ.get('INSTAGRAM_URL')
    linkedin_name = os.environ.get('LINKEDIN_NAME')
    linkedin_url = os.environ.get('LINKEDIN_URL')

    for key in author_keys:
        if key in metadata:
            author = metadata[key]
            break

    if not author and not organization_url and not instagram_name and not instagram_url and not linkedin_name and not linkedin_url:
        return None

    assertion = {"label": "stds.schema-org.CreativeWork",
                 "data": {"@context": "https://schema.org",
                          "@type": "CreativeWork"},
                 "kind": "Json"}

    if author:
        assertion["data"].setdefault("author", []).append({"@type": "Person", "name": author})

    if organization_url:
        assertion["data"]["url"] = organization_url

    if instagram_url and instagram_name:
        assertion["data"].setdefault("author", []).append({"@id": instagram_url,
                                                           "@type": "Organization",
                                                           "name": instagram_name})

    if linkedin_url and linkedin_name:
        assertion["data"].setdefault("author", []).append({"@id": linkedin_url,
                                                           "@type": "Organization",
                                                           "name": linkedin_name})

    return assertion


def _get_exif_wrapper() -> Dict:
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


def get_exif_gps_assertion(metadata: Dict) -> Optional[Dict]:
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
    if 'EXIF:Make' not in metadata or 'EXIF:Model' not in metadata:
        return None

    exif_wrapper = _get_exif_wrapper()

    if 'EXIF:Make' in metadata:
        exif_wrapper["data"]["EXIF:Make"] = metadata['EXIF:Make']
    if 'EXIF:Model' in metadata:
        exif_wrapper["data"]["EXIF:Model"] = metadata['EXIF:Model']

    return exif_wrapper


def get_exif_datetime_original_assertion(metadata: Dict) -> Optional[Dict]:
    if 'EXIF:DateTimeOriginal' not in metadata:
        return None

    exif_wrapper = _get_exif_wrapper()
    exif_wrapper["data"]["EXIF:DateTimeOriginal"] = metadata['EXIF:DateTimeOriginal']

    return exif_wrapper
