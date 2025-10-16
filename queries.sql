SELECT seller_id, COUNT(*) AS publicaciones
FROM meli_items
WHERE job_run = :job_run
GROUP BY seller_id
HAVING COUNT(*) > 1
ORDER BY publicaciones DESC;

SELECT seller_id,
       AVG(COALESCE(sold_quantity,0)) AS promedio_ventas_por_publicacion
FROM meli_items
WHERE job_run = :job_run
GROUP BY seller_id
ORDER BY promedio_ventas_por_publicacion DESC;

SELECT ROUND(AVG(price_usd)::numeric, 2) AS precio_promedio_usd
FROM meli_items
WHERE job_run = :job_run;

SELECT
  ROUND(100.0 * SUM(CASE WHEN NULLIF(TRIM(warranty), '') IS NOT NULL THEN 1 ELSE 0 END)::numeric
            / NULLIF(COUNT(*),0), 2) AS pct_con_garantia
FROM meli_items
WHERE job_run = :job_run;

SELECT COALESCE(logistic_type, 'desconocido') AS logistic_type,
       COALESCE(shipping_mode, 'desconocido') AS shipping_mode,
       SUM(CASE WHEN free_shipping THEN 1 ELSE 0 END) AS con_envio_gratis,
       COUNT(*) AS publicaciones
FROM meli_items
WHERE job_run = :job_run
GROUP BY COALESCE(logistic_type, 'desconocido'),
         COALESCE(shipping_mode, 'desconocido')
ORDER BY publicaciones DESC;
