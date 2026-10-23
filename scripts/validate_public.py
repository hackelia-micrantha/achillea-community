#!/usr/bin/env python3
"""Offline public documentation/fixture validation; no private sources or network."""

from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


CONFORMANCE_PATH = Path("docs/specifications/conformance/application-cycle-v0.1.json")
SCHEMA_VERSION = "0.1-draft"
LOCAL_MARKDOWN = ("*.md", "docs/**/*.md")
ALLOWED_REMOTE_SCHEMES = frozenset({"https", "http", "mailto"})
FENCE = re.compile(r"^ {0,3}(?P<marker>\x60{3,}|~{3,})(?P<rest>.*)$")
INLINE_CODE = re.compile(r"(?<![\\\x60])(\x60+)(?!\x60)(.*?)(?<!\\)\1(?!\x60)")
INLINE_LINK = re.compile(
    r"""(?<!\\)!?\[[^\]\n]*\]\(\s*(?P<url><[^>\n]+>|[^\s)]+)(?:\s+(?:"[^"\n]*"|'[^'\n]*'))?\s*\)"""
)


class SiteLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append((self.getpos()[0], value))


def validate_link(root: Path, source: Path, line: int, href: str) -> list[str]:
    href = unescape(href.strip("<>"))
    if not href or href.startswith("#") or href.startswith("//"):
        return []
    parsed = urlsplit(href)
    display = f"{source.relative_to(root)}:{line}"
    if parsed.scheme:
        if parsed.scheme.lower() not in ALLOWED_REMOTE_SCHEMES:
            return [f"{display}: unsupported URI scheme: {href}"]
        return []
    if not parsed.path:
        return []
    local = Path(unquote(parsed.path))
    if local.is_absolute():
        return [f"{display}: absolute repository link: {href}"]
    target = (source.parent / local).resolve()
    if not target.is_relative_to(root):
        return [f"{display}: link escapes repository: {href}"]
    if not target.exists():
        return [f"{display}: missing link target: {href}"]
    return []


def validate_documents(root: Path) -> list[str]:
    root = root.resolve()
    findings: list[str] = []
    docs = sorted({p for pattern in LOCAL_MARKDOWN for p in root.glob(pattern)})
    if not docs:
        findings.append("No public Markdown documents found")
    for doc in docs:
        fence: tuple[str, int] | None = None
        for line_no, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
            matched = FENCE.match(line)
            if fence is not None:
                if matched:
                    marker = matched.group("marker")
                    if marker[0] == fence[0] and len(marker) >= fence[1] and not matched.group("rest").strip():
                        fence = None
                continue
            if line.startswith(("    ", "\t")):
                continue
            if matched:
                marker = matched.group("marker")
                fence = (marker[0], len(marker))
                continue
            prose = INLINE_CODE.sub(lambda m: " " * len(m.group()), line)
            for match in INLINE_LINK.finditer(prose):
                findings.extend(validate_link(root, doc, line_no, match.group("url")))
    site = root / "web/index.html"
    if not site.is_file():
        findings.append("Missing public site web/index.html")
    else:
        parser = SiteLinks()
        parser.feed(site.read_text(encoding="utf-8"))
        for line_no, href in parser.links:
            findings.extend(validate_link(root, site, line_no, href))
    return findings


def validate_fixture(data: object) -> list[str]:
    if not isinstance(data, dict):
        return ["conformance fixture must be a JSON object"]
    findings: list[str] = []
    if data.get("schemaVersion") != SCHEMA_VERSION:
        findings.append(f"schemaVersion must be {SCHEMA_VERSION}")
    if not isinstance(data.get("status"), str) or "proposal" not in data["status"].lower():
        findings.append("fixture status must identify a proposal, not certification")
    events = data.get("events")
    if not isinstance(events, list) or not events or not all(isinstance(e, str) and e for e in events):
        findings.append("events must be nonempty strings")
        events = []
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        return findings + ["scenarios must be a nonempty list"]
    seen: set[str] = set()
    for index, scenario in enumerate(scenarios):
        label = f"scenarios[{index}]"
        if not isinstance(scenario, dict):
            findings.append(f"{label} must be an object")
            continue
        identifier = scenario.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            findings.append(f"{label}.id must be a nonempty string")
        elif identifier in seen:
            findings.append(f"duplicate scenario id: {identifier}")
        else:
            seen.add(identifier)
        for key in ("initialState", "expectedFinalState"):
            if not isinstance(scenario.get(key), dict):
                findings.append(f"{label}.{key} must be an object")
        for key in ("intents", "reducerContract", "effectContract"):
            if not isinstance(scenario.get(key), list) or not scenario[key]:
                findings.append(f"{label}.{key} must be a nonempty list")
        trace = scenario.get("expectedTrace")
        if not isinstance(trace, list) or not trace:
            findings.append(f"{label}.expectedTrace must be a nonempty list")
            continue
        for step, event in enumerate(trace):
            if not isinstance(event, dict) or not isinstance(event.get("event"), str) or event["event"] not in events:
                findings.append(f"{label}.expectedTrace[{step}] has unknown/missing event")
    return findings


def validate_repository(root: Path) -> list[str]:
    root = root.resolve()
    findings = validate_documents(root)
    files = sorted(root.rglob("*.json"))
    if not files:
        findings.append("No public JSON files found")
    for file in files:
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            findings.append(f"{file.relative_to(root)}: invalid JSON: {error}")
            continue
        if file.relative_to(root) == CONFORMANCE_PATH:
            findings.extend(validate_fixture(data))
    if not (root / CONFORMANCE_PATH).is_file():
        findings.append(f"Missing public conformance fixture: {CONFORMANCE_PATH}")
    return findings


if __name__ == "__main__":
    issues = validate_repository(Path(__file__).resolve().parents[1])
    if issues:
        raise SystemExit("\n".join(issues))
    print("Public Markdown, site links, and draft JSON structure: OK")
