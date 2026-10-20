# Builds obtainium-android-recomps.json (the Obtainium import file) and the app table in README.md.
# To add an app: append a row to APPS, then run `python3 -I gen.py`.
import json, os, re, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "obtainium-android-recomps.json"
REPO = "heyalmoo/Obtainium-Android-Recomps"
REPO_ID = "1427406465"  # GitHub repo id; Obtainium uses it as the id of track-only GitHub apps
CATEGORY = "Recomp"

# Default per-app settings, taken from RJNY/Obtainium-Emulation-Pack
base = json.load(open(os.path.join(HERE, "base-settings.json")))
V3 = r"\d+\.\d+\.\d+"

APPS = [
 # package id, owner/repo, name, game (platform), overrides of the default settings
 ("com.aure.banjorecomp", "AurelioB/BanjoRecomp-Android", "Banjo Recompiled",
  "Banjo-Kazooie (N64)",
  dict(includePrereleases=True, versionExtractionRegEx=V3)),
 ("dev.twilitrealm.dusk", "TwilitRealm/dusklight", "Dusklight",
  "The Legend of Zelda: Twilight Princess (GameCube)",
  dict(apkFilterRegEx=r"android-arm64\.apk$")),
 ("dev.net64.ghostship", "HarbourMasters/Ghostship", "Ghostship",
  "Super Mario 64 (N64)",
  dict(includeZips=True, apkFilterRegEx=r"Android", zippedApkFilterRegEx=r"\.apk$", versionDetection=False)),
 ("com.halo.decomp", "FulGerNet/halo-ce-android", "Halo CE Android",
  "Halo: Combat Evolved (Xbox / PC)",
  dict(versionDetection=False)),
 ("com.ast.openmw", "Andiweli/OpenMW-Android", "OpenMW",
  "The Elder Scrolls III: Morrowind (PC)",
  dict(versionDetection=False)),
 ("com.linkzenic.soh", "linkzenic/Shipwright-Android", "Ship of Harkinian",
  "The Legend of Zelda: Ocarina of Time (N64)",
  dict(apkFilterRegEx=r"^soh[-_](release[-_])?v\d", versionDetection=False)),
 ("io.github.hm64recomp", "igawa6/HarvestMoon64Recomp", "Harvest Moon 64 Recompiled",
  "Harvest Moon 64 (N64)",
  {}),
 ("com.starship.android", "izzy2lost/Starship", "Starship",
  "Star Fox 64 (N64)",
  {}),
 ("com.openport.galaxyandroid", "OpenPort-Labs/Galaxy-Android", "Galaxy Android",
  "Super Mario Galaxy (Wii)",
  dict(versionDetection=False)),
]

def entry(pid, repo, name, about, settings, allow_id_change=True):
    s = dict(base); s.update(about=about, **settings)
    return {"id": pid, "url": "https://github.com/" + repo, "author": repo.split("/")[0], "name": name,
            "preferredApkIndex": 0, "additionalSettings": json.dumps(s, ensure_ascii=False),
            "categories": [CATEGORY], "allowIdChange": allow_id_change, "overrideSource": "GitHub"}

def add_link(app):
    # Same one-tap link format as RJNY: opens Obtainium with this single app prefilled
    a = dict(app, otherAssetUrls=None, apkUrls=None)
    a.pop("categories")
    return "https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/" + urllib.parse.quote(json.dumps(a, separators=(",", ":")), safe="")

apps = [entry(pid, repo, name, f"{game} native port", ov) for pid, repo, name, game, ov in APPS]
# The pack tracks itself: Obtainium notifies when a new release of this list is out
self_app = entry(REPO_ID, REPO, "Obtainium Android Recomps", "This pack: notifies you when a new version of the list is released",
                 dict(trackOnly=True, appName="Obtainium Android Recomps"), allow_id_change=False)
json.dump({"apps": apps + [self_app]}, open(os.path.join(HERE, OUT), "w"), ensure_ascii=False, indent=2)

rows = ["| Port | Game | Add to Obtainium |", "|---|---|:---:|"]
for app, (_, repo, name, game, _) in zip(apps, APPS):
    rows.append(f"| [{name}](https://github.com/{repo}) | {game} | [Add to Obtainium!]({add_link(app)}) |")
rows.append(f"| [Obtainium Android Recomps](https://github.com/{REPO}) | this pack, track-only | [Add to Obtainium!]({add_link(self_app)}) |")
readme = os.path.join(HERE, "README.md")
text = open(readme).read()
text = re.sub(r"(<!-- apps:start -->\n).*?(<!-- apps:end -->)", lambda m: m[1] + "\n".join(rows) + "\n" + m[2], text, flags=re.S)
open(readme, "w").write(text)
print(len(apps), "apps + self-tracking entry")
