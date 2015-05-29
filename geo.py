import pandas as pd
import numpy as np
import re

class GEOMatrix():
    def __init__(self, title, annotations, covars, data, description):
        self.title = title
        self.annotations = annotations
        self.covars = covars
        self.data = data
        self.description = description
        
        

def parseGEOmatrixMetadata(f, characteristicSep, charLabelSep, description):
    annotations = {}
    covariatesArray = []
    covariatesIndex = []


    dataIndex = []
    dataLines = []

    hitData = False


    def parseSampleCharacteristicData(s):
        """ parse data for a single sample """
        cRecs = []
        # hack for hodges datasets 
        s = s.replace("CN ", "CN, ")
        for charNum, characteristic in enumerate( re.split(characteristicSep, s) ):
            parsedC = re.split(charLabelSep, characteristic.replace('"', ''))
            # print parsedC
            if len(parsedC) > 2:
                cRecs.append(map(lambda x: x.rstrip().lstrip(), parsedC[-2:]))
            elif len(parsedC) == 2:
                cRecs.append(map(lambda x: x.rstrip().lstrip(), parsedC))
            else:
                cRecs.append(("sampleChar_%d" % charNum, parsedC[0].lstrip().rstrip()))
        
        return pd.Series(dict(cRecs))
    
    
    
    for l in f:
        fields = l.rstrip().replace('"','').split("\t")
        
        if not hitData:
            if fields[0] == "!series_matrix_table_begin":
                hitData = True
            if len(fields) == 2:
                annotations[fields[0][1:]] = fields[1]
            if len(fields) > 2:
                if fields[0] == "!Sample_characteristics_ch1":
                    # nested fields may be separated by either ; or ,
                    characteristics = pd.DataFrame(map(parseSampleCharacteristicData, fields[1:])).transpose()
                else:
                    covariatesIndex.append(fields[0][1:])
                    covariatesArray.append(fields[1:])

        else:
            if fields[0] == "ID_REF":
                dataColumnNames = fields[1:]
            else:       
                if fields[0] != "!series_matrix_table_end":
                    dataIndex.append(fields[0])
                    dataLines.append(fields[1:])
                

    covars = pd.concat([characteristics, pd.DataFrame(covariatesArray, index=covariatesIndex)])
    covars.columns = covars.ix["Sample_geo_accession", :]
    gd = GEOMatrix( title = annotations["Series_geo_accession"],
                    annotations = annotations,
                    covars = covars,
                    data = pd.DataFrame(data=dataLines, index=dataIndex, 
                                 columns=dataColumnNames, 
                                         dtype=np.float),
                    description = description
                    )

    return gd
            

