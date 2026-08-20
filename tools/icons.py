"""Line icons for the practice areas.

Single-weight 24x24 strokes so the row reads as one set rather than a pile of
borrowed clipart. Keyed by the Turkish slug, which is the stable identifier in
content.json.
"""

_WRAP = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.15" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
)

_PATHS = {
    # Columned facade — the company itself.
    "ticaret-ve-sirketler-hukuku":
        '<path d="M3 20h18M4 20V9m4 11V9m4 11V9m4 11V9m4 11V9M2.5 9 12 3.5 21.5 9Z"/>',
    # Scales in balance.
    "dava-ve-tahkim":
        '<path d="M12 3v17M8 20h8M5 7h14M5 7 2.5 13h5ZM19 7l-2.5 6h5Z"/>'
        '<path d="M2.5 13a2.5 2.5 0 0 0 5 0M16.5 13a2.5 2.5 0 0 0 5 0"/>',
    # Anchor.
    "deniz-ticareti-hukuku":
        '<circle cx="12" cy="4.5" r="2"/><path d="M12 6.5V21M8 10h8"/>'
        '<path d="M4 13a8 8 0 0 0 16 0"/><path d="M4 13H2m18 0h2"/>',
    # Caduceus-free cross with a pulse.
    "saglik-hukuku":
        '<path d="M4 7h16v12H4Z"/><path d="M12 4v3"/>'
        '<path d="M7 13h2.5l1.5-3 2 6 1.5-3H17"/>',
    # Building under a crane hook.
    "gayrimenkul-ve-insaat-hukuku":
        '<path d="M3 21h18M6 21V8l7-4v17M13 21V11h5v10"/>'
        '<path d="M9 8.5v2m0 3v2M16 14.5v2"/>',
    # Bank with a coin.
    "banka-ve-finans-hukuku":
        '<path d="M3 20h18M5 20V10m4 10V10m6 10V10m4 10V10M2 10 12 4l10 6Z"/>'
        '<circle cx="12" cy="14.5" r="1.6"/>',
    # Pick over strata.
    "maden-hukuku":
        '<path d="M2 21h20"/><path d="M4 21 12 8l8 13"/>'
        '<path d="M8.5 14.5h7"/><path d="M12 8V3"/><path d="M9 4.5h6"/>',
    # Sealed document with a gavel strike.
    "icra-ve-iflas-hukuku":
        '<path d="M5 3h9l5 5v13H5Z"/><path d="M14 3v5h5"/>'
        '<path d="M8 13h8M8 17h5"/>',
    # Two figures.
    "is-hukuku":
        '<circle cx="8.5" cy="8" r="2.6"/><circle cx="16.5" cy="9.5" r="2.1"/>'
        '<path d="M3.5 19a5 5 0 0 1 10 0"/><path d="M14.5 15.2a4.4 4.4 0 0 1 6 3.8"/>',
    # Ministry facade with a receipt.
    "idare-ve-vergi-hukuku":
        '<path d="M4 21h16M6 21V10m12 11V10M3 10 12 4l9 6Z"/>'
        '<path d="M9.5 21v-5.5h5V21"/><path d="M12 13v1.5"/>',
    # Registered mark inside a lamp of ideas.
    "fikri-mulkiyet-hukuku":
        '<path d="M9 18h6M10 21h4"/>'
        '<path d="M12 3a6 6 0 0 0-3.4 10.9c.5.4.9 1.1.9 1.8V16h5v-.3c0-.7.4-1.4.9-1.8A6 6 0 0 0 12 3Z"/>',
    # Shield with a check.
    "sigorta-hukuku":
        '<path d="M12 3 4.5 6v6c0 4.3 3 8.1 7.5 9 4.5-.9 7.5-4.7 7.5-9V6Z"/>'
        '<path d="m9 12 2.2 2.2L15.5 10"/>',
}


def icon(slug):
    """Return the inline SVG for a practice-area slug, or an empty string."""
    path = _PATHS.get(slug)
    return _WRAP.format(path) if path else ""


ALL = sorted(_PATHS)
