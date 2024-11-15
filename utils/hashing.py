import bcrypt

# Hash a password using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# Verify a password against a hash
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
