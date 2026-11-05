# Anonymized Hoymiles HB-4020X three-signal comparison

Source: Home Assistant history export provided by the device owner for November 3, 2026 (local evening). No IP addresses, locations, account details, entity IDs, hardware IDs, or Home Assistant configuration are included.

## Data preparation
- All samples are UTC timestamps, organized in 30-second bins.
- For each signal, the median of original readings inside each bin is used.
- Only bins containing measurements from all three sources are retained (456 rows).
- Signs are normalized to positive when discharging to the AC side. The Omnibattery battery-power signal was sign-inverted; the other two signals retain their original polarity.
- AC port: direct MQTT `sys_plug_p` measurement, exported through an HA MQTT entity.
- Omnibattery battery power: HA Omnibattery entity, derived by driver from `sys_bat_p` with sign reversal.
- External AC reference: independent Zendure 3CT clamp on the relevant AC branch.
- `pv_free_discharge_candidate` is 1 when all three normalized power values exceed 100 W. **The source CSV does not contain a PV channel**; this is a discharge screening criterion, not a measured PV=0 certification. The observations were obtained during the evening.
- `steady_discharge_flag` is 1 if a sample is a discharge candidate, both adjacent 30-second bins are present, and the Omnibattery power changes by at most 10 W from the preceding bin and to the following bin. This avoids confounding from asynchronous telemetry during transients. Every aligned row is retained, including those that do not meet these criteria.

## Reproducible statistics
On the 298 `steady_discharge_flag=1` rows:
- Sum(AC port power) / Sum(Omnibattery power) = 0.9999603553 = 99.9960%.
- Sum(external 3CT power) / Sum(Omnibattery power) = 0.9964555293 = 99.6456%.
- Input Omnibattery power ranges from 103 W to 1,245 W in the stable subset.

The ratios are **ratios of summed 30-s bin median powers**, equivalent to constant-width quadrature on the sampled points, not certified metered energy totals. A live integration's filtering/timing may differ.

The data directly establishes close AC-port / `sys_bat_p` numerical agreement corroborated by an independent AC clamp. The DC-side interpretation of native `chg_e` was evaluated in a separate earlier V × I energy experiment, not in this attached file.