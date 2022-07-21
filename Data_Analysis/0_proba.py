import numpy as np
import pandas as pd





df = pd.DataFrame({"a":np.array([1,2,3,4,5,6])})


df["a"][-2::] = "x"






r = [1,2,3,4,5,6]



r[4:6] = [0,0]


print(r)
