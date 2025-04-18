from sklearn.model_selection import train_test_split, RandomizedSearchCV

class RegressorTuner:
    def __init__(self, model, dataset, target_column, model_name):
        self.model = model
        self.dataset = dataset
        self.target_column = target_column
        self.model_name = model_name

        self.param_grids = {
            "Linear Regression": {},
            "Random Forest": {
                "n_estimators": [50, 100, 150],
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 5, 10],
            },
            "Support Vector Machine": {
                "C": [0.1, 1, 10],
                "kernel": ["linear", "rbf", "poly"],
                "gamma": ["scale", "auto"],
            },
            "Decision Tree": {
                "max_depth": [None, 5, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
            },
            "Gradient Boosting": {
                "n_estimators": [50, 100],
                "learning_rate": [0.01, 0.1, 0.2],
                "max_depth": [3, 5, 7],
            },
            "Ridge Regression": {
                "alpha": [0.01, 0.1, 1.0, 10.0],
            },
            "Lasso Regression": {
                "alpha": [0.01, 0.1, 1.0, 10.0],
            },
            "Elastic Net": {
                "alpha": [0.01, 0.1, 1.0],
                "l1_ratio": [0.2, 0.5, 0.8],
            },
        }

    def tune(self):
        if self.model_name not in self.param_grids:
            print(f"\u26a0\ufe0f No tuning grid available for '{self.model_name}'. Returning the original model.")
            return self.model

        if self.param_grids[self.model_name] == {}:
            print(f"\u2139\ufe0f '{self.model_name}' does not require tuning. Using default model.")
            return self.model

        X = self.dataset.drop(columns=[self.target_column])
        y = self.dataset[self.target_column]

        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        print(f"\ud83d\udd0d Tuning hyperparameters for {self.model_name}...")

        search = RandomizedSearchCV(
            estimator=self.model,
            param_distributions=self.param_grids[self.model_name],
            n_iter=10,
            scoring="r2",
            cv=3,
            random_state=42,
            n_jobs=-1
        )
        search.fit(X_train, y_train)

        print(f"\u2705 Best parameters for {self.model_name}: {search.best_params_}")
        return search.best_estimator_


class ClassifierTuner:
    def __init__(self, model, dataset, target_column, model_name):
        self.model = model
        self.dataset = dataset
        self.target_column = target_column
        self.model_name = model_name

        self.param_grids = {
            "Logistic Regression": {
                "C": [0.1, 1.0, 10.0],
                "solver": ["liblinear", "lbfgs"]
            },
            "Random Forest Classifier": {
                "n_estimators": [50, 100, 150],
                "max_depth": [None, 10, 20],
                "min_samples_split": [2, 5, 10],
            },
            "SVC": {
                "C": [0.1, 1, 10],
                "kernel": ["linear", "rbf"],
                "gamma": ["scale", "auto"],
            },
            "Decision Tree Classifier": {
                "max_depth": [None, 5, 10, 20],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
            },
            # Add more classifiers as needed
        }

    def tune(self):
        if self.model_name not in self.param_grids:
            print(f"\u26a0\ufe0f No tuning grid available for '{self.model_name}'. Returning the original model.")
            return self.model

        X = self.dataset.drop(columns=[self.target_column])
        y = self.dataset[self.target_column]

        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

        print(f"\ud83d\udd0d Tuning hyperparameters for {self.model_name}...")

        search = RandomizedSearchCV(
            estimator=self.model,
            param_distributions=self.param_grids[self.model_name],
            n_iter=10,
            scoring="accuracy",
            cv=3,
            random_state=42,
            n_jobs=-1
        )
        search.fit(X_train, y_train)

        print(f"\u2705 Best parameters for {self.model_name}: {search.best_params_}")
        return search.best_estimator_
