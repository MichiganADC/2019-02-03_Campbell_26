#---------#---------#---------#---------#---------#---------#---------#---------
# test_get_ift_dups.py

import unittest
from madc_helpers import get_ift_dups

class TestGetIftDups(unittest.TestCase):
  '''
  Test `get_ift_dups` function in madc_helpers.py
  '''
  
  def test_get_ift_dups(self):
    
    test_list_0 = []                            # => []
    test_list_1 = ['']                          # => ['']
    test_list_2 = ['foo']                       # => ['foo']
    test_list_3 = ['foo', 'fu_foo']             # => ['foo']
    test_list_4 = ['foo', 'tele_foo']           # => ['foo']
    test_list_5 = ['foo', 'fu_foo', 'tele_foo'] # => ['foo']
    test_list_6 = ['fu_foo']                    # => ['foo']
    test_list_7 = ['tele_foo']                  # => ['foo']
    test_list_8 = ['fu_foo', 'tele_foo']        # => ['foo']
    test_list_9 = \
    ['foo', 'bar', 'baz', 'fu_bar', 'tele_baz', 'fu_qux', 'tele_qux']
    # => ['foo', 'bar', 'baz', 'qux']
    
    res_0 = get_ift_dups(test_list_0)
    res_1 = get_ift_dups(test_list_1)
    res_2 = get_ift_dups(test_list_2)
    res_3 = get_ift_dups(test_list_3)
    res_4 = get_ift_dups(test_list_4)
    res_5 = get_ift_dups(test_list_5)
    res_6 = get_ift_dups(test_list_6)
    res_7 = get_ift_dups(test_list_7)
    res_8 = get_ift_dups(test_list_8)
    res_9 = get_ift_dups(test_list_9)
    
    self.assertEqual(res_0, [])
    self.assertEqual(res_1, [''])
    self.assertEqual(res_2, ['foo'])
    self.assertEqual(res_3, ['foo'])
    self.assertEqual(res_4, ['foo'])
    self.assertEqual(res_5, ['foo'])
    self.assertEqual(res_6, ['foo'])
    self.assertEqual(res_7, ['foo'])
    self.assertEqual(res_8, ['foo'])
    self.assertEqual(res_9, ['foo', 'bar', 'baz', 'qux'])

if __name__ == '__main__':
  unittest.main()
