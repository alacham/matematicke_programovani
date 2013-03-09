def collatz(num):
    maxi = num
    step = 0
    while num != 1:
        maxi = max(num,maxi)
        step += 1
        if num % 2 == 0:
            num = num /2
        else:
            num = num * 3 + 1
    return [step, maxi]


def print_collatz_csv(first_n):
    for i in range(1,first_n):
        print i, ';', ";".join(map(str,collatz(i)))

if __name__ == '__main__':
    print_collatz_csv(10000)
