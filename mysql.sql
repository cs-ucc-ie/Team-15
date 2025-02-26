CREATE TABLE Users (
    Userid INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    Password_hash TEXT NOT NULL
);


INSERT INTO Users (Username, Password, Password_hash) VALUES
('user1', 'password1', 'hashed_password_1'),
('user2', 'password2', 'hashed_password_2'),
('user3', 'password3', 'hashed_password_3');


CREATE TABLE Ingredients (
    Ingredientid INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Type TEXT NOT NULL,
    Alcohol_content REAL
);


INSERT INTO Ingredients (Name, Type, Alcohol_content) VALUES
('Vodka', 'Spirit', 40.0),
('Lime Juice', 'Juice', 0.0),
('Simple Syrup', 'Sweetener', 0.0);


CREATE TABLE Cocktails (
    Cocktailid INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Glass_type TEXT NOT NULL
);


INSERT INTO Cocktails (Name, Glass_type) VALUES
('Margarita', 'Cocktail Glass'),
('Mojito', 'Highball Glass'),
('Old Fashioned', 'Rocks Glass');


CREATE TABLE Favorites (
    Favouriteid INTEGER PRIMARY KEY AUTOINCREMENT,
    Userid INTEGER NOT NULL,
    Cocktailid INTEGER NOT NULL,
    FOREIGN KEY (Userid) REFERENCES Users(Userid),
    FOREIGN KEY (Cocktailid) REFERENCES Cocktails(Cocktailid)
);


INSERT INTO Favorites (Userid, Cocktailid) VALUES
(1, 1),
(2, 2),
(3, 3);