def user_sch(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
            }

def users_schema(users) -> list:
    return [user_sch(user) for user in users]
        