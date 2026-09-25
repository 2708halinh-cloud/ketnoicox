# GGDV — CONNECTOR/DEVICE PROJECTS IN PROGRESS — 2026-09-25

REPO = 2708halinh-cloud/ketnoicox
BRANCH = in-progress-sync-20260925
SECRET_EXPORT = NONE

## Unfinished connector/device fronts

### Shared agent work device
- CURRENT carrier: `1rf0nffn1s7JrW4HYKvPXneqZS6idLSeYAI6iS5MKEGg`
- Structural graph is assembled.
- PC execution path: materialized; current daemon/executor receipt still required for live proof.
- Android execution path: materialized; current ADB round-trip not verified.
- Local-AI path: materialized; current process/model receipt not verified.
- FPGA path: materialized/optional; current process receipt not verified.
- Readback path: materialized.

### DV10 live-device action gate
- CURRENT: `1e5t9bZaBnsDiSVRlZbGaptJyMB_bcHyOeMcNDKeR6aA`
- Drive-side callable/Saga proof exists.
- Live-device execution is explicitly still unproven.

## Security boundary

Existing `ketnoicox` README warns that recovered bot source may contain hardcoded Telegram/Zalo credentials. This sync does not copy, echo, or duplicate any credentials. Secret rotation/remediation is a separate action and is not silently performed here.

## Branch contract

Keep unfinished connector/device work on this additive branch until a fresh runtime receipt proves the relevant path. Do not equate source presence with daemon/process liveness.
