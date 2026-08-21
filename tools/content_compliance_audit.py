#!/usr/bin/env python3
"""Lightweight wording guard for a Turkish law-firm website.

This is not a legal-compliance opinion. It only prevents a short list of
comparative, guaranteed-result and superiority-style marketing phrases from
quietly reappearing in public HTML. Final content remains subject to lawyer
review and applicable TBB rules.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("başarı oranı", re.compile(r"başarı\s+oran", re.I)),
    ("garanti/garantili sonuç", re.compile(r"\bgaranti(?:li|si|lenmiş)?\b", re.I)),
    ("en iyi", re.compile(r"\ben\s+iyi\b", re.I)),
    ("lider konum", re.compile(r"\blider\s+konum", re.I)),
    ("rakiplerden üstün", re.compile(r"\brakip\w*\s+(?:üstün|daha\s+iyi)", re.I)),
    ("well-regarded", re.compile(r"\bwell[- ]regarded\b", re.I)),
    ("leading companies", re.compile(r"\bleading\s+compan(?:y|ies)\b", re.I)),
    ("best law firm", re.compile(r"\bbest\s+law\s+firm\b", re.I)),
    ("success rate", re.compile(r"\bsuccess\s+rate\b", re.I)),
    ("guaranteed result", re.compile(r"\bguarantee(?:d)?\s+(?:result|outcome)\b", re.I)),
]

for path in sorted(ROOT.rglob("*.html")):
    rel = path.relative_to(ROOT)
    if ".git" in rel.parts or "tools" in rel.parts:
        continue
    text = path.read_text(encoding="utf-8")
    for label, pattern in PATTERNS:
        match = pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            ERRORS.append(f"{rel.as_posix()}:{line} -> riskli ifade: {label}")

if ERRORS:
    print(f"CONTENT COMPLIANCE AUDIT FAILED — {len(ERRORS)} sorun")
    for problem in ERRORS:
        print("  -", problem)
    sys.exit(1)

print("CONTENT COMPLIANCE AUDIT OK — karşılaştırmalı/garantili pazarlama dili bulunmadı")
