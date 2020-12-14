import json
import os
import json
from configparser import ConfigParser

import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances

from xml import cXml

DATA_DIR = './'

def load_df(xmlpath='name.xml'):
    """
    source: borrowed to kaggle competition gstore
    """

    sKeys = read_config("XML", "keys")
    # print(sKeys)
    oXml = cXml(xmlpath)
    arKeys = sKeys.split(",")
    # iIndex = 0
    AllStatements = []
    for key in arKeys:

        sStatement = oXml.ReadNode("//" + key + "/StepDefinition/@Statement")
        sExternalData = oXml.ReadNode("//" + key + "/StepDefinition/@ExternalData")
        sInstructions = oXml.ReadNode("//" + key + "/StepDefinition/@Instructions")
        iIndex = 0
        for value in sStatement:
            Statements = []
            Statements.append(sStatement[iIndex])
            Statements.append(sExternalData[iIndex])
            Statements.append(sInstructions[iIndex])
            Statements.append(iIndex)
            AllStatements.append(Statements)
            # print(sStatement[iIndex])
            iIndex = iIndex + 1

    # print(AllStatements)
    df = pd.DataFrame(AllStatements, columns=['Text', 'ExternalData', 'Instructions',
                                                   'Index'])
    # print(df.shape)
    # print(df)
    return df


def read_config(sCollection, sKey):
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")
    userinfo = config_object[sCollection]
    return userinfo[sKey]

def splitDataFrameList(df,target_column,separator):
    
    ''' 
    source: https://gist.github.com/jlln/338b4b0b55bd6984f883 modified to keep punctuation
    df = dataframe to split,
    target_column = the column containing the values to split
    separator = the symbol used to perform the split
    returns: a dataframe with each entry for the target column separated, with each element moved into a new row. 
    The values in the other columns are duplicated across the newly divided rows.
    '''
    def split_text(line, separator):
        splited_line =  [e+d for e in line.split(separator) if e]
        return splited_line
    
    def splitListToRows(row,row_accumulator,target_column,separator):
        split_row = row[target_column].split(separator)
        for s in split_row:
            new_row = row.to_dict()
            new_row[target_column] = s
            row_accumulator.append(new_row)
    new_rows = []
    df.apply(splitListToRows,axis=1,args = (new_rows,target_column,separator))
    new_df = pd.DataFrame(new_rows)
    return new_df

class Autocompleter:
    def __init__(self):
        pass

    def import_xml(self, json_filename):
        # print("load json file...")
        df = load_df(json_filename)
        return df
        
    def process_data(self, new_df):

        # print("select representative threads...")
        # new_df = new_df[new_df.IsFromCustomer==False]
        
        # print("split sentenses on punctuation...")
        for sep in ['. ',', ','? ', '! ', '; ']:
            new_df = splitDataFrameList(new_df, 'Text', sep)
            
        # print("Text Cleaning using simple regex...")
        new_df['Text']=new_df['Text'].apply(lambda x: " ".join(x.split()))
        new_df['Text']=new_df['Text'].apply(lambda x: x.strip("."))
        new_df['Text']=new_df['Text'].apply(lambda x: " ".join(x.split()))
        new_df['Text']=new_df['Text'].apply(lambda x: x.replace(' i ',' I '))
        new_df['Text']=new_df['Text'].apply(lambda x: x.replace(' ?','?'))
        new_df['Text']=new_df['Text'].apply(lambda x: x.replace(' !','!'))
        new_df['Text']=new_df['Text'].apply(lambda x: x.replace(' .','.'))
        new_df['Text']=new_df['Text'].apply(lambda x: x.replace('OK','Ok'))
        new_df['Text']=new_df['Text'].apply(lambda x: x[0].upper()+x[1:])
        new_df['Text']=new_df['Text'].apply(lambda x: x+"?" if re.search(r'^(Wh|How).+([^?])$',x) else x)
        
        # print("calculate nb words of sentenses...")
        new_df['nb_words'] = new_df['Text'].apply(lambda x: len(str(x).split(' ')))
        new_df = new_df[new_df['nb_words']>2]
        
        # print("count occurence of sentenses...")
        new_df['Counts'] = new_df.groupby(['Text'])['Text'].transform('count')
        
        # print("remove duplicates (keep last)...")
        new_df = new_df.drop_duplicates(subset=['Text'], keep='last')
        
        new_df = new_df.reset_index(drop=True)
        # print(new_df.shape)
        
        return new_df
    
    def calc_matrice(self, df):
        # define tfidf parameter in order to count/vectorize the description vector and then normalize it.
        model_tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 5), min_df=0)
        tfidf_matrice = model_tf.fit_transform(df['Text'])
        # print("tfidf_matrice ", tfidf_matrice.shape)
        return model_tf, tfidf_matrice

    def generate_completions(self, prefix_string, data, model_tf, tfidf_matrice):
        
        prefix_string = str(prefix_string)
        new_df = data.reset_index(drop=True)
        weights = new_df['Counts'].apply(lambda x: 1+ np.log1p(x)).values

        # tranform the string using the tfidf model
        tfidf_matrice_spelling = model_tf.transform([prefix_string])
        # calculate cosine_matrix
        cosine_similarite = linear_kernel(tfidf_matrice, tfidf_matrice_spelling)
        
        #sort by order of similarity from 1 to 0:
        similarity_scores = list(enumerate(cosine_similarite))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[0:10]

        similarity_scores = [i for i in similarity_scores]
        similarity_indices = [i[0] for i in similarity_scores]

        #add weight to the potential results that had high frequency in orig data
        for i in range(len(similarity_scores)):
            similarity_scores[i][1][0]=similarity_scores[i][1][0]*weights[similarity_indices][i]

        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[0:3]
        similarity_indices_w = [i[0] for i in similarity_scores]
        
        return new_df.loc[similarity_indices_w]['Text'].tolist()

if __name__ == "__main__":

    autocompl = Autocompleter()
    df = autocompl.import_xml("C:\\Users\\vamsi\\Documents\\MetaData.xml")
    new_df = autocompl.process_data(df)
    model_tf, tfidf_matrice = autocompl.calc_matrice(new_df)
    prefix = 'control'
    print(prefix, "    \n ")
    print(autocompl.generate_completions(prefix, new_df, model_tf, tfidf_matrice))