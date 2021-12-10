import tkinter
import random
from tkinter import *
import pandas as pd

import numpy as np
from matplotlib import pyplot as plt

list_functions = []
clear_time_series = [10, 12, 17, 20, 22, 17, 10, 11, 14, 15, 20, 24]
list_time_marks = []
graph_indexes = []  # 0,1,2
list_tendentions = []
prognoze_list = []


def getNext(listing):
    add_list = []
    predict = listing[len(listing) - 1][1]
    for item in listing:
        if item[0] == predict:
            add_list.append(item)
    a = pd.Index(add_list)
    print(a.value_counts())
    print(a.value_counts().index[0])
    return a.value_counts().index[0][1]


def predict():
    prognoze_list.clear()
    for i in range(len(list_tendentions) - 2):
        list_work = [list_tendentions[i], list_tendentions[i + 1]]
        prognoze_list.append(list_work)#добавляем пары в список
    print(prognoze_list)
    print(getNext(prognoze_list))
    graph_indexes.append(graph_indexes[len(graph_indexes) - 2] + getNext(prognoze_list))
    max = list_functions[graph_indexes[len(graph_indexes) - 2]][0]

    index = 0
    for i in range(len(list_functions[graph_indexes[len(graph_indexes) - 2]])):
        if list_functions[graph_indexes[len(graph_indexes) - 2]][i] > max:
            max = list_functions[graph_indexes[len(graph_indexes) - 2]][i]
            index = i
#фазефекация, дефазефекация, график нечетких множеств
    clear_time_series.append(index)
    razn = (clear_time_series[len(clear_time_series) - 2] - clear_time_series[len(clear_time_series) - 1]) / \
           clear_time_series[len(clear_time_series) - 2]

    print(razn)


def graph_NVK():
    plt.plot(list_time_marks)
    plt.grid('on')
    plt.show()


def graph_ChVK():
    list_help = clear_time_series.copy()
    list_help_clear_time = clear_time_series.copy()
    list_help_clear_time.pop(len(list_help_clear_time) - 2)
    list_help.pop()
    plt.plot(list_help_clear_time, color='r')
    plt.plot(list_help, color='g')
    plt.show()


def print_CTS():
    print(f"Нечеткий временной ряд")
    for i in range(len(clear_time_series)):
        print(f"{i}. {list_time_marks[i]} - {clear_time_series[i]}")


def graph_tend():
    dop_list = []
    for i in range(len(clear_time_series) - 1):
        dop_list.append([clear_time_series[i], clear_time_series[i + 1]])
    for i in range(len(dop_list)):
        color = ''
        if list_tendentions[i] == 0:
            color = 'g'
        if list_tendentions[i] == -1:
            color = 'b'
        if list_tendentions[i] == 1:
            color = 'r'
        plt.plot((i, i + 1), dop_list[i], color=color)
    plt.grid('on')
    plt.show()


def get_fuzzy_estimate():
    list_time_marks.clear()
    graph_indexes.clear()
    for i in clear_time_series:
        number = get_max(i)
        graph_indexes.append(number)
        if number <= 2:
            if number == 0:
                list_time_marks.append("холодно")
            if number == 1:
                list_time_marks.append("тепло")
            if number == 2:
                list_time_marks.append("жарко")
        else:
            list_time_marks.append("очень жарко")
    print_CTS()


def get_max(number):
    list_coinsidens = []
    for i in list_functions:
        list_coinsidens.append(i[number])
    max = list_coinsidens[0]
    index = 0
    for i in range(len(list_coinsidens)):
        if list_coinsidens[i] > max:
            max = list_coinsidens[i]
            index = i
    return index


def get_tendentions():
    list_tendentions.clear()
    for i in range(len(graph_indexes) - 1):
        if graph_indexes[i] == graph_indexes[i + 1]:
            list_tendentions.append(0)
        if graph_indexes[i] < graph_indexes[i + 1]:
            list_tendentions.append(1)
        if graph_indexes[i] > graph_indexes[i + 1]:
            list_tendentions.append(-1)
    print(list_tendentions)


def peres():
    res = []
    for i in range(len(list_functions[lbox.curselection()[0]])):
        min = list_functions[lbox.curselection()[0]][i]
        if list_functions[lbox.curselection()[1]][i] < min:
            min = list_functions[lbox.curselection()[1]][i]
        res.append(min)
    list_functions.append(res)
    listbox_update()


def obed():
    res = []
    for i in range(len(list_functions[lbox.curselection()[0]])):
        max = list_functions[lbox.curselection()[0]][i]
        if list_functions[lbox.curselection()[1]][i] > max:
            max = list_functions[lbox.curselection()[1]][i]
        res.append(max)
    list_functions.append(res)
    listbox_update()


def count_function(x, a, b, c, d, isTrapezoid):
    result = []
    if isTrapezoid:
        for i in x:
            if a <= i <= d:
                if a <= i <= b:
                    result.append(1 - (b - i) / (b - a))
                    continue
                if b <= i <= c:
                    result.append(1)
                    continue
                if c <= i <= d:
                    result.append(1 - (i - c) / (d - c))
                    continue
            else:
                result.append(0)
    else:
        for i in x:
            if a <= i <= c:
                if a <= i <= b:
                    result.append(1 - (b - i) / (b - a))
                    continue
                if b <= i <= c:
                    result.append(1 - (i - b) / (c - b))
            else:
                result.append(0)

    return result


# поля для ввода значений
def clicked():
    x = np.arange(100)

    a = int(fn_1_1.get())
    b = int(fn_1_2.get())
    c = int(fn_1_3.get())
    d = int(fn_1_4.get())

    list_functions.append(count_function(x, a, b, c, d, CheckVar1.get()))
    listbox_update()


def show():
    for i in list_functions:
        plt.plot(i)
    plt.grid('on')
    plt.show()


def change():
    list_functions.pop(lbox.curselection()[0])

    x = np.arange(100)

    a = int(fn_1_1.get())
    b = int(fn_1_2.get())
    c = int(fn_1_3.get())
    d = int(fn_1_4.get())

    list_functions.append(count_function(x, a, b, c, d, CheckVar1.get()))
    listbox_update()


def del_function():
    list_functions.pop(lbox.curselection()[0])
    listbox_update()


def listbox_update():
    lbox.delete(0, tkinter.END)
    for i in range(len(list_functions)):
        lbox.insert(i, str(i))


def global_method():
    get_fuzzy_estimate()
    get_tendentions()
    show()
    graph_NVK()
    graph_tend()


window = Tk()  # окно
window.title("Оценка объемов продаж")
window.geometry('400x250')  # размер окна

# function 1
lbl_fn1 = Label(window, text="Функция")
lbl_fn1.grid(column=0, row=1)

fn_1_1 = Entry(window, width=5)
fn_1_1.grid(column=1, row=1)

fn_1_2 = Entry(window, width=5)
fn_1_2.grid(column=1, row=2)

fn_1_3 = Entry(window, width=5)
fn_1_3.grid(column=1, row=3)

fn_1_4 = Entry(window, width=5)
fn_1_4.grid(column=1, row=4)

CheckVar1 = BooleanVar()
chk_fn1 = Checkbutton(window, text='Трапецевидная', variable=CheckVar1)
chk_fn1.grid(column=2, row=1)

btn = Button(window, text="Нажать", command=clicked)
btn.grid(column=2, row=2)

btn_del = Button(window, text="Показать", command=show)
btn_del.grid(column=2, row=3)

btn_change = Button(window, text="Редактировать", command=change)
btn_change.grid(column=2, row=4)

btn_del = Button(window, text="Удалить", command=del_function)
btn_del.grid(column=2, row=5)

lbox = Listbox(width=15, height=8, selectmode='multiple')
lbox.grid(column=1, row=8)

btn_obed = Button(window, text="Объеденить", command=obed)
btn_obed.grid(column=3, row=5)

btn_peres = Button(window, text="Пересечь", command=peres)
btn_peres.grid(column=3, row=6)

btn_time = Button(window, text="НВР", command=get_fuzzy_estimate)
btn_time.grid(column=7, row=1)

btn_tend = Button(window, text="Тенденции", command=get_tendentions)
btn_tend.grid(column=7, row=2)

btn_graph_ChVK = Button(window, text="График предсказания", command=graph_ChVK)
btn_graph_ChVK.grid(column=8, row=3)

btn_graph_ChVK = Button(window, text="График чвр", command=graph_ChVK)
btn_graph_ChVK.grid(column=7, row=3)

btn_graph_NVK = Button(window, text="График НВР", command=graph_NVK)
btn_graph_NVK.grid(column=7, row=4)

btn_graph_tend = Button(window, text="График тенденций", command=graph_tend)
btn_graph_tend.grid(column=7, row=5)

btn_global = Button(window, text="Глобальный клик", command=global_method)
btn_global.grid(column=8, row=2)

btn_pred = Button(window, text="Прогноз!", command=predict)
btn_pred.grid(column=8, row=1)

x = np.arange(100)
list_functions.append(count_function(x, 1, 10, 14, 100, True))
list_functions.append(count_function(x, 1, 15, 20, 100, True))
list_functions.append(count_function(x, 1, 21, 30, 100, True))
listbox_update()

window.mainloop()
