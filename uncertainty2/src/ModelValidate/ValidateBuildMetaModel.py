# -*- coding: utf-8 -*-
import numpy
import ValidateRealModel as rm
import ValidateDoubleLoop
from sklearn import svm
from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.kernel_ridge import KernelRidge as KRR
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.gaussian_process.kernels import (RBF, Matern, RationalQuadratic,
                                              ExpSineSquared, DotProduct,
                                              ConstantKernel)
import ValidateGetSample as gs
import ValidateUi as cp

cog_p_all = 0
cog_p = 0
inh_p = 0
input_v = 0
input_v1 = 0
input_v2 = 0
output1 = 0
output2 = 0

def importData(snb, n_id):
    global cog_p_all
    global cog_p
    global inh_p
    global input_v
    global input_v1
    global input_v2
    global output1
    global output2

    cog_p_all = gs.get_samp(nid = n_id, arg_type=2)   # 根据你选择的模型导入相应的数据
    inh_p = gs.get_samp(nid = n_id, arg_type=1)
    input_v = gs.get_samp(nid = n_id, arg_type=0)

    cog_p = cog_p_all[0:200, :]

    shape = input_v.shape
    d1 = shape[0]/3
    input_v1 = input_v[0:d1*2, :]
    input_v2 = input_v[d1*2:, :]

    output1 = rm.run_real_model(inh_p, input_v1)
    output2 = rm.run_real_model(inh_p, input_v2)

    show_log = ''

    show_log = show_log + str(cog_p_all.shape) + '\n'
    print '认知不确定参数:'
    show_log = show_log + '认知不确定参数' + '\n'
    print cog_p.shape
    show_log = show_log + str(cog_p.shape) + '\n'
    print cog_p
    show_log = show_log + '%r'%(cog_p) + '\n'
    print '固有不确定参数:'
    show_log = show_log + '固有不确定参数:' + '\n'
    print inh_p.shape
    show_log = show_log + str(inh_p.shape) + '\n'
    print inh_p
    show_log = show_log + '%r'%(inh_p) + '\n'
   #print '训练输入:'
   # show_log = show_log + '训练输入:' + '\n'
   # print input_v1.shape
   # show_log = show_log + str(input_v1.shape) + '\n'
   # print input_v1
  #  show_log = show_log + '%r'%(input_v1) + '\n'
  #  print '对比输入:'
   # show_log = show_log + '对比输入:' + '\n'
   # print input_v2.shape
    #show_log = show_log + str(input_v2.shape) + '\n'
   # print input_v2
   # show_log = show_log + '%r'%(input_v2) + '\n'
    print '训练输出:'
    show_log = show_log + '训练输出:' + '\n'
    print output1.shape
    show_log = show_log + str(output1.shape) + '\n'
    print output1
    show_log = show_log + '%r'%(output1) + '\n'
    print '对比输出:'
    show_log = show_log + '对比输出:' + '\n'
    print output2.shape
    show_log = show_log + str(output2.shape) + '\n'
    print output2
    show_log = show_log + '%r'%(output2) + '\n'

    show_panel = snb.panel_import
    csw = snb.sw
    csw.text_ctrl.SetValue(show_log)
    show_panel.Layout()
    return output1.shape,output2.shape



if __name__ == '__main__':
    aa= importData()
    print (aa[0])

def buildSVR(snb, cog_p, inh_p, output1, input_v1):
    y_v = DoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    y_va = numpy.array(y_v)
    print('一致性度量输出:')
    print(y_va)
    print('最佳参数取值对应的实际输出:')
    best_p = numpy.mat([[4, 1, 8]])
    y_vaa = DoubleLoop.outer_level_loop(best_p, inh_p, output1, input_v1)
    print(y_vaa)

    cog_pa = numpy.array(cog_p)
    tuned_parameters = [{'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                         'gamma': ['auto', 0.1, 0.001, 0.0001],
                         'C': [1, 10, 100, 1000],
                         'epsilon': [0.1, 0.001, 1],
                         }]

    X_train, X_test, y_train, y_test = train_test_split(cog_pa, y_va, test_size=0.5, random_state=0)
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

    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)
    plt.plot(y_pred, 'r')
    plt.plot(y_test, 'g')
    plt.plot(best_pred, 'b.')
    plt.show()
    return clf

def buildGPR(snb, cog_p, inh_p, output1, input_v1):
    y_v = DoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    y_va = numpy.array(y_v)
    print('一致性度量输出:')
    print(y_va)
    print('最佳参数取值对应的实际输出:')
    best_p = numpy.mat([[4, 1, 8]])
    y_vaa = DoubleLoop.outer_level_loop(best_p, inh_p, output1, input_v1)
    print(y_vaa)

    cog_pa = numpy.array(cog_p)
    tuned_parameters = [{'kernel': [1.0 * RBF(length_scale=1.0, length_scale_bounds=(1e-1, 10.0)),
                                    1.0 * RationalQuadratic(length_scale=1.0, alpha=0.1),
                                    # 1.0 * ExpSineSquared(length_scale=1.0, periodicity=3.0,
                                    #     length_scale_bounds=(0.1, 10.0),
                                    #     periodicity_bounds=(1.0, 10.0)),
                                    ConstantKernel(0.1, (0.01, 10.0))
                                    * (DotProduct(sigma_0=1.0, sigma_0_bounds=(0.0, 10.0)) ** 2),
                                    1.0 * Matern(length_scale=1.0, length_scale_bounds=(1e-1, 10.0), nu=1.5)],
                         'alpha': [1E-10, 0.1, 1]
                         }]

    X_train, X_test, y_train, y_test = train_test_split(cog_pa, y_va, test_size=0.5, random_state=0)
    showlog = ''
    print "建立超参数搜索模型"
    showlog = showlog + '建立超参数搜索模型' + '\n'
    clf = GridSearchCV(GPR(), tuned_parameters)

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

    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)
    plt.plot(y_pred, 'r')
    plt.plot(y_test, 'g')
    plt.plot(best_pred, 'b.')
    plt.show()
    return clf

def buildKRR(snb, cog_p, inh_p, output1, input_v1):
    y_v = DoubleLoop.outer_level_loop(cog_p, inh_p, output1, input_v1)
    y_va = numpy.array(y_v)
    print('一致性度量输出:')
    print(y_va)
    print('最佳参数取值对应的实际输出:')
    best_p = numpy.mat([[4, 1, 8]])
    y_vaa = DoubleLoop.outer_level_loop(best_p, inh_p, output1, input_v1)
    print(y_vaa)

    cog_pa = numpy.array(cog_p)
    tuned_parameters = [{'kernel': ['linear', 'rbf', 'laplacian', 'sigmoid'],
                         'alpha': [1, 0.0001, 0.00001, 1E-6, 1E-7, 1E-8, 0],
                         "gamma": numpy.logspace(-2, 2, 5)
                         }]

    X_train, X_test, y_train, y_test = train_test_split(cog_pa, y_va, test_size=0.5, random_state=0)
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

    best_pred = clf.predict(best_p)

    y_pred = clf.predict(X_test)
    plt.plot(y_pred, 'r')
    plt.plot(y_test, 'g')
    plt.plot(best_pred, 'b.')
    plt.show()
    return clf
