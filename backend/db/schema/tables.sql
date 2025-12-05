DROP TABLE IF EXISTS User;
-- USER DETAILS --
CREATE TABLE User (
    username VARCHAR(50) NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    age INT,
    home_city VARCHAR(50)
);

CREATE TABLE Interests (
    interest_id INT NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE User_Interests_Map (
    username VARCHAR(50) NOT NULL,
    interest_id INT NOT NULL,
    PRIMARY KEY (username, interest_id),
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE,
    FOREIGN KEY (interest_id) REFERENCES Interests(interest_id) ON DELETE CASCADE
);

CREATE TABLE User_Visit (
    visit_id INT NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    attraction_name VARCHAR(100) NOT NULL,
    visit_date DATE NOT NULL,
    rating FLOAT,
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE
);

-- ATTRACTION TABLES --
CREATE TABLE Attractions (
    name VARCHAR(100) NOT NULL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    price FLOAT,
    rating FLOAT
);

CREATE TABLE Attraction_Tags (
    tag_id INT NOT NULL PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Attraction_Tags_Map (
    attraction_name VARCHAR(100) NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (attraction_name, tag_id),
    FOREIGN KEY (attraction_name) REFERENCES Attractions(name) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Attraction_Tags(tag_id) ON DELETE CASCADE
);

-- RECOMMENDATION TABLES --
CREATE TABLE Recommendations (
    recommendation_id INT NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    attraction_name VARCHAR(100) NOT NULL,
    reason VARCHAR(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE,
    FOREIGN KEY (attraction_name) REFERENCES Attractions(name) ON DELETE CASCADE
);

CREATE TABLE Recommendation_Result (
    recommendation_id INT PRIMARY KEY,
    username VARCHAR(50),
    FOREIGN KEY (recommendation_id) REFERENCES Recommendations(recommendation_id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE
);

CREATE TABLE Recommended_Attractions (
    recommendation_id INT PRIMARY KEY,
    attraction_name VARCHAR(100),
    FOREIGN KEY (recommendation_id) REFERENCES Recommendations(recommendation_id) ON DELETE CASCADE,
    FOREIGN KEY (attraction_name) REFERENCES Attractions(name) ON DELETE CASCADE
);