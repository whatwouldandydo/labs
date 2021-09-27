from decorators import timer

@timer
def waste_some_time(num_time):
    for _ in range(num_time):
        sum([i**2 for i in range(1000)])

        ii = []
        for i in range(1000):
            i = i**2
            ii.append(i)
        #     print(i)
        print(sum(ii))

        print(sum([i**2 for i in range(1000)]))

waste_some_time(10)


from decorators import slow_down

@slow_down
def count_down(numb):
    if numb < 1:
        print("Lift Off")
    else:
        print(numb)
        count_down(numb - 1) # This create a loop count down until 1


count_down(3)