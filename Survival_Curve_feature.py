from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import lifelines
from lifelines import CoxPHFitter  # 导入Cox包
from lifelines import KaplanMeierFitter
from lifelines.plotting import add_at_risk_counts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# 计算多元对数秩检验——生存分析是否具有差异性
# 在零假设下，所有组具有相同的生存函数。在所有变量都具有相同生存函数的情况下，计算多元对数秩检验，以在“生存”的生存数据中以“ y”定义的组之间的差异生存。（即测试至少一组是否具有不同的生存率）
def multivariate_logrank_test(data_df, labels):
    log_rank_model = lifelines.statistics.multivariate_logrank_test(
        data_df['times'],
        labels,
        data_df['status']
    )
    return round(log_rank_model.test_statistic, 3), round(log_rank_model.p_value, 3)


class Survival_Curve_feature():
    def __init__(self, duration_column='times', observed_column='status'):
        # self.path = None
        self.duration_column = duration_column
        self.observed_column = observed_column

        self.data_df = None
        self.feature_survival = None

        self.test_statistic = 0.0  # 各组的生存差异stat值（生存曲线中的取值）
        self.p_value = 0.0  # 各组的生存差异p值（生存曲线中的取值）
        self.median_survival_time = {}  # 以字典的形式存储中位生存时间
        self.survival_rate_result = None  # 存储不同组之间的生存率结果（不同月）

        self.cox_report_for_HR = None  # 输出Cox-PH对分组后的HR值
        self.HR = 0.0  # 获取HR风险率
        self.CI = []  # 获取置信区间

    def read_data_cox(self, path, features_name):
        self.data_df = pd.DataFrame(pd.read_csv(path))
        self.feature_survival = pd.DataFrame(pd.concat(
            [self.data_df[self.duration_column], self.data_df[self.observed_column], self.data_df[features_name]],
            axis=1))

    # 生存曲线
    def estimate_kaplan_meier(self, features_name):
        labels = self.feature_survival[features_name]  # 将data_label的DataFrame格式转化为Series格式
        sfs = {}
        # 画生存曲线图
        # plt.figure(1)
        ax = plt.subplot()
        fitter = []

        for label in sorted(labels.unique()):
            data_label_index = list(set(labels[labels == label].index) & set(self.feature_survival.index))
            kmf = KaplanMeierFitter()
            kmf.fit(
                self.feature_survival.loc[data_label_index][self.duration_column],
                self.feature_survival.loc[data_label_index][self.observed_column],
                label=label
            )
            # 将每一个训练的kmf放入fitter中存储，用于画出每个标签的对应的时间的生存人数
            fitter.append(kmf)

            sfs[label] = kmf.survival_function_  # 得到每个标签的生存率
            self.median_survival_time[label] = kmf.median_

            ax = kmf.plot(ax=ax)  # 画生存曲线图

        # 画对应时间的生存人数
        add_at_risk_counts(*fitter)
        # 计算log_rank值看分组的生存差异是否显著
        self.test_statistic, self.p_value = multivariate_logrank_test(self.feature_survival, labels)
        if self.p_value == 0:
            self.p_value = '< 0.001'
            p_transform = True
        else:
            self.p_value = str(self.p_value)
            p_transform = False
        # 输出所有组的生存率
        self.survival_rate_result = pd.concat([sfs[k] for k in list(sorted(labels.unique()))], axis=1).interpolate()
        if len(self.CI) > 0:
            # 在图中显示log_rank中p值
            if p_transform == False:
                ax.text(0.35, 0.8, 'log_rank p=%s' % self.p_value, transform=ax.transAxes, va='top', fontsize=12)
                ax.text(0.35, 0.9, "HR=%.3f(95%% CI:%.3f-%.3f)" % (self.HR, self.CI[0], self.CI[1]), transform=ax.transAxes,
                        va='top', fontsize=12)
            else:
                ax.text(0.35, 0.8, 'log_rank p %s' % self.p_value, transform=ax.transAxes, va='top', fontsize=12)
                ax.text(0.35, 0.9, "HR=%.3f(95%% CI:%.3f-%.3f)" % (self.HR, self.CI[0], self.CI[1]), transform=ax.transAxes,
                        va='top', fontsize=12)
        else:
            # 在图中显示log_rank中p值
            ax.text(0.35, 0.8, 'log_rank p=%s' % self.p_value, transform=ax.transAxes, va='top', fontsize=12)
        plt.title('Full Data')
        print("Median survival time of data: %s" %self.median_survival_time)
        plt.show()

    #         return test_statistic, p_value, median_survival_time, survival_rate_result

    # Cox-PH模型根据已知的分组作为特征计算HR值和置信区间（带标签的总数据）
    def Cox_Label_HR(self):
        cph = CoxPHFitter()
        try:
            cph.fit(self.feature_survival, self.duration_column, event_col=self.observed_column)
            self.cox_report_for_HR = cph.print_summary()
            self.HR = cph.hazard_ratios_[0]
            self.CI = cph.confidence_intervals_.values[0]
        #         return cph.print_summary()
        except:
            print("The truncation has problem. ")