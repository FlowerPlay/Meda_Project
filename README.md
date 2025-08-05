# Meda_Project
Repo for Medaxion assessment Python code, SQLite db, &amp; readme files - August 4-8, 2025

Assumptions:
1.  It doesn't matter which 500 products are pulled from the Open Food Facts database, as long as at least 500 products are pulled.
2.  It does not matter where this code is run (ie, doesn't matter if it is run locally or on a virtual server).  Therefore, I can set this up in Github Codespaces and run it on Linux in a virtual instance there.
3.  Validations only have to be the most basic, to illustrate that I know how to do this in Python. (Because my background is as a DBA & Data QA Architect, typically, most of the Data QA that I would run would be automated and not necessarily done during the initial data load.)
4.  Wherever Python has libraries to do the work, I do not need to create my own.  Hence, for this project I used requests, val, time, logging, sqlite3, and csv.
5.  Wherever errors might be thrown, there needed to be at least rudimentary error logging, so I've written the code to create n errors log in the same Github repo folder.
6.  The code should be able to run in a single Python file, so I have not broken it up into multiple files.
7.  Once DJ gets the code from me, he will simply take the .zip file from Github and put it into a repo of his choice, then run the code in a Python environment of his choice.  Therefore, I have only saved the original .csv files that the code generated AND the original SQLite database that the code created into an Original_Data folder in my repo for DJ's reference.
8.  Once this code was completed, it would need to be run on some time table regularly to update the data, so to simulate this requirement I've also put a .bat file into the repo to show how a Task could be set up to run the code hourly and update continually for reporting / analytical purposes.
9.  If I had more time, I would have used a different database than SQLite, such as PostgreSQL or MySQL, so that indexing and performance management, etc could be more accurately demonstrated.  However, I went with SQLite because it was DJ's choice.  I am not a fan of SQLite personally, but I can work with it and if I had more time I'd spend time optimizing, indexing, and creating the data visualizations.
10.  Now that I've spent 3 days coding, DJ will hire me immediately and pay me beyond my wildest dreams.  (just kidding, but I do hope he reads this file and appreciate the effort I put into his assessment).
----------------------------------------------------------------------------------------------------------------------------------

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
