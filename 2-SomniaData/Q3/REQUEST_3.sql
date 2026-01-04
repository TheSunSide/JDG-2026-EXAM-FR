-- ============================================================================
-- REQUEST_3.sql - Somnia Data
-- ============================================================================
-- Objectif: Récupérer toutes les recommandations non actives pour un plan donné (id = 30)
-- ============================================================================

-- TODO: Écrire la requête SQL ici
SELECT
    ip.id,
    ipr.*
FROM intervention_plans ip
LEFT JOIN intervention_plan_recommendations ipr on ip.id = ipr.intervention_plan_id
WHERE
    ip.id = 30 AND
    ipr.status = 'COMPLETED' || ipr.status = 'AWAITING'