"""Format list shows your device public IP address.
Why?:
 It seems like YouTube makes the video available
 specifically for your IP for some reason.
 The IP address is found in the video url query.

There is also a timelimit found in the query. The link is not permanent.
To prevent your IP from getting leaked, run this script.
Replaces url strings, from 'format.json', 'filtered format.json'
Also removes http_header dictionary."""

import json, pathlib

ROOT = pathlib.Path(__file__).parent.parent

CEN_MSG: str = "Removed for safety"

global result

# results
with open(ROOT / "tests/results.json", "r") as f:
    result = json.load(f)

for info in result["formats"]:
    if info.get("url"):
        info["url"] = CEN_MSG

    if info.get("manifest_url"):
        info["manifest_url"] = CEN_MSG

    if info.get("fragments"):
        for frag in info["fragments"]:
            frag["url"] = CEN_MSG

    if info.get("http_headers"):
        info["http_headers"] = {}

if result.get("thumbnails"):
    for thumb_data in result["thumbnails"]:
        thumb_data["url"] = CEN_MSG

if result.get("requested_formats"):
    for info in result["requested_formats"]:
        if info.get("url"):
            info["url"] = CEN_MSG

        if info.get("http_headers"):
            info["http_headers"] = {}

if result.get("automatic_captions"):
    for k, data_list in result["automatic_captions"].items():
        for format in data_list:
            format["url"] = CEN_MSG

if result.get("subtitles"):
    for k, data_list in result["subtitles"].items():
        for subtitle in data_list:
            subtitle["url"] = CEN_MSG

with open(ROOT / "tests/results.json", "w") as f:
    json.dump(result, f, indent=4)

# formats
with open(ROOT / "tests/formats.json", "r") as f:
    result = json.load(f)

for info in result:
    if info.get("url"):
        info["url"] = CEN_MSG

    if info.get("manifest_url"):
        info["manifest_url"] = CEN_MSG

    if info.get("fragments"):
        for frag in info["fragments"]:
            frag["url"] = CEN_MSG

    if info.get("http_headers"):
        info["http_headers"] = {}

with open(ROOT / "tests/formats.json", "w") as f:
    json.dump(result, f, indent=4)

# filtered formats
with open(ROOT / "tests/filtered formats.json", "r") as f:
    result = json.load(f)

for info in result:
    if info.get("url"):
        info["url"] = CEN_MSG

    if info.get("manifest_url"):
        info["manifest_url"] = CEN_MSG

    if info.get("fragments"):
        for frag in info["fragments"]:
            frag["url"] = CEN_MSG

    if info.get("http_headers"):
        info["http_headers"] = {}

with open(ROOT / "tests/filtered formats.json", "w") as f:
    json.dump(result[::-1], f, indent=4)
