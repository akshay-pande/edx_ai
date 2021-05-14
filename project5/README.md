NLP classification of IMDB movie reviews using unigrams, bigrams and TF-IDF

Submission score: 81%

Main file: driver.py

Unzip imdb_tr.zip to same folder as program before proceeding

Note: For the sake of simplicity, I've commented out the part of the code which combines reviews from individual text files into the single imdb_tr.csv training set

The "Large Movie Review Dataset"(*) shall be used for this project. The dataset is compiled from a collection of 50,000 reviews from IMDB on the condition there are no more than 30 reviews each movie. Number of positive and negative reviews are equal. Negative reviews have scores lesser or equal 4 out of 10 while a positive review greater or equal 7 out of 10. Neutral reviews are not included on the other hand. Then, 50,000 reviews are divided evenly into the training and test set.

*Dataset is credited to Prof. Andrew Mass in the paper, Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. (2011). Learning Word Vectors for Sentiment Analysis. The 49th Annual Meeting of the Association for Computational Linguistics (ACL 2011).
