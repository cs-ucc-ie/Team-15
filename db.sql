CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cocktails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL DEFAULT 'basic.jpg', -- Default image set to 'basic.jpg'
    popularity INTEGER DEFAULT 5, -- Number of likes
    reviews_number INTEGER DEFAULT 1,
    alcohol_content INTEGER NOT NULL,
    recipe_by TEXT NOT NULL,
    method TEXT NOT NULL DEFAULT '',
    created_by INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO ingredients (name) VALUES
('Vodka'), ('Gin'), ('Rum'), ('Tequila'), ('Whiskey'), ('Triple Sec'), ('Vermouth'),
('Campari'), ('Cointreau'), ('Amaretto'), ('Bitters'), ('Grenadine'), ('Simple Syrup'),
('Lime Juice'), ('Lemon Juice'), ('Orange Juice'), ('Pineapple Juice'), ('Cranberry Juice'),
('Coconut Cream'), ('Tonic Water'), ('Soda Water'), ('Cola'), ('Ginger Beer'), ('Mint Leaves'),
('Sugar Cubes'), ('Egg White'), ('Angostura Bitters'), ('Blue Curaçao'), ('Sweet Vermouth'),
('Dry Vermouth'), ('Cherry Liqueur'), ('Peach Schnapps'), ('Baileys Irish Cream'), ('Coffee Liqueur'),
('Absinthe'), ('Mezcal'), ('Maraschino Liqueur'), ('Chartreuse'), ('Aperol'), ('Honey Syrup'),
('Club Soda'), ('Dark Rum'), ('Prosecco'), ('Irish Whiskey'), ('Espresso'), ('Cinnamon'), ('Nutmeg'),
('Bourbon'), ('Maple Syrup'), ('Apple Cider'), ('Red Wine'), ('Egg Nog');

INSERT INTO cocktails (name, image, popularity, reviews_number, alcohol_content, recipe_by) VALUES
('Cosmopolitan', 'cosmopolitan.jpg', 50, 20, 1, 'c4rriebradshaw'),
('Old Fashioned', 'old_fashioned.jpg', 80, 40, 1, 'mhobbes'),
('Aperol Spritz', 'aperol_spritz.jpg', 60, 30, 1, 'charY0rk'),
('Dirty Martini', 'dirty_martini.jpg', 55, 25, 1, 'SamJones'),
('Vodka with Coke', 'vodka_with_coke.jpg', 123, 100, 1, 'OP'),
('Whiskey with Coke', 'whiskey_with_coke.jpg', 90, 50, 1, 'OP'),
('Mojito', 'mojito.jpg', 70, 35, 1, 'BartenderX'),
('Margarita', 'margarita.jpg', 85, 45, 1, 'DrinkMaster42'),
('Pina Colada', 'pina_colada.jpg', 78, 38, 1, 'TropicalJoe'),
('Long Island Iced Tea', 'long_island_iced_tea.jpg', 95, 50, 1, 'PartyGuru'),
('Negroni', 'negroni.jpg', 65, 28, 1, 'ClassicCocktail'),
('Espresso Martini', 'espresso_martini.jpg', 88, 47, 1, 'CaffeineAddict'),
('Irish Coffee', 'irish_coffee.jpg', 58, 22, 1, 'DublinBartender'),
('Mai Tai', 'mai_tai.jpg', 75, 33, 1, 'TikiMan'),
('Daiquiri', 'daiquiri.jpg', 72, 31, 1, 'CubaLibre'),
('Manhattan', 'manhattan.jpg', 82, 39, 1, 'NYCDrinker'),
('Boulevardier', 'boulevardier.jpg', 62, 27, 1, 'WhiskeyAficionado'),
('Sazerac', 'sazerac.jpg', 55, 20, 1, 'NewOrleansMixologist');

CREATE TABLE IF NOT EXISTS cocktail_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cocktail_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE,
    UNIQUE (cocktail_id, ingredient_id)
);

CREATE TABLE IF NOT EXISTS favorites (
    favorites_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    cocktail_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (cocktail_id) REFERENCES cocktails (id) ON DELETE CASCADE
);

INSERT INTO favorites (user_id, cocktail_id) VALUES
(3, 1);

INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id) VALUES
(1, 1), (1, 9), 
(1, 18), (1, 14),
(2, 5), (2, 11), 
(2, 24), (3, 39), 
(3, 44), (3, 21),
(4, 2), (4, 30),
(5, 1), (5, 22),
(6, 5), (6, 22),
(7, 3), (7, 24), 
(7, 14), (7, 23), 
(7, 21),(8, 4), 
(8, 9), (8, 14), 
(9, 3), (9, 19), 
(9, 17),(10, 1), 
(10, 2), (10, 3), 
(10, 4), (10, 6), 
(10, 14), (10, 22),
(11, 2), (11, 7), 
(11, 8), (12, 1), 
(12, 34), (12, 43),
(13, 45), (13, 34), 
(13, 43), (14, 3), 
(14, 31), (14, 14),
(15, 3), (15, 14), 
(15, 12), (16, 5), 
(16, 7), (16, 11),
(17, 5), (17, 8), 
(17, 7), (18, 5), 
(18, 35), (18, 11), 
(18, 24);

SELECT name FROM ingredients;


SELECT * FROM cocktails ORDER BY popularity/reviews_number DESC;

SELECT * FROM cocktail_ingredients;
SELECT * FROM cocktails;


