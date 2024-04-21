meta = {
    "summary": "Gets user by ID",
    "description": "Retrieves user information for a given user ID.",
    "tags": ["User Management"]
}


async def handler(user_id: str):
    return {
        "user": user_id
    }
