import requests
import csv
import time
import sqlite3
import logging
from collections import defaultdict

# Setup logging
logging.basicConfig(filename="openfoodfacts_errors.log", level=logging.ERROR,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_openfoodfacts_data(category, target_count=500):
    base_url = "https://world.openfoodfacts.org/cgi/search.pl"
    headers = {
        "User-Agent": "OpenFoodFacts Python Client - Relational Extractor"
    }

    products_data = []
    nutrients_data = []
    ingredients_data = []
    categories_data = []
    countries_data = []

    skipped_count = 0
    page = 1
    page_size = 50
    timeout = 100

    while len(products_data) < target_count:
        params = {
            "search_terms": "",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "page_size": page_size,
            "page": page,
            "json": True
        }

        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            page_products = data.get("products", [])

            for product in page_products:
                barcode = product.get("code")
                if not barcode:
                    logging.error(f"Missing barcode for product on page {page}")
                    skipped_count += 1
                    continue

                products_data.append({
                    "barcode": barcode,
                    "product_name": product.get("product_name", ""),
                    "brand": ", ".join(product.get("brands_tags", [])),
                    "packaging": product.get("packaging", ""),
                    "create_t": product.get("created_t", ""),
                    "last_modified_t": product.get("last_modified_t", ""),
                    "quantity": product.get("quantity", ""),
                    "labels": product.get("labels", ""),
                    "ecoscore_score": product.get("ecoscore_score", ""),
                    "nova_group": product.get("nova_group", "")
                })

                nutriments = product.get("nutriments", {})
                nutrients_data.append({
                    "barcode": barcode,
                    "energy_kcal_100g": nutriments.get("energy-kcal_100g", ""),
                    "fat_100g": nutriments.get("fat_100g", ""),
                    "saturated_fat_100g": nutriments.get("saturated-fat_100g", ""),
                    "carbohydrates_100g": nutriments.get("carbohydrates_100g", ""),
                    "sugars_100g": nutriments.get("sugars_100g", ""),
                    "fiber_100g": nutriments.get("fiber_100g", ""),
                    "proteins_100g": nutriments.get("proteins_100g", ""),
                    "salt_100g": nutriments.get("salt_100g", "")
                })

                ingredients_data.append({
                    "barcode": barcode,
                    "ingredient_text": product.get("ingredients_text", "")
                })

                for cat in product.get("categories_tags", []):
                    categories_data.append({
                        "barcode": barcode,
                        "category": cat
                    })

                for country in product.get("countries_tags", []):
                    countries_data.append({
                        "barcode": barcode,
                        "country": country
                    })

                if len(products_data) >= target_count:
                    break

            print(f"Fetched {len(products_data)} products so far...")
            page += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            logging.error(f"API request error on page {page}: {e}")
            break

    def save_csv(filename, data, fieldnames):
        try:
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            logging.error(f"Error writing CSV file {filename}: {e}")

    save_csv("products.csv", products_data, [
        "barcode", "product_name", "brand", "packaging", "create_t", "last_modified_t",
        "quantity", "labels", "ecoscore_score", "nova_group"
    ])
    save_csv("nutrients.csv", nutrients_data, [
        "barcode", "energy_kcal_100g", "fat_100g", "saturated_fat_100g",
        "carbohydrates_100g", "sugars_100g", "fiber_100g", "proteins_100g", "salt_100g"
    ])
    save_csv("ingredients.csv", ingredients_data, ["barcode", "ingredient_text"])
    save_csv("categories.csv", categories_data, ["barcode", "category"])
    save_csv("countries.csv", countries_data, ["barcode", "country"])

    def insert_into_sqlite(db_name):
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                barcode TEXT PRIMARY KEY,
                product_name TEXT,
                brand TEXT,
                packaging TEXT,
                create_t TEXT,
                last_modified_t TEXT,
                quantity TEXT,
                labels TEXT,
                ecoscore_score TEXT,
                nova_group TEXT
            )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS nutrients (
                barcode TEXT,
                energy_kcal_100g TEXT,
                fat_100g TEXT,
                saturated_fat_100g TEXT,
                carbohydrates_100g TEXT,
                sugars_100g TEXT,
                fiber_100g TEXT,
                proteins_100g TEXT,
                salt_100g TEXT
            )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS ingredients (
                barcode TEXT,
                ingredient_text TEXT
            )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
                barcode TEXT,
                category TEXT
            )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS countries (
                barcode TEXT,
                country TEXT
            )""")

            def insert_data(table, data, fields):
                placeholders = ','.join(['?'] * len(fields))
                query = f"INSERT INTO {table} ({','.join(fields)}) VALUES ({placeholders})"
                for row in data:
                    try:
                        values = [row.get(field, "") for field in fields]
                        cursor.execute(query, values)
                    except Exception as e:
                        logging.error(f"Database insertion error in table {table} for barcode {row.get('barcode')}: {e}")

            insert_data("products", products_data, [
                "barcode", "product_name", "brand", "packaging", "create_t", "last_modified_t",
                "quantity", "labels", "ecoscore_score", "nova_group"
            ])
            insert_data("nutrients", nutrients_data, [
                "barcode", "energy_kcal_100g", "fat_100g", "saturated_fat_100g",
                "carbohydrates_100g", "sugars_100g", "fiber_100g", "proteins_100g", "salt_100g"
            ])
            insert_data("ingredients", ingredients_data, ["barcode", "ingredient_text"])
            insert_data("categories", categories_data, ["barcode", "category"])
            insert_data("countries", countries_data, ["barcode", "country"])

            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error creating or inserting into SQLite database: {e}")

    insert_into_sqlite("openfoodfacts.db")

    print("Data saved to CSV files and SQLite database.")
    print(f"Skipped {skipped_count} products due to missing barcodes.")

if __name__ == "__main__":
    fetch_openfoodfacts_data(category="snacks")