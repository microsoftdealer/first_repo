import copy

def draw_matrix(matrix):
    for row in matrix:
        print(row)

def count_quads(matrix_raw):
    r = 0
    t = 0
    matrix = copy.deepcopy(matrix_raw)
    quad_counter = 0
    length = len(matrix) * len(matrix[0])
    for sym in range(length):
        if matrix[r][t] == 0:
            pass
        else:
            quad_counter += 1
            wide, height = def_quad_size(matrix, r, t)
            matrix = zeroize_quad(matrix, wide, height, r, t)
        t += 1
        if t >= len(matrix[0]):
            t = 0
            r += 1
    draw_matrix(matrix_raw)
    print(f'Number of quads in matrix is equal to {quad_counter}')
    return quad_counter

def def_quad_size(matrix, r, t):
    wide = check_right(matrix, r, t)
    poss_height = []
    for num in range(wide):
        poss_height.append(check_down(matrix,r,t))
        t += 1
    height = min(poss_height)
    return wide, height

def zeroize_quad(matrix, wide, height, r, t, zeroize=True):
    for row in matrix[r:r+height]:
        temp_t = t
        for val in row[t:t+wide]:
            if zeroize:
                matrix[r][temp_t] = 0
            else:
                matrix[r][temp_t] = 1
            temp_t += 1
        r += 1
    return matrix

def check_right(matrix, r, t, wide=0):
    wide += 1
    t += 1
    if t >= len(matrix[0]):
        return wide
    if matrix[r][t] == 1:
        return check_right(matrix, r, t, wide=wide)
    else:
        return wide

def check_down(matrix, r, t, height=0):
    if r + 1 > len(matrix):
        return height
    elif matrix[r][t] == 1:
        r += 1
        height += 1
        return check_down(matrix, r, t, height=height)
    else:
        return height

if __name__ == "__main__":
    matr = [[1,0,1,1,0,1],
            [0,0,1,1,0,0],
            [1,0,0,1,0,1],
            [1,0,1,1,0,1]]
    print(count_quads(matr))