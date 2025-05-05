CREATE TABLE wine_samples (
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

