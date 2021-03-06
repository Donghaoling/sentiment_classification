__author__ = 'hzdonghaoling'

from svmutil import *

y, x = svm_read_problem('E:/libsvm-3.21/heart_scale')
m = svm_train(y[:200], x[:200], '-c 4')
p_label, p_acc, p_val = svm_predict(y[200:], x[200:], m)
