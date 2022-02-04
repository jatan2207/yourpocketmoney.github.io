DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_data;
DROP TABLE IF EXISTS lease;

CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gmail TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );

CREATE TABLE user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        availabe_coins INTEGER NOT NULL,
        balance INTEGER NOT NULL,
        daily_income INTEGER NOT NULL,
        total_income INTEGER NOT NULL,
        withdrawable_amount INTEGER NOT NULL,
        withdrawn_amount INTEGER NOT NULL
    );    

CREATE TABLE lease (
    user_id INTEGER NOT NULL PRIMARY KEY,
    daily_income INTEGER NOT NULL,
    total_income INTEGER NOT NULL,
    leased_days INTEGER NOT NULL,
    accumulated_income INTEGER NOT NULL
    );
