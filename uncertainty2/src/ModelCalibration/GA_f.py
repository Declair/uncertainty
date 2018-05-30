# -*- coding: utf-8 -*-
import double_loop
import numpy
import matplotlib.pyplot as plt
import build_meta

avg_dif = list()
max_dif = list()
min_dif = list()
cmp_dif = list()
best_mat = 1
sym = 0
cross_num = 0
mut_num = 0

def Get_prol(cog_p, svr):
    shape_v = cog_p.shape
    population_num = shape_v[0]
    output_l = list()
    pro_l = list()
    sum_o = 0
    tot_dis = 0
    for i in range(population_num):
        cog_p_r = cog_p[i]
        # print("输入:", end=" ")
        # print(input_x_v, end= " ")
        output_t = svr.predict(cog_p_r)
        # print input_x_v,
        # print '的预测输出:'
        # print output_t
        # print(output_t, end=" ")
        output_l.append(output_t[0])
        sum_o = sum_o + 1 / output_t[0]
        tot_dis = tot_dis + output_t[0]

    # print "平均一致性度量:",
    # print tot_dis / population_num,
    # avg_dif.append(tot_dis/population_num)
    # print("种群大小:", end=" ")
    # print(population_num, end=" ")
    sum_p = 0
    max_p = 0
    min_p = 2
    max_p_index = 0
    min_p_index = 0

    for i in range(population_num):
        pro_temp = 1 / output_l[i] / sum_o
        if max_p < pro_temp:
            max_p = pro_temp
            max_p_index = i
        if min_p > pro_temp:
            min_p = pro_temp
            min_p_index = i
        sum_p = pro_temp + sum_p
        pro_l.append(sum_p)

    global sym
    global best_mat
    if sym == 0:
        sym=1
        best_mat = cog_p[max_p_index]
    else:
        best_mat = numpy.row_stack((best_mat, cog_p[max_p_index]))

    avg_dif.append(tot_dis / population_num)
    min_dif.append(output_l[max_p_index])
    max_dif.append(output_l[min_p_index])

    y_v = double_loop.outer_level_loop(cog_p[max_p_index], build_meta.test_cmp_inh_p, build_meta.test_cmp_output, build_meta.test_cmp_input)
    cmp_dif.append(y_v[0])
    return pro_l

def Get_index(pro_l, len, r_v):  # 随机选取一个个体的下标  按照概率的大小
    i = 0
    for i in range(len):
        if pro_l[i] >= r_v:
            return i
    return i

def Cross_op(individual_1, individual_2):
    global cross_num
    cross_num = cross_num+1
    shape_v = individual_1.shape
    len = shape_v[1]
    cross_point = numpy.random.randint(1, len)
    # ret_indi = numpy.mat(numpy.full(individual_1.shape, 0))
    ret_indi = individual_1
    for i in range(shape_v[1]):
        if i <= cross_point:
            ret_indi[0, i] = individual_1[0, i]
        else:
            ret_indi[0, i] = individual_2[0, i]
    return ret_indi

def Mut_op(indi):
    global mut_num
    mut_num = mut_num+1
    shape_v = indi.shape
    r_v = numpy.random.randint(1, shape_v[1])
    r_v_a = numpy.random.rand()
    if r_v_a >= 0.5:
        indi[0, r_v] = indi[0, r_v] + 1
    else:
        indi[0, r_v] = indi[0, r_v] - 1
    return indi

def New_pop(pro_l, cog_p, cross_p, mut_p):  # 产生新种群
    shape_v = cog_p.shape
    num_iter = shape_v[0]
    row_t = cog_p[Get_index(pro_l, num_iter, numpy.random.rand())]
    # print '...'
    # print row_t
    # new_cog_p = numpy.mat(numpy.full(row_t.shape, 0))
    # shape_va = row_t.shape
    # for i in range(shape_va[1]):
    new_cog_p = row_t
    i = 1
    while i <= num_iter - 1:
        rand_c = numpy.random.rand()
        if rand_c >= 0 and rand_c < cross_p:  # 交叉成立
            # print '交叉'
            r_1 = numpy.random.rand()
            r_2 = numpy.random.rand()
            index_1 = Get_index(pro_l, num_iter, r_1)
            index_2 = Get_index(pro_l, num_iter, r_2)
            while index_2 == index_1:
                r_2 = numpy.random.rand()
                index_2 = Get_index(pro_l, num_iter, r_2)
            individual_1 = cog_p[index_1]
            individual_2 = cog_p[index_2]
            new_indi = Cross_op(individual_1, individual_2)
            r_3 = numpy.random.rand()
            if r_3 >= 0 and r_3 < mut_p:
                # print '交叉得变异'
                new_indi = Mut_op(new_indi)
            new_cog_p = numpy.row_stack((new_cog_p, new_indi))
            i = i + 1
        else:
            r = numpy.random.rand()
            index = Get_index(pro_l, num_iter, r)
            new_indi = cog_p[index]
            # print cog_p[index]
            # print new_indi
            r_3 = numpy.random.rand()
            if r_3 >= 0 and r_3 < mut_p:
                # print '变异'
                new_indi = Mut_op(new_indi)
            new_cog_p = numpy.row_stack((new_cog_p, new_indi))
            i = i + 1
    return new_cog_p

def GA(snb, meta_model, pn=100, itn=50, cp=0.3, mp=0.05, cog_p_n=4):
    show_panel = snb.show_panel
    csw = snb.sw
    # csw.text_ctrl.SetValue(showlog)
    # show_panel.Layout()
    log = ''
    global max_dif
    global min_dif
    global avg_dif
    global cmp_dif
    max_dif = list()
    min_dif = list()
    avg_dif = list()
    cmp_dif = list()
    population_num = pn  # 种群大小
    iter_num = itn  # 迭代次数
    cross_p = cp  # 交叉概率
    mut_p = mp  # 变异概率
    print '种群大小: %d' % (population_num),
    print '迭代次数: %d' % (iter_num),
    print '交叉概率: %f' % (cross_p),
    print '变异概率: %f' % (mut_p)
    cog_p = numpy.mat(numpy.random.rand(population_num, cog_p_n))*9  # 初始种群

    print '期望最佳预测:'
    log = log+'期望最佳预测'+'\n'
    print meta_model.predict([[4,1,8]])
    log = log + '%f'%(meta_model.predict([[4,1,8]])) + '\n'
    for i in range(iter_num):
        print "第%d次迭代" % (i+1)
        # print '种群:'
        # print cog_p
        pro_l = Get_prol(cog_p, meta_model)
        # print '概率列表:'
        # print pro_l
        cog_p = New_pop(pro_l, cog_p, cross_p, mut_p)

    print '交叉次数: %d'%(cross_num)
    log = log + '交叉次数: %d'%(cross_num) + '\n'
    print '变异次数: %d'%(mut_num)
    log = log + '变异次数: %d'%(mut_num) + '\n'

    print 'max_dif:'
    print max_dif
    print 'avg_dif:'
    print(avg_dif)
    print 'min_dif:'
    print min_dif
    print 'cmp_dif:'
    print(cmp_dif)

    log = log + '%d次迭代优化中每次的最大差异度量为\n%r' % (iter_num, max_dif) + '\n'
    log = log + '%d次迭代优化中每次的最小差异度量为\n%r' % (iter_num, min_dif) + '\n'
    log = log + '%d次迭代优化中每次的平均差异度量为\n%r' % (iter_num, avg_dif) + '\n'
    log = log + '%d次迭代优化中每次的比较差异度量为\n%r' % (iter_num, cmp_dif) + '\n'

    print 'best_mat:'
    print best_mat

    log = log + '%d次迭代优化中每次的最佳参数取值为\n%r' % (iter_num, best_mat) + '\n'

    csw.text_ctrl.SetValue(log)
    show_panel.Layout()

    plt.figure(num=1, figsize=(6, 3))
    x = len(avg_dif)
    x= range(x)
    plt.plot(x, avg_dif)
    plt.plot(x, max_dif)
    plt.plot(x, min_dif)
    plt.xlabel('iter num')
    plt.ylabel('measure size')
    plt.title('average measure size trend')
    plt.figure(num=2, figsize=(6, 3))
    plt.plot(x, cmp_dif)
    plt.xlabel('iter num')
    plt.ylabel('measure size')
    plt.title('verify trend')
    plt.show()