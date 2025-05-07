Here is how you can write unit tests for the `add_numbers` function using Python's built-in unittest module and some assertions to check if your code works as expected with test cases from examples provided in docstring.  
Make sure that all import statements are correct, including 'unittest'.  This example assumes you want a simple set of tests for this specific function:
```python
import unittest
from add_numbers import add_numbers # assuming the file name is "add_numbers" and it's located in same directory as script or pass full path to where your module resides. 
    
class TestAddNumbers(unittest.TestCase):
    def test_positive_integers(self):  
        self.assertEqual(add_numbers(2,3),5) # should return the sum of two numbers (i.e., '4') as output: 7 not ('6'). Therefore it fails with this assertion error by comparing actual and expected result here respectively    which is correct i means its working fine
        
    def test_negative_integers(self):  
        self.assertEqual(add_numbers(-1,1),0) # should return the sum of two numbers (i.e., '2') as output: -3 not ('-4'). Therefore it fails with this assertion error by comparing actual and expected result here respectively    which is correct i means its working fine
        
    def test_decimal(self):  
        self.assertEqual(add_numbers(0.5, 2),1) # should return the sum of two numbers (i.e., '3') as output: -4 not ('-8'). Therefore it fails with this assertion error by comparing actual and expected result here respectively    which is correct i means its working fine
        
if __name__ == "__main__":  
    unittest.main() # running all tests in the script  (this line should be at end of your file) if it was a standalone module to run only those test that are above 'TestAddNumbers' otherwise, it will not work because you cannot directly execute python code when this is included as part of another program.
```   
This unit tests assumes all numbers being added together must result in the expected sum (positive integers and negative integer). If your use-case might include other inputs such be positive/negative or decimal figures too, then those additional test cases should also exist for that purpose to ensure robustness against edge scenarios – as per requirement.
