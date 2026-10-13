"""What one frame of this module's replay must contain, besides "t" (seconds on the replay timeline).

This module owns its own fields. Change them here, in the frontend meta.js `summarize`, and in the frontend index.jsx
page, all inside this module's folders. Fusion (frontend/src/features/fusion/rules.js) reads these fields, so tell its owner.
"""

FRAME_FIELDS = ['status', 'confidence']

FIELD_NOTES = {
    "status": "breathing, none or not_assessable",
    "confidence": "0 to 1"
}
