# madc_helpers.py

import re
from collections import OrderedDict

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
            df = df.drop(columns=[f_fields[i], t_fields[i]])
            
        elif i_fields[i] in df.columns and \
        f_fields[i] in df.columns and \
        t_fields[i] not in df.columns:
            df[i_fields[i]] = df[i_fields[i]].combine_first(df[f_fields[i]])
            df = df.drop(columns=[f_fields[i]])
        
        elif i_fields[i] in df.columns and \
        f_fields[i] not in df.columns and \
        t_fields[i] in df.columns:
            df[i_fields[i]] = df[i_fields[i]].combine_first(df[t_fields[i]])
            df = df.drop(columns=[t_fields[i]])
            
        elif i_fields[i] not in df.columns and \
        f_fields[i] in df.columns and \
        t_fields[i] in df.columns:
            df[i_fields[i]] = df[f_fields[i]].combine_first(df[t_fields[i]])
            df.drop(columns=[f_fields[i], t_fields[i]])
        
        elif i_fields[i] not in df.columns and \
        f_fields[i] in df.columns and \
        t_fields[i] not in df.columns:
            df[i_fields[i]] = df[f_fields[i]]
            df = df.drop(columns=[f_fields[i]])
        
        elif i_fields[i] not in df.columns and \
        f_fields[i] not in df.columns and \
        t_fields[i] in df.columns:
            df[i_fields[i]] = df[t_fields[i]]
            df = df.drop(columns=[t_fields[i]])
    
    return(df)
    