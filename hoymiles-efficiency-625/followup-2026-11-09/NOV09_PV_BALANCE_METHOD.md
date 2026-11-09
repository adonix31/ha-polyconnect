# Additional November 9 PV-input / AC-port / battery-power capture — methodology

## Provenance and privacy
Source: user-supplied Home Assistant history export covering approximately 2026-11-09 13:41–13:45 UTC. Three entity identifiers have been mapped to neutral signal names; no original Home Assistant entity IDs, account details, IP addresses, or device identifiers are included in the cleaned files. Dates/times are retained for synchronization; if publication requires hiding observation dates, use relative elapsed seconds instead.

## Measurements
- `battery_reported_w`: Omnibattery sensor derived from MQTT `sys_bat_p` (positive charge in this example).
- `pv_reported_w`: Omnibattery solar-power sensor; driver uses `sys_pv_p`/`pv_p`, **and can combine an off-grid input**. Thus it is a reported solar quantity, not a independently verified raw `pv_p` field or DC-MPPT terminal meter.
- `ac_port_raw_w`: Hoymiles AC socket measurement as exported, negative for AC draw in this example; `ac_input_w = -ac_port_raw_w`.

## Alignment
The original export includes 297 history rows: 68 battery, 15 PV and 214 AC-port updates. Keep all original value changes in `nov09_pv_power_raw_clean.csv` (neutral labels). For `nov09_pv_power_pv_anchored_aligned.csv`, anchor each of the 15 PV update timestamps and use the closest independent battery and AC-port sample within ±1 s. Rows with missing matches remain missing; neither signals nor timestamps are filled or interpolated. The exact offsets and selection flags are included. This method is intentionally strict and illustrates sample-level limitations.

## Results
- PV-anchored instants: 15.
- Fully matched within ±1 s: 10.
- |residual| ≤ 1 W: 6 of the fully matched instants.
- Residual definition: `battery_reported_w - (pv_reported_w + ac_input_w)`; median signed residual 0.50 W, median absolute residual 0.70 W.
- Most straightforward first point: 125 W PV + 25 W AC input = 150 W reported battery power.
- Other matched residuals are not suppressed. Intermittent AC readings near 0 and −17 W, compared with the usual approximately −25 W, and different per-sensor update rates create occasional residuals up to ±9 W; these should not be reinterpreted as measured conversion losses.

## Engineering interpretation / limits
This strongly supports **a shared upstream or AC-equivalent accounting convention** for reported battery power and the measured PV and AC-port contributions. It **does not establish that the physically DC-connected photovoltaic modules are AC-connected**, nor independently prove where internal firmware samples or derives `pv_p`. It does not by itself establish the efficiency of the MPPT or the DC battery charge path. The experiment conditions stated by the owner are that commanded AC charging was disabled, while an approximately 25 W AC-port draw was present. The CSV does not itself encode charger command state or independent MPPT-terminal power.

The richer October power-flow file in the package provides longer-duration mixed-mode evidence; the independently validated battery V×I and native counter measurements establish DC-battery-side energy, rather than this four-minute trace alone.