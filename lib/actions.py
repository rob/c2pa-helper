from typing import Dict


def get_c2pa_created_action(metadata: Dict, type: str = "minorHumanEdits") -> Dict:
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


def get_c2pa_published_action() -> Dict:
    """
    Returns the assertion for a published action in c2pa.

    Returns:
        Dict: The assertion for the published action.
    """
    return {"label": "c2pa.actions",
            "data": {"actions": [{"action": "c2pa.published"}]}}
