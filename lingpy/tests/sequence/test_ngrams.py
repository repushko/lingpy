# *-* coding: utf-8 *-*

from collections import Counter
from nose.tools import assert_raises
from unittest import TestCase

from lingpy.sequence.ngrams import get_n_ngrams, bigrams, \
    trigrams, fourgrams, get_all_ngrams, get_skipngrams, \
    get_posngrams, get_all_posngrams


"""
Tests for the ngrams module
"""

# Note on test implementation:
# we can't directly compare the reference list and the
# list of returned elements, as the lists might have
# different orders; we also cannot convert them to
# sets and compare the sets, as we would miss duplicates.
# The best solution is to make counters out of both lists
# and compare them (no problem as the iterator returns
# tuples, which are hasheable)

class Tests(TestCase):
    def setUp(self):
        pass

    def test_get_n_grams(self):
        # String and list sequences
        str_seq = "A B C"
        lst_seq = str_seq.split()

        # The length of the collections of 0-grams must be zero
        assert len(list(get_n_ngrams(str_seq, 0))) == 0
        assert len(list(get_n_ngrams(lst_seq, 0))) == 0

        # Test monogram (no padding)
        ref = Counter([('A',), ('B',), ('C',)])
        assert ref == Counter(get_n_ngrams(str_seq, 1))
        assert ref == Counter(get_n_ngrams(lst_seq, 1))

        # Test large n-gram with padding
        ref = Counter([('$', '$', '$', '$', 'A'),
                       ('$', '$', '$', 'A', 'B'),
                       ('$', '$', 'A', 'B', 'C'),
                       ('$', 'A', 'B', 'C', '$'),
                       ('A', 'B', 'C', '$', '$'),
                       ('B', 'C', '$', '$', '$'),
                       ('C', '$', '$', '$', '$')])
        assert ref == Counter(get_n_ngrams(str_seq, 5))
        assert ref == Counter(get_n_ngrams(lst_seq, 5))

    def test_bigrams(self):
        # String and list sequences
        str_seq = "A B C D E"
        lst_seq = str_seq.split()

        # Test with padding
        ref = Counter([('$', 'A'), ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', '$')])
        assert ref == Counter(bigrams(str_seq))
        assert ref == Counter(bigrams(lst_seq))

        # Test without padding
        ref = Counter([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')])
        assert ref == Counter(bigrams(str_seq, pad_symbol=None))
        assert ref == Counter(bigrams(lst_seq, pad_symbol=None))

    def test_trigrams(self):
        # String and list sequences
        str_seq = "A B C D E"
        lst_seq = str_seq.split()

        # Test with padding
        ref = Counter([('$', '$', 'A'),
                       ('$', 'A', 'B'),
                       ('A', 'B', 'C'),
                       ('B', 'C', 'D'),
                       ('C', 'D', 'E'),
                       ('D', 'E', '$'),
                       ('E', '$', '$')])
        assert ref == Counter(trigrams(str_seq))
        assert ref == Counter(trigrams(lst_seq))
        
        # Test without padding
        ref = Counter([('A', 'B', 'C'), ('B', 'C', 'D'), ('C', 'D', 'E')])
        assert ref == Counter(trigrams(str_seq, pad_symbol=None))
        assert ref == Counter(trigrams(lst_seq, pad_symbol=None))
        
    def test_fourgrams(self):
        # String and list sequences
        str_seq = "A B C D E"
        lst_seq = str_seq.split()
        
        # Test with padding
        ref = Counter([('$', '$', '$', 'A'),
                       ('$', '$', 'A', 'B'),
                       ('$', 'A', 'B', 'C'),
                       ('A', 'B', 'C', 'D'),
                       ('B', 'C', 'D', 'E'),
                       ('C', 'D', 'E', '$'),
                       ('D', 'E', '$', '$'),
                       ('E', '$', '$', '$')])
        assert ref == Counter(fourgrams(str_seq))
        assert ref == Counter(fourgrams(lst_seq))
        
        # Test without padding
        ref = Counter([('A', 'B', 'C', 'D'), ('B', 'C', 'D', 'E')])
        assert ref == Counter(fourgrams(str_seq, pad_symbol=None))
        assert ref == Counter(fourgrams(lst_seq, pad_symbol=None))
        
    def test_get_all_ngrams(self):
        # String and list sequences
        str_seq = "A B C"
        lst_seq = str_seq.split()
        
        # Test with no value for `orders`
        ref = Counter([('A',),
                       ('B',),
                       ('C',),
                       ('$', 'A'), 
                       ('A', 'B'),
                       ('B', 'C'),
                       ('C', '$'),
                       ('$', '$', 'A'),
                       ('$', 'A', 'B'),
                       ('A', 'B', 'C'),
                       ('B', 'C', '$'),
                       ('C', '$', '$')])
        assert ref == Counter(get_all_ngrams(str_seq))
        assert ref == Counter(get_all_ngrams(lst_seq))
        
        # Test with a list for `orders`
        ref = Counter([('A',),
                       ('B',),
                       ('C',),
                       ('$', '$', 'A'),
                       ('$', 'A', 'B'),
                       ('A', 'B', 'C'),
                       ('B', 'C', '$'),
                       ('C', '$', '$')])
        assert ref == Counter(get_all_ngrams(str_seq, orders=[1, 3]))
        assert ref == Counter(get_all_ngrams(lst_seq, orders=[1, 3]))
        
    def test_get_skipngrams(self):
        # String and list sequences
        str_seq = "A B C D"
        lst_seq = str_seq.split()
        
        # Test with no gaps and padding
        ref = Counter([('$', 'A'), ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', '$')])
        assert ref == Counter(get_skipngrams(str_seq, 2, 0))
        assert ref == Counter(get_skipngrams(lst_seq, 2, 0))
        
        # Test with no gaps and no padding
        ref = Counter([('A', 'B'), ('B', 'C'), ('C', 'D')])
        assert ref == Counter(get_skipngrams(str_seq, 2, 0, pad_symbol=None))
        assert ref == Counter(get_skipngrams(lst_seq, 2, 0, pad_symbol=None))
        
        # String and list sequences
        str_seq = "A B C D E"
        lst_seq = str_seq.split()
        
        # Test with gaps and single gap opening
        ref = Counter([('$', '$', 'A'),
                       ('$', 'A', 'B'),
                       ('A', 'B', 'C'),
                       ('B', 'C', 'D'),
                       ('C', 'D', 'E'),
                       ('D', 'E', '$'),
                       ('E', '$', '$'),
                       ('$', 'A', 'B'),
                       ('$', 'B', 'C'),
                       ('A', 'C', 'D'),
                       ('B', 'D', 'E'),
                       ('C', 'E', '$'),
                       ('D', '$', '$'),
                       ('$', '$', 'B'),
                       ('$', 'A', 'C'),
                       ('A', 'B', 'D'),
                       ('B', 'C', 'E'),
                       ('C', 'D', '$'),
                       ('D', 'E', '$'),
                       ('$', 'B', 'C'),
                       ('$', 'C', 'D'),
                       ('A', 'D', 'E'),
                       ('B', 'E', '$'),
                       ('C', '$', '$'),
                       ('$', '$', 'C'),
                       ('$', 'A', 'D'),
                       ('A', 'B', 'E'),
                       ('B', 'C', '$'),
                       ('C', 'D', '$')])
        assert ref == Counter(get_skipngrams(str_seq, 3, 2))
        assert ref == Counter(get_skipngrams(lst_seq, 3, 2))
        
        # Test with gaps and multiple gap openings
        ref = Counter([('$', '$', 'A'),
                       ('$', '$', 'B'),
                       ('$', '$', 'C'),
                       ('$', 'A', 'B'),
                       ('$', 'A', 'C'),
                       ('$', 'B', 'C'),
                       ('$', 'A', 'B'),
                       ('$', 'A', 'C'),
                       ('$', 'A', 'D'),
                       ('$', 'B', 'C'),
                       ('$', 'B', 'D'),       
                       ('$', 'C', 'D'),
                       ('A', 'B', 'C'),
                       ('A', 'B', 'D'),
                       ('A', 'B', 'E'),
                       ('A', 'C', 'D'),
                       ('A', 'C', 'E'),
                       ('A', 'D', 'E'),
                       ('B', 'C', 'D'),
                       ('B', 'C', 'E'),
                       ('B', 'C', '$'),
                       ('B', 'D', 'E'),
                       ('B', 'D', '$'),
                       ('B', 'E', '$'),
                       ('C', 'D', 'E'),
                       ('C', 'D', '$'),
                       ('C', 'D', '$'),
                       ('C', 'E', '$'),
                       ('C', 'E', '$'),
                       ('C', '$', '$'),
                       ('D', 'E', '$'),
                       ('D', 'E', '$'),
                       ('D', '$', '$'),
                       ('E', '$', '$')])      
        assert ref == Counter(get_skipngrams(str_seq, 3, 2, single_gap=False))
        assert ref == Counter(get_skipngrams(lst_seq, 3, 2, single_gap=False))

    def test_get_posngrams(self):
        # String and list sequences
        str_seq = "A B C D"
        lst_seq = str_seq.split()
        
        # Test with zero left and zero right length
        ref = Counter([(('###',), 'A', 0),
                       (('###',), 'B', 1),
                       (('###',), 'C', 2),
                       (('###',), 'D', 3)])
        assert ref == Counter(get_posngrams(str_seq, 0, 0))
        assert ref == Counter(get_posngrams(lst_seq, 0, 0))
        
        # Test with non-zero left and zero right length
        ref = Counter([(('$', '$', '###'), 'A', 0),
                       (('$', 'A', '###'), 'B', 1),
                       (('A', 'B', '###'), 'C', 2),
                       (('B', 'C', '###'), 'D', 3)])
        assert ref == Counter(get_posngrams(str_seq, 2, 0))
        assert ref == Counter(get_posngrams(lst_seq, 2, 0))
        
        # Test with zero left and non-zero right length
        ref = Counter([(('###', 'B', 'C'), 'A', 0),
                       (('###', 'C', 'D'), 'B', 1),
                       (('###', 'D', '$'), 'C', 2),
                       (('###', '$', '$'), 'D', 3)])
        assert ref == Counter(get_posngrams(str_seq, 0, 2))
        assert ref == Counter(get_posngrams(lst_seq, 0, 2))
        
        # Test with non-zero left and non-zero right length
        ref = Counter([(('$', '$', '###', 'B', 'C'), 'A', 0),
                       (('$', 'A', '###', 'C', 'D'), 'B', 1),
                       (('A', 'B', '###', 'D', '$'), 'C', 2),
                       (('B', 'C', '###', '$', '$'), 'D', 3)])
        assert ref == Counter(get_posngrams(str_seq, 2, 2))
        assert ref == Counter(get_posngrams(lst_seq, 2, 2))        
        
    def test_get_all_posngrams(self):
        # String and list sequences
        str_seq = "A B C"
        lst_seq = str_seq.split()
        
        # Test with ints as orders
        ref = Counter([(('###',), 'A', 0),
                       (('###',), 'B', 1),
                       (('###',), 'C', 2),
                       (('###', 'B'), 'A', 0),
                       (('###', 'C'), 'B', 1),
                       (('###', '$'), 'C', 2),
                       (('$', '###'), 'A', 0),
                       (('A', '###'), 'B', 1),
                       (('B', '###'), 'C', 2),
                       (('$', '###', 'B'), 'A', 0),
                       (('A', '###', 'C'), 'B', 1),
                       (('B', '###', '$'), 'C', 2),
                       (('$', '$', '###'), 'A', 0),
                       (('$', 'A', '###'), 'B', 1),
                       (('A', 'B', '###'), 'C', 2),
                       (('$', '$', '###', 'B'), 'A', 0),
                       (('$', 'A', '###', 'C'), 'B', 1),
                       (('A', 'B', '###', '$'), 'C', 2)])
        assert ref == Counter(get_all_posngrams(str_seq, 2, 1))
        assert ref == Counter(get_all_posngrams(lst_seq, 2, 1))
        
        # String and list sequences
        str_seq = "A B C D"
        lst_seq = str_seq.split()
        
        # Test with lists as orders
        ref = Counter([(('$', '$', '###', 'B'), 'A', 0),
                       (('$', 'A', '###', 'C'), 'B', 1),
                       (('A', 'B', '###', 'D'), 'C', 2),
                       (('B', 'C', '###', '$'), 'D', 3),
                       (('$', '$', '$', '###', 'B'), 'A', 0),
                       (('$', '$', 'A', '###', 'C'), 'B', 1),
                       (('$', 'A', 'B', '###', 'D'), 'C', 2),
                       (('A', 'B', 'C', '###', '$'), 'D', 3)])
        assert ref == Counter(get_all_posngrams(str_seq, [2, 3], [1]))
        assert ref == Counter(get_all_posngrams(lst_seq, [2, 3], [1]))
