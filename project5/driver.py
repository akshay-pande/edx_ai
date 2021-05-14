import pandas as pd
import pathlib
import csv
import numpy as np
import re 
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

train_path = "../resource/lib/publicdata/aclImdb/train/" # use terminal to ls files under this directory
#test_path = "../resource/lib/publicdata/imdb_te.csv" # test data for grade evaluation
test_path = 'imdb_te.csv'


def read_texts(path_name:str, out_file:str, num_records:int, polarity:int, stop_list):
    texts = pd.Series([])    
    row = 0     
    print(path_name)    

    for path in pathlib.Path(path_name).iterdir():
        current_file = open(path,"r",encoding="utf8")   
        
        if row > num_records :
            break
        if path.is_file() :
            row = row + 1                                
            current_text = current_file.read()  
            current_text = re.sub('[0-9]+', '', current_text)
            current_text = current_text.replace("_"," ")
            current_text = re.sub(r'http\S+', '',current_text)                 
            texts[row-1] = current_text
            current_file.close()
        
    df = pd.DataFrame(texts)
    df['label'] = polarity
    df.to_csv(out_file, mode='a', header=False, index=True)
    return True



def predictor(inp_path:str, test_inp_path:str, stoplist):
    df = pd.DataFrame()
    df = pd.read_csv(inp_path, header=0, index_col=0)
    df['row'] = df.index          
    docs_list = df['text'].tolist()
    bi_docs_list = docs_list
    
    for i in range(0,len(bi_docs_list)):
        bi_docs_list[i] = bi_docs_list[i].replace("."," stopp asterisk ")
        
    print("Corpus size ", len(docs_list))
    
    doc_outputs = df['label'].tolist()
    doc_outputs = [0 if x==-1 else x for x in doc_outputs]
    print("Num outputs ", len(doc_outputs))    
    
    
    vectorizer = CountVectorizer(min_df=2, stop_words=stoplist, strip_accents='unicode')
    vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(2, 2), min_df=2, stop_words=stoplist, strip_accents='unicode')
    vectorizer_tf = TfidfVectorizer( min_df=2, stop_words=stoplist, strip_accents='unicode')
    vectorizer_tf2 = TfidfVectorizer(analyzer='word', ngram_range=(2, 2), min_df=2, stop_words=stoplist, strip_accents='unicode',sublinear_tf=True)
    
    X = vectorizer.fit_transform(docs_list)
    X2 = vectorizer2.fit_transform(bi_docs_list)   
    X_tf = vectorizer_tf.fit_transform(docs_list)
    X2_tf = vectorizer_tf2.fit_transform(bi_docs_list)       
    
    Vocab = vectorizer.get_feature_names()
    Vocab_bi = vectorizer2.get_feature_names()    
    print(len(Vocab))
    print(len(Vocab_bi))    
    
    clf = SGDClassifier(loss="hinge", penalty="l1", max_iter=2000)
    clf.fit(X, doc_outputs)
    print("Uni classifier done")
    clf_bi = SGDClassifier(loss="hinge", penalty="l1", max_iter=3000)
    clf_bi.fit(X2, doc_outputs)
    print("Bi classifier done")
    clf_tf = SGDClassifier(loss="hinge", penalty="l1", max_iter=2000)
    clf_tf.fit(X_tf, doc_outputs)
    print("Uni TF classifier done")
    clf_bi_tf = SGDClassifier(loss="hinge", penalty="l1", max_iter=3000)
    clf_bi_tf.fit(X2_tf, doc_outputs)
    print("Bi TF classifier done")
    
    
    df_test_values = pd.read_csv(test_inp_path, encoding="iso-8859-1", error_bad_lines=False)   
    
    test_inputs = df_test_values['text'].tolist()  
    bi_test_inputs = test_inputs
    
    for i in range(0,len(bi_test_inputs)):
        bi_test_inputs[i] = bi_test_inputs[i].replace("."," stopp asterisk ")
    
    X = vectorizer.transform(test_inputs)
    X2 = vectorizer2.transform(bi_test_inputs)   
    X_tf = vectorizer_tf.transform(test_inputs)
    X2_tf = vectorizer_tf2.transform(bi_test_inputs)  
    
    
    print("size of test inps:" , len(test_inputs))
    file_uni = open('unigram.output.txt', mode="a")        
    file_bi = open('bigram.output.txt', mode="a")
    file_uni_tf = open('unigramtfidf.output.txt', mode="a")
    file_bi_tf = open('bigramtfidf.output.txt', mode="a")
    
    Y_pred = clf.predict(X)
    Y_pred2 = clf_bi.predict(X2)
    Y_pred_tf = clf_tf.predict(X_tf)
    Y_pred2_tf = clf_bi_tf.predict(X2_tf)
    print("prediction complete")
    
    for i in range(0, len(test_inputs)):    
        
        file_uni.write(str(Y_pred[i])+'\n')
        file_bi.write(str(Y_pred2[i] or Y_pred[i])+'\n')
        file_uni_tf.write(str(Y_pred_tf[i])+'\n')
        file_bi_tf.write(str(Y_pred2_tf[i] or Y_pred_tf[i])+'\n')
        
        file_uni.flush()
        file_bi.flush()
        file_uni_tf.flush()
        file_bi_tf.flush()
    

    file_uni.close()
    file_bi.close()
    file_uni_tf.close()
    file_bi_tf.close()
    print("print complete")
    return True


def main():
   
   #create the training csv file from raw data
   training_out_file =   'imdb_tr.csv'
   test_in_file = test_path 

   df = pd.DataFrame(columns = ['text','label'])
   df_out = pd.DataFrame()
   df.to_csv(training_out_file, header=True, index=True)
   

   #preprocess - remove stopwords from data
   stoplist = pd.Series([])
   stoplist = pd.read_csv("stopwords.en.txt", index_col=False, header=None, squeeze=True)
   stoplist = stoplist.values.tolist()

   #read_texts(train_path+"neg/", training_out_file, polarity=-1, num_records=20000, stop_list=stoplist)
   #read_texts(train_path+"pos/", training_out_file, polarity=1, num_records=20000, stop_list=stoplist)   
   
   if os.path.exists('unigram.output.txt'):
       os.remove('unigram.output.txt')        
   if os.path.exists('bigram.output.txt'):
       os.remove('bigram.output.txt')
   if os.path.exists('unigramtfidf.output.txt'):
       os.remove('unigramtfidf.output.txt')
   if os.path.exists('bigramtfidf.output.txt'):   
       os.remove('bigramtfidf.output.txt')
   
   clf_uni = predictor(training_out_file, test_in_file, stoplist)
    
        
  
if __name__ == "__main__":
 	
    main()