-- ============================================================================
-- REQUEST_5.sql - Somnia Data
-- ============================================================================
-- Objectif: Récupérer tous les plans d'intervention avec leur profil et utilisateur 
--          associé créés entre le 1er décembre et le 1er janvier, triées en ordre 
--          chronologique selon la date de création
-- ============================================================================

-- TODO: Écrire la requête SQL ici

SELECT *
FROM intervention_plans ip
LEFT JOIN user_sleep_profiles usp ON ip.user_sleep_profile_id = usp.id
LEFT JOIN users usr ON usp.user_id = usr.id
WHERE  ip.creation_date  BETWEEN '2025-12-01 00:00:01' AND '2026-01-01 00:00:01'
ORDER BY
    ip.creation_date,
    usp.creation_date