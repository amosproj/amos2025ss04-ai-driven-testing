import string

class Testclass:
    def __init__(self):
        self.alphabet = string.digits + string.ascii_uppercase
        
    def setUp(self):
        pass  # For testing purposes
    
    def test_convert_to_base64(self, value):
        if isinstance(value, str):
            encoded = self.encode_to_base64(value)
        else:
            encoded = value
        return encoded
            
    def test_to_base(self, num, base):
        if num < 0 or base <= 1:
            raise ValueError("Base must be greater than 1 and non-negative.")
        
        try:
            result = self._to_base(num, base)
            return result
        except ZeroDivisionError as e:
            raise ValueError("Number cannot be divided by zero.") from e
            
    def test_to_base_64(self):
        for value in ["abc", "def"]:
            if isinstance(value, str):
                encoded = self.encode_to_base64(value)
            else:
                encoded = value
            self.assertEqual(encoded, "ABC")

# Convert to base 64 using the alphabet string
def encode_to_base64(text: str) -> str:
    result = ""
    for c in text:
        if c >= '0' and c <= '9':
            result += string.digits[c - '0']
        elif c >= 'A' and c <= 'Z':
            result += self.alphabet.index(c)
        else:
            raise ValueError(f"Invalid character: {c}")
    return result

# Convert to base using the alphabet string
def convert_to_base(num: int, base: int) -> str:
    if num < 0 or base <= 1:
        raise ValueError("Base must be greater than 1 and non-negative.")
    
    try:
        while num > 0:
            remainder = num % base
            num = num // base
            result = self.alphabet[remainder] + result
        return result