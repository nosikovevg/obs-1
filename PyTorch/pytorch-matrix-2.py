import torch

#Пример 1

A = torch.tensor([[1, 2, 3], [2, 1, 4], [3, 2, 3]])
B = torch.tensor([[1, 3, 4], [5, 7, 8], [1, 2, 4]])

C = 2*A+B
print(C)
