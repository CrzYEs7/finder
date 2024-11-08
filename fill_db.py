from cs50 import SQL

def fake_fill_db(t_db, n):
    for fake_part in range(n):
        try:
            print("fake_part: " + str(fake_part))
            name = "name_" + str(fake_part)
            reference = "reference_" + str(fake_part)
            car_brand_name = "car_brand_" + str(fake_part)
            part_manufacturer_name = "part_manufacturer_" + str(fake_part)
            tag_1_name = "tag_" + str(fake_part) + "_1"
            tag_2_name = "tag_" + str(fake_part) + "_2"

            print("car_brand_id not success", fake_part)

            car_brand_id = t_db.execute(
                "INSERT INTO car_brands (name) VALUES (?)", str(car_brand_name)
            )

            part_manufacturer_id = t_db.execute(
                "INSERT INTO part_manufacturers (name) VALUES (?)", str(part_manufacturer_name)
            )

            new_part_id = t_db.execute(
                "INSERT INTO car_parts (name, reference, car_brand_id, part_manufacturer_id) VALUES(?, ?, ?, ?)",
                name.capitalize(), reference.upper(), int(car_brand_id), int(part_manufacturer_id)
            )

            tag_1_id = t_db.execute("INSERT INTO tags (name) VALUES (?)", tag_1_name)
            tag_2_id = t_db.execute("INSERT INTO tags (name) VALUES (?)", tag_2_name)

            t_db.execute("INSERT INTO car_parts_tags (tag_id, part_id) VALUES (?, ?)",
                         tag_1_id, new_part_id)
            t_db.execute("INSERT INTO car_parts_tags (tag_id, part_id) VALUES (?, ?)",
                         tag_2_id, new_part_id)
            print("fake_part success: " + str(fake_part))

        except:
            # print("error on fake_part: " + str(fake_part))
            return "error on fake_part: " + str(fake_part)

    return "db filled successfully"

"""fill the database from a python dict"""
def fill_db(t_db, data_list):
    unaccepted = ["(", ")"]
    for item in data_list:
        try:
            tags = []
            name = item["name"]
            reference = item["reference"]
            car_brand_name = item["car_brand"]
            part_manufacturer_name = item["part_manufacturer"]
            description = item["description"]

            #print("here is the item: ", name)

            # create some tags from description and name
            if name:
                for word in name.split(" "):
                    if not word == "":
                        tags.append(word.strip("() "))
                else:
                    print(f"{item}: this item has no name")
                    # must have a name
                    pass

            if description:
                for word in description.split(" "):
                    if not word == "":
                        tags.append(word.strip("() "))

            for tag in tags:
                for char in unaccepted:
                    tag = tag.replace(char, "")

            car_brand_id = t_db.execute("""
                INSERT INTO car_brands (name) VALUES (?)
                ON CONFLICT (name) DO NOTHING
                """,
                str(car_brand_name)) or t_db.execute(
                """
                SELECT id FROM car_brands WHERE name = (?)
                """,
                str(car_brand_name)
            )[0]["id"]

            part_manufacturer_id = t_db.execute(
                """
                INSERT INTO part_manufacturers (name) VALUES (?)
                ON CONFLICT (name) DO NOTHING
                """,
                str(part_manufacturer_name)) or t_db.execute(
                """
                SELECT id FROM part_manufacturers WHERE name = (?)
                """,
                str(part_manufacturer_name)
            )[0]["id"]

            t_db.execute("""
                INSERT INTO car_parts (name, reference, car_brand_id, part_manufacturer_id)
                VALUES(?, ?, ?, ?)
                ON CONFLICT (reference) DO UPDATE SET car_brand_id=excluded.car_brand_id
                WHERE car_brand_id = (SELECT car_brands.id FROM car_brands
                    WHERE car_brands.name = "unknown")
                """,
                name.capitalize(), reference.upper(),
                int(car_brand_id), int(part_manufacturer_id)
            )
            new_part_id = t_db.execute("""SELECT car_parts.id
                                       FROM car_parts WHERE reference = (?)""",
                                       reference.upper())[0]["id"]

            for tag in tags:
                tag_id = t_db.execute("""
                    INSERT INTO tags (name) VALUES (?)
                    ON CONFLICT (name) DO NOTHING""",
                    tag
                ) or t_db.execute("SELECT id FROM tags WHERE name = (?)", tag)[0]["id"]

                t_db.execute("""
                    INSERT INTO car_parts_tags (tag_id, part_id)
                    VALUES (?, ?)
                    ON CONFLICT (part_id, tag_id) DO NOTHING
                    """, tag_id, new_part_id)

            print("Part success: " + str(item))

        except Exception as e:
            print(f"On item {str(item)} -> Error: {str(e)}")
            return e

    return "db filled successfully"
