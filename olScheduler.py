import json
from LRUCache import ContainerCache
from config import MAX_CONTAINER_NUM, MACHINE_NUM, DEPENDENCY_NUM, CLOUD_FUNCTION_NUM

MD = DEPENDENCY_NUM / MACHINE_NUM
# 保存了每个机器有哪些容器
machines = [ContainerCache(MAX_CONTAINER_NUM)] * MACHINE_NUM
# 保存了每个容器在哪些机器
func_machines = [[]] * CLOUD_FUNCTION_NUM
# 每个机器的负载情况
mloads = [0] * MACHINE_NUM

# functions_dep记录了每个函数的所有依赖
with open('./data/functions_dep.json', 'r') as f:
    functions_dep = json.load(f)
# subsets预计算了每个云函数的子集云函数
with open('./data/sorted_subsets.json', 'r') as f:
    subsets = json.load(f)


def handleSubOrNone(machine, base, target):
    cc = machines[machine]
    hit, deleted = cc.handleNone(target) if base is None else cc.handleSubInter(target)
    func_machines[int(target[1:])] = [machine]
    if deleted is not None:
        func_machines[int(deleted[1:])] = []


def handleRequest(req):
    # 根据最大的依赖来确定机器位置, tm是选中机器的id
    tm = functions_dep[req][0] % MACHINE_NUM
    if len(functions_dep[req]) > 1:
        tm1 = functions_dep[req][1] % MACHINE_NUM
        if mloads[tm1] < mloads[tm]:
            tm = tm1
    # 机器负载加一
    mloads[tm] += 1
    # cc即为选中的机器
    cc = machines[tm]
    # 1. 直接命中率
    if req in cc.cache:
        cc.handleHit(req)
        return 0, req + ' okay'
    # 2. 尝试子集命中
    elif req in subsets:
        subs = subsets[req]
        for sub in subs:
            sf = sub[1]
            if tm in func_machines[int(sf[1:])]:
                handleSubOrNone(tm, sf, req)
                return 1, sub[1]
        handleSubOrNone(tm, None, req)
        return 2, req + ' nope 2'
    else:
        handleSubOrNone(tm, None, req)
        return 3, req + ' nope 3'


if __name__ == '__main__':
    with open('data/functions_dep.json', 'r') as fd:
        functions_dep = json.load(fd)

    num = [0, 0, 0, 0]
    dep_saving, dep_rate = 0, 0
    with open('data/function_request.txt') as f:
        requests = f.readlines()
        for r in requests:
            tmp = handleRequest(r[:-1])
            num[tmp[0]] += 1
            if tmp[0] == 1:
                dep_saving += len(functions_dep[tmp[1]])
                dep_rate += (len(functions_dep[tmp[1]]) / len(functions_dep[r[:-1]]))

        print(num[0])
        print(num[1])
        print(num[2])
        print(num[1] / 25007596)
        print((num[0] + num[1]) / 25007596)
        print(dep_saving)
        print(dep_rate)
        print(dep_saving / num[1])
        print(dep_rate / num[1])

        print("\n machine loads:")
        mloads = [str(m) for m in mloads]
        print(", ".join(mloads))

# -----> 100
# 663741
# 3932921
# 20361106
# 49828
#
#  machine loads:
# 2699928
# 2699927
# 2699927
# 2699927
# 2699928
# 2681257
# 2563552
# 2283991
# 2112517
# 1866642

# -----> 200
# 1324732
# 6938283
# 16696096
# 48485
#
#  machine loads:
# 2699928
# 2699927
# 2699927
# 2699927
# 2699928
# 2681257
# 2563552
# 2283991
# 2112517
# 1866642

# -----> 300
# 1984158
# 9147712
# 13828591
# 47135
#
#  machine loads:
# 2699928
# 2699927
# 2699927
# 2699927
# 2699928
# 2681257
# 2563552
# 2283991
# 2112517
# 1866642

# -----> 400
# 2640916
# 10768431
# 11552459
# 0.4306064045500415
# 0.5362109576626238
# 19206199
# 1535048.1133817066
# 1.783565219482764
# 0.1425507683878651
#
#  machine loads:
# 2699928, 2699927, 2699927, 2699927, 2699928, 2681257, 2563552, 2283991, 2112517, 1866642