"""Audit this package's references, rule IDs and restricted metadata format.

Python 3 standard library only. This is not a general YAML parser, the bundled
skill-creator validator, a skill-routing evaluation or an application behaviour test.
"""

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


LIBRARIES = {
    "ux": ("ui", "UI_UX_DOCS_ROOT", r"(?:GOV|UX|VIS|STATE|VAL|FLOW|CONTENT|A11Y|PERF|CAP|VERIFY|AI)-\d{2}", "D"),
    "backend": ("backend", "BACKEND_DOCS_ROOT", r"(?:BGV|API|DOM|MID|SEC|DB|TX|MIG|JOB|INT|CACHE|OPS|BV)-\d{2}", "BD"),
}
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")


def audit(root, library="ux"):
    prefix, environment, rule_id, decision_prefix = LIBRARIES[library]
    skills = tuple(prefix + "-" + action for action in ("spec", "build", "verify"))
    rule_row = re.compile(r"^\| (" + rule_id + r") \|", re.MULTILINE)
    docs_relative = "docs/" + library
    root = root.resolve()
    errors = []
    documents = sorted((root / docs_relative).rglob("*.md"))
    documents.extend(root / "skills" / name / "SKILL.md" for name in skills if (root / "skills" / name / "SKILL.md").is_file())
    if not documents:
        errors.append("No Markdown documents found")
    contents = {path: path.read_text(encoding="utf-8") for path in documents}
    local_links = 0
    for path, content in contents.items():
        for match in LINK.finditer(content):
            target = match.group(1)
            if urlsplit(target).scheme or target.startswith("#"):
                continue
            local_links += 1
            target_path = unquote(target.split("#", 1)[0])
            resolved = (path.parent / target_path).resolve()
            if not resolved.is_relative_to(root):
                errors.append(f"{path.relative_to(root)}: link escapes package: {target}")
            elif not resolved.is_file():
                errors.append(f"{path.relative_to(root)}: missing linked file: {target}")

    entry_names = []
    for name in skills:
        path = root / "skills" / name / "SKILL.md"
        content = contents.get(path)
        if content is None:
            errors.append(f"Missing entry skill: {name}")
            continue
        # Installed entries use library-root-relative paths, not broken package links.
        references = re.findall(r"`((?:(?:modules|templates)/)?[a-z][a-z0-9-]*\.md)`", content)
        for reference in references:
            if not (root / docs_relative / reference).is_file():
                errors.append(f"{name}: missing shared-library reference: {reference}")
        if not references or environment not in content or "library-root.txt" not in content:
            errors.append(f"{name}: missing shared-library resolution contract")
        match = re.match(r"\A---\n(.*?)\n---\n", content, re.DOTALL)
        if not match:
            errors.append(f"{name}: missing frontmatter delimiters")
            continue
        fields = {}
        for line in match.group(1).splitlines():
            field = re.fullmatch(r"(name|description): ([^\n]+)", line)
            if not field:
                errors.append(f"{name}: outside audited flat metadata subset: {line}")
                continue
            key, value = field.groups()
            if key in fields:
                errors.append(f"{name}: duplicate metadata field {key}")
            if ": " in value or " #" in value or value[0] in "[]{}&*!|>'\"%@`":
                errors.append(f"{name}: metadata requires a full YAML parser: {key}")
            fields[key] = value
        if set(fields) != {"name", "description"}:
            errors.append(f"{name}: expected exactly name and description")
        if fields.get("name") != name or len(name) >= 64:
            errors.append(f"{name}: invalid or mismatched name")
        description = fields.get("description", "")
        if not description.strip() or len(description) > 1024 or any(c in description for c in "<>"):
            errors.append(f"{name}: invalid description")
        if "[TODO:" in content:
            errors.append(f"{name}: unfinished scaffold marker")
        entry_names.append(name)

    definitions = []
    strengths = ("MUST", "DEFAULT WITH OVERRIDE", "CONDITIONAL", "PRODUCT DECISION REQUIRED")
    canonical = [root / (docs_relative + "/governance.md")]
    canonical.extend(sorted((root / (docs_relative + "/modules")).glob("*.md")))
    for path in canonical:
        content = contents.get(path, "")
        for line in content.splitlines():
            match = rule_row.match(line)
            if not match:
                continue
            definitions.append(match.group(1))
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) != 6 or not all(cells):
                errors.append(f"{match.group(1)}: expected six nonempty rule-envelope columns")
            elif not any(strength in cells[1] for strength in strengths):
                errors.append(f"{match.group(1)}: missing recognised requirement strength")
    if not definitions:
        errors.append("No canonical rule definitions found")
    for definition_id, count in Counter(definitions).items():
        if count != 1:
            errors.append(f"Duplicate rule owner: {definition_id}")
    referenced = set()
    for content in contents.values():
        referenced.update(re.findall(r"\b" + rule_id + r"\b", content))
    for missing in sorted(referenced - set(definitions)):
        errors.append(f"Referenced rule has no canonical definition: {missing}")
    decision_path = root / (docs_relative + "/decisions.md")
    decisions = re.findall(r"^\| (" + decision_prefix + r"\d{2}) \|", contents.get(decision_path, ""), re.MULTILINE)
    for decision, count in Counter(decisions).items():
        if count != 1:
            errors.append(f"Duplicate decision: {decision}")
    referenced_decisions = set()
    for content in contents.values():
        referenced_decisions.update(re.findall(r"\b" + decision_prefix + r"\d{2}\b", content))
    for missing in sorted(referenced_decisions - set(decisions)):
        errors.append(f"Referenced decision has no register entry: {missing}")
    return {
        "status": "FAILED" if errors else "VERIFIED",
        "scope": "Static package integrity only; restricted metadata, not general YAML",
        "markdown_files": len(documents),
        "entry_skills": entry_names,
        "local_file_links": local_links,
        "canonical_rules": len(definitions),
        "decisions": len(decisions),
        "errors": errors,
    }


def main(default_library="ux"):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--library", choices=LIBRARIES, default=default_library)
    args = parser.parse_args()
    result = audit(args.root, args.library)
    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
