import torch

a = torch.tensor([1,2,3])
b = torch.tensor([1.2, 3.6, 2.4])

print(a)
print(b)

print(torch.__version__)
print(torch.cuda.is_available()) #доступна GPU?
print(torch.version.cuda)
x=torch.tensor([1., 2., 3.]).to('cuda')
y=torch.tensor([2., 3., 4.]).to('cuda')
print('x=', x)
print('y=', y)
z=x@y
print('x@y=',z)
print('******************')
