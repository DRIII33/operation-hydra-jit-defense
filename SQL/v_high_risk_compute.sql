-- Path: sql/v_high_risk_compute.sql
CREATE OR REPLACE VIEW `driiiportfolio.compute_abuse_logs.v_high_risk_compute` AS
SELECT
    account_id,
    revenue_tier,
    -- Time-series context for SLA tracking
    MAX(timestamp) AS last_detected_at,
    
    -- Detection Metrics (HONESTCUE Signature)
    COUNT(*) AS total_transactions,
    COUNTIF(entropy_score > 7.2 AND cpu_burst_rate > 85.0 AND egress_pivots > 20) AS malicious_event_count,
    
    -- Behavioral Severity Profile
    ROUND(AVG(entropy_score), 3) AS avg_entropy,
    MAX(cpu_burst_rate) AS max_cpu_spike,
    MAX(egress_pivots) AS max_network_pivots,
    
    -- Financial Impact: Estimating $50 cost per malicious compute burst
    ROUND(COUNTIF(entropy_score > 7.2 AND cpu_burst_rate > 85.0 AND egress_pivots > 20) * 50.0, 2) AS estimated_revenue_at_risk,

    -- 2026 Zero-Tolerance Risk Classification
    CASE
        WHEN COUNTIF(entropy_score > 7.2 AND cpu_burst_rate > 85.0 AND egress_pivots > 20) >= 1 THEN 'CRITICAL_RISK'
        WHEN MAX(entropy_score) > 6.5 THEN 'SUSPICIOUS'
        ELSE 'SAFE'
    END AS risk_level
FROM `driiiportfolio.compute_abuse_logs.jit_raw_telemetry`
GROUP BY 1, 2;
