# Validation helpers

def validate_password(password):
    if len(password) < 8:
        return "Password must contain at least  8 characters."

    if len(password) > 20:
        return "Password must contain at most 20 characters."

    if not any(character.isupper() for character in password):
        return "Password must contain at least an uppercase letter."
    
    if not any(character.isdigit() for character in password):
        return "Password must contain a digit."
    
    return None
    