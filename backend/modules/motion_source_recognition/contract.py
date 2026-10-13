"""What one frame of this module's replay must contain, besides "t" (seconds on the replay timeline).

This module owns its own fields. Change them here, in the frontend meta.js `summarize`, and in the frontend index.jsx
page, all inside this module's folders. Fusion (frontend/src/features/fusion/rules.js) reads these fields, so tell its owner.
"""

FRAME_FIELDS = ['label', 'confidence', 'probs']

FIELD_NOTES = {
    "label": "Human, Pet, IRobot, Fan or unknown",
    "confidence": "probability of the chosen label, 0 to 1",
    "probs": "probability of each class"
}
