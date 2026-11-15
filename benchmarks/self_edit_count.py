"""Count mechanical error markers in the 0.16.2 self-edit scope, per git ref.

Usage (from the repository root):
    python3 benchmarks/self_edit_count.py Gốc=823ce7a Sonnet=edit/0162-sonnet Opus=edit/0162-opus HEAD

Each argument is a ref or NAME=REF. The first ref is the baseline that
"files changed" is measured against. Scope is the 42 shipped Markdown files;
in docs/changelog.md only the 0.16.2 entry is counted. Code spans, fenced code,
tables, headings, HTML, lines with URLs and bold labels are skipped.
"""
import json
import re
import subprocess
import sys

PAT = re.compile(
    r"^(SKILL\.md|references/[^/]+\.md|profiles/[^/]+/[^/]+\.md|profiles/[^/]+/styles/[^/]+\.md"
    r"|\.plugin-skills/[^/]+/SKILL\.md|README\.md|PRIVACY\.md|TERMS\.md|SECURITY\.md|CONTRIBUTING\.md"
    r"|docs/[^/]+\.md)$"
)
LOWER = "a-zàáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ"
RA_SOAT = re.compile(r"(?<![\w])(rà(?! soát| lại)|(?<!rà )soát)(?![\w])", re.I)
COLON = re.compile(rf":\s+(?=[{LOWER}])")
LABEL = re.compile(r"^\s*(?:[-*]|\d+\.)?\s*\*\*[^*]+:\*\*")
KEYS = ("dấu hai chấm giữa câu", "rà/soát đứng một mình")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def count(text):
    c = dict.fromkeys(KEYS, 0)
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence or line.lstrip().startswith(("|", "#", "<", "!")) or "http" in line:
            continue
        s = re.sub(r"`[^`]*`", "``", line)
        c["rà/soát đứng một mình"] += len(RA_SOAT.findall(s))
        if re.match(r"^(name|description|version):", s):
            continue
        body = LABEL.sub("", s)
        for m in COLON.finditer(body):
            head = re.split(r"[.;!?]\s|^\s*(?:[-*]|\d+\.)\s", body[: m.start()])[-1].strip()
            if len(head.split()) > 3:
                c["dấu hai chấm giữa câu"] += 1
    return c


def files_at(ref):
    return [f for f in git("ls-tree", "-r", "--name-only", ref).splitlines() if PAT.match(f)]


def text_at(ref, path):
    txt = git("show", f"{ref}:{path}")
    if path == "docs/changelog.md":
        m = re.search(r"### 0\.16\.2.*?(?=\n### )", txt, re.S)
        txt = m.group(0) if m else ""
    return txt


def main(argv):
    if not argv:
        sys.exit(__doc__)
    refs = [a.split("=", 1) if "=" in a else [a, a] for a in argv]
    base = refs[0][1]
    out = {}
    for name, ref in refs:
        files = files_at(ref)
        tot = dict.fromkeys(KEYS, 0)
        for f in files:
            for k, v in count(text_at(ref, f)).items():
                tot[k] += v
        changed = [f for f in files if f in files_at(base) and text_at(base, f) != text_at(ref, f)]
        out[name] = {"files": len(files), "files changed": len(changed), **tot}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:])
