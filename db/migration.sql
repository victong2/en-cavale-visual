CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR (50) UNIQUE NOT NULL
);

INSERT INTO categories 
  (name)
VALUES
  ('Hébergement'),
  ('Visite'),
  ('Course'),
  ('Snack'),
  ('Transport'),
  ('Restaurant');

CREATE TABLE spending (
  id SERIAL PRIMARY KEY,
  date DATE NOT NULL,
  amount money NOT NULL,
  category_id INT,
  description TEXT,
  FOREIGN KEY(category_id) 
    REFERENCES categories(id)
);

\copy spending (date, amount, category, description) from '/home/victorng/src/en-cavale/data/spending.csv' delimiter ',' CSV HEADER;

-- This table has been manually populated
CREATE TABLE countries (
  id SERIAL PRIMARY KEY,
  name VARCHAR (50) UNIQUE NOT NULL, 
  arrival DATE NOT NULL,
  departure DATE NOT NULL
);

CREATE TYPE category AS ENUM ('Transport', 'Restaurant', 'Courses', 'Visite', 'Hébergement', 'Snack');

ALTER TABLE spending ALTER COLUMN category TYPE category USING (trim(category)::category);
