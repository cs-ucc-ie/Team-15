CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cocktails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL, -- Path to image in static folder
    popularity INTEGER DEFAULT 5, -- Number of likes
    reviews_number INTEGER DEFAULT 1,
    alcohol_content INTEGER NOT NULL,
    recipe_by TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO ingredients (name) VALUES
('Vodka'),
('Gin'),
('Rum'),
('Tequila'),
('Whiskey'),
('Triple Sec'),
('Vermouth'),
('Campari'),
('Cointreau'),
('Amaretto'),
('Bitters'),
('Grenadine'),
('Simple Syrup'),
('Lime Juice'),
('Lemon Juice'),
('Orange Juice'),
('Pineapple Juice'),
('Cranberry Juice'),
('Coconut Cream'),
('Tonic Water'),
('Soda Water'),
('Cola'),
('Ginger Beer'),
('Mint Leaves'),
('Sugar Cubes'),
('Egg White'),
('Angostura Bitters'),
('Blue Curaçao'),
('Sweet Vermouth'),
('Dry Vermouth'),
('Cherry Liqueur'),
('Peach Schnapps'),
('Baileys Irish Cream'),
('Coffee Liqueur'),
('Absinthe'),
('Mezcal'),
('Maraschino Liqueur'),
('Chartreuse'),
('Aperol');

INSERT INTO cocktails (name,image,popularity, reviews_number, alcohol_content,recipe_by) VALUES
('Cosmopolitan','cosmopolitan.jpg',0, 1, 1,'c4rriebradshaw'),
('Old Fashioned','old_fashioned.jpg',7, 4, 1, 'mhobbes'),
('Aperol Spritz','aperol_spritz.jpg',1, 1, 1, 'charY0rk'),
('Dirty Martini','dirty_martini.jpg',2, 1, 1, 'SamJones'),
('Vodka with coke', 'vodka_with_coke', 123, 100, 1, 'OP'),
('Whiskey with coke', 'whiskey_with_coke', 15, 3, 1, 'OP');

SELECT name FROM ingredients;


SELECT * FROM cocktails ORDER BY popularity/reviews_number DESC;