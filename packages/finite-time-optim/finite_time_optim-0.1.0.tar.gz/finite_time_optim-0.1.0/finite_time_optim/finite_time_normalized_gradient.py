import torch
from torch.optim import Optimizer

class FiniteTimeNormalizedGradient(Optimizer):
    def __init__(self, params, lr=1e-2, a=-0.5):
        defaults = dict(lr=lr, a=a)
        super(FiniteTimeNormalizedGradient, self).__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = closure() if closure is not None else None

        for group in self.param_groups:
            lr = group['lr']
            a = group['a']

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad
                norm_grad = torch.norm(grad) + 1e-8

                p.add_(-lr * norm_grad**a * grad / norm_grad)

        return loss
