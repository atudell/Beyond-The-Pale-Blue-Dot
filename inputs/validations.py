# Create a class whose methods are dedicated to validating inputs
class Input:
    
    # Initialize object with a string
    def __init__(self, string):
           self.string = string
    
    # Method to determine if the characters in a string are valid ASCII
    def isAscii(self):
        for char in self.string:
            # if the integer value of the character is between 0-127, its part of the standard ASCII set
            # This might be too restrictive, but should cover most cases
            if not 0 <= ord(char) <= 127:
                return False
        
        # If none of the values return false, the string must have only ASCII characters
        return True
                
    # Method to determine if the string is too long
    def isCorrectLength(self, min_length, max_length):
        
        # If the length of string is greater than the min but less than the max (inclusive), return true
        if min_length <= len(self.string) <= max_length:
            return True
        else:
            return False
        
    # Since the variable types aren't strictly defined, it's possible a non-string gets passes as the string attribute
    # Consequently, this method will check and convert accordingly
    def checkDataType(self):
        if type(self.string) != str:
            self.string = str(self.string)
            