import bcrypt

salt = bytes('$2b$12$E2XnwBQaOz.N8.dZ127XJukXPZts/GhJCD3/c5tfGcDpXSrBb5Piq'.encode('utf-8'))

def create_password_hash(password : str) -> str: 
    return bcrypt.hashpw(password.encode('utf-8'), salt=salt)

def check_password_hash(password, hash_password) -> bool: 
    return bcrypt.checkpw(password=password, hashed_password=hash_password)
    
if __name__ == '__main__':
    strc = 'string'
    hash_str = create_password_hash(strc)
    print(hash_str)
    print(check_password_hash('string'.encode('utf-8'), hash_str))