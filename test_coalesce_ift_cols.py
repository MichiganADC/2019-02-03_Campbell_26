#---------#---------#---------#---------#---------#---------#---------#---------
# test_coalesce_ift_cols.py

import unittest
import pandas as pd
import numpy as np
from madc_helpers import coalesce_ift_cols

class TestCoalesceIftCols(unittest.TestCase):
  '''
  Test `coalesce_ift_cols` function in madc_helpers.py
  '''
  
  def test_coalesce_ift_cols(self):
    
    test_df = pd.DataFrame({'A':      [  1.,   2.,   3.,   4.],
                            'B':      [None, None,   3.,   4.],
                            'fu_B':   [  1.,   2., None, None],
                            'C':      [None, None,   3.,   4.],
                            'tele_C': [  1.,   2., None, None],
                            'D':      [None, None, None,   4.],
                            'fu_D':   [None, None,   3., None],
                            'tele_D': [  1.,   2., None, None],
                            'fu_E':   [  1.,   2.,   3.,   4.],
                            'tele_F': [  1.,   2.,   3.,   4.],
                            'fu_G':   [None, None,   3.,   4.],
                            'tele_G': [  1.,   2.,   3.,   4.]#,
                            # 'Z':      [None, None, None, None]
                           })
    
    targ_df = pd.DataFrame({'A':      [  1.,   2.,   3.,   4.],
                            'B':      [  1.,   2.,   3.,   4.],
                            'C':      [  1.,   2.,   3.,   4.],
                            'D':      [  1.,   2.,   3.,   4.],
                            'E':      [  1.,   2.,   3.,   4.],
                            'F':      [  1.,   2.,   3.,   4.],
                            'G':      [  1.,   2.,   3.,   4.]#,
                            # 'Z':      [None, None, None, None]
                           })
    
    res_df = coalesce_ift_cols(test_df)
    self.assertTrue(res_df.equals(targ_df))
    
if __name__ == '__main__':
  unittest.main()
