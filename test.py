# -*- coding: utf-8 -*-
import pickle
import unittest

import categories
import confusables

is_good = u'Allo'
looks_good = is_good.replace(u'A', u'Α')

latin_a = u'A'
greek_a = u'Α'


class TestCategories(unittest.TestCase):
    def test_generated(self):
        with open('categories.pkl', 'r') as file:
            categories_data = pickle.load(file)
        self.assertEqual(type(categories_data), type({}))

    def test_aliases_categories(self):
        self.assertEqual(categories.aliases_categories(latin_a), (
            categories.alias(latin_a), categories.category(latin_a)))
        self.assertEqual(categories.aliases_categories(greek_a), (
            categories.alias(greek_a), categories.category(greek_a)))

    def test_alias(self):
        self.assertEqual(categories.alias(latin_a), 'LATIN')
        self.assertEqual(categories.alias(greek_a), 'GREEK')

    def test_category(self):
        self.assertEqual(categories.category(latin_a), 'L')
        self.assertEqual(categories.category(greek_a), 'L')

    def test_unique_aliases(self):
        self.assertEqual(categories.unique_aliases(is_good), set(['LATIN']))
        self.assertEqual(categories.unique_aliases(looks_good), set(['GREEK', 'LATIN']))


class TestConfusables(unittest.TestCase):
    def test_generated(self):
        with open('confusables.pkl', 'r') as file:
            confusables_matrix = pickle.load(file)
        self.assertEqual(type(confusables_matrix), type({}))

    def test_is_mixed_script(self):
        self.assertTrue(confusables.is_mixed_script(looks_good))
        self.assertTrue(confusables.is_mixed_script(u' ρττ a'))

        self.assertFalse(confusables.is_mixed_script(is_good))
        self.assertFalse(confusables.is_mixed_script(u'ρτ.τ'))
        self.assertFalse(confusables.is_mixed_script(u'ρτ.τ '))

    def test_is_confusable(self):
        greek = confusables.is_confusable(looks_good)
        self.assertEqual(greek[0]['character'], '\xce\x91')
        self.assertIn(('A', 'LATIN CAPITAL LETTER A'), greek[0]['homoglyphs'])
        latin = confusables.is_confusable(is_good, preferred_aliases=['latin'])
        self.assertFalse(latin)

        # stop at first confusable character
        self.assertEqual(len(confusables.is_confusable(u'Αlloρ', greedy=False)), 1)
        # find all confusable characters
        # Α (greek), l, o, and ρ can be confused with other unicode characters
        self.assertEqual(len(confusables.is_confusable(u'Αlloρ', greedy=True)), 4)
        # Only Α (greek) and ρ (greek) can be confused with a latin character
        self.assertEqual(
            len(confusables.is_confusable(u'Αlloρ', greedy=True, preferred_aliases=['latin'])), 2)

        # for "Latin" readers, ρ is confusable!    ↓
        confusable = confusables.is_confusable(u'paρa', preferred_aliases=['latin'])[0]['character']
        self.assertEqual(confusable, unicode.encode(u'ρ', 'utf-8'))
        # for "Greek" readers, p is confusable!  ↓
        confusable = confusables.is_confusable(u'paρa', preferred_aliases=['greek'])[0]['character']
        self.assertEqual(confusable, 'p')

    def test_dangerous(self):
        self.assertTrue(confusables.is_dangerous(looks_good))
        self.assertTrue(confusables.is_dangerous(u' ρττ a'))
        self.assertTrue(confusables.is_dangerous(u'ρττ a'))
        self.assertTrue(confusables.is_dangerous(u'Alloτ'))
        self.assertTrue(confusables.is_dangerous(u'www.micros﻿оft.com'))
        self.assertTrue(confusables.is_dangerous(u'www.Αpple.com'))
        self.assertTrue(confusables.is_dangerous(u'www.faϲebook.com'))
        self.assertFalse(confusables.is_dangerous(is_good))
        self.assertFalse(confusables.is_dangerous(u' ρτ.τ'))
        self.assertFalse(confusables.is_dangerous(u'ρτ.τ'))

if __name__ == '__main__':
    unittest.main()
