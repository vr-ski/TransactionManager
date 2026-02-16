-- ============================
-- Drop existing tables (development only)
-- ============================

DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS transaction_status_translations CASCADE;
DROP TABLE IF EXISTS transaction_status_colors CASCADE;
DROP TABLE IF EXISTS transaction_statuses CASCADE;
DROP TABLE IF EXISTS transaction_types CASCADE;
DROP TABLE IF EXISTS transaction_type_translations CASCADE;
DROP TABLE IF EXISTS contractors CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS languages CASCADE;

-- ============================
-- Users
-- ============================

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL CHECK (char_length(username) <= 50),
    password_hash TEXT NOT NULL
);

-- ============================
-- Languages
-- ============================

CREATE TABLE languages (
    language_code TEXT PRIMARY KEY CHECK (char_length(language_code) <= 5),
    name TEXT NOT NULL
);

-- ============================
-- Contractors
-- ============================

CREATE TABLE contractors (
    contractor_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    name TEXT NOT NULL CHECK (char_length(name) <= 100),
    UNIQUE (user_id, name)
);

-- ============================
-- Transaction Status System
-- ============================

-- Base status table (stable internal codes)
CREATE TABLE transaction_statuses (
    status_id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL CHECK (char_length(code) <= 50)
);

-- Colors (one per status)
CREATE TABLE transaction_status_colors (
    status_id INTEGER PRIMARY KEY REFERENCES transaction_statuses(status_id),
    color TEXT NOT NULL CHECK (char_length(color) <= 20)
);

-- Multilingual translations
CREATE TABLE transaction_status_translations (
    status_id INTEGER NOT NULL REFERENCES transaction_statuses(status_id),
    language_code TEXT NOT NULL REFERENCES languages(language_code),
    display_name TEXT NOT NULL CHECK (char_length(display_name) <= 100),
    PRIMARY KEY (status_id, language_code)
);

-- Transaction Types
CREATE TABLE transaction_types (
    transaction_type_id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL CHECK (char_length(code) <= 50)
);

-- Multilingual translations
CREATE TABLE transaction_type_translations (
    transaction_type_id INT NOT NULL REFERENCES transaction_types(transaction_type_id),
    language_code TEXT NOT NULL REFERENCES languages(language_code),
    display_name TEXT NOT NULL CHECK (char_length(display_name) <= 100),
    PRIMARY KEY (transaction_type_id, language_code)
);


-- ============================
-- Transactions
-- ============================

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    contractor_from_id INTEGER NOT NULL REFERENCES contractors(contractor_id),
    contractor_to_id INTEGER NOT NULL REFERENCES contractors(contractor_id),
    amount NUMERIC(12,2) NOT NULL,
    transaction_type_id INT  NOT NULL REFERENCES transaction_types(transaction_type_id),
    status_id INTEGER NOT NULL REFERENCES transaction_statuses(status_id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- update trigger
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON transactions
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();


-- ============================
-- Indexes (performance)
-- ============================

CREATE INDEX idx_transactions_from_contractor ON transactions(contractor_from_id);
CREATE INDEX idx_transactions_to_contractor ON transactions(contractor_to_id);
CREATE INDEX idx_transactions_created_at ON transactions(created_at);
