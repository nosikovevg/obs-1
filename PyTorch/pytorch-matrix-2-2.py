import torch
A = torch.tensor([[2, 4, 1]])
B = torch.tensor([[1],[4], [3]]) 

C=A@B
print(C)
