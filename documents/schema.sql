-- TechWayFinder Database Schema
-- This file contains the complete database schema for the TechWayFinder application

-- USERS TABLE
-- Stores user account information
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    age INTEGER,
    qualification TEXT
);

-- QUIZ_SCORES TABLE
-- Stores the scores for each skill category from the quiz
CREATE TABLE IF NOT EXISTS quiz_scores (
    user_id INTEGER PRIMARY KEY,
    Database_Fundamentals INTEGER,
    Computer_Architecture INTEGER,
    Distributed_Computing_Systems INTEGER,
    Cyber_Security INTEGER,
    Networking INTEGER,
    Development INTEGER,
    Programming_Skills INTEGER,
    Project_Management INTEGER,
    Computer_Forensics_Fundamentals INTEGER,
    Technical_Communication INTEGER,
    AI_ML INTEGER,
    Software_Engineering INTEGER,
    Business_Analysis INTEGER,
    Communication_Skills INTEGER,
    Data_Science INTEGER,
    Troubleshooting_Skills INTEGER,
    Graphics_Designing INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- QUESTIONS TABLE
-- Stores quiz questions with options and their respective weights
CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    option_A TEXT NOT NULL,
    option_B TEXT NOT NULL,
    option_C TEXT NOT NULL,
    option_D TEXT NOT NULL,
    weight_A INTEGER NOT NULL,
    weight_B INTEGER NOT NULL,
    weight_C INTEGER NOT NULL,
    weight_D INTEGER NOT NULL
);
