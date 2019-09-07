def rotate_matrix(matrix):
     rotated_matrix = list(zip(*matrix))[::-1]
     rotated_matrix = [list(elem) for elem in rotated_matrix]
     return rotated_matrix


def generate_spin_matrix(side):
     list_of_elements = [elem for elem in range(1, side ** 2 + 1)]
     matrix = [[0 for o in range(side)] for o in range(side)]
     write_row_counter = 0
     write_elem_counter = 0
     r = 0
     s = 0
     delta_s = 0
     #  delta_r = 0
     for num in list_of_elements:
          matrix[r][s] = num
          s += 1
          write_elem_counter += 1
          if write_elem_counter == side:
              matrix = rotate_matrix(matrix)
              s = delta_s + 1
              write_elem_counter = 0
              write_row_counter += 1
              if write_row_counter % 2 == 1:
                  side -= 1
              elif write_row_counter % 4 == 0:
                  r += 1
                  delta_s += 1

     while matrix[0][0] != 1:
         matrix = rotate_matrix(matrix)

     return matrix

if __name__ == "__main__":
    print(generate_spin_matrix(5))
