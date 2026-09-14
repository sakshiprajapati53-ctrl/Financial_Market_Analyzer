import numpy as np
from main import data
close = data["Close"].to_numpy()

print("Number of trading days:", close.size)
print("Average:", np.mean(close))
print("Highest:", np.max(close))
print("Lowest:", np.min(close))