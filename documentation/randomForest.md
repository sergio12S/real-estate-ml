
from sklearn.ensemble import RandomForestClassifier

# Поиск оптимальных параметров
param_grid = {
    'max_depth': [30, 50],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [3, 5]
    }

rf = RandomForestRegressor(n_estimators=100, n_jobs=-1, max_features='auto', random_state=42)
grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='r2', n_jobs=-1)

grid_search.fit(X_train, y_train)
print(grid_search.best_params_)

rf_best = grid_search.best_estimator_
predictions_rf = rf_best.predict(X_test)

# feature importance
importance = rf.coef_[0]

for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))
pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()

# Рекомендации
1. Не нужно делать масштабирование. Это можно привести к "утечке данных", а также алгоритму тяжелее увидеть не линейные закономерности.
2. Использовать LabelEncoder, OneHotEncoder