def factorial(n):
    return 1 if n == 1 else factorial(n - 1) * n
print('Факториал:', factorial(5))
 
def nod(a, b):
    return min(a, b) if a % b == 0 else nod(b, a % b)
print('Наименьший общий делитель равен:', nod(12, 11)) 
