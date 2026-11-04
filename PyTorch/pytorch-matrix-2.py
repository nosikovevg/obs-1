import torch

#Пример 2

A = torch.tensor([[1], [4], [3]])
B = torch.tensor([2, 4, 1])

C = A@B
print(C)
