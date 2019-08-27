
def dif_list(list1, list2):
        num_l = 0
        num_r = 0
        not_last = True
        while True:
            if list1[num_l] == list2[num_r]:
               print('"' + list1[num_l] + '" SAME "' + list2[num_r] + '"')
               num_l += 1
               num_r += 1
            elif list1[num_l] not in list2:
               print('"' + list1[num_l] + '" REMOVED')
               num_l += 1
            elif list2[num_r] not in list1:
               print(f'"{list2[num_r]}" ADDED')
               num_r +=1
            else:
                print(f'"{list1[num_l]}" REMOVED\n'
                      f'"{list2[num_r]}" ADDED' )
                num_l +=1
                num_r +=1
            if num_l == len(list1):
                if num_r != len(list2) - 1:
                    for val in list2[num_r:]:
                        print(f'"{list2[num_r]}" ADDED')
                        num_r += 1
                    else:
                        break
                else:
                    break

if __name__ == "__main__":
    list1 = ['1', '2', '3', '4', '5', '1', '2', '3', '1', '2', '3']
    list2 = ['1', '3', '5', '0', '1', '3','3','3', '3','3','3']
    dif_list(list1, list2)