# Meda_Project
Repo for Medaxion assessment Python code, SQLite db, &amp; readme files - August 5, 2025

Assumptions:
1.  It doesn't matter which 500 products are pulled from the Open Food Facts database, as long as at least 500 products are pulled.
2.  It does not matter where this code is run (ie, doesn't matter if it is run locally or on a virtual server).  Therefore, I can set this up in Github Codespaces and run it on Linux in a virtual instance there.
3.  Validations only have to be the most basic, to illustrate that I know how to do this in Python. (Because my background is as a DBA & Data QA Architect, typically, most of the Data QA that I would run would be automated and not necessarily done during the initial data load.)
4.  Wherever Python has libraries to do the work, I do not need to create my own.  Hence, for this project I used requests, validate, marshmallow, time, and csv.
5.   

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The Relational Tables
There are CSV files representing each table in the schema:

products.csv — barcode, product name, brand, packaging, creation time
nutrients.csv — barcode, energy, fat, carbs, protein, etc.
ingredients.csv — barcode, ingredient text
categories.csv — barcode, category (one per row)
countries.csv — barcode, country (one per row)

Schema Recap:
Each table is linked by the barcode field:

Table	Description
products	General product metadata
nutrients	Nutritional values per 100g
ingredients	Raw ingredient text
categories	One row per category per product
countries	One row per country per product
Would you like help importing these into a database (e.g., SQLite or PostgreSQL), or visualizing the data?

Suggested Data Visualizations for This Data:
1.  Top 10 categories by product count
2.  Distribution of energy (kcal per 100g)
3.  Top 10 countries of origin
4.  Word cloud of ingredients


Suggested Relational Schema
David:  You've proposed a solid schema. 
Here's a slightly refined version (with reasoning by each Table name):


1. products - for this table, I just added in a bit of metadata 

    --barcode (PK)

    --product_name

    --brands

    --packaging

    --created_t

    --last_modified_t

    --quantity

    --labels

    --ecoscore_score

    --nova_group

    --(other general metadata)


2. nutrients - for this table, I added in saturated fat, sugars, fiber, and salt because these elements would be key fields for real-world metrics.)

    --barcode (FK)
    
    --energy_kcal_100g

    --fat_100g
    
    --saturated_fat_100g

    --carbohydrates_100g

    --sugars_100g

    --fiber_100g

    --proteins_100g

    --salt_100g


3. ingredients - for this table, I left it as you'd suggested - schema as is.

    --barcode (FK)

    --ingredient_text


4. categories - for this table, I left this table with 2 fields as you'd suggested, but I did have to split the categories string to extract the category data.

    --barcode (FK)

    --category (split from categories string)


5. countries - and for this table, I left it as you'd suggested - schema as is.

    --barcode (FK)

    --country (from countries_tags)
