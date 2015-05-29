# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:00:13 2014

@author: adrian
"""

import json

class TagMan():
    def __init__(self):
        pass
    
    # encode
    def e(self, tagGroup):
        # sort tag tree recursively 
        return json.dumps( sorted( tagGroup ) )
        
    # decode
    def d(self, tagString):
        return json.loads(tagString)
    
    # match
    # return all the strings that match the specified tags
    # if only a tag type is specified, then any string containing that tag is ok, but must have that tag
    # if a value is also specified, then value must match too
    def m(self, searchTagList, encodedStrings):
        resultStrings = []
        for s in encodedStrings:
            try:
                td = dict(self.d(s))

                current_match = True
                for searchTag in searchTagList:
                    if isinstance(searchTag, (list, tuple)):
                        if td.get(searchTag[0], None) == searchTag[1]:
                            pass
                        else:
                            current_match = False
                            
                    else:
                        if td.has_key(searchTag):
                            pass
                        else:
                            current_match = False
                        
                        
                if current_match is True:
                    resultStrings.append(s)

            except:
                print "not an encoded tag list"

                
        return resultStrings
    
