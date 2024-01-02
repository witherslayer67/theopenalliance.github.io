import json

import validators
from tbapy import TBA
from tqdm import tqdm

tba = TBA("shLVepNTB23kq5KYRfb9OeboVb98Sd13YKd4d5WDYqVU94ZGzmNUQPk15QfAshss")


def maybe_add_url(arr, url, tooltip):
    if not url.startswith("http"):
        url = f"https://{url}"

    if len(url) > 0 and validators.url(url):
        arr.append({"url": url, "name": tooltip})


with open("oa.tsv", "r") as f:
    out = []
    warnings = []

    for line in tqdm(list(f.readlines()[1:])):
        _, number, name, _, *maybe_urls = line.split("\t")
        urls = []

        for idx, tooltip in [
            [0, "Build Thread"],
            [1, "CAD"],
            [2, "Code"],
            [3, "Photos"],
            [4, "Videos"],
        ]:
            maybe_add_url(urls, maybe_urls[idx], tooltip)

        if len(maybe_urls[5]) > 0:
            warnings.append(number)

        tba_info = tba.team(team=f"frc{number}")

        out.append(
            {
                "number": int(number),
                "name": name,
                "location": f'{tba_info["city"]}, {tba_info["state_prov"]}, {tba_info["country"]}',
                "media": urls,
            }
        )

out.sort(key=lambda d: d["number"])

print(f"Review other URLs for {warnings}")

with open("oa.json", "w+") as f:
    json.dump(out, f, indent=4)
