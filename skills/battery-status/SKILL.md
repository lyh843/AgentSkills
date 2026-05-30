---
name: battery-status
description: Check the current battery and charging information on this Linux machine, especially when the user asks for charging wattage, battery percentage, charging state, voltage, estimated time to full, or a compact power-status summary. Use when the user invokes $battery-status or asks to view laptop battery or charging power from the local system.
---

# Battery Status

## Overview
Use this skill to read the local machine's battery and AC adapter status and report it in a fixed compact format.

## Workflow
1. Run [scripts/check_battery.sh](scripts/check_battery.sh).
2. If the script returns battery information, present the output directly and add at most one brief note if needed.
3. If the script reports that `upower` is missing or no battery is present, say that clearly instead of guessing.

## Output Format
Return the result as a short block with these fields when available:
- `Timestamp`
- `AC Online`
- `Battery State`
- `Battery Percentage`
- `Charging Power`
- `Voltage`
- `Energy`
- `Time To Full`
- `Time To Empty`
- `Cycle Count`

## Rules
- Prefer the script output over hand-written parsing in the reply.
- Treat `energy-rate` as the battery-side charge or discharge power, not necessarily the charger's wall power.
- If the battery is charging, label the power line as current charging power.
- If the battery is discharging, label the power line as current discharge power.
- Keep the answer concise.

## Fast Prompt Patterns
- `Use $battery-status to check my current charging power.`
- `Use $battery-status to show my battery summary.`
- `Use $battery-status to tell me whether I am charging and at what wattage.`
