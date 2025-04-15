import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'finite_time_optim')))

from finite_time_optim import FiniteTimeMomentum, FiniteTimeNormalizedGradient, FiniteTimeSignGradient

def test_optimizers():
    # 假设你已经设置好模型和损失函数
    # 可以在这里测试每个优化器的功能
    print("Testing FiniteTimeMomentum...")
    # 你的测试代码

    print("Testing FiniteTimeNormalizedGradient...")
    # 你的测试代码

    print("Testing FiniteTimeSignGradient...")
    # 你的测试代码

if __name__ == "__main__":
    test_optimizers()
