# 得到标签y_hat
# 根据silhouette（互信息有真实标签时）或silhouette（无序真实标签）的值来确定K，并通过KMeans方法得到预测的类别yhat和取不同K时所得的scores
import numpy as np
import pandas as pd
import warnings
from sklearn.metrics import adjusted_mutual_info_score
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import lifelines
from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter
from lifelines.plotting import add_at_risk_counts
from lifelines import utils
import matplotlib.pyplot as plt
import winreg
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return (winreg.QueryValueEx(key, "Desktop")[0])


the_user_desktop = get_desktop()

# 在零假设下，所有组具有相同的生存函数。在所有变量都具有相同生存函数的情况下，计算多元对数秩检验，以在“生存”的生存数据中以“ y”定义的组之间的差异生存。（即测试至少一组是否具有不同的生存率）
def multivariate_logrank_test(yhat_final, time_cluster_label, duration_column="time", observed_column="status"):
    data_index = list(set(yhat_final.index) & set(time_cluster_label.index))
    log_rank_model = lifelines.statistics.multivariate_logrank_test(
        time_cluster_label.loc[data_index][duration_column],
        yhat_final.loc[data_index],
        time_cluster_label.loc[data_index][observed_column],
    )
    return round(log_rank_model.test_statistic, 3), round(log_rank_model.p_value, 3)



class K_Means_Class(object):
    def __init__(self, select_features_data):
        self.select_features_data = select_features_data   # 带有time,status,特征筛选后的特征的数据(如若有标签需用户添加标签)
        self.yhat_final = None  # K_Means聚类得到的标签，只有标签
        self.time_cluster_label = None   # 带有time，status的label
        self.kmeans_scores = None  # 记录sillute方法的score
        self.test_statistic = 0.0
        self.p_value = 0.0
        self.median_survival_time = {}  # 以字典的形式存储中位生存时间
        self.survival_rate_result = None
    def cluster(self,
                seed=1234,
                k=None,
                optimal_k_method="silhouette",
                ami_y=None,
                kmeans_kwargs=None
                ):
        '''
        输入：带有time,status,特征筛选后的特征的数据(如若有标签需用户添加标签)
        输出：带有time,status,label的相结合的数据
        '''
        # 输出只包含筛选的特征的数据
        z = self.select_features_data.drop(['times', 'status'], axis=1)
        # z = self.select_features_data[2:]
        if kmeans_kwargs is None:
            kmeans_kwargs = {"n_init": 1000, "n_jobs": 2}
        if k is not None:
            self.yhat_final1 = pd.Series(KMeans(k, **kmeans_kwargs, random_state=seed).fit_predict(z), index=z.index)
            # 对得到的标签进行生存分析
            # 带有time,status,label的相结合的数据
            self.yhat_final1 = pd.DataFrame(self.yhat_final1)
            self.yhat_final1.columns = ['label']
            self.time_cluster_label = pd.DataFrame(
                pd.concat([self.select_features_data['times'], self.select_features_data['status'], self.yhat_final1],
                          axis=1))
            path = the_user_desktop + '\\user_set_time_label.csv'
            self.time_cluster_label.to_csv(path)
#             return self.yhat_final
        else:
            if optimal_k_method == "ami":
                ami_y = self.select_features_data['ami_label']
                z_to_use = z.loc[pd.DataFrame(ami_y).index]
                scorer = lambda yhat: adjusted_mutual_info_score(ami_y, yhat)

            elif optimal_k_method == "silhouette":
                z_to_use = z
                scorer = lambda yhat: silhouette_score(z_to_use, yhat)
            # 输出k不同取值时kmeans聚类得到的yhat结果
            yhats = {
                k: pd.Series(
                    KMeans(k, **kmeans_kwargs, random_state=seed).fit_predict(z_to_use),
                    index=z_to_use.index,
                )
                for k in range(3, 10)
            }

            # 输出k不同取值时的kmeans_scores得分情况（分越高越好）,index为k的取值
            self.kmeans_scores = pd.Series(
                [scorer(yhats[k]) for k in range(3, 10)],
                index=range(3, 10),
                name=optimal_k_method,

            )
            self.kmeans_scores.index.name = "K"  # index名字为k
            optimal_k = np.argmax(self.kmeans_scores)  # 输出scores值最大的索引index也就是k的取值
            self.yhat_final2 = yhats[optimal_k]
            # 对kmeans_scores进行绘图（根据AMI互信息）
            plt.plot(self.kmeans_scores)
            plt.ylabel("silhouette")
            plt.title("silhouette find K")
            plt.show()
            # return self.yhat_final, self.kmeans_scores
            # 对得到的标签进行生存分析
            # 带有time,status,label的相结合的数据
            self.yhat_final2 = pd.DataFrame(self.yhat_final2)
            self.yhat_final2.columns = ['label']
            self.time_cluster_label = pd.DataFrame(
                pd.concat([self.select_features_data['times'], self.select_features_data['status'], self.yhat_final2],
                          axis=1))
            path = the_user_desktop + '\\system_set_time_label.csv'
            self.time_cluster_label.to_csv(path)
        # return self.time_cluster_label

