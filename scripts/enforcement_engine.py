import pandas as pd

"""
FILE: scripts/enforcement_engine.py
PROJECT: Operation Hydra (2026)
Author: Daniel Rodriguez III
PURPOSE: Weighted Behavioral Detection & Automated Enforcement Logic
"""

from dataclasses import dataclass
from typing import Dict, List
import math

# ==========================================
# 2026 ROADMAP CONFIGURATION (Scientific Thresholds)
# ==========================================
ENTROPY_THRESHOLD = 7.2    # Shannon Entropy for Packed/Encrypted Payloads
JIT_THRESHOLD = 90         # CPU Burst Rate indicating JIT Code Mutation
PIVOT_THRESHOLD = 30       # Egress IP Tunneling count (C2 Activity)
CPU_THRESHOLD = 85         # Baseline for Heavy Compute Abuse

# TPM Risk Weighting Logic
WEIGHTS = {
    "entropy": 30,
    "jit": 30,
    "cpu": 20,
    "pivots": 20
}

SYNERGY_BONUS = 25  # Applied when High Entropy + High JIT synergy is detected
EXTREME_BONUS = 20  # Applied for extreme anomalies (H > 8.0)

@dataclass
class Telemetry:
    account_id: str
    entropy_score: float
    cpu_usage_pct: float
    jit_regen_pct: float
    network_pivots: int

# ==========================================
# DETECTION & ENFORCEMENT ENGINE
# ==========================================

class RevenueProtectionEngine:
    """
    Simulates the internal Trust & Safety automated analyst logic.
    Balances detection precision with safe revenue protection.
    """

    def __init__(self):
        self.audit_log = []

    def evaluate(self, telemetry: Telemetry) -> Dict:
        risk_score = 0
        rationale = []

        # 1. Individual Signal Analysis
        if telemetry.entropy_score > ENTROPY_THRESHOLD:
            risk_score += WEIGHTS["entropy"]
            rationale.append(f"High Entropy ({telemetry.entropy_score})")

        if telemetry.jit_regen_pct > JIT_THRESHOLD:
            risk_score += WEIGHTS["jit"]
            rationale.append(f"High JIT Regeneration ({telemetry.jit_regen_pct}%)")

        if telemetry.cpu_usage_pct > CPU_THRESHOLD:
            risk_score += WEIGHTS["cpu"]
            rationale.append("Sustained High CPU Usage")

        if telemetry.network_pivots > PIVOT_THRESHOLD:
            risk_score += WEIGHTS["pivots"]
            rationale.append(f"Aggressive Egress Pivots ({telemetry.network_pivots})")

        # 2. Synergy Detection (The 'Operation Hydra' Signature)
        if (telemetry.entropy_score > ENTROPY_THRESHOLD and
            telemetry.jit_regen_pct > JIT_THRESHOLD):
            risk_score += SYNERGY_BONUS
            rationale.append("SYNERGY: Entropy + JIT (Probable Model Extraction)")

        # 3. Extreme Anomaly Handling
        if (telemetry.entropy_score > 8.0 and telemetry.jit_regen_pct > 95):
            risk_score += EXTREME_BONUS
            rationale.append("EXTREME: Zero-Day Polymorphism Detected")

        # 4. Normalization and Decisioning
        # Confidence is capped at 1.0 (100%)
        confidence = min(risk_score / 150, 1.0)

        intent = self.classify_intent(telemetry)
        enforcement = self.determine_enforcement(risk_score)

        result = {
            "account_id": telemetry.account_id,
            "intent_classification": intent,
            "risk_score": risk_score,
            "confidence_score": round(confidence, 2),
            "rationale": " | ".join(rationale),
            "enforcement_action": enforcement
        }

        self.audit_log.append(result)
        return result

    def classify_intent(self, telemetry: Telemetry) -> str:
        """Determines the motive behind the technical signals."""
        if telemetry.entropy_score > ENTROPY_THRESHOLD and telemetry.jit_regen_pct > JIT_THRESHOLD:
            return "MODEL_EXTRACTION"
        if telemetry.cpu_usage_pct > CPU_THRESHOLD and telemetry.network_pivots <= PIVOT_THRESHOLD:
            return "RESOURCE_HIJACKING"
        if telemetry.network_pivots > PIVOT_THRESHOLD:
            return "LATERAL_PROPAGATION"
        return "UNKNOWN_ABUSE"

    def determine_enforcement(self, risk_score: int) -> str:
        """Maps risk score to the SOP Enforcement Matrix."""
        if risk_score >= 100:
            return "BLOCK"
        if risk_score >= 60:
            return "THROTTLE"
        return "MONITOR"

# ==========================================
# VALIDATION MODULE (Logic Test)
# ==========================================

if __name__ == "__main__":
    engine = RevenueProtectionEngine()
    all_test_results = []

    # Test Case: Known Critical Threat (acct_bfdc9309)
    # Expected: High Score, Synergy Bonus, Extreme Bonus, Action: BLOCK
    critical_threat = Telemetry("acct_bfdc9309", 8.2, 95, 97, 50)
    critical_result = engine.evaluate(critical_threat)
    print("--- HYDRA ENFORCEMENT ENGINE TEST RUN ---")
    print(f"CRITICAL TEST: {critical_result}")
    all_test_results.append(critical_result)

    # Test Case: Suspicious but potentially safe (acct_77a3d049)
    # Expected: Moderate Score, Action: THROTTLE
    suspicious_case = Telemetry("acct_77a3d049", 7.3, 87, 45, 20)
    suspicious_result = engine.evaluate(suspicious_case)
    print("-" * 30)
    print(f"SUSPICIOUS TEST: {suspicious_result}")
    all_test_results.append(suspicious_result)

    # Save all test results to a CSV
    df_test_results = pd.DataFrame(all_test_results)
    df_test_results.to_csv("hydra_test_results.csv", index=False)
    print("\nTest results saved to hydra_test_results.csv")
