#INSTALL PACKAGES
!pip install pandas numpy uuid


import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import uuid

# --- CONFIGURATION ---
NUM_RECORDS = 5000
MALWARE_RATIO = 0.08  # 8% of traffic is malicious (HONESTCUE infections)

# --- 2026 BEHAVIORAL PROFILES ---

def generate_safe_traffic():
    """Simulates standard web server or database compute patterns."""
    return {
        "entropy_score": np.random.uniform(3.5, 6.0),     # Normal code/text variance
        "cpu_burst_rate": np.random.uniform(10.0, 45.0),  # Steady utilization
        "egress_pivots": np.random.randint(1, 5),         # Standard API calls
        "revenue_tier": np.random.choice(["Free", "SMB", "Enterprise"], p=[0.5, 0.3, 0.2]),
        "is_malicious": False
    }

def generate_honestcue_traffic():
    """
    Simulates JIT-Malware (HONESTCUE) behavior:
    1. High Entropy (>7.2) due to in-memory packing/encryption.
    2. High CPU Burst (>85%) during LLM inference/code generation.
    3. High Egress Pivots due to command-and-control (C2) fetching.
    """
    return {
        "entropy_score": np.random.uniform(7.2, 8.0),      # THE RED FLAG
        "cpu_burst_rate": np.random.uniform(85.0, 99.9),   # The "Regeneration Event"
        "egress_pivots": np.random.randint(15, 50),        # Aggressive fetching
        "revenue_tier": np.random.choice(["Free", "SMB", "Enterprise"], p=[0.7, 0.2, 0.1]), # Mal actors prefer Free tier
        "is_malicious": True
    }

# --- DATA GENERATION LOOP ---

data = []
current_time = datetime.now()

for _ in range(NUM_RECORDS):
    # Randomly decide if this event is Malicious or Safe
    if random.random() < MALWARE_RATIO:
        profile = generate_honestcue_traffic()
    else:
        profile = generate_safe_traffic()

    row = {
        "timestamp": current_time - timedelta(seconds=random.randint(0, 86400)), # Past 24 hours
        "account_id": f"acct_{uuid.uuid4().hex[:8]}",
        "entropy_score": round(profile["entropy_score"], 4),
        "cpu_burst_rate": round(profile["cpu_burst_rate"], 2),
        "egress_pivots": profile["egress_pivots"],
        "revenue_tier": profile["revenue_tier"],
        # We include a 'label' for verification, but in production, we wouldn't know this!
        "label_ground_truth": "MALWARE_HONESTCUE" if profile["is_malicious"] else "SAFE_COMPUTE"
    }
    data.append(row)

# --- DATAFRAME CREATION ---
df = pd.read_json(pd.Series(data).to_json(orient='records')) # Cleanest way to load mixed types

# Sort by time
df = df.sort_values(by="timestamp")

# Preview the "Threats"
print("--- DETECTED THREAT PREVIEW (HONESTCUE SIGNATURES) ---")
print(df[df['label_ground_truth'] == "MALWARE_HONESTCUE"].head(5))

# --- EXPORT ---
df.to_csv("jit_telemetry_2026.csv", index=False)
print("\nSUCCESS: 'jit_telemetry_2026.csv' generated with scientific behavioral markers.")
