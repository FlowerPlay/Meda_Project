import requests
import csv
import time

def fetch_openfoodfacts_data(category, target_count=500, output_file="openfoodfacts_products.csv"):
    base_url = "https://world.openfoodfacts.org/cgi/search.pl"
    headers = {
        "User-Agent": "OpenFoodFacts Python Client - Data Extractor"
    }

    products = []
    page = 1
    page_size = 10

    while len(products) < target_count:
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
            response = requests.get(base_url, params=params, headers=headers, timeout=100)
            response.raise_for_status()
            data = response.json()
            page_products = data.get("products", [])

            for product in page_products:
                if "code" not in product:
                    continue  # Skip products without barcode

                products.append({
                    "barcode": product.get("code", ""),
                    "product_name": product.get("product_name", ""),
                    "ingredients": product.get("ingredients_text", ""),
                    "nutrients": product.get("nutriments", {}),
                    "categories": product.get("categories", ""),
                    "countries": ", ".join(product.get("countries_tags", []))
                })

                if len(products) >= target_count:
                    break

            print(f"Fetched {len(products)} products so far...")
            page += 1
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Error on page {page}: {e}")
            break

    # Write to CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "barcode", "product_name", "ingredients", "nutrients", "categories", "countries"
        ])
        writer.writeheader()
        for product in products:
            # Flatten nutrients dictionary for CSV
            nutrients_flat = "; ".join([f"{k}: {v}" for k, v in product["nutrients"].items()])
            product["nutrients"] = nutrients_flat
            writer.writerow(product)

    print(f"Saved {len(products)} products to {output_file}")

# Example usage
if __name__ == "__main__":
    fetch_openfoodfacts_data(category="snacks")
