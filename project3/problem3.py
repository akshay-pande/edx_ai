import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

out_row = 0
df_inp = pd.read_csv("input3.csv")

# df_features = pd.DataFrame(columns=["x1", "x2"])
# f_output = pd.DataFrame(columns=["y"])
n = df_inp.shape[0]
df_X = df_inp[["A", "B"]].copy()
df_y = df_inp[["label"]].copy()

x_train, x_test, y_train, y_test = train_test_split(
    df_X, df_y, test_size=0.4, stratify=df_y
)
x_train_arr = x_train.to_numpy()
y_train_arr = y_train.to_numpy()
x_test_arr = x_test.to_numpy()
y_test_arr = y_test.to_numpy()


def svm():
    tuned_parameters_linear = [
        {"kernel": ["linear"], "C": [0.1, 0.5, 1, 5, 10, 50, 100]}
    ]
    tuned_parameters_poly = [
        {"kernel": ["poly"], "gamma": [0.1, 0.5], "C": [0.1, 1, 3], "degree": [4, 5, 6]}
    ]
    tuned_parameters_rbf = [
        {
            "kernel": ["rbf"],
            "gamma": [0.1, 0.5, 1, 3, 6, 10],
            "C": [0.1, 0.5, 1, 5, 10, 50, 100],
        }
    ]

    print("Training set size : ", x_train.shape[0])
    print("Test set size: ", y_test.shape[0])

    clf_linear = GridSearchCV(
        SVC(), tuned_parameters_linear, scoring=None, cv=5, return_train_score=True
    )
    clf_poly = GridSearchCV(
        SVC(), tuned_parameters_poly, scoring=None, cv=5, return_train_score=True
    )
    clf_rbf = GridSearchCV(
        SVC(), tuned_parameters_rbf, scoring=None, cv=5, return_train_score=True
    )
    print("clf successful")

    clf_linear.fit(x_train_arr, y_train_arr.ravel())
    clf_poly.fit(x_train_arr, y_train_arr.ravel())
    clf_rbf.fit(x_train_arr, y_train_arr.ravel())
    print("fit successful")

    print("Best params linear: ", clf_linear.best_params_)
    print("Best params poly: ", clf_poly.best_params_)
    print("Best params rbf: ", clf_rbf.best_params_)

    means_linear = clf_linear.cv_results_["mean_test_score"]
    means_poly = clf_poly.cv_results_["mean_test_score"]
    means_rbf = clf_rbf.cv_results_["mean_test_score"]
    means_linear_train = clf_linear.cv_results_["mean_train_score"]
    means_poly_train = clf_poly.cv_results_["mean_train_score"]
    means_rbf_train = clf_rbf.cv_results_["mean_train_score"]

    rbf_scores = max(means_rbf)
    linear_scores = max(means_linear)
    poly_scores = max(means_poly)

    rbf_train_scores = max(means_rbf_train)
    linear_train_scores = max(means_linear_train)
    poly_train_scores = max(means_poly_train)

    print(
        "Best test scores: RBF ",
        rbf_scores,
        " Linear ",
        linear_scores,
        " Polynomial ",
        poly_scores,
    )

    print(
        "Best train scores: RBF ",
        rbf_train_scores,
        " Linear ",
        linear_train_scores,
        " Polynomial ",
        poly_train_scores,
    )

    print(
        "Best scores: RBF ",
        clf_rbf.best_score_,
        " Linear ",
        clf_linear.best_score_,
        " Polynomial ",
        clf_poly.best_score_,
    )

    y_true_linear, y_pred_linear = y_test_arr, clf_linear.predict(x_test_arr)
    print("Accuracy score linear: ", str(accuracy_score(y_true_linear, y_pred_linear)))

    y_true_poly, y_pred_poly = y_test_arr, clf_poly.predict(x_test_arr)
    print("Accuracy score poly: ", str(accuracy_score(y_true_poly, y_pred_poly)))

    y_true_rbf, y_pred_rbf = y_test_arr, clf_rbf.predict(x_test_arr)
    print("Accuracy score rbf: ", str(accuracy_score(y_true_rbf, y_pred_rbf)))


def log_reg():
    C_list = [0.1, 0.5, 1, 5, 10, 50, 100]
    lreg_params = [{"C": [0.1, 0.5, 1, 5, 10, 50, 100]}]

    lreg = LogisticRegression()
    grid_clf = GridSearchCV(lreg, lreg_params, cv=5, return_train_score=True)

    clf = LogisticRegressionCV(Cs=C_list, cv=5)
    print("clf successful")

    clf.fit(x_train_arr, y_train_arr.ravel())
    grid_clf.fit(x_train_arr, y_train_arr.ravel())
    print("fit successful")
    print("Best params : ", grid_clf.best_params_)
    print("Best score : ", grid_clf.best_score_)

    print("CLF test score: ", str(clf.score(x_test_arr, y_test_arr)))

    print("---***---")
    y_pred_logistic = grid_clf.predict(x_test_arr)
    print("Accuracy score: ", str(accuracy_score(y_test_arr, y_pred_logistic)))


def knn():
    neighbours = [i for i in range(1, 51)]
    leaf_sizes = [5 * i for i in range(1, 13)]
    # print(neighbours, " ", leaf_sizes)
    knn_params = {"n_neighbors": neighbours, "leaf_size": leaf_sizes}

    gs = GridSearchCV(KNeighborsClassifier(), knn_params, cv=5, verbose=1)
    gs.fit(x_train_arr, y_train_arr.ravel())

    print("Best params : ", gs.best_params_)
    print("Best score : ", gs.best_score_)

    y_pred_knn = gs.predict(x_test_arr)
    print("Accuracy score: ", str(accuracy_score(y_test_arr, y_pred_knn)))


def decision_tree():
    max_depth = [i for i in range(1, 51)]
    min_samples_split = [2 * i for i in range(1, 6)]
    tree_param = {"max_depth": max_depth, "min_samples_split": min_samples_split}
    d_clf = GridSearchCV(DecisionTreeClassifier(), tree_param, cv=5, verbose=1)
    d_clf.fit(x_train_arr, y_train_arr)

    print("Best params : ", d_clf.best_params_)
    print("Best score : ", d_clf.best_score_)

    y_pred_dtree = d_clf.predict(x_test_arr)
    print("Accuracy score: ", str(accuracy_score(y_test_arr, y_pred_dtree)))


def random_forest():

    max_depth = [i for i in range(1, 51)]
    min_samples_split = [2 * i for i in range(1, 6)]
    rf_param = {"max_depth": max_depth, "min_samples_split": min_samples_split}
    rf_clf = GridSearchCV(RandomForestClassifier(), rf_param, cv=5, verbose=1)
    rf_clf.fit(x_train_arr, y_train_arr.ravel())

    print("Best params : ", rf_clf.best_params_)
    print("Best score : ", rf_clf.best_score_)

    y_pred_rf = rf_clf.predict(x_test_arr)
    print("Accuracy score: ", str(accuracy_score(y_test_arr, y_pred_rf)))


def main():

    svm()
    random_forest()
    knn()
    decision_tree()
    log_reg()


if __name__ == "__main__":
    main()
