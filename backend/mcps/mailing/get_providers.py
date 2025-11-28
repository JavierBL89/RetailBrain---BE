from mcps.db.init_db import get_db_connection

def get_providers() -> list[dict]:
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT provider_id, name, email FROM providers")
        providers = cursor.fetchall()
        return [{"provider_id": row[0], "name": row[1], "email": row[2]} for row in providers]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_provider_email(provider_id: int) -> dict[str, str]:
    providers = get_providers()
    for provider in providers:
        if provider["provider_id"] == provider_id:
            return {"email": provider["email"]}
    return {"error": "Provider not found"}


