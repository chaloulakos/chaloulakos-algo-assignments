from sys import argv

method = argv[1]
input_filename = argv[2]

input = open(input_filename, 'r').read().strip()
input = input.split()
input = list(map(int, input))
input = sorted(input)

groups = [[x] for x in input]

d = []
for group in input:
    distances = []
    for g2 in input:
        distances.append(abs(group-g2))
    d.append(distances)

def get_groups_to_merge(d):
    s, t = None, None
    for i in range(len(d)):
        for j in range(len(d[0])):
            if d[i][j] != 0 and (s is None or d[i][j] < d[s][t]):
                s = i
                t = j
    return s, t, d[s][t]


def get_coefficients(s, t, v, method):
    c = [
        [0.5,0.5,0,-0.5],
        [0.5,0.5,0,0.5],
        [len(s)/(len(s)+len(t)), len(t)/(len(s)+len(t)),0,0],
        [(len(s)+len(v))/(len(s)+len(t)+len(v)),(len(v)+len(t))/(len(s)+len(t)+len(v)),-len(v)/(len(s)+len(t)+len(v)), 0]
    ]
    if method == "single":
        return c[0]
    if method == "complete":
        return c[1]
    if method == "average":
        return c[2]
    return c[3]


while len(groups) > 1:
    s_index, t_index, dist = get_groups_to_merge(d)
    s = groups[s_index]
    t = groups[t_index]
    new_group = s + t

    print(str(tuple(s)).replace(',',''), str(tuple(t)).replace(',',''), "{:.2f}".format(dist), len(new_group))

    groups[s_index] = new_group
    del groups[t_index]

    new_d = []
    for row in d:
        new_row = []
        for el in row:
            new_row.append(el)
        new_d.append(new_row)

    del new_d[t_index]
    for row in new_d:
        del row[t_index]

    for v in range(len(groups)):
        if v == s_index:
            new_d[v][v] = 0
        else:
            c = get_coefficients(s, t, groups[v], method)
            i = v
            if i >= t_index:
                i += 1
            new_distance = c[0]*d[s_index][i] + c[1]*d[t_index][i] + c[2]*dist + c[3] * abs(d[s_index][i]-d[t_index][i])
            new_d[v][s_index] = new_distance
            new_d[s_index][v] = new_distance
    d = new_d


