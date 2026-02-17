import random

def pick_winner(users: dict[int, int]) -> int | None:
    """
    users: `{user_id: chance}`
    Returns winner `user_id` or `None`.
    """

    if not users:
        return None

    user_ids = list(users.keys())
    weights = list(users.values())

    return random.choices(user_ids, weights=weights, k=1)[0]