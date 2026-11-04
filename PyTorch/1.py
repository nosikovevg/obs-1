import torch
# Создание тензора из списка
t1 = torch.tensor([2,3])
print(f"1D тензор {t1.dtype}:\n", t1, "\n")

# Создание 2D тензора с явным указанием типа данных
t2 = torch.tensor([[2, 3], [4, 5]], dtype=torch.float32)
print(f"2D тензор {t2.dtype}:\n", t2, "\n")

# Создание тензора с требованием вычисления градиента
t3 = torch.tensor([[2.0, 3.0], [4.0, 5.0], [4.0, 5.0]], requires_grad=True)
print(f"2D тензор {t3.dtype}:\n", t3, "\n")

# print (dir(t3))
print(t3.shape)
print(t3.shape[1])
print('*****************')
B = torch.tensor([[5, 7], 
                  [6, 8]])

# Проверяем результат и её размерность
print("Матрица B:\n", B)
print("Размерность (shape):", B.shape)