CREATE TABLE promouters (
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL
);

CREATE TABLE events (
    name VARCHAR(255) PRIMARY KEY,
    nm_prime VARCHAR(255),
    nm_usual VARCHAR(255)
);

CREATE TABLE tickets (
    ticket_number VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    ticket_type VARCHAR(50) NOT NULL CHECK (ticket_type IN ('Prime', 'Usual')),
    event_name VARCHAR(255) REFERENCES events(name) ON DELETE CASCADE
);
