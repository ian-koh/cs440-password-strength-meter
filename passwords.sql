CREATE TABLE
    users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        last_password_change_date DATE NOT NULL
    );

INSERT INTO
    users (
        username,
        password_hash,
        last_password_change_date
    )
VALUES (
        'alice',
        '$2b$12$WYKPmQJHtckb0n1BZYJ5IeVGCVF3qJx.fkJlSzm2j8WbBLlrOvdcG',
        '2022-03-01'
    ), (
        'bob',
        '$2b$12$zJXe8LYSPfnzj2w0ZM5zZuJKsWfJ.nptl0xwbDdsG9jEEhF1n51dG',
        '2022-03-02'
    ), (
        'charlie',
        '$2b$12$yU6rM8eY67uOCqCUwN7Zfu2zRr7VuzhylOXYp7eUaMc6EHtyYl3Oq',
        '2022-03-05'
    );