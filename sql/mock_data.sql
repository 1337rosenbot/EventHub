-- Drop and recreate the database
DROP DATABASE IF EXISTS event_hub_db;
CREATE DATABASE event_hub_db;
USE event_hub_db;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Create events table
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create attendees table
CREATE TABLE attendees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Users
INSERT INTO users (name, email, password_hash) VALUES
('Ada Lovelace', 'ada@aihub.com', 'hash1'),
('Alan Turing', 'alan@aihub.com', 'hash2'),
('Grace Hopper', 'grace@aihub.com', 'hash3'),
('Linus Torvalds', 'linus@aihub.com', 'hash4'),
('Elon Bot', 'elon@aihub.com', 'hash5'),
('GPT McAIface', 'gpt@aihub.com', 'hash6'),
('Tux Penguin', 'tux@aihub.com', 'hash7'),
('HAL 9000', 'hal@aihub.com', 'hash8'),
('Robo Copilot', 'copilot@aihub.com', 'hash9'),
('Neo Matrix', 'neo@aihub.com', 'hash10'),
('Trinity Code', 'trinity@aihub.com', 'hash11'),
('Morpheus Dream', 'morpheus@aihub.com', 'hash12'),
('Sudo King', 'sudo@aihub.com', 'hash13'),
('Kernel Panic', 'kernel@aihub.com', 'hash14'),
('Tensor Flow', 'tensor@aihub.com', 'hash15'),
('Py Torch', 'py@aihub.com', 'hash16'),
('Julia Lang', 'julia@aihub.com', 'hash17'),
('Rusty Crab', 'rusty@aihub.com', 'hash18'),
('Cee Plus', 'cee@aihub.com', 'hash19'),
('Ada Byte', 'adabyte@aihub.com', 'hash20'),
('Bit Flip', 'bit@aihub.com', 'hash21'),
('Null Pointer', 'null@aihub.com', 'hash22'),
('Seg Fault', 'seg@aihub.com', 'hash23'),
('Stack Overflow', 'stack@aihub.com', 'hash24'),
('Heap Sprayer', 'heap@aihub.com', 'hash25'),
('Quantum Leap', 'quantum@aihub.com', 'hash26'),
('Logic Gate', 'logic@aihub.com', 'hash27'),
('Crypto Miner', 'crypto@aihub.com', 'hash28'),
('Pixel Pusher', 'pixel@aihub.com', 'hash29'),
('Cache Miss', 'cache@aihub.com', 'hash30');

-- Events
INSERT INTO events (user_id, name, date, location, description) VALUES
(1, 'AI Meme Hackathon', '2025-05-10', 'Discord', 'Compete to create the funniest AI memes.'),
(2, 'Neural Network Bake-Off', '2025-05-15', 'Zoom', 'Who can build the tastiest neural net?'),
(3, 'Quantum Computing Karaoke', '2025-05-20', 'Club Qubit', 'Sing your favorite quantum algorithms.'),
(4, 'Linux Kernel Panic Party', '2025-05-25', 'IRC', 'Celebrate the best kernel panics.'),
(5, 'GPT-4.1 Standup Night', '2025-05-30', 'Comedy Cellar', 'AI-generated standup comedy.'),
(6, 'Retro Game AI Jam', '2025-06-01', 'Twitch', 'Build AIs to play retro games.'),
(7, 'Robot Dance Off', '2025-06-05', 'Main Hall', 'Robots and humans compete in dance.'),
(8, 'AI Art & Code Gallery', '2025-06-10', 'Virtual Gallery', 'Showcase AI-generated art and code.'),
(9, 'Data Science Speed Dating', '2025-06-15', 'Meetup.com', 'Find your data soulmate.'),
(10, 'Turing Test Trivia', '2025-06-20', 'Pub Quiz', 'Can you outsmart the AI?');

-- Attendees (randomly assigned)
INSERT INTO attendees (event_id, user_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 10), (1, 15),
(2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
(3, 9), (3, 10), (3, 11), (3, 12), (3, 13),
(4, 14), (4, 15), (4, 16), (4, 17), (4, 18),
(5, 19), (5, 20), (5, 21), (5, 22), (5, 23),
(6, 24), (6, 25), (6, 26), (6, 27), (6, 28),
(7, 29), (7, 30), (7, 1), (7, 2), (7, 3),
(8, 4), (8, 5), (8, 6), (8, 7), (8, 8),
(9, 9), (9, 10), (9, 11), (9, 12), (9, 13),
(10, 14), (10, 15), (10, 16), (10, 17), (10, 18);