# SOP: Operation Hydra - Behavioral Enforcement
**Version:** 2.0 (Revised for Enforcement vs. Detection Parity)  
**Status:** PRODUCTION READY  

## 1. Goal
Maintain a <0.1% False Positive Rate for Enterprise customers while ensuring 100% containment of Model Extraction attempts.

## 2. Technical Enforcement Matrix
The engine distinguishes between **Detection** (identifying intent) and **Enforcement** (taking action). 

| Risk Score | Peak Confidence | Enforcement Action | Policy Basis |
| :--- | :--- | :--- | :--- |
| **110+** | **> 0.95** | **Hard Block** | Zero-tolerance for Model Extraction. |
| **60 - 109**| **0.60 - 0.94**| **Dynamic Throttle**| Mitigates Lateral Propagation & Abuse. |
| **< 60** | **< 0.60** | **Silent Monitor** | Used for heuristic baseline & safe noise. |

## 3. The 340/402 Discrepancy (Operational Policy)
Operation Hydra detected 402 malicious events. However, only **340** were subjected to "Hard Mitigation" (Block/Throttle). The remaining 62 events (primarily Resource Hijacking in Free Tiers) were diverted to **Silent Monitoring** to:
1. Gather intelligence on new JIT-mutation patterns.
2. Avoid over-enforcement in non-revenue generating tiers.

## 4. Human-in-the-Loop (HITL) / Appeals
- **Enterprise Safeguard:** All accounts flagged in the Enterprise tier trigger an automated TAM (Technical Account Manager) notification.
- **Behavioral Allowlisting:** Legitimate HPC research that mimics JIT behavior can be allowlisted via the `hpc_behavioral_whitelist` table.
