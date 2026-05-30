#!/usr/bin/env bash
set -euo pipefail

if ! command -v upower >/dev/null 2>&1; then
  echo "Battery Status"
  echo "Error: upower is not installed"
  exit 1
fi

battery_path="$(upower -e | awk '/battery_/ { print; exit }')"
ac_path="$(upower -e | awk '/line_power_|AC/ { print; exit }')"

if [[ -z "${battery_path}" ]]; then
  echo "Battery Status"
  echo "Error: no battery device reported by upower"
  exit 1
fi

battery_info="$(upower -i "$battery_path")"
ac_info=""
if [[ -n "${ac_path}" ]]; then
  ac_info="$(upower -i "$ac_path")"
fi

get_value() {
  local key="$1"
  awk -F': *' -v key="$key" '$1 ~ key { print $2; exit }' <<<"$battery_info"
}

get_ac_value() {
  local key="$1"
  awk -F': *' -v key="$key" '$1 ~ key { print $2; exit }' <<<"$ac_info"
}

timestamp="$(date '+%F %T %Z')"
ac_online="$(get_ac_value '^[[:space:]]*online$')"
state="$(get_value '^[[:space:]]*state$')"
percentage="$(get_value '^[[:space:]]*percentage$')"
energy_rate="$(get_value '^[[:space:]]*energy-rate$')"
voltage="$(get_value '^[[:space:]]*voltage$')"
energy="$(get_value '^[[:space:]]*energy$')"
energy_full="$(get_value '^[[:space:]]*energy-full$')"
time_to_full="$(get_value '^[[:space:]]*time to full$')"
time_to_empty="$(get_value '^[[:space:]]*time to empty$')"
cycles="$(get_value '^[[:space:]]*charge-cycles$')"

if [[ -z "${ac_online}" ]]; then
  ac_online="unknown"
fi

power_label="Power"
if [[ "${state}" == "charging" ]]; then
  power_label="Charging Power"
elif [[ "${state}" == "discharging" ]]; then
  power_label="Discharge Power"
fi

echo "Battery Status"
echo "Timestamp: ${timestamp}"
echo "AC Online: ${ac_online}"
echo "Battery State: ${state:-unknown}"
echo "Battery Percentage: ${percentage:-unknown}"
echo "${power_label}: ${energy_rate:-unknown}"
echo "Voltage: ${voltage:-unknown}"
if [[ -n "${energy}" || -n "${energy_full}" ]]; then
  echo "Energy: ${energy:-unknown} / ${energy_full:-unknown}"
fi
if [[ -n "${time_to_full}" ]]; then
  echo "Time To Full: ${time_to_full}"
fi
if [[ -n "${time_to_empty}" ]]; then
  echo "Time To Empty: ${time_to_empty}"
fi
if [[ -n "${cycles}" ]]; then
  echo "Cycle Count: ${cycles}"
fi
