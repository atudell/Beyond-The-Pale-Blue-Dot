from secrets import token_hex
from hashlib import blake2b
from random import randint


# Create a class for security methods
class Secure:
    
    # Initialize the class with the username and password along with a key
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    # Method that returns a randomized salt as bytes
    def generateSalt(self, min_length = 32, max_length = 50):
        return token_hex(randint(min_length, max_length))

    # Method to mix the salt in the username and password
    def seasonInputs(self, salt, pepper):
        self.username = self.username + pepper 
        self.password = self.password + salt
    
    # Method to encrypt inputs
    def encryptInputs(self, n):
        
        # Encrypt once separately to get all the data types in order
        username = blake2b(self.username.encode("utf-8")).hexdigest()
        password = blake2b(self.password.encode("utf-8")).hexdigest()
        
        # Hash and rehash the username and password n times
        for i in range(n-1):
            username = blake2b(username.encode("utf-8")).hexdigest()
            password = blake2b(password.encode("utf-8")).hexdigest()
        
        return [username, password]
        
