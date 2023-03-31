import pandas as pd
import numpy as np
from collections import Counter
def exec():
    sdata = []
    for k1 in np.linspace(1.5, 2, 2):
        for k2 in np.linspace(2, 3, 3):
            for k3 in np.linspace(2.5, 4, 4):
                for k4 in np.linspace(3.5, 4.5, 3):
                    if k2 >= k1 and k3 >= k2 and k4 >= k3:
                        sdata.append((k1, k2, k3, k4))
    print(len(sdata))
    return sdata

if __name__ == '__main__':
    exec()




























# yd_pb =[0.5977, 0.2047, 0.1976, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# qf_pb = [0, 0, 0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ls_1 = [yd_pb.index(x) for x in yd_pb if x != 0]
# ls_2 = [qf_pb.index(x) for x in qf_pb if x != 0]
# print(len(list(set(ls_1).intersection(set(ls_2)))))
# print(ls_1)
# print(ls_2)