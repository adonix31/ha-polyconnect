# Hoymiles HB-4020X | Issue #625 follow-up measurement evidence
These cleaned, anonymized measurements accompany the technical response to [Omnibattery issue #625](https://github.com/ffunes/Omnibattery/issues/625).

## Contents
- **October 9:** measured battery V×I interval estimates and native charging-counter comparison. These are two different forms of evidence: V×I versus native `chg_e` is a DC-side cross-check.
- **October 15–22:** historic aligned power-flow observations, split across `oct15_22_aligned_power_flows_part1_1000rows.csv` (first **1,000 observations**) and `oct15_22_aligned_power_flows_part2_103rows.csv` (remaining **103 observations**), in chronological order. Both contain compatible columns; for combined analysis concatenate them, keeping one CSV header and **dropping the leading `index` field from the part-1 export**. The first file has index 0..999 and the second begins at 2026-10-21T16:50:02Z.
- **November 3:** independent three-signal AC corroboration; methodology and visualization were previously published [here](../).
- **November 9:** 297 cleaned raw source observations and 15 PV-anchored time-aligned rows (10 complete three-signal matches at ±1 s). Raw timestamps are preserved; gaps are not filled.

## Key measured relationships
1. No-PV discharge: `sys_bat_p`-derived battery power closely follows raw MQTT AC socket `sys_plug_p` and independent AC clamp.
2. Native `chg_e` energy increment agreed with integrated battery V×I within 0.19% in the October 9 experiment.
3. Mixed-input October capture, 193 screened records: median `battery_reported − (PV_reported + AC_input)` = **−0.4 W**. Some large transient differences remain.
4. November 9, *commanded grid AC charging disabled*: e.g., PV 125 W + residual grid-port input 25 W = reported battery power 150 W. Median absolute residual across 10 tightly aligned complete rows = **0.7 W**.
5. October historical data contain **41** screened PV-charge / low-AC-port observations.
 
## Limitations
- The solar field is *Omnibattery's reported solar-power value*, potentially aggregating input sources; this dataset alone cannot establish that raw `pv_p` is measured at a specific physical point or is exactly an AC or DC signal.
- October aligned data reflect asynchronous historical Home Assistant readings, not raw MQTT device/system message reception timestamps.
- The November 9 capture has only four minutes of data, and its residual AC socket input persisted despite commanded AC charging being disabled.
- As in the accompanying technical reply, `sys_bat_p`-derived charging energy should be called **upstream / AC-equivalent reported energy**, not a proven pure grid AC energy measurement when PV contributes.
- Time stamps are UTC. Original identifiers, MQTT topics, account information and IPs have been removed. Note that timestamps are preserved.

For detailed filters, thresholds, and field definitions consult [METHOD_AND_LIMITATIONS.md](https://github.com/adonix31/ha-polyconnect/blob/evidence/hoymiles-efficiency-625/hoymiles-efficiency-625/followup-2026-11-09/METHOD_AND_LIMITATIONS.md) and [NOV09_PV_BALANCE_METHOD.md](https://github.com/adonix31/ha-polyconnect/blob/evidence/hoymiles-efficiency-625/hoymiles-efficiency-625/followup-2026-11-09/NOV09_PV_BALANCE_METHOD.md).
