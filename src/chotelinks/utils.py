import random
import string

# Generate random string
def code_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Create a short code for an object
def create_shortcode(instance, size=6):
    new_code = code_generator(size=size)
    Klass = instance.__class__
    alreadyExists = Klass.objects.filter(short_code=new_code).exists()
    if alreadyExists:
        return create_shortcode(instance, size=size)
    return new_code
