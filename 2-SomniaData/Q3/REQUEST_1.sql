-- ============================================================================
-- REQUEST_1.sql - Somnia Data
-- ============================================================================
-- Objectif: Récupérer la liste des utilisateurs qui ont plus de 3 plans d'intervention actifs
-- ============================================================================

-- TODO: Écrire la requête SQL ici
WITH tmp AS (
    SELECT
    usr.id,
    COUNT(*) AS plan_count
FROM users usr
LEFT JOIN user_sleep_profiles usp ON usr.id = usp.user_id
LEFT JOIN intervention_plans ip ON usp.id = ip.user_sleep_profile_id
WHERE ip.status = 'ACTIVE'
GROUP BY 1
)

SELECT *
FROM tmp 
WHERE plan_count > 3