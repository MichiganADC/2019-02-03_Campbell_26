# madc_helpers.py

# Import useful globals
from config import *

# Package(s) for REDCap API
import pycurl
from io import BytesIO
import certifi

import re
from collections import OrderedDict

import sys


#---------#---------#---------#---------#---------#---------#---------#---------
def rc_get_api_data(uri    = REDCAP_API_URI, 
                    token  = None, 
                    fields = "", 
                    forms  = "",
                    secure = True):
  '''
  Simple abstraction function for simplifying REDCAP API record export
  '''
  
  if token is None:
    sys.exit("Missing API token.")
  
  post_data = [
    ('token',                  (token)),
    ('content',                ('record')),
    ('format',                 ('json')),
    ('type',                   ('flat')),
    ('rawOrLabel',             ('raw')),
    ('rawOrLabelHeaders',      ('raw')),
    ('exportCheckboxLabel',    ('false')),
    ('exportSurveyFields',     ('false')),
    ('exportDataAccessGroups', ('false')),
    ('returnFormat',           ('json')),
    ('fields',                 (fields)),
    ('forms',                  (forms))
  ]
  
  buf = BytesIO()
  c = pycurl.Curl()
  
  # Set cURL options
  c.setopt(pycurl.CAINFO, certifi.where())
  c.setopt(pycurl.URL, REDCAP_API_URI)
  c.setopt(pycurl.HTTPPOST, post_data)
  c.setopt(c.WRITEFUNCTION, buf.write)
  c.setopt(c.SSL_VERIFYPEER, secure)
  # ^^^ UM MICHR REDCap server evidently can't verify local certificate
  #     from certain languages or platforms (Python Jupyter NB, Linux)
  
  c.perform()
  c.close()
  
  return(buf.getvalue())
  

#---------#---------#---------#---------#---------#---------#---------#---------
def get_ift_dups(field_names):
    '''
    Reduce UDS 3-derived IVP/FVP/TVP field names to just the IVP field names
    '''
    
    return(
        list(
            OrderedDict.fromkeys(
                [re.sub(r'^fu_|^tele_', '', f) for f in field_names]
            )
        )
    )

  
#---------#---------#---------#---------#---------#---------#---------#---------
def coalesce_ift_cols(df):
    '''
    Coalesce UDS 3-derived IVP/FVP/TVP fields, leaving only IVP fields
    '''
       
    # Get collapsible fields and the correpsonding
    # follow-up visit `fu_` and telephone visit `tele_` fields
    i_fields = get_ift_dups(df.columns)
    f_fields = ['fu_' + f for f in i_fields]
    t_fields = ['tele_' + f for f in i_fields]
    
    
    for i in range(len(i_fields)):
        if i_fields[i] in df.columns and \
        f_fields[i] in df.columns and \
        t_fields[i] in df.columns:
            df[i_fields[i]] = df[i_fields[i]].combine_first(
                df[f_fields[i]].combine_first(df[t_fields[i]])
            )
            df.drop(columns=[f_fields[i], t_fields[i]], inplace=True)
            
        elif i_fields[i] in df.columns and \
        f_fields[i] in df.columns and \
        t_fields[i] not in df.columns:
            df[i_fields[i]] = df[i_fields[i]].combine_first(df[f_fields[i]])
            df.drop(columns=[f_fields[i]], inplace=True)
        
        elif i_fields[i] in df.columns and \
        f_fields[i] not in df.columns and \
        t_fields[i] in df.columns:
            df[i_fields[i]] = df[i_fields[i]].combine_first(df[t_fields[i]])
            df.drop(columns=[t_fields[i]], inplace=True)
            
        elif i_fields[i] not in df.columns and \
        f_fields[i] in df.columns and \
        t_fields[i] in df.columns:
            df[i_fields[i]] = df[f_fields[i]].combine_first(df[t_fields[i]])
            df.drop(columns=[f_fields[i], t_fields[i]], inplace=True)
        
        elif i_fields[i] not in df.columns and \
        f_fields[i] in df.columns and \
        t_fields[i] not in df.columns:
            df[i_fields[i]] = df[f_fields[i]]
            df.drop(columns=[f_fields[i]], inplace=True)
        
        elif i_fields[i] not in df.columns and \
        f_fields[i] not in df.columns and \
        t_fields[i] in df.columns:
            df[i_fields[i]] = df[t_fields[i]]
            df.drop(columns=[t_fields[i]], inplace=True)
    
    return(df)
    