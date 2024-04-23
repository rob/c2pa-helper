# c2pa-helper

This Python script is a small wrapper around the [sign_file](https://github.com/contentauth/c2pa-python?tab=readme-ov-file#add-a-signed-manifest-to-a-media-file) function from the [c2pa-python](https://github.com/contentauth/c2pa-python) library that helps generate the [manifest](https://opensource.contentauthenticity.org/docs/manifest/manifest-ref/#manifest) JSON necessary before [signing and attaching](https://opensource.contentauthenticity.org/docs/c2pa-python/#add-a-signed-manifest-to-a-media-file) the manifest to a media file.

### More information

-   [Coalition for Content Provenance and Authenticity (C2PA)](https://c2pa.org/)
-   [Content Authenticity Initiative (CAI)](https://contentauthenticity.org/)
-   [Open-source tools for content authenticity and provenance](https://opensource.contentauthenticity.org/)
-   [Working with manifests](https://opensource.contentauthenticity.org/docs/manifest/understanding-manifest)
-   [Manifest store reference](https://opensource.contentauthenticity.org/docs/manifest/manifest-ref)
-   [Signing manifests](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests)

## Overview

This script extracts metadata from a media file (e.g., EXIF, IPTC, and XMP) and generates the [manifest](https://opensource.contentauthenticity.org/docs/manifest/manifest-ref/#manifest) JSON with C2PA's [assertions and actions](https://opensource.contentauthenticity.org/docs/manifest/assertions-actions). It uses this generated manifest JSON to [sign](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests) and [attach](https://opensource.contentauthenticity.org/docs/c2pa-python/#add-a-signed-manifest-to-a-media-file) the manifest to a media file, optionally using your own [certificate](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests#example).

Once the media file is signed, end users can use something like the C2PA's online [Verify tool](https://opensource.contentauthenticity.org/docs/verify) to upload the media file and view its signed content credentials (i.e., the manifests.) There's also a command line tool called [c2patool](https://opensource.contentauthenticity.org/docs/c2patool/) available.

> [!IMPORTANT] > **This script was designed to be modified to fit your individual needs. It includes support for the metadata below and assumes certain things — like your media file never being signed before (see [Considerations](#considerations)).**
>
> **For example, you might need to support custom IPTC fields not handled below, change the order in how you search for the "author" field, or want to remove the GPS data assertion from being included for privacy reasons.**
>
> **Out of the box, this script handles a lot of the actions, assertions, and organizational information (i.e., website and social networks) that are displayed on the C2PA's online [Verify tool](https://opensource.contentauthenticity.org/docs/verify) when uploading and validating content credentials found inside a media file.**

### Metadata included

If any of the following metadata is found in the media file, it's included in the generated manifest:

| Metadata                   | Description                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------ |
| **Title**                  | Extracted from `XMP:Title` <br> (or defaults to filename)                            |
| **Author**                 | First occurance of `EXIF:Artist`, `XMP:Creator`, or `XMP:Credit` <br>(in that order) |
| **Camera make and model**  | Extracted from `EXIF:Make` and `EXIF:Model`                                          |
| **GPS information**        | Extracted from `EXIF:GPS*` fields                                                    |
| **Original date and time** | Extracted from `EXIF:DateTimeOriginal`                                               |

### Extra metadata included

In addition to the above, the following is also included in the manifest:

-   Assertions for your organization's [website, Instagram page, and LinkedIn page](https://opensource.contentauthenticity.org/docs/verify#credit-and-usage) (shown in the [Verify tool](https://contentcredentials.org/verify))
    -   These values are edited in your `.env` file (see [Configuration](#configuration))
-   [Do not train](https://opensource.contentauthenticity.org/docs/manifest/assertions-actions#do-not-train-assertion) assertions, to specify the media file shouldn't be used for data mining, machine learning (ML) training, or inference purposes

## Installation

### Dependencies

-   [c2pa-python](https://github.com/contentauth/c2pa-python)
-   [PyExifTool](https://github.com/sylikc/pyexiftool)
-   [python-dotenv](https://github.com/theskumar/python-dotenv)

> [!NOTE]
> Depending on your OS and environment, you may need to modify some of these commands.

```
git clone https://github.com/rob/c2pa-helper.git && \
cd c2pa-helper && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -r requirements.txt
```

## Configuration

Copy `.env.sample` to `.env` and modify the variable values.

> [!NOTE]
> All of the variables found in `.env` are optional — remove any that you don't need.

| Variable             | Description                                                                                                                                                                                               |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAIM_GENERATOR`    | Specifies the generator of the claim (e.g., "org-name/0.1.0") ([docs](https://opensource.contentauthenticity.org/docs/verify/#app-or-device-used))                                                        |
| `CERT_TYPE`          | The type of certificate, e.g., "ps256" ([docs](https://opensource.contentauthenticity.org/docs/c2patool/x_509/))                                                                                          |
| `CERT`               | Path to the certificate file ([docs](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests))                                                                                         |
| `CERT_PRIVATE_KEY`   | Path to the certificate's private key file ([docs](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests))                                                                           |
| `CERT_TIMESTAMP_URL` | URL for the certificate timestamping service ([docs](https://opensource.contentauthenticity.org/docs/manifest/understanding-manifest/#time-stamps))<br>(You shouldn't need to modify this in most cases.) |
| `ORGANIZATION_URL`   | The URL of the organization's homepage ([docs](https://opensource.contentauthenticity.org/docs/verify/#produced-by))                                                                                      |
| `LINKEDIN_NAME`      | The name of the organization on LinkedIn ([docs](https://opensource.contentauthenticity.org/docs/verify/#social-media-accounts))                                                                          |
| `LINKEDIN_URL`       | URL to the organization's LinkedIn page ([docs](https://opensource.contentauthenticity.org/docs/verify/#social-media-accounts))                                                                           |
| `INSTAGRAM_NAME`     | The organization's Instagram username ([docs](https://opensource.contentauthenticity.org/docs/verify/#social-media-accounts))                                                                             |
| `INSTAGRAM_URL`      | URL to the organization's Instagram page ([docs](https://opensource.contentauthenticity.org/docs/verify/#social-media-accounts))                                                                          |

> [!IMPORTANT]
> If you don't have your own [certificate](https://opensource.contentauthenticity.org/docs/manifest/signing-manifests), remove all of the `CERT` variables and `sign_file` will use the built-in certificate found in `certs/sample`. This certificate is pulled directly from the [C2PA repository](https://github.com/contentauth/c2patool/tree/main/sample) and will show as "C2PA Test Signing Cert" in the C2PA's online [Verify tool](https://opensource.contentauthenticity.org/docs/verify).

## Modifying

Assertions are functions stored in `lib/assertions.py` that return a `Dict` if they're valid, or `None` if the assertion isn't valid (e.g., you're looking for the `EXIF:DateTimeOriginal` field but it isn't found in the metadata.)

You can modify these assertion functions or add new ones.

These assertion functions are called from `lib/manifest.py` in the `potential_assertions` `List` in the order you specify. They're only included in the final manifest JSON if they return a `Dict` (i.e., not `None`.)

## Usage

Assuming your `.env` is set up and the `potential_assertions` `List` in `lib/manifest.py` contains all of the actions and assertions you want to include, you can run the script via `cli.py` (for a single file) or `batch.py` (to batch process multiple files inside a directory.)

### cli.py

`python cli.py /path/to/original_file /path/to/signed_file`

### batch.py

[...]

## Considerations

### `c2pa.published` action

Right now, this script assumes you are generating a manifest and signing a media file for the first time, so everything signed gets the [c2pa.published](https://c2pa.org/specifications/specifications/1.3/specs/C2PA_Specification.html#_actions) action included in its manifest.

This might not make sense if you're trying to re-sign a media file after making changes to it and have already signed it previously. You would want to use a different action, most likely.

For example, you might want to use `c2pa.resized`, `c2pa.filtered`, or `c2pa.color_adjustments` instead.
