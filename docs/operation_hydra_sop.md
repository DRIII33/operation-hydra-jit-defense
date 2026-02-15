# SOP: Operation Hydra - Behavioral Enforcement
**Version:** 1.2 (Revised for Weighted Scoring)  
**Status:** PRODUCTION READY  

## 1. Goal
To provide a structured, automated response path for JIT-based compute abuse while maintaining a <0.1% False Positive Rate for Enterprise-tier customers.

## 2. Technical Enforcement Matrix
Enforcement is driven by the **RevenueProtectionEngine** risk score.

| Risk Score | Confidence | Action Path | Owner | SLA |
| :--- | :--- | :--- | :--- | :--- |
| **100 - 150+** | High (>0.9) | **Hard Block** (IAM Revoke) | Infrastructure SRE | < 1 min |
| **60 - 99** | Med (0.6-0.9) | **Dynamic Throttling** (Quota -70%) | T&S Operations | 1 hour |
| **< 60** | Low (<0.6) | **Silent Monitoring** (Log Only) | Abuse Analyst | 24 hours |

## 3. Incident Rationale Logic
Our automated notifications to users include specific behavioral markers to reduce support ticket friction:
- **SYNERGY_JIT_H:** Detection of simultaneous encrypted payload execution and JIT mutation.
- **EGRESS_C2:** Abnormal outbound pivots suggesting a Command-and-Control model.
- **EXTREME_ANOMALY:** Statistical outliers in entropy indicating advanced zero-day tools.

## 4. Human-in-the-Loop (HITL) / Appeals
1. **Automated Notification:** All blocks/throttles trigger an immediate email to the account owner.
2. **Enterprise Escalation:** Accounts with `revenue_tier == 'Enterprise'` are automatically routed to a Technical Account Manager (TAM) for manual confirmation before a Hard Block.
3. **Behavioral Allowlisting:** If an appeal is granted (e.g., legitimate HPC research), the `account_id` is added to the `hpc_behavioral_whitelist` BigQuery table to prevent future detection cycles.

## 5. Cross-Functional Stakeholders
- **TPM (Author):** Maintains detection thresholds and synergy weights.
- **Engineering:** Manages the API-based IAM revocation scripts.
- **Legal/Policy:** Reviews intent classifications for Terms of Service (ToS) compliance.
