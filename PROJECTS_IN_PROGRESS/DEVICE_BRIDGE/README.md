# DEVICE BRIDGE — PC / ANDROID / LOCAL AI

STATUS = STRUCTURALLY_MATERIALIZED / LIVE_RECEIPTS_PENDING
CURRENT = `1rf0nffn1s7JrW4HYKvPXneqZS6idLSeYAI6iS5MKEGg`

## PC route
`AGENT TASK → INBOX_TO_PC → WINDOWS LOCAL EXECUTOR/MONITOR → OUTBOX_FROM_PC + RECEIPTS → READBACK`

Current source says executor/monitor code exists, but source presence does not prove the daemon is running now.

## Android route
`AGENT COMMAND → command.json → rclone → PHONE AGENT → ADB → PHONE → result.json / screenshot → READBACK`

Current source says the route is materialized; fresh ADB device presence + command/result round trip is still required for live proof.

## Local compute
AI_LOCAL_NEURON/Ollama path is materialized but requires a fresh process/model receipt when used. FPGA is optional and likewise receipt-bound.

## NEXT live gate
1. Fresh PC executor/daemon receipt.
2. If phone is required: ADB online + round-trip receipt.
3. If local AI is required: model/process receipt.
4. Optional FPGA receipt only when the task uses it.
5. Output + receipt must return to the correct carrier and be read back.

## Security note
The existing recovered bot README warns of hardcoded Telegram/Zalo credentials in source. This sync copies no credentials and does not duplicate those values.
