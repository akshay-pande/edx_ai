Three-part Machine Learning assignment

1. PLA
2. Linear Regression
3. Classification algortihms

Submission Score: 100%

I. Perceptron Learning Algorithm

Implements the perceptron learning algorithm ("PLA") for a linearly separable dataset. input1.csv, contains a series of data points. Each point is a comma-separated ordered triple, representing feature_1, feature_2, and the label for the point. You can think of the values of the features as the x- and y-coordinates of each point. The label takes on a value of positive or negative one. You can think of the label as separating the points into two categories.

The code is available in problem1.py, which will be executed like so:

$ python3 problem1.py input1.csv output1.csv

This should generate an output file called output1.csv. With each iteration of the PLA (each time we go through all examples), the program must print a new line to the output file, containing a comma-separated list of the weights w_1, w_2, and b in that order. Upon convergence, the program will stop, and the final values of w_1, w_2, and b will be printed to the output file. This defines the decision boundary that your PLA has computed for the given dataset.

II. Linear Regression

In this problem, we work on linear regression with multiple features using gradient descent. input2.csv, contains a series of data points. Each point is a comma-separated ordered triple, representing age, weight, and height (derived from CDC growth charts data).

Data Preparation and Normalization. The features are not on the same scale. They represent age (years), and weight (kilograms). What is the mean and standard deviation of each feature? The last column is the label, and represents the height (meters). Each feature (i.e. age and weight) is scaled by its (population) standard deviation, which sets its mean to zero. 

Gradient Descent. Implemented gradient descent to find a regression model. Initialized β’s to zero. 

Using the following learning rates: α ∈ {0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10}. For each value of α, 100 iterations. 

Implemened in file problem2.py, which will be executed like so:

$ python3 problem2.py input2.csv output2.csv

This should generate an output file called output2.csv. There are ten cases in total, nine with the specified learning rates (and 100 iterations), and one with my own choice of learning rate (and number of iterations). 

III. Classification

This problem used the support vector classifiers in the sklearn package to learn a classification model for a chessboard-like dataset. input3.csv contains a series of data points. 

Used SVM with different kernels to build a classifier. Split the data into training (60%) and testing (40%). Also used stratified sampling (i.e. same ratio of positive to negative in both the training and testing datasets), cross validation (with the number of folds k = 5) instead of a validation set. 

Tried below classification approaches:

    SVM with Linear Kernel. tried values of C = [0.1, 0.5, 1, 5, 10, 50, 100]. 

    SVM with Polynomial Kernel. (Similar to above).
    Try values of C = [0.1, 1, 3], degree = [4, 5, 6], and gamma = [0.1, 0.5].

    SVM with RBF Kernel. (Similar to above).
    Try values of C = [0.1, 0.5, 1, 5, 10, 50, 100] and gamma = [0.1, 0.5, 1, 3, 6, 10].

    Logistic Regression. (Similar to above).
    Try values of C = [0.1, 0.5, 1, 5, 10, 50, 100].

    k-Nearest Neighbors. (Similar to above).
    Try values of n_neighbors = [1, 2, 3, ..., 50] and leaf_size = [5, 10, 15, ..., 60].

    Decision Trees. (Similar to above).
    Try values of max_depth = [1, 2, 3, ..., 50] and min_samples_split = [2, 3, 4, ..., 10].

    Random Forest. (Similar to above).
    Try values of max_depth = [1, 2, 3, ..., 50] and min_samples_split = [2, 3, 4, ..., 10].



