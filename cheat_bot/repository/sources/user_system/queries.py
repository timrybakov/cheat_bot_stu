CREATE_USER_MATERIAL_QUERY = """
INSERT INTO users(
    telegram_id,
    username,
    file_path,
    image_id,
    academy_year,
    file_id
) VALUES (
    :telegram_id,
    :username,
    :file_path,
    :image_id,
    :academy_year,
    :file_id
)
"""

FETCH_FIRST_QUERY = """
    SELECT 
        id,
        telegram_id,
        username,
        file_path,
        image_id,
        academy_year,
        file_id 
    FROM users
    ORDER BY users.id ASC LIMIT 1
"""

DELETE_USER_MATERIAL_QUERY = """
DELETE FROM users
WHERE id=:id
"""