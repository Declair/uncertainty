# -*- coding: utf-8 -*-
import numpy
import real_model as rm
import double_loop
from sklearn import svm
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.kernel_ridge import KernelRidge as KRR
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.gaussian_process.kernels import (RBF, Matern, RationalQuadratic,
                                              ExpSineSquared, DotProduct,
                                              ConstantKernel)
import get_sampling as gs
test_cog_p = 1
test_inh_p = 1
test_cmp_inh_p =1

test_input = 1
test_cmp_input = 1

test_output = 1
test_cmp_output = 1

def initData(cog_p_gn=400, cog_p_n=4, inh_p_gn=20, inh_p_n=1, c_data_n=30, cmp_data_n=20):
    global test_cog_p
    test_cog_p = numpy.mat(numpy.random.rand(cog_p_gn, cog_p_n))*9  # 认知不确定参数 实际应该通过抽样获得

    global test_inh_p
    test_inh_p = numpy.mat(numpy.random.standard_normal(size=(inh_p_gn, inh_p_n)))  # 固有不确定参数  实际应该通过抽样获得
    global test_cmp_inh_p
    test_cmp_inh_p = test_inh_p

    global test_input
    test_input = numpy.mat(
        numpy.random.rand(c_data_n, 3))*5+1  # 这个输入是为了让实际系统和仿真系统在不确定参数确定的情况下获得相应的输出，进而可以比较获得马氏距离，进而来训练SVR模型

    global test_cmp_input
    test_cmp_input = numpy.mat(
        numpy.random.rand(cmp_data_n, 3))*5+1 # 这个输入是在每一次优化中获得的最优参数下仿真模型的输出和实际系统在这个输入下的输出的比较，进而可以看见优化参数的效果

    global test_output
    test_output = rm.run_real_model(test_inh_p, test_input)  # 为了获取一致性度量结果

    global test_cmp_output  # 为了比较验证仿真校准结果
    test_cmp_output = rm.run_real_model(test_inh_p, test_cmp_input)


cog_p = 0
inh_p = 0
input_v = 0
train_input_v = 0
cmp_input_v = 0
train_output = 0
cmp_output = 0
def importData():
    global cog_p
    global inh_p
    global input_v
    global train_output
    global cmp_output

    cog_p = gs.get_samp(arg_type=2)
    inh_p = gs.get_samp(arg_type=1)
    input_v = gs.get_samp(arg_type=0)

    shape = input_v.shape
    d1 = shape[0]/2
    train_input_v = input_v[0:d1, :]
    cmp_input_v = input_v[d1:, :]

    train_output = rm.run_real_model(inh_p, train_input_v)
    cmp_output = rm.run_real_model(inh_p, cmp_input_v)

    print '认知不确定参数:'
    print cog_p
    print '固有不确定参数:'
    print inh_p
    print '训练输入:'
    print train_input_v
    print '对比输入:'
    print cmp_input_v
    print '训练输出:'
    print train_output
    print '对比输出:'
    print cmp_output

if __name__ == '__main__':
    importData()

def buildSVR(snb, test_cog_p, test_inh_p, test_output, test_input):
    print('认知不确定参数矩阵:')
    print(test_cog_p)
    print('固有不确定参数')
    print(test_inh_p)
    print('参考输入:')
    print(test_input)
    print('参考输出矩阵:')
    print(test_output)
    print('对比输入:')
    print(test_cmp_input)
    print('对比输出矩阵')
    print(test_cmp_output)
    y_v = double_loop.outer_level_loop(test_cog_p, test_inh_p, test_output, test_input)  # 运行仿真系统获得输出向量，即马氏距离的向量  该输出和认知不确定参数Es_p共同构成训练数据集
    y_va = numpy.array(y_v)
    print('训练输出:')
    print(y_va)

    print('最佳参数取值对应的实际输出:')
    best_p = numpy.mat([[4,1,8]])
    y_vaa = double_loop.outer_level_loop(best_p, test_inh_p, test_output, test_input)
    print(y_vaa)

    test_cog_pa = numpy.array(test_cog_p)

    # X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size = .4, random_state = 0)
    # svr = svm.SVR(kernel=cus_kernel, C=cus_C, epsilon=cus_epsilon).fit(X_train, y_train)
    #
    # print 'score:'
    # print svr.score(X_test, y_test)

    tuned_parameters = [{'kernel' : ['linear', 'poly', 'rbf', 'sigmoid'],
                         'gamma' : ['auto', 0.1, 0.001, 0.0001],
                         'C' : [1, 10, 100, 1000],
                         'epsilon' : [0.1, 0.001, 1],
                         }]
    X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size=0.5, random_state=0)

    showlog = ''
    print "建立超参数搜索模型"
    showlog = showlog + '建立超参数搜索模型' + '\n'
    clf = GridSearchCV(svm.SVR(), tuned_parameters)

    print '开始搜索'
    showlog = showlog + '开始搜索' + '\n'
    clf.fit(X_train, y_train)
    print '搜索结束'
    showlog = showlog + '搜索结束' + '\n'

    print "在参数集上搜索得到的最佳参数组合为:"
    showlog = showlog + '在参数集上搜索得到的最佳参数组合为' + '\n'
    print clf.best_params_
    showlog = showlog + '%r' % (clf.best_params_) + '\n'
    print "在参数集上每个参数组合得得分为:"
    showlog = showlog + '在参数集上每个参数组合得得分为' + '\n'
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']

    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params)
        showlog = showlog + "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params) + '\n'

    show_panel = snb.show_panel
    csw = snb.sw
    csw.text_ctrl.SetValue(showlog)
    show_panel.Layout()


    # print '最优值对应得预测输出:'
    # print clf.predict(best_p)
    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)
    plt.plot(y_pred, 'r')
    plt.plot(y_test, 'g')
    plt.plot(best_pred, 'b.')
    plt.show()

    # X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size=.4, random_state=0)
    #
    # svr = svm.SVR(kernel=cus_kernel, C=cus_C, epsilon=cus_epsilon).fit(X_train, y_train)
    #
    # y_predict = svr.predict(X_test)
    #
    # plt.plot(y_train, 'r')
    # plt.plot(y_predict, 'b')
    # plt.plot(y_test, 'g')
    # plt.show()

    return clf

def buildGPR(snb, test_cog_p, test_inh_p, test_output, test_input):#, cus_alpha):
    # print ("GPR建模方法，alpha：%f"%(cus_alpha))
    print('认知不确定参数矩阵:')
    print(test_cog_p)
    print('固有不确定参数')
    print(test_inh_p)
    print('参考输入:')
    print(test_input)
    print('参考输出矩阵:')
    print(test_output)
    print('对比输入:')
    print(test_cmp_input)
    print('对比输出矩阵')
    print(test_cmp_output)
    y_v = double_loop.outer_level_loop(test_cog_p, test_inh_p, test_output, test_input)  # 运行仿真系统获得输出向量，即马氏距离的向量  该输出和认知不确定参数Es_p共同构成训练数据集
    y_va = numpy.array(y_v)
    print('训练输出:')
    print(y_va)

    print('最佳参数取值对应输出:')
    best_p = numpy.mat([[4, 1, 8]])
    y_vaa = double_loop.outer_level_loop(best_p, test_inh_p, test_output, test_input)
    print(y_vaa)

    test_cog_pa = numpy.array(test_cog_p)

    # X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size=.4, random_state=0)
    # gpr = GaussianProcessRegressor(alpha=cus_alpha).fit(X_train, y_train)
    #
    # print 'score:'
    # gpr.score(X_test, y_test)

    tuned_parameters = [{'kernel': [1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0)),
                                    1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1),
                                    # 1.0 * ExpSineSquared(length_scale=1.0, periodicity=3.0,
                                    #     length_scale_bounds=(0.1, 10.0),
                                    #     periodicity_bounds=(1.0, 10.0)),
                                    ConstantKernel(0.1, (0.01, 10.0))
                                        * (DotProduct(sigma_0=1.0, sigma_0_bounds=(0.0, 10.0)) ** 2),
                                    1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-1, 10.0),nu=1.5)],
                         'alpha' : [1E-10, 0.1, 1]
                         }]
    X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size=0.5, random_state=0)

    showlog = ''
    print "建立超参数搜索模型"
    showlog = showlog+'建立超参数搜索模型'+'\n'
    clf = GridSearchCV(GPR(), tuned_parameters)
    print '开始搜索'
    showlog = showlog+'开始搜索'+'\n'
    clf.fit(X_train, y_train)
    print '搜索结束'
    showlog = showlog+'搜索结束'+'\n'

    print "在参数集上搜索得到的最佳参数组合为:"
    showlog = showlog + '在参数集上搜索得到的最佳参数组合为' + '\n'
    print clf.best_params_
    showlog = showlog + '%r' % (clf.best_params_) + '\n'
    print "在参数集上每个参数组合得得分为:"
    showlog = showlog + '在参数集上每个参数组合得得分为' + '\n'
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']


    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params)
        showlog = showlog+"%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params)+'\n'


    show_panel = snb.show_panel
    csw = snb.sw
    csw.text_ctrl.SetValue(showlog)
    show_panel.Layout()
    # print '最优值对应得预测输出:'
    # print clf.predict(best_p)
    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)
    plt.plot(y_pred, 'r')
    plt.plot(y_test, 'g')
    plt.plot(best_pred, 'b.')
    plt.show()






    # X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size=.4, random_state=0)
    #
    # gpr = GaussianProcessRegressor(alpha=cus_alpha).fit(X_train, y_train)
    #
    # y_predict = gpr.predict(X_test)
    #
    # plt.plot(y_train, 'r')
    # plt.plot(y_predict, 'b')
    # plt.plot(y_test, 'g')
    # plt.show()

    return clf

def buildKRR(snb, test_cog_p, test_inh_p, test_output, test_input):#, cus_n_iter, cus_tol ):
    # print("Bayes建模方法，iter：%d，tol：%d"%(cus_n_iter, cus_tol))
    print('认知不确定参数矩阵:')
    print(test_cog_p)
    print('固有不确定参数')
    print(test_inh_p)
    print('参考输入:')
    print(test_input)
    print('参考输出矩阵:')
    print(test_output)
    print('对比输入:')
    print(test_cmp_input)
    print('对比输出矩阵')
    print(test_cmp_output)
    y_v = double_loop.outer_level_loop(test_cog_p, test_inh_p, test_output, test_input)  # 运行仿真系统获得输出向量，即马氏距离的向量  该输出和认知不确定参数Es_p共同构成训练数据集
    y_va = numpy.array(y_v)
    print('训练输出:')
    print(y_va)

    print('最佳参数取值对应输出:')
    best_p = numpy.mat([[4, 1, 8]])
    y_vaa = double_loop.outer_level_loop(best_p, test_inh_p, test_output, test_input)
    print(y_vaa)

    test_cog_pa = numpy.array(test_cog_p)

    # X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size=.4, random_state=0)
    # bayes = linear_model.BayesianRidge(n_iter=cus_n_iter, tol=cus_tol).fit(X_train, y_train)
    #
    # print 'score:'
    # print bayes.score(X_test, y_test)

    tuned_parameters = [{'kernel' : ['linear', 'rbf', 'laplacian', 'sigmoid'],
                         'alpha' : [1, 0.0001, 0.00001, 1E-6, 1E-7, 1E-8, 0],
                         "gamma": numpy.logspace(-2, 2, 5)
                         }]
    X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size=0.5, random_state=0)
    showlog = ''
    print "建立超参数搜索模型"
    showlog = showlog + '建立超参数搜索模型' + '\n'

    clf = GridSearchCV(KRR(), tuned_parameters)
    print '开始搜索'
    showlog = showlog + '开始搜索' + '\n'
    clf.fit(X_train, y_train)
    print '搜索结束'
    showlog = showlog + '搜索结束' + '\n'

    print "在参数集上搜索得到的最佳参数组合为:"
    showlog = showlog + '在参数集上搜索得到的最佳参数组合为' + '\n'
    print clf.best_params_
    showlog = showlog + '%r' % (clf.best_params_) + '\n'
    print "在参数集上每个参数组合得得分为:"
    showlog = showlog + '在参数集上每个参数组合得得分为' + '\n'
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']

    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params)
        showlog = showlog + "%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params) + '\n'

    show_panel = snb.show_panel
    csw = snb.sw
    csw.text_ctrl.SetValue(showlog)
    show_panel.Layout()

    # print '最优值对应得预测输出:'
    # print clf.predict(best_p)
    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)
    plt.plot(y_pred, 'r')
    plt.plot(y_test, 'g')
    plt.plot(best_pred, 'b.')
    plt.show()





    # X_train, X_test, y_train, y_test = train_test_split(test_cog_pa, y_va, test_size=.4, random_state=0)
    #
    # bayes = linear_model.BayesianRidge(n_iter=cus_n_iter, tol=cus_tol).fit(X_train, y_train)
    #
    # y_predict = bayes.predict(X_test)
    #
    # plt.plot(y_train, 'r')
    # plt.plot(y_predict, 'b')
    # plt.plot(y_test, 'g')
    # plt.show()
    return clf