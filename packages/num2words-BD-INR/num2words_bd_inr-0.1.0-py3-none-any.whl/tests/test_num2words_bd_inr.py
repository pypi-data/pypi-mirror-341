
import unittest
from num2words_bd_inr import amount_in_words

class TestNum2WordsBdInr(unittest.TestCase):
    """Test cases for the num2words_bd_inr package."""
    
    def test_basic_conversion(self):
        """Test basic conversion functionality."""
        result = amount_in_words(1234.56, 'INR', 'en')
        self.assertIn("One Thousand Two Hundred Thirty Four", result)
        self.assertIn("Rupees", result)
        self.assertIn("Fifty Six", result)
        self.assertIn("Paisa", result)
    
    def test_rounding(self):
        """Test rounding functionality."""
        result = amount_in_words(1234.56, 'BDT', 'en', rounding=True)
        self.assertIn("One Thousand Two Hundred Thirty Five", result)
        self.assertIn("Taka", result)
        self.assertNotIn("Paisa", result)
    
    def test_remove_fraction(self):
        """Test removing fractional part."""
        result = amount_in_words(1234.56, 'USD', 'en', rem_fraction=True)
        self.assertIn("One Thousand Two Hundred Thirty Four", result)
        self.assertIn("Dollars", result)
        self.assertNotIn("Cents", result)
    
    def test_text_styling(self):
        """Test text styling options."""
        # Test title style
        result = amount_in_words(1234.56, 'EUR', 'en', title_style=True)
        words = result.split()
        for word in words:
            if len(word) > 0:
                self.assertTrue(word[0].isupper())
        
        # Test cap style
        result = amount_in_words(1234.56, 'EUR', 'en', cap_style=True)
        self.assertTrue(result[0].isupper())
    
    def test_prefix_suffix(self):
        """Test prefix and suffix functionality."""
        prefix = "Only"
        suffix = "Only"
        result = amount_in_words(1234.56, 'GBP', 'en', prefix_val=prefix, subfix_val=suffix)
        self.assertTrue(result.startswith(prefix))
        self.assertTrue(result.strip().endswith(suffix))
    
    def test_separators(self):
        """Test separator functionality."""
        # Test int separator
        result = amount_in_words(1234.56, 'USD', 'en', int_sep=",")
        self.assertIn(",", result)
    
    def test_indian_rupees(self):
        """Test specifically for Indian Rupees (INR)."""
        result = amount_in_words(2500.75, 'INR', 'en')
        self.assertIn("Rupees", result)
        self.assertIn("Paisa", result)
    
    def test_bangladeshi_taka(self):
        """Test specifically for Bangladeshi Taka (BDT)."""
        result = amount_in_words(2500.75, 'BDT', 'en')
        self.assertIn("Taka", result)
        self.assertIn("Paisa", result)


if __name__ == '__main__':
    unittest.main()