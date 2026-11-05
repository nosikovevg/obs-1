import torch
A = torch.tensor([[1, 2]])
B = torch.tensor([[3, 4],[5, 6]]) 

C=A@B
print(C)
