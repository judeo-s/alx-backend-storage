-- Retrieves the band name and lifespan of glam rock bands from the
-- metal_bands table.

SELECT band_name,
    (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
