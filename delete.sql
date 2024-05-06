
# este subidtituir no codigo
SELECT car_parts_tags.part_id, car_parts.*, COUNT(part_id) AS count
FROM car_parts_tags JOIN car_parts ON car_parts.id = car_parts_tags.part_id
WHERE car_parts_tags.part_id IN (1, 2, 3, 4, 5, 6, 7, 36, 37)
GROUP BY car_parts.id ORDER BY count DESC;



SELECT car_parts_tags.part_id, car_parts.*, part_manufacturers.name, COUNT(part_id) AS count
FROM car_parts_tags JOIN car_parts ON car_parts.id = car_parts_tags.part_id
JOIN part_manufacturers ON part_manufacturers.id = car_parts.part_manufacturer_id
WHERE car_parts_tags.tag_id IN (?)
GROUP BY car_parts.id ORDER BY count DESC

CREATE TABLE IF NOT EXISTS 'favorites_by_users'
(part_id INTEGER NOT NULL , user_id INTEGER NOT NULL,
FOREIGN KEY (part_id) REFERENCES car_parts(id),
FOREIGN KEY (user_id) REFERENCES users(id),
PRIMARY KEY (part_id, user_id));

CREATE TABLE IF NOT EXISTS 'users_username'
('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
'username' TEXT NOT NULL UNIQUE,'hash' TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS 'part_manufacturers'
('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'name' TEXT NOT NULL UNIQUE);




SELECT cp.*, pm.name AS manufacturer_name, fav.part_id as favorited,
        ((CASE WHEN LOWER(t.name) LIKE '%' || LOWER("filtro") || '%' THEN 1 ELSE 0 END) +
        (CASE WHEN LOWER(cb.name) LIKE '%' || LOWER("filtro") || '%' THEN 1 ELSE 0 END) +
        (CASE WHEN LOWER(pm.name) LIKE '%' || LOWER("filtro") || '%' THEN 1 ELSE 0 END) +
        (CASE WHEN LOWER(cp.reference) LIKE '%' || LOWER("filtro") || '%' THEN 5 ELSE 0 END)) AS match_count
        FROM car_parts_tags AS cpt
        JOIN car_parts AS cp ON cpt.part_id = cp.id
        LEFT JOIN tags AS t ON cpt.tag_id = t.id
        LEFT JOIN favorites_by_users AS fav ON cp.id = fav.part_id AND fav.user_id = 1
        LEFT JOIN car_brands AS cb ON cp.car_brand_id = cb.id
        LEFT JOIN part_manufacturers AS pm ON cp.part_manufacturer_id = pm.id
        GROUP BY cp.id
        HAVING match_count >= 1
        ORDER BY match_count DESC
        LIMIT 20

'1998', ' 1999', '1998', ' 1999', '1998', ' 1999', '1998', ' 1999', 1

SELECT cp.*,
        ((CASE WHEN LOWER(t.name) LIKE '%' || LOWER("respiro") || '%' THEN 1 ELSE 0 END) +
        (CASE WHEN LOWER(cp.reference) LIKE '%' || LOWER("respiro") || '%' THEN 5 ELSE 0 END)) AS match_count
        FROM car_parts_tags AS cpt
        LEFT JOIN car_parts AS cp ON cp.id = cpt.part_id
        LEFT JOIN tags AS t ON cpt.tag_id = t.id
        GROUP BY t.id, cp.name
        HAVING match_count >= 1
        ORDER BY match_count DESC
        LIMIT 20

SELECT cp.*, COUNT(cp.id) as cp_count, (CASE WHEN LOWER(t.name) LIKE '%' || LOWER("borne") || '%' THEN 5 ELSE 0 END) AS match_count
        FROM car_parts_tags AS cpt
        LEFT JOIN car_parts AS cp ON cp.id = cpt.part_id
        LEFT JOIN tags AS t ON cpt.tag_id = t.id
        WHERE match_count >= 1
        GROUP BY cp.id
        ORDER BY match_count + cp_count DESC
        LIMIT 20;


        HAVING match_count >= 1
        ORDER BY match_count DESC
        LIMIT 20
        WHERE LOWER(t.name) LIKE '%' || LOWER("respiro") || '%';

