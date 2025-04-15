import torch
from torch.optim import Optimizer

class FiniteTimeMomentum(Optimizer):
    def __init__(self, params, lr=1e-2, a=-0.5, k1=-20.0, k2=-20.0, eps=1.0):
        defaults = dict(lr=lr, a=a, k1=k1, k2=k2, eps=eps)
        super(FiniteTimeMomentum, self).__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = closure() if closure is not None else None

        for group in self.param_groups:
            lr = group['lr']
            a = group['a']
            k1 = group['k1']
            k2 = group['k2']
            eps = group['eps']

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad
                state = self.state[p]

                # Initialize velocity buffer
                if 'v' not in state:
                    state['v'] = torch.zeros_like(p)

                v = state['v']
                z = torch.cat([grad.view(-1), v.view(-1)])
                norm_z = torch.norm(z) + 1e-8

                # Semi-implicit: update p then v
                p.add_(lr * norm_z**a * (k1 * grad + eps * v))
                v_new = lr * norm_z**a * (eps * grad )/(1 + lr * k2 * norm_z**a )

                state['v'] = v_new

        return loss
