import random
import string


def generate_random_string(length):
    import random
    import string
    # Select characters from letters and digits
    characters = string.ascii_letters + string.digits
    # Generate random string
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
