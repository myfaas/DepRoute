import json
from LRUCache import ContainerCache
from config import MAX_CONTAINER_NUM, MACHINE_NUM


machines = [ContainerCache(MAX_CONTAINER_NUM)] * MACHINE_NUM
# subsets预计算了每个云函数的子集云函数
with open('./data/sorted_subsets.json', 'r') as f:
    subsets = json.load(f)

# def roundRobin(req, index):
#     cc = machines[index]
#     return cc.handle(req)[0]


def roundRobin(req, index):
    cc = machines[index]
    if req in cc.cache:
        cc.handleHit(req)
        return 0, req + ' okay'
    elif req in subsets:
        subs = subsets[req]
        for sub in subs:
            sf = sub[1]
            if sf in cc.cache:
                cc.handleSubInter(req)
                return 1, sf
        return 2, req + ' nope 2'
    else:
        cc.handleNone(req)
        return 3, req + ' nope 3'


if __name__ == '__main__':
    with open('data/functions_dep.json', 'r') as fd:
        functions_dep = json.load(fd)

    num = [0, 0, 0, 0]
    dep_saving, dep_rate = 0, 0
    with open('./data/function_request.txt') as f:
        requests, i = f.readlines(), 0
        for r in requests:
            tmp = roundRobin(r[:-1], i)
            i = (i + 1) % MACHINE_NUM
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

# -- 10 machines + 100 containers
# 663146
# 4386321
# 19910643
# 47486

# -- 10 machines + 200 containers
# 1321734
# 6586992
# 17053968
# 44902

#  -- 10 machines + 400 containers
# 1973259
# 7910127
# 15081425
# 42785

#  -- 10 machines + 400 containers
# 2620224
# 8780650
# 13565740
# 40982
# 0.3511193159070548
# 0.4558964404255411
# 22394354
# 1272345.7705543234
# 2.5504209825012953
# 0.14490336940366869
