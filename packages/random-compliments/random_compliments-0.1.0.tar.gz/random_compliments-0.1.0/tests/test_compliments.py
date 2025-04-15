"""
Tests for the random_compliments package.
Written with the enthusiasm of someone writing documentation for a toaster.
"""

import unittest
from unittest.mock import patch

from random_compliments.compliments import get_compliment, shower_compliments, COMPLIMENTS

class TestCompliments(unittest.TestCase):
    """
    Tests that ensure our compliments work as advertised.
    Like crash-testing a pillow - important but ridiculous.
    """
    
    def test_get_compliment_returns_string(self):
        """
        Test that get_compliment returns a string.
        The bar is so low it's practically underground.
        """
        compliment = get_compliment()
        self.assertIsInstance(compliment, str)
        self.assertTrue(len(compliment) > 0)  # Ensuring it's not an empty string, like my soul
    
    def test_get_compliment_returns_valid_compliment(self):
        """
        Test that get_compliment returns a valid compliment.
        Like checking if water is wet - obvious but necessary.
        """
        compliment = get_compliment()
        self.assertIn(compliment, COMPLIMENTS)
    
    @patch('random.choice')
    def test_get_compliment_uses_random_choice(self, mock_choice):
        """
        Test that get_compliment uses random.choice.
        Making sure our randomness isn't as predictable as my weekend plans.
        """
        mock_choice.return_value = "Test compliment"
        compliment = get_compliment()
        
        mock_choice.assert_called_once_with(COMPLIMENTS)
        self.assertEqual(compliment, "Test compliment")
    
    def test_shower_compliments_returns_list(self):
        """
        Test that shower_compliments returns a list.
        As if the function name wasn't descriptive enough.
        """
        compliments = shower_compliments(3)
        self.assertIsInstance(compliments, list)
        self.assertEqual(len(compliments), 3)
    
    def test_shower_compliments_respects_count(self):
        """
        Test that shower_compliments respects the count parameter.
        Like respecting someone's boundaries - a novel concept.
        """
        for count in range(1, 6):
            compliments = shower_compliments(count)
            self.assertEqual(len(compliments), count)
    
    def test_shower_compliments_handles_large_count(self):
        """
        Test that shower_compliments handles large counts.
        Like testing if your bank account can handle your shopping habits.
        """
        # Test with a count larger than the number of compliments
        compliments = shower_compliments(1000)
        self.assertEqual(len(compliments), len(COMPLIMENTS))
        
        # Make sure all compliments are unique
        self.assertEqual(len(compliments), len(set(compliments)))
    
    def test_all_compliments_are_strings(self):
        """
        Test that all compliments in COMPLIMENTS are strings.
        Because occasionally someone tries to sneak in an integer and ruin the party.
        """
        for compliment in COMPLIMENTS:
            self.assertIsInstance(compliment, str)
            self.assertTrue(len(compliment) > 0)

if __name__ == '__main__':
    # Running these tests is like checking if your parachute works before skydiving
    # Except the penalty for failure is just mild embarrassment
    unittest.main() 