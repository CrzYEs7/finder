import sqlite3

def search_car_parts(user_inputs, user_id, db_file):
    """Search car parts"""

    # Prepare base query with joins
    base_query = """
        SELECT
            cp.*,
            pm.name AS manufacturer_name,
            fav.part_id as favorited,
            COUNT(cp.id) as cp_count,
            (
                (CASE WHEN {} THEN 1 ELSE 0 END) +
                (CASE WHEN {} THEN 1 ELSE 0 END) +
                (CASE WHEN {} THEN 1 ELSE 0 END) +
                (CASE WHEN {} THEN 5 ELSE 0 END)
            ) AS match_count
        FROM car_parts AS cp
        LEFT JOIN favorites_by_users AS fav
            ON cp.id = fav.part_id AND fav.user_id = ?
        LEFT JOIN car_parts_tags AS cpt
            ON cp.id = cpt.part_id
        LEFT JOIN tags AS t
            ON cpt.tag_id = t.id
        LEFT JOIN car_brands AS cb
            ON cp.car_brand_id = cb.id
        LEFT JOIN part_manufacturers AS pm
            ON cp.part_manufacturer_id = pm.id
        WHERE match_count >= 1
        GROUP BY cp.id
        ORDER BY match_count + cp_count DESC
        LIMIT 20;
    """

    # possible types of input to query for in the data base
    fields = ['t.name', 'cb.name', 'pm.name', 'cp.reference']

    ## will be inserted into the base_query in a iqual amout of the users input
    condition_template = "LOWER({}) LIKE '%' || LOWER(?) || '%'"
    conditions = {}

    # for every category
    for field in fields:
        conditions[field] = " OR ".join(
            [condition_template.format(field) for input in user_inputs])

    # print("conditions: ", conditions)

    base_query = base_query.format(
        conditions[fields[0]], conditions[fields[1]],
        conditions[fields[2]], conditions[fields[3]])

    # database connection
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # query input
    query_content_to_search = user_inputs * 4
    # print("query_content_to_search: ", query_content_to_search)

    # query
    res = cursor.execute(base_query, query_content_to_search + [user_id])
    result = [dict(row) for row in res.fetchall()]

    conn.close()

    # print(base_query)
    # print(result)

    return result
