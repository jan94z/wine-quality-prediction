/*CREATE TABLE wine_samples (
    id SERIAL PRIMARY KEY,
    fixed_acidity REAL,
    volatile_acidity REAL,
    citric_acid REAL,
    residual_sugar REAL,
    chlorides REAL,
    free_sulfur_dioxide REAL,s
    total_sulfur_dioxide REAL,
    density REAL,
    pH REAL,
    sulphates REAL,
    alcohol REAL,
    quality INTEGER,
    wine_type TEXT
);
*/

CREATE TABLE train_samples AS
SELECT * FROM wine_samples
WHERE random() < 0.7;

CREATE TABLE val_samples AS
SELECT * FROM wine_samples
WHERE random() >= 0.7 AND random() < 0.85;

CREATE TABLE test_samples AS
SELECT * FROM wine_samples
WHERE random() >= 0.85;
