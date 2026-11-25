"""Prepare browser app terms and offline assets in sibling repository checkouts."""
import argparse
import hashlib
import html
import json
import re
import zipfile
from pathlib import Path

PROJECTS = Path(__file__).resolve().parents[1]
APPLICATIONS = {
    "FQ-Lite": "FirmQuill Lite", "CurbQuill": "CurbQuill", "Day-Leaf": "DayLeaf",
    "MileQuill-Lite": "MileQuill Lite", "PocketQuill": "PocketQuill",
}

def read(path):
    return path.read_text(encoding="utf-8-sig")

def write(path, content):
    path.write_text(content, encoding="utf-8", newline="\n")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def version_number(version):
    return [int(part) for part in version.split(".")]

def render_article(document):
    lines = ['<article data-terms-version="' + document["version"] + '">']
    for i, paragraph in enumerate(document["text"].strip().split("\n\n")):
        tag = "p"
        if i == 0:
            tag = "h1"
        elif i > 1 and len(paragraph) < 80 and not paragraph.endswith((".", "?", "!")):
            tag = "h2"
        lines.append(f"<{tag}>{html.escape(paragraph)}</{tag}>")
    return "\n".join(lines) + "</article>"

def refresh_offline(root, name):
    worker = read(root / "sw.js")
    compact = (",", ":")
    if name in ("FQ-Lite", "PocketQuill"):
        pattern = r"(const (?:shell|assets)\s*=\s*)(\[[^\]]+\])"
        match = re.search(pattern, worker)
        files = json.loads(match[2].replace("'", '"'))
        for path in ("terms.json", "privacy.html", "privacy.css"):
            if path not in files:
                files.append(path)
        version = digest(b"".join((root / path).read_bytes() for path in files))[:20]
        worker = worker.replace(match[0], match[1] + json.dumps(files, separators=compact))
        if name == "FQ-Lite":
            worker = re.sub(r"const cacheName=prefix\+'[^']*'", f"const cacheName=prefix+'{version}'", worker)
        else:
            worker = re.sub(r"const VERSION = '[^']*'", f"const VERSION = '{version}'", worker)
    else:
        dayleaf = name == "Day-Leaf"
        pattern = r"const assetDigests = (\{[^}]+\});" if dayleaf else r"const (?:INVENTORY|release) = (\{[^\n]+\});"
        match = re.search(pattern, worker)
        inventory = json.loads(match[1])
        files = inventory if dayleaf else inventory["files" if name == "CurbQuill" else "assets"]
        files.update({path: "" for path in ("terms.json", "privacy.html", "privacy.css")})
        for path in files:
            data = (root / path).read_bytes()
            if name != "CurbQuill" and Path(path).suffix in (".js", ".mjs", ".css", ".html", ".json", ".webmanifest"):
                data = data.replace(b"\r\n", b"\n")
            files[path] = digest(data)
        stable = dict(files)
        if dayleaf:
            # The handshake itself contains this build ID.
            stable.pop("offline.js")
        version = digest(json.dumps(stable, sort_keys=True).encode())[:20]
        if dayleaf:
            for path in ["offline.js", "sw.js"]:
                text = worker if path == "sw.js" else read(root / path)
                updated = re.sub(r"const build = '[^']+'", f"const build = '{version}'", text)
                if path == "sw.js":
                    worker = updated
                else:
                    write(root / path, updated)
            files["offline.js"] = digest((root / "offline.js").read_bytes())
            encoded = json.dumps(files, indent=2)
        else:
            inventory["version"] = version
            encoded = json.dumps(inventory, separators=compact)
        worker = worker.replace(match[1], encoded)
    write(root / "sw.js", worker)
    if name == "Day-Leaf":
        archive = root / "Dayleaf-static.zip"
        # Package the verified runtime inventory, including the worker and Pages marker.
        paths = sorted(set(files) | {"sw.js", ".nojekyll"})
        temp = archive.with_suffix(".tmp")
        with zipfile.ZipFile(temp, "w", zipfile.ZIP_DEFLATED) as updated:
            for path in paths:
                updated.write(root / path, path)
        temp.replace(archive)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", choices=APPLICATIONS)
    parser.add_argument("agreement", type=Path, help="UTF-8 text with title, blank line, then Version N.N  |  date")
    parser.add_argument("--approved", action="store_true", help="Mark the supplied text as publisher-approved")
    parser.add_argument("--app-root", type=Path, help="App checkout if outside the sibling directories")
    args = parser.parse_args()
    root = args.app_root.resolve() if args.app_root else PROJECTS.parent / args.app
    document = json.loads(read(root / "terms.json"))
    text = read(args.agreement).strip()
    title = APPLICATIONS[args.app] + " Terms of Service"
    match = re.match(re.escape(title) + r"\n\nVersion (\d+(?:\.\d+)*) +\| +[^\n]+\n\n\S", text)
    if not match:
        parser.error("The document must use the app title and a numbered version/date line.")
    version = match[1]
    if text != document["text"] and version_number(version) <= version_number(document["version"]):
        parser.error("Use a higher version number for revised terms.")
    document.update(version=version, text=text, status="approved" if args.approved else "draft")
    page = PROJECTS / "terms" / document["appId"] / "index.html"
    public = read(page)
    status = "Publisher-approved terms" if args.approved else "Draft for publisher review"
    public, count = re.subn(r'<p class="kicker">(?:Publisher-approved terms|Draft for publisher review)</p>\s*<article data-terms-version="[^"]+">.*?</article>', lambda _: '<p class="kicker">' + status + '</p>' + render_article(document), public, count=1, flags=re.S)
    if count != 1:
        parser.error("The agreement section in the public page could not be identified.")
    write(root / "terms.json", json.dumps(document, ensure_ascii=False, indent=2) + "\n")
    write(page, public)
    refresh_offline(root, args.app)
    print(args.app, version, document["status"], "prepared locally")

if __name__ == "__main__":
    main()

