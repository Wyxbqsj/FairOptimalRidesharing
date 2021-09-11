month = 7
day = 28
data_path = "D:/ExperimentData/raw_data/%02d/%d.csv" % (month, day)
# 随机种子
seed = 71437

# 司机数量
driverCount = 4000

# 司机速度

# 派单间隔
fragment = 60
# 算法
algorithm = "random"

bigDistance = 0.01271 * 3
#
takeTime = 60 * 3

# 区域分割
regionx = 10
regiony = 10


XREGION = (-74.01, -73.93)
YREGION = (40.70, 40.92)
# 折扣率
discount = 0.8
learningRate = 0.1



# 模型
modelType = "BasicNetwork"
# 是否策略评估
EVALUATE = True

