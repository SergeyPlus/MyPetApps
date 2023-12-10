import random

list = [random.randint(0, 20) for _ in range(10)]


def bubble_bubble(list):
    # first edition
    for number in range(1, len(list)):
        for index in range(len(list) - number):

            if list[index] > list[index + 1]:
                list[index], list[index + 1] = list[index + 1], list[index]

    return list


def bubble_sort_2(list):

    flag = True
    while flag:
        flag = False

        for i in range(len(list) - 1):
            if list[i] > list[i + 1]:
                flag = True
                list[i], list[i + 1] = list[i + 1], list[i]
    print('Сортировка пузырьком (метод 2)', list)


def insert_sort(list):
    """
    The function starts with diapason of integers as len == 2 and further increase diapason.
    If we meet smallest integer we put it in the first position.

    :param list:
    :return:
    """
    for i_number in range(1, len(list)):
        while i_number > 0 and list[i_number] < list[i_number - 1]:
            list[i_number - 1], list[i_number] = list[i_number], list[i_number - 1]
            i_number -= 1

    return list


def choice_sort(list):
    """The function searchs for the smallest digit compare with interate number in the list(iteration starts
        since second digit.
    """
    for i_index in range(0, len(list) - 1):
        #print('Летит число: ', list[i_index])
        for index in range(i_index + 1, len(list)):
            if list[i_index] > list[index]:
                list[i_index], list[index] = list[index], list[i_index]
  

    return list


list_for_bubble = list[:]
bubble_list = bubble_bubble(list_for_bubble)

list_for_bubble_2 = list[:]
bubble_sort_2(list_for_bubble_2)

list_for_insert = list[:]
insert_list = insert_sort(list_for_insert)

list_for_choice = list[:]
choice_list = choice_sort(list_for_choice)

print('Первоначальный список: {0}'
      '\nРезультаты сортировок: \n'
      '     Сортировка пузырьком:   {1}\n'
      '     Сортировка вставкой:    {2}\n'
      '     Сортировка выбором:     {3}\n'.format(
    list,
    bubble_list,
    insert_list,
    choice_list
))


 # hoar sort
def hoar_sort(l):

    if len(l) <= 1:
        return l
  
    bas_elem = l[0]
    left_l = [elem for elem in l if bas_elem > elem]
    right_l = [elem for elem in l if bas_elem < elem]
    mid_l = [elem for elem in l if bas_elem == elem]
    
    return hoar_sort(left_l) + mid_l + hoar_sort(right_l)
 
list_not_sort = [random.randint(-10, 10) for _ in range(10)]
result = hoar_sort(list_not_sort)
 
print('Неотсортированный список: {},\nОтсортированный список: {}'.format(list_not_sort, result))
 

 # merge sort
def lists_sort(L1, L2):

    final_list = []
    index_1 = 0
    index_2 = 0
    while len(L1) > index_1 and len(L2) > index_2:
        
        if L1[index_1] > L2[index_2]:
            final_list.append(L2[index_2])
            index_2 += 1
 
        else:
            final_list.append(L1[index_1])
            index_1 += 1
 
    final_list += L1[index_1: ] + L2[index_2: ]
    return final_list


def merge_sort(unsort_list):

    middle_i = len(unsort_list) // 2
    L_list = unsort_list[ :middle_i]
    R_list = unsort_list[middle_i: ]
 
    if len(L_list) > 1:
        L_list = merge_sort(L_list)
    if len(R_list) > 1:
        R_list = merge_sort(R_list)
 
    return lists_sort(L_list, R_list)


unsort_list = [random.randint(-9, 9) for _ in range(10)]
result_list = merge_sort(unsort_list)
 
print('Неотсортированный список: {} \nОтсортированный список: {}'.format(unsort_list, result_list))
