-- ============================================================================
-- REQUEST_2.sql - Somnia Data
-- ============================================================================
-- Objectif: Récupérer la liste de tous les profils d'un utilisateur donné (id = 42) 
--          avec son nombre de plans d'intervention en attente
-- ============================================================================

-- TODO: Écrire la requête SQL ici
WITH tmp AS (
    SELECT
    usr.id,
    usp.*,
    COUNT(*) AS plan_count
FROM users usr
LEFT JOIN user_sleep_profiles usp ON usr.id = usp.user_id
LEFT JOIN intervention_plans ip ON usp.id = ip.user_sleep_profile_id
WHERE
    usr.id = 42 AND
    ip.status = 'AWAITING'
GROUP BY 1
)

SELECT *
FROM tmp;