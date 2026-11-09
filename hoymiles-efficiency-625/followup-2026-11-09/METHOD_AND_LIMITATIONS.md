# Evidence for Omnibattery issue #625: previously collected Hoymiles measurements

## Provenance and privacy
- Original data supplied by the device owner and aligned during an earlier Home Assistant investigation. No IPs, MACs, MQTT topic identifiers, HA entity identifiers, account information or local geographic information are included in these public extracts.
- All timestamps are in UTC. The October multi-day dataset derives from an earlier event-aligned/processed file with observations spaced roughly five minutes apart, **not synchronized original MQTT packets**. There are missing values and possible reporting/staleness offsets. Values were not filled in or interpolated again for this export.
- The November 3 CSV comes from an earlier 30-second median alignment of three separate sensors. Its `pv_free_discharge_candidate` flag is NOT proof of PV=0: PV telemetry is absent from that source.
- Sign convention for October file: positive battery, AC port, and 3CT values indicate power flowing **into** the storage unit (charging); negative indicates discharge / export. Reported PV is positive incoming generation. `battery_dc_vi_charge_positive_w = battery_current_a × battery_voltage_v`.
- `reported_battery_power_w` is the Omnibattery `battery_power` signal, mapped from `sys_bat_p` with sign inversion. `ac_port_charge_positive_w` comes from MQTT socket/plug power. `external_ac_3ct_charge_positive_w` comes from an independent AC current clamp. The raw `pv_p` provenance and whether the historical PV value is aggregation must be verified against original entity mapping before treating the field as a native physical port power.
- `power_balance_residual_w = reported_battery_power_w − reported_pv_power_w − ac_port_charge_positive_w` when all inputs are present.

## October 15–22 analysis / screening
Rows in `oct15_22_aligned_power_flows.csv`: 1103.
- `solar_charge_low_ac`: 41 rows; reported PV >100 W, battery charge >100 W, |AC port| ≤30 W, |3CT| ≤35 W, measured V×I >30 W. These are low-AC windows, not mathematically exact zero-AC or necessarily single-path energy flow.
- `mixed_pv_ac_charge`: 193 rows; reported PV >100 W, battery charge >200 W, AC input >100 W, V×I >30 W. Median power-balance residual = -0.4 W. Some transients are poorly aligned and differ greatly; report median rather than pretending all snapshots satisfy a power balance.
- `low_pv_discharge`: 6 rows; reported PV ≤10 W, discharging battery/AC with V×I negative. Small and sparse subset, insufficient for a definitive discharge efficiency estimate on its own.
- No clearly verified **AC-only charging (PV=0) with all signals** was found in this October event-aligned file. This remains a genuine gap.

## November 3 three-way AC validation
The other file preserves all 456 30-second aligned bins and its existing steady-state flags. On the 298 steady-discharge flagged bins, Σ AC port / Σ Omnibattery discharge = 99.996%, and Σ external AC 3CT / Σ Omnibattery discharge = 99.646%. It lacks V×I and PV fields. Do not infer DC conversion efficiency from these three AC-equivalent signals.

## October 9 V×I cross-check
The interval-estimates and counter files preserve the earlier battery V×I integration analysis and native daily charge counter history. The prior engineering comparison yielded 564.00 Wh native chg_e versus 565.07 Wh integrated V×I (0.19%). This is a separately analyzed interval, not a contemporaneous sample with the October 15–22 or November 3 datasets. The interval-estimates CSV is a calculated artifact; do not present it as original MQTT telemetry.

## Outstanding requested information
1. No clean, **proven PV=0 AC-only charge** interval with all of V×I, AC power and battery reported power was identified in these already-aligned sources.
2. No raw device/state and system/state MQTT *receipt timestamps* are in these files; the observed snapshot cadence is not enough to measure arrival skew.
3. Exact raw physical definition of `pv_p` is not established by these files alone. The owner's PV is AC-coupled and the observed input balance is consistent with an AC-equivalent PV contribution. This must not be casually equated to a DC panel-side MPPT reading.
4. Discharge V×I data exists in the October multi-day file, but asynchronous snapshots and sparse low-PV subset limit quantitative conversion-loss claims.