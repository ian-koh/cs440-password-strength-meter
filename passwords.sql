-- Create the users table

CREATE TABLE
    users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );

-- Insert sample data into the users TABLE

#passwords are hashed with bcrypt
INSERT INTO
    users (username, password)
VALUES (
        'alice',
        '$2b$12$9n9uV7.o8k03pYV7TCw6cuFg6nJU6rGIfsONsO9XkXWJy8.uv4.1O'
    ), (
        'bob',
        '$2b$12$T/N/3F3mTKXzOgE.M8meYONJgQ2C1OxRnlqwHtJMy0t9AfQbGO7hK'
    ), (
        'charlie',
        '$2b$12$VhAzoRuZ1uNNTLe0hXOcHu7JgY.y3qyfnrtZY6LDD50mJlMB18Axi'
    );