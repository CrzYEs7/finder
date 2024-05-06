import pandas as pd
from helpers import guess_manufacturer
# import time

car_brands = [
    "honda", "peugeot", "volkswagen", "citroen", "renault", "audi", "skoda",
    "fiat", "lancia", "bmw", "hyundai", "lancia", "volvo", "mitsubishi",
    "nissan", "rover", "mercedes", "isuzu"
]
# start = time.time()


def get_parts_data(file):
    excel_doc = pd.read_excel(file, sheet_name=None, skiprows=[0],
                              names=['name', 'description', 'reference'], na_filter=False)

    # the indice sheet has no point for this matter
    excel_doc.pop('Indice')

    parts = []
    for sheet in excel_doc:
        for index, row in excel_doc[sheet].iterrows():
            if row["name"] and row["reference"]:
                part_manufacturer = guess_manufacturer(row["reference"]) or "unknown"
                name = str(row['name'])
                description = str(row['description']).lower()
                reference = str(row['reference']).upper()
                parts.append({
                    "name": name,
                    "description": description,
                    "reference": reference,
                    "part_manufacturer": part_manufacturer,
                    "car_brand": sheet if sheet.lower() in car_brands else "unknown"
                })
                # print(f"{index} - {row["name"]} | {row["description"]} | {row["reference"]} | {part_manufacturer}")
    return parts

# end = time.time()

# print("Exec time: ", end - start)
