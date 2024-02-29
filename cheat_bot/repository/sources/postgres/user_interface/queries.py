CREATE_USER_MATERIAL_QUERY = """
INSERT INTO users(user_telegram_id, username, file_path, image_id, bucket, file_unique_id)
VALUES (:user_telegram_id, :username, :file_path, :image_id, :bucket, :file_unique_id)
"""

FETCH_FIRST_QUERY = """
SELECT id, user_telegram_id, username, file_path, image_id, bucket, file_unique_id 
FROM users ORDER BY users.id ASC LIMIT 1
"""

DELETE_USER_MATERIAL_QUERY = """
DELETE FROM users WHERE id=:id
"""