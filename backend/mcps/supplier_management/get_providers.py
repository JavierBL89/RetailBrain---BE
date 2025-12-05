from mcps.db.init_db import get_db_connection


def supplier_management_info():
    """
    Returns information about the Supplier Management module.
    """
    return {
        "module": "supplier_management",
        "description": "Module for listing providers and sending notification emails.",
        "functions": [
            "get_all_providers", "Get a list of all providers contact details"
            "get_provider_email", " Get a provider email address by provider id"
            "send_email_providers" "Send an product stcok reordering email to the given supplier using a predifined template."
        ]
    }


def get_all_providers() -> list[dict]:
    """
    Get a list of all providers
    """
    connection = None
    cursor = None
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cur:
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
    """
    Get a provider email address by provider id
    """
    providers = get_all_providers()
    for provider in providers:
        if provider["provider_id"] == provider_id:
            return {"email": provider["email"]}
    return {"error": "Provider not found"}


