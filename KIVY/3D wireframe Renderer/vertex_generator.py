def cuboid(center, length):
    x, y, z = center
    vertex_list = []
    l1, l2, l3 = length
    l1 = l1 // 2
    l2 = l2 // 2
    l3 = l3 // 2

    for i in (-l1, l1):
        for j in (-l2, l2):
            for k in (-l3, l3):
                vertex_list.append((x + i, y + j, z + k))

    edge_list = ((0, 2), (2, 3), (3, 7), (5, 7), (1, 5), (1, 3), (2, 6), (6, 7), (4, 6), (4, 5), (0, 4), (0, 1))
    return vertex_list, edge_list, list(center)
