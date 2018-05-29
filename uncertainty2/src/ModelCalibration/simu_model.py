import numpy
def run_simu_model_inner(p1, p2, input_Xi):
    shape_v1 = p1.shape
    shape_v2 = p2.shape
    s = 0
    sa = 0
    for i in range(shape_v1[1]):
        s = s+p1[0,i]*input_Xi[0,i]
        sa = sa+p1[0, i]*input_Xi[0, i]
    ts = 0
    for i in range(shape_v2[1]):
        ts = ts+p2[0, i]

    s = s+ts
    sa = sa+ts
    return s, sa


def run_simu_model(p1, p2, input_X):
    shape_v = input_X.shape
    n = shape_v[0]
    rans = run_simu_model_inner(p1, p2, input_X[0])
    for i in range(n):
        if i == 0:
            continue
        tans = run_simu_model_inner(p1, p2, input_X[i])
        rans = numpy.row_stack((rans, tans))
    return numpy.mat(rans)
