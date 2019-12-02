from repeat_and_time import repeat_and_time

@repeat_and_time(100)
def do_somthing():
    a = 1
    print(a + 1)
    return a + 1


do_somthing()
