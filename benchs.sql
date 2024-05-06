SELECT car_parts.*, part_manufacturers.name
AS manufacturer_name FROM car_parts JOIN part_manufacturers
ON car_parts.part_manufacturer_id = part_manufacturers.id
WHERE car_parts.id
IN (SELECT part_id FROM car_parts_tags WHERE tag_id IN (500))
