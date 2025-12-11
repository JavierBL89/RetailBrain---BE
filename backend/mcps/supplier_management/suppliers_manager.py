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
            "send_email_providers", "Send an product stcok reordering email to the given supplier using a predifined template."
            "update_provider_details", "Update provider details dynamically based on provided fields"
        ]
    }


def get_all_providers() -> list[dict]:
    """
    Get a list of all providers
    """
    db_conn = get_db_connection()

    try:
        with db_conn.cursor() as cur:
            cur.execute("SELECT provider_id, name, email FROM providers")
            providers = cur.fetchall()
            return [{"provider_id": row[0], "name": row[1], "email": row[2]} for row in providers]
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if db_conn:
            db_conn.close()


def get_provider_email(provider_id: int) -> dict[str, str]:
    """
    Get a provider email address by provider id
    """
    providers = get_all_providers()
    for provider in providers:
        if provider["provider_id"] == provider_id:
            return {"email": provider["email"]}
    return {"error": "Provider not found"}


def update_provider_details(user_query: dict) -> dict:
    """
    Update provider details dynamically based on provided fields
    Expected user_query format:
    {
        "provider_id": 1,  # Required
        "name": "New Name",  # Optional
        "email": "new_email@example.com",  # Optional
        "description": "New description"  # Optional
    }
    """
    db_conn = get_db_connection()
    
    try:
        provider_id = user_query.get("provider_id")
        
        if not provider_id:
            return {"error": "provider_id is required"}
        
        # Build dynamic UPDATE query
        allowed_fields = ["name", "email", "description"]
        fields_to_update = {}
        
        for field in allowed_fields:
            if field in user_query and user_query[field] is not None:
                fields_to_update[field] = user_query[field]
        
        if not fields_to_update:
            return {"error": "No fields to update. Provide at least one of: name, email, description"}
        
        # Build SET clause dynamically
        set_clause = ", ".join([f"{field} = %s" for field in fields_to_update.keys()])
        values = list(fields_to_update.values())
        values.append(provider_id)  # Add provider_id for WHERE clause
        
        query = f"""
            UPDATE providers 
            SET {set_clause}, updated_at = NOW()
            WHERE provider_id = %s 
            RETURNING provider_id, name, email, description
        """
        
        with db_conn.cursor() as cur:
            cur.execute(query, values)
            updated = cur.fetchone()
            
            if not updated:
                return {"error": f"Provider with id {provider_id} not found"}
            
            db_conn.commit()
            
            return {
                "status": "success",
                "message": f"Provider updated successfully. Updated fields: {', '.join(fields_to_update.keys())}",
                "provider": {
                    "provider_id": updated[0],
                    "name": updated[1],
                    "email": updated[2],
                    "description": updated[3]
                }
            }
    
    except Exception as e:
        db_conn.rollback()
        print(f"An error occurred: {e}")
        return {"error": f"Failed to update provider: {str(e)}"}
    
    finally:
        if db_conn:
            db_conn.close()