import bcrypt

password = input()
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())