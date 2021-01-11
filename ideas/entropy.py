import matplotlib.pyplot as plt
import numpy as np

pos_fraction = np.linspace(0.00, 1.00, 1000)
gini = 1 - pos_fraction**2 - (1-pos_fraction)**2

plt.plot(pos_fraction, gini)
plt.ylim(0, 1)
plt.xlabel('Positive fraction')
plt.ylabel('Gini Impurity')
plt.show()


def gini_impurity(labels):
    # When the set is empty, it is also pure
    if not labels:
        return 0
    # Count the occurrences of each label
    counts = np.unique(labels, return_counts=True)[1]
    fractions = counts / float(len(labels))
    return 1 - np.sum(fractions ** 2)


print(f'{gini_impurity([0, 1, 1, 1, 0, 0]):.4f}')

'''
Чтобы оценить качество разделение мы складываем impurity всех групп,
комбинируя доли групп и подбирая числовые коэффициенты.
Чем меньше взвешенная сумма impuriy, тем лучше разбиение
'''

# Снижение неопределенности после разделения.
'''
Для оценки качества разделения используется Information Gain
Чем высше коэффициент, тем лучше. Мы получаем информационный прирост от
разделения дерева.
Энтропия - это вероятностная мера неопределенности. Чем меньше энтропия,
тем более чистое разделение без двухсмысленного понимания.

На графике следует обратить внимание, что если разделение 50/50
то этропия наибольшая, так как существует наибольшая неопределенность.
'''

pos_fraction = np.linspace(0.00, 1.00, 1000)
ent = - (pos_fraction * np.log2(pos_fraction) +
         (1 - pos_fraction) * np.log2(1 - pos_fraction))
plt.plot(pos_fraction, ent)
plt.xlabel('Positive fraction')
plt.ylabel('Entropy')
plt.ylim(0, 1)
plt.show()


def entropy(labels):
    if not labels:
        return 0
    counts = np.unique(labels, return_counts=True)[1]
    fractions = counts / float(len(labels))
    return - np.sum(fractions * np.log2(fractions))


print(f'{entropy([1, 1, 0, 1, 0, 0]):.4f}')
print(f'{entropy([0, 0, 0, 1, 0, 0, 0, 0]):.4f}')

# 3 Объеденение джини и энтропии
criterion_function = {'gini': gini_impurity,
                      'entropy': entropy}


def weighted_impurity(groups, criterion='gini'):
    total = sum(len(group) for group in groups)
    weighted_sum = 0.0
    for group in groups:
        weighted_sum += len(group) / float(total) * \
            criterion_function[criterion](group)
    return weighted_sum


children_1 = [[1, 0, 1], [0, 1]]
children_2 = [[1, 1], [0, 0, 1]]
print(
    f"Entropy of  # 1 split: {weighted_impurity(children_1, 'entropy'): .4f}")
print(f"Entropy of #2 split: {weighted_impurity(children_2, 'entropy'):.4f}")
