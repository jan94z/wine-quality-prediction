-- FIRST CREATE THE MAIN TABLE
CREATE TABLE wine_samples (
    id SERIAL PRIMARY KEY,
    fixed_acidity REAL,
    volatile_acidity REAL,
    citric_acid REAL,
    residual_sugar REAL,
    chlorides REAL,
    free_sulfur_dioxide REAL,
    total_sulfur_dioxide REAL,
    density REAL,
    pH REAL,
    sulphates REAL,
    alcohol REAL,
    quality INTEGER,
    wine_type TEXT
);

-- THEN INSERT CSV DATA

-- THEN MAKE THE DATASPLIT
SELECT setseed(0);

CREATE TABLE wine_samples_split AS
SELECT
    id,
    random() AS split_random
FROM wine_samples;

ALTER TABLE wine_samples_split
ADD split_group TEXT;

UPDATE wine_samples_split
SET split_group = 'train'
WHERE split_random <= 0.8;

UPDATE wine_samples_split
SET split_group = 'valid'
WHERE split_random > 0.8 AND split_random <= 0.9;

UPDATE wine_samples_split
SET split_group = 'test'
WHERE split_random > 0.9;

-- MAKE MODEL REGISTRY TABLE
CREATE TABLE model_registry (
    id SERIAL PRIMARY KEY,
    model_name TEXT,
    version TEXT,
  	type TEXT,
    path TEXT,
  	accuracy_train REAL,
    accuracy_val REAL,
    accuracy_test REAL
);

-- THEN YOU CAN TRAIN AND REGISTTER NEW MODELS






