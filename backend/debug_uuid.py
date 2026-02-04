import uuid

# Simulate the issue
user_id_from_db = uuid.UUID('c9168fe7-c099-423f-a4e4-a7ccaf2a9243')  # This is from DB as UUID object
user_id_from_url = 'c9168fe7-c099-423f-a4e4-a7ccaf2a9243'  # This is from URL as string

print(f"DB UUID: {user_id_from_db} (type: {type(user_id_from_db)})")
print(f"URL String: {user_id_from_url} (type: {type(user_id_from_url)})")
print(f"Are they equal? {user_id_from_db == user_id_from_url}")
print(f"What happens when we convert string to UUID? {user_id_from_db == uuid.UUID(user_id_from_url)}")