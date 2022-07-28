# Q3 Answer template
def get_divisors(n):
    divisors = [1, n]
    for i in range(2, n):
        if n % i == 0:
            divisors += [i, n // i]

    return list(set(divisors))

def solution(left, right):
    answer = 0
    for i in range(left, right + 1):
        if len(get_divisors(i)) % 2 == 0:
            answer += i
        else:
            answer -= i

    return answer