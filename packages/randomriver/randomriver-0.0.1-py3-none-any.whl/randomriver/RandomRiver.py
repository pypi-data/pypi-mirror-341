import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error, root_mean_squared_error,
    mean_squared_log_error, mean_absolute_percentage_error,
    max_error, r2_score, explained_variance_score
)





class RandomRiver:

    def __init__(
        self,
        df: pd.core.frame.DataFrame,
        date_col: str,
        y_col: str,
        x_var_list: list = None,
        split_frac: float = 0.8
    ) -> None:
        self.__df = df
        self.__date_col = date_col
        self.__y_col = y_col
        self.__x_var_list = x_var_list
        self.__split_frac = split_frac
        self.__model = None


    def __repr__(self) -> str:
        if self.__x_var_list:
            lst_str = "['"+ "', '".join(self.__x_var_list) + "']"
            return f"RandomRiver(date_col = '{self.__date_col}', y_col = '{self.__y_col}', x_var_list = {lst_str})"
        else:
            return f"RandomRiver(date_col = '{self.__date_col}', y_col = '{self.__y_col}')"


    def __tryel(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                print(f"Method '{func.__name__}' failed with Exception:\n{e}")
        return wrapper


    def __split_data(self) -> list:
        flow_df = self.flow
        train = flow_df.sample(frac = self.__split_frac)
        train_X = train.drop(self.__y_col, axis = 1).reset_index(drop = True)
        train_y = train[self.__y_col].reset_index(drop = True)
        test = flow_df.drop(train.index)
        test_X = test.drop(self.__y_col, axis = 1).reset_index(drop = True)
        test_y = test[self.__y_col].reset_index(drop = True)
        return [train_X, train_y, test_X, test_y]


    def __flow(self, df, test_data = False) -> pd.core.frame.DataFrame:
        date_df = pd.DataFrame({
            "year": pd.to_datetime(df[self.__date_col]).dt.year,
            "month": pd.to_datetime(df[self.__date_col]).dt.month,
            "day": pd.to_datetime(df[self.__date_col]).dt.day,
            "dayofweek": pd.to_datetime(df[self.__date_col]).dt.dayofweek
        })
        if test_data:
            if self.__x_var_list:
                return pd.concat([date_df, df[self.__x_var_list]], axis = 1)
            else:
                return date_df
        else:
            if self.__x_var_list:
                return pd.concat([date_df, df[(self.__x_var_list + [self.__y_col])]], axis = 1)
            else:
                return pd.concat([date_df, df[self.__y_col]], axis = 1)


    @property
    def flow(self) -> pd.core.frame.DataFrame:
        date_df = pd.DataFrame({
            "year": pd.to_datetime(self.__df[self.__date_col]).dt.year,
            "month": pd.to_datetime(self.__df[self.__date_col]).dt.month,
            "day": pd.to_datetime(self.__df[self.__date_col]).dt.day,
            "dayofweek": pd.to_datetime(self.__df[self.__date_col]).dt.dayofweek
        })
        if self.__x_var_list:
            return pd.concat([date_df, self.__df[(self.__x_var_list + [self.__y_col])]], axis = 1)
        else:
            return pd.concat([date_df, self.__df[self.__y_col]], axis = 1)


    def fit(
        self,
        rf_n_estimators: int = 200,
        rf_criterion: str = "squared_error",
        rf_max_depth: int = None,
        rf_min_samples_split: int | float = 2
    ):
        train_X, train_y, _, _ = self.__split_data()
        self.__model = RandomForestRegressor(
            n_estimators = rf_n_estimators,
            criterion = rf_criterion,
            max_depth = rf_max_depth,
            min_samples_split = rf_min_samples_split
        )
        return self.__model.fit(train_X, train_y)


    @property
    def accuracy(self) -> dict:
        if self.__model:
            _, _, test_X, test_y = self.__split_data()
            rf_pred = self.__model.predict(test_X)
            return {
                "R2": r2_score(test_y, rf_pred),
                "RMSE": root_mean_squared_error(test_y, rf_pred),
                "MAE": mean_absolute_error(test_y, rf_pred),
                "MSLE": mean_squared_log_error(test_y, rf_pred),
                "MAPE": mean_absolute_percentage_error(test_y, rf_pred),
                "MaxError": max_error(test_y, rf_pred),
                "ExplainedVarianceScore": explained_variance_score(test_y, rf_pred)
            }
        else:
            print("No model exists - use the '.fit()' method to train one")
            return {
                "R2": np.nan,
                "RMSE": np.nan,
                "MAE": np.nan,
                "MSLE": np.nan,
                "MAPE": np.nan,
                "MaxError": np.nan,
                "ExplainedVarianceScore": np.nan
            }


    @property
    def importance(self) -> list | None:
        if self.__model:
            feat_imp = self.__model.feature_importances_
            return np.std([tree.feature_importances_ for tree in self.__model.estimators_], axis = 0)
        else:
            print("No model exists - use the '.fit()' method to train one")
            return None


    def predict(self, new_df):
        x_var_df = self.__flow(new_df, test_data = True)
        return self.__model.predict(x_var_df)
