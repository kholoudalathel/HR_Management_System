# Check if a user belongs to a specific group.

def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()