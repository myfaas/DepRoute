import json
from LRUCache import ContainerCache
from config import MAX_CONTAINER_NUM, MACHINE_NUM, CLOUD_FUNCTION_NUM

# 保存了每个机器有哪些容器，总共有多少容器
machines = [ContainerCache(MAX_CONTAINER_NUM)] * MACHINE_NUM
# 保存了每个容器在哪些机器
func_machines = [[]] * CLOUD_FUNCTION_NUM
# 每个机器的负载情况
mloads = [0] * MACHINE_NUM

# intersection预计算了每个云函数的最大交集
with open('data/intersections.json', 'r') as f:
    intersections = json.load(f)


def handleInterOrNone(machine, base, target):
    cc = machines[machine]
    hit, deleted = cc.handleNone(target) if base is None else cc.handleSubInter(target)
    func_machines[int(target[1:])] = [machine]
    if deleted is not None:
        func_machines[int(deleted[1:])] = []


def handleRequest(req):
    rid = int(req[1:])
    if len(func_machines[rid]) > 0:  # 已经存在可用容器
        assert len(func_machines[rid]) == 1
        tm = func_machines[rid][0]
        mloads[tm] += 1
        machines[tm].handleHit(req)
        return 0, 'okay'
    else:
        for ins in intersections[req]:  # 逐个检查交集云函数
            sub = ins['name']
            if len(func_machines[int(sub[1:])]) > 0:
                tm = func_machines[int(sub[1:])][0]
                mloads[tm] += 1
                handleInterOrNone(tm, sub, req)
                return 1, ins['ins']

    tm, mls = 0, mloads[0]
    for i in range(1, MACHINE_NUM):
        if mloads[i] < mls:
            tm, mls = i, mloads[i]
    mloads[tm] += 1
    handleInterOrNone(tm, None, req)
    return 2, 'nope 1'


if __name__ == '__main__':
    with open('data/functions_dep.json', 'r') as fd:
        functions_dep = json.load(fd)

    num = [0, 0, 0]
    dep_saving, dep_rate = 0, 0
    with open('data/function_request.txt') as f:
        requests = f.readlines()
        for r in requests:
            tmp = handleRequest(r[:-1])
            num[tmp[0]] += 1
            if tmp[0] == 1:
                dep_saving += tmp[1]
                dep_rate += (tmp[1] / len(functions_dep[r[:-1]]))

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
