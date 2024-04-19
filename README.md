# c2pa-helper

Helper for generating [C2PA](https://opensource.contentauthenticity.org/) [manifests](https://opensource.contentauthenticity.org/docs/manifest/understanding-manifest) and attaching them to media assets.

## Overview

This tool helps extract metadata from a media asset (e.g., EXIF, IPTC, and XMP) and generate the proper [assertions and actions](https://opensource.contentauthenticity.org/docs/manifest/assertions-actions) to be included in the [manifest](https://opensource.contentauthenticity.org/docs/manifest/understanding-manifest). It then takes this generated manifest and [signs](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests) the media asset with it, optionally using your own [certificate](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests#example).

Once the media asset is signed, you can use tools like the C2PA's [Verify tool](https://opensource.contentauthenticity.org/docs/verify) to upload the media asset and view its signed credentials.

### Metadata

If any of the following is found in the media asset, it's included in the generated manifest:

- **Title**, by looking at the `XMP:Title` field (otherwise, it defaults to the filename itself)
- **Author**, by looking for `'EXIF:Artist'`, `'XMP:Creator'`, or `'XMP:Credit'` fields
- **Camera make and model**, by looking for `EXIF:Make` or `EXIF:Model`
- **GPS information**, by looking at the numerous `EXIF:GPS*` fields
- **Original date and time**, by looking at the `EXIF:DateTimeOriginal` field

In addition to metadata like EXIF, IPTC, and XMP above, this tool also includes support for including other information in the manifest, such as:

- Your organization's [website, Instagram page, and LinkedIn page](https://opensource.contentauthenticity.org/docs/verify#credit-and-usage) (shown in the [Verify tool](https://contentcredentials.org/verify))
- [Do not train](https://opensource.contentauthenticity.org/docs/manifest/assertions-actions#do-not-train-assertion) assertions, to specify the media asset shouldn't be used for AI purposes

## Installation

> [!NOTE]
> Depending on your OS and environment, you may need to modify some of these commands.

```
git clone https://github.com/rob/c2pa-helper.git && \
cd c2pa-helper && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt
```

### Dependencies

- [c2pa-python](https://github.com/contentauth/c2pa-python)
- [PyExifTool](https://github.com/sylikc/pyexiftool)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## Configuration

Copy `.env.sample` to `.env` and modify the values to fit your needs.

Every single variable in this file is optional; if you don't need it, remove it.

> [!IMPORTANT]
> If you don't have your own [certificate](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests), remove all of the `CERT` variables and it will use the built-in certificate found in `certs/sample`. This certificate is pulled directly from the [C2PA repository](https://github.com/contentauth/c2patool/tree/main/sample).

## Limitations

Right now, the tool assumes you are generating a manifest and signing a media asset for the first time, so everything you sign gets the [c2pa.published](https://c2pa.org/specifications/specifications/1.3/specs/C2PA_Specification.html#_actions) action included in its manifest.

This might not make sense if you're trying to re-sign a media asset after making changes to it and already signing it previously.
