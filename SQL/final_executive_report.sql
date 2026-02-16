-- Path: sql/final_executive_report_v2.sql
CREATE OR REPLACE TABLE `driiiportfolio.compute_abuse_logs.final_executive_report` AS

WITH weighted_scoring AS (
  SELECT 
    account_id,
    revenue_tier,
    last_detected_at,
    total_transactions,
    malicious_event_count,
    avg_entropy,
    max_cpu_spike,
    max_network_pivots,
    risk_level,
    estimated_revenue_at_risk,

    -- Precise Weighted Logic (2026 Heuristics)
    (
      (CASE WHEN avg_entropy > 7.2 THEN 30 ELSE 0 END) +
      (CASE 
          WHEN max_cpu_spike > 90 THEN 30
          WHEN max_cpu_spike > 85 THEN 20
          ELSE 0
       END) +
      (CASE WHEN max_network_pivots > 30 THEN 20 ELSE 0 END) +
      -- Synergy Bonus: The signature of Agentic Malware (HONESTCUE)
      (CASE WHEN avg_entropy > 7.2 AND max_cpu_spike > 90 THEN 25 ELSE 0 END) +
      -- Extreme Anomaly: High entropy polymorphic payloads
      (CASE WHEN avg_entropy > 8.0 AND max_cpu_spike > 95 THEN 20 ELSE 0 END)
    ) AS raw_risk_score

  FROM `driiiportfolio.compute_abuse_logs.v_high_risk_compute`
),

classification_layer AS (
  SELECT
    *,
    -- Dashboard Safeguard: Cap confidence at 1.0 (100%)
    LEAST(SAFE_DIVIDE(raw_risk_score, 110.0), 1.0) AS confidence_score,

    CASE 
      WHEN raw_risk_score >= 100 THEN 'BLOCK'
      WHEN raw_risk_score >= 60 THEN 'THROTTLE'
      ELSE 'MONITOR'
    END AS enforcement_action,

    -- Intent Priority Logic (Lateral Movement is highest priority)
    CASE
      WHEN max_network_pivots > 30 THEN 'LATERAL_PROPAGATION'
      WHEN avg_entropy > 7.2 AND max_cpu_spike > 90 THEN 'MODEL_EXTRACTION'
      WHEN max_cpu_spike > 85 THEN 'RESOURCE_HIJACKING'
      ELSE 'UNKNOWN_ABUSE'
    END AS intent_classification

  FROM weighted_scoring
)

SELECT
  *,
  -- Boolean for Looker Studio 'Threats Mitigated' metrics
  CASE WHEN enforcement_action IN ('BLOCK', 'THROTTLE') THEN TRUE ELSE FALSE END AS is_mitigated,
  
  -- ROI Logic: Calculating Business Value Protected
  CASE 
    WHEN enforcement_action = 'BLOCK' THEN estimated_revenue_at_risk
    WHEN enforcement_action = 'THROTTLE' THEN (estimated_revenue_at_risk * 0.7)
    ELSE 0 
  END AS revenue_protected
FROM classification_layer;
