from random import random, randint, shuffle
import json
from config import DEPENDENCY_NUM, CLOUD_FUNCTION_NUM


def genCloudFunction():
    prob = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
    functions, k = {}, 0
    for p in prob:
        per = int(CLOUD_FUNCTION_NUM / len(prob))
        for i in range(per):
            tmp = []
            for d in range(DEPENDENCY_NUM):
                if random() < p:
                    tmp.append(d)
            if len(tmp) == 0:
                tmp = [randint(0, DEPENDENCY_NUM - 1)]
            functions['f' + str(k)] = tmp
            k += 1
    with open('data/functions_dep.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(functions, indent=4, ensure_ascii=False))
    print("functions: done,", len(functions))
    return functions


def genFunctionRequest():
    res = []
    for i in range(CLOUD_FUNCTION_NUM):
        times = randint(10, 10000)
        res += times * ['f' + str(i) + '\n']
    shuffle(res)
    with open('data/function_request.txt', 'w') as f:
        f.writelines(res)
    print("function requests:", len(res))


def genSubSets(functions):
    subsets = {}
    for i in range(0, CLOUD_FUNCTION_NUM):
        tmp = []
        for j in range(0, CLOUD_FUNCTION_NUM):
            fi, fj = functions.get('f' + str(i)), functions.get('f' + str(j))
            if i == j or len(fj) > len(fi):
                continue
            yes = True
            for jj in fj:
                if jj not in fi:
                    yes = False
                    break
            if yes:
                tmp.append('f' + str(j))
        if len(tmp) > 0:
            subsets['f' + str(i)] = tmp

    with open('data/subsets.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(subsets, indent=4, ensure_ascii=False))


def genSortedSubSets(functions):
    subsets = {}
    for i in range(0, CLOUD_FUNCTION_NUM):
        tmp = []
        for j in range(0, CLOUD_FUNCTION_NUM):
            fi, fj = functions.get('f' + str(i)), functions.get('f' + str(j))
            if i == j or len(fj) > len(fi):
                continue
            yes = True
            for jj in fj:
                if jj not in fi:
                    yes = False
                    break
            if yes:
                tmp.append((len(functions.get('f' + str(j))), 'f' + str(j)))
        if len(tmp) > 0:
            subsets['f' + str(i)] = sorted(tmp, reverse=True)

    with open('data/sorted_subsets.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(subsets, indent=4, ensure_ascii=False))


def genIntersection(functions):
    intersections = {}
    for i in range(0, CLOUD_FUNCTION_NUM):
        tmp = []
        for j in range(0, CLOUD_FUNCTION_NUM):
            fi, fj = functions.get('f' + str(i)), functions.get('f' + str(j))
            if i == j:
                continue
            ins = 0
            for jj in fj:
                if jj in fi:
                    ins += 1
            if ins > 0:
                tmp.append({"ins": ins, "len": len(functions.get('f' + str(j))), "name": 'f' + str(j)})
        smp = sorted(tmp,  key=lambda x: (-x['ins'], x['len']))[:50]
        intersections['f' + str(i)] = smp

    with open('data/intersections.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(intersections, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    # func = genCloudFunction()
    # genFunctionRequest()
    # genSubSets(func)

    # with open('data/functions_dep.json', 'r') as fd:
    #     func = json.load(fd)
    # genSortedSubSets(func)

    with open('data/functions_dep.json', 'r') as fd:
        func = json.load(fd)
    genIntersection(func)
