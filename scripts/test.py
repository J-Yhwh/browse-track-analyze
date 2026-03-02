import sys
print(f"Python version: {sys.version}")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch



print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"Python version: {sys.version}")
print(f"MPS (Apple GPU) available: {torch.backends.mps.is_available()}")  # True on M-series!

# Fun mini-demo: Quick plot with all libs
df = pd.DataFrame({'x': np.linspace(0, 10, 100), 'y': np.sin(np.linspace(0, 10, 100))})
plt.plot(df['x'], df['y'])
plt.title("Hello from Python 3.14 + Your Libs!")
plt.show()  # Pops up a window
