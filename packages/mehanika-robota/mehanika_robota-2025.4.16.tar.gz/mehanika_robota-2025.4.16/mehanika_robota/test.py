import numpy as np
import mehanika_robota.mehanika.kinematika as kin
import mehanika_robota.mehanika.mat_prostor as mp
import mehanika_robota.roboti.niryo_one as n_one
import mehanika_robota.mehanika.trajektorija as traj
import timeit

np.set_printoptions(14, suppress=None, floatmode='unique')

# T_start = kkt.SE3_sastavi(
#     np.eye(3),
#     [1, 0, 0]
# )

# T_fin = kkt.SE3_sastavi(
#     np.eye(3),
#     [5, 0, 0]
# )

# tr = traj.pravolin_traj(T_start, T_fin, 50)

# for i in range(len(tr)):
#     print(tr[i])

R_start = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]], dtype=float)

R_end = np.array([[1, 0,  0, 0],
                  [0, 0, -1, 0],
                  [0, 1,  0, 0],
                  [0, 0,  0, 1]], dtype=float)

# s = 1/3

# R = R_start@mp.exp(mp.log(mp.inv(R_start)@R_end)*0.15625)
# print(R)
# R = R_start@mp.exp(mp.log(mp.inv(R_start)@R_end)*0.84375)
# print(R)

print(traj.pravolin_traj(
    [[1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]],
    [[1, 0,  0, 0],
        [0, 0, -1, 0],
        [0, 1,  0, 0],
        [0, 0,  0, 1]],
    {
        "n": 3,
        "t_ukupno": 4,
        "stepen": 5
    }
))