from math import dist


def find_centr(cl):
    e = []
    d0 = float("inf")
    for q1 in cl:
        d = 0
        for q2 in cl:
            d += dist(q1, q2)
        if d < d0:
            d0 = d
            e = q1
    return e


def sr_of_centr(centr):
    s_x, s_y = 0, 0
    for i in range(len(centr)):
        s_x += centr[i][0]
        s_y += centr[i][1]
    return s_x / len(centr) * 10000, s_y / len(centr) * 10000


def num_27(path, distance, t):
    data = [x.split(" ") for x in open(path)]
    if data[0][0] == "X":
        del data[0]
    for _ in range(len(data)):
        for __ in range(len(data[_])):
            data[_][__] = data[_][__].replace(",", ".")
            data[_][__] = float(data[_][__])

    clust = []
    while data:
        clust.append([data.pop()])
        for p1 in clust[-1]:
            for p2 in data[:]:
                if dist(p1, p2) <= distance:
                    clust[-1].append(p2)
                    data.remove(p2)

    centroids = []
    for i in clust:
        centroids.append(find_centr(i))

    if t == "clusters":
        return clust
    elif t == "centroids":
        return centroids
    else:
        return sr_of_centr(centroids)


# e = num_27("27_B_21425 (1).txt", 5, t="")
# print(e)
