# предполагается, что эту таблицу я сделаю в файле db
from db import Session, Features
from sklearn.feature_selection import RFECV
import numpy as np
from sklearn.model_selection import KFold
from sklearn import model_selection, preprocessing, feature_selection
from nltk.stem import WordNetLemmatizer
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from scipy import stats
import seaborn as sns
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
import matplotlib.pyplot as plt
from collections import Counter
import string
from db import Session, Apartments
import pandas as pd


session = Session()
PUNCT_TO_REMOVE = string.punctuation
lemmatizer = WordNetLemmatizer()
SEED = 2020
kf = KFold(n_splits=5, random_state=2)
# не пойму, почему при импорте библиотек VSC выдает ошибки

session = Session()


class Extractor:
    def __init__(self):
        pass

    def simple_imputer(self, df):
        for col in df:
            if df[col].dtype == 'object':
                df[col].fillna('N', inplace=True)
            else:
                df[col].fillna(df[col].median(), inplace=True)
        return df

    def remove_punctuation(self, text):
        """custom function to remove the punctuation"""
        return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

    def lemmatize_words(self, text):
        return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

    def description_transformator(self, df):
        df['desc_len'] = df['desc'].apply(lambda x: len(str(x)))
        df["desc"] = df["desc"].apply(
            lambda text: self.remove_punctuation(text))
        df["desc"] = df["desc"].apply(lambda text: self.lemmatize_words(text))
        df['near_sea'] = df['desc'].str.contains('sea').astype(int)
        df['near_school'] = df['desc'].str.contains('school').astype(int)
        df['near_kindergarten'] = df['desc'].str.contains(
            'kindergarten').astype(int)
        df['near_park'] = df['desc'].str.contains('park').astype(int)
        df['parking'] = df['desc'].str.contains('parking').astype(int)
        df['new'] = df['desc'].str.contains('new').astype(int)
        df['with_builtin'] = df['desc'].str.contains('builtin').astype(int)
        df['after_renovation'] = df['desc'].str.contains(
            'renovation', 'renovated').astype(int)
        df['large'] = df['desc'].str.contains('large', 'spacious').astype(int)
        df['good'] = df['desc'].str.contains('good', 'excellent').astype(int)
        df.drop('desc', axis=1, inplace=True)
        return df

    def feature_extractor(self, df):
        df = df.drop_duplicates()
        df = self.simple_imputer(df)
        df = self.description_transformator(df)
        df['floors_floor'] = df['floors']*df['floor']
        df.drop(['floor', 'floors'], axis=1, inplace=True)
        df.rooms = df.rooms.astype(str)
        df = pd.get_dummies(df)
        df['price'] = np.log1p(df['price'])
        return df

    def x_y_separator(self, df):
        X = df.drop('price', axis=1)
        y = df.price
        X['n0'] = (X == 0).sum(axis=1)  # one add feature
        # scale features between 1 and 0
        scaler = preprocessing.MinMaxScaler()
        X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
        return X, y

    def feature_importance(self, X, y, cv=5):
        regressor = DecisionTreeRegressor(max_depth=5, random_state=SEED)
        selector = RFECV(regressor, step=1, cv=cv, n_jobs=-
                         1, verbose=1,  scoring='r2')
        selector.fit(X, y)
        features_rfecv = [f for f, s in zip(X, selector.support_) if s]
        X = X[features_rfecv]
        return X, y


def fearures_selector(df):
    ext = Extractor()
    df = ext.feature_extractor(df)
    X, y = ext.x_y_separator(df)
    X, y = ext.feature_importance(X, y)
    return features


if __name__ == '__main__':

    df = session.query(Apartments)\
        .with_entities(
            Apartments.Price,
            Apartments.District,
            Apartments.Rooms,
            Apartments.Floors,
            Apartments.Area,
            Apartments.Type,
            Apartments.Cond,
            Apartments.Walls,
            Apartments.Desc,
            Apartments.Name
    )\
        .order_by(Apartments.Price.desc())\
        .all()
    df = pd.DataFrame(df)
    features = fearures_selector(df)
    for i in features:
        add_data = Features(
            Area=i['area'],
            FloorsFloor=i['floors_floor'],
            Primorsky=i['district_Primorsky'],
            Rooms=i['rooms_1.0'],
            Renovation=i['cond_Renovation'],
        )
        session.add(add_data)
    session.commit()
