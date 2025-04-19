import unittest

from pseudomatic import pseudonym


class TestPseudomatic(unittest.TestCase):
    def test_pseudonym_generation(self):
        # Test that the same seed produces the same pseudonym
        seed = "test-seed"
        result1 = pseudonym(seed)
        result2 = pseudonym(seed)
        self.assertEqual(result1, result2)

    def test_different_seeds(self):
        # Test that different seeds produce different pseudonyms
        seed1 = "test-seed-1"
        seed2 = "test-seed-2"
        result1 = pseudonym(seed1)
        result2 = pseudonym(seed2)
        self.assertNotEqual(result1, result2)

    def test_language_support(self):
        # Test English language
        seed = "test-seed"
        en_result = pseudonym(seed, language="en")
        self.assertIsInstance(en_result, str)
        self.assertTrue(len(en_result) > 0)

        # Test Ukrainian language
        ua_result = pseudonym(seed, language="ua")
        self.assertIsInstance(ua_result, str)
        self.assertTrue(len(ua_result) > 0)

        # Test that different languages produce different results
        self.assertNotEqual(en_result, ua_result)

    def test_theme_support(self):
        # Test different themes
        seed = "test-seed"
        default_result = pseudonym(seed, theme="default")
        business_result = pseudonym(seed, theme="business")
        retail_result = pseudonym(seed, theme="retail")

        # Test that different themes produce different results
        self.assertNotEqual(default_result, business_result)
        self.assertNotEqual(default_result, retail_result)
        self.assertNotEqual(business_result, retail_result)

    def test_invalid_language(self):
        # Test that an invalid language raises a ValueError
        with self.assertRaises(ValueError):
            pseudonym("test-seed", language="invalid")

    def test_no_seed_provided(self):
        # Test that calling pseudonym() without a seed returns a non-empty string
        result = pseudonym()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

        # Test that calling pseudonym() with an empty string also generates a pseudonym
        result_empty = pseudonym("")
        self.assertIsInstance(result_empty, str)
        self.assertTrue(len(result_empty) > 0)

    def test_random_pseudonyms_are_different(self):
        # Test that calling pseudonym() multiple times returns different pseudonyms
        result1 = pseudonym()
        result2 = pseudonym()
        self.assertNotEqual(result1, result2)

        # Test with different languages
        en_result = pseudonym(language="en")
        ua_result = pseudonym(language="ua")
        self.assertNotEqual(en_result, ua_result)

        # Test with different themes
        default_result = pseudonym(theme="default")
        business_result = pseudonym(theme="business")
        retail_result = pseudonym(theme="retail")
        self.assertNotEqual(default_result, business_result)
        self.assertNotEqual(default_result, retail_result)
        self.assertNotEqual(business_result, retail_result)

if __name__ == "__main__":
    unittest.main()
