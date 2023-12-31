from lpsolve55 import *


def politicalExample():
    solver = lpsolve('make_lp', 0, 4)

    ret = lpsolve('add_constraint', solver, [-2.0, 8.0, 0.0, 10.0], GE, 50.0)
    ret = lpsolve('add_constraint', solver, [5.0, 2.0, 0.0, 0.0], GE, 100.0)
    ret = lpsolve('add_constraint', solver, [3.0, -5.0, 10.0, -2.0], GE, 25.0)

    ret = lpsolve('set_obj_fn', solver, [1.0, 1.0, 1.0, 1.0])

    ret = lpsolve('solve', solver)

    obj_func = lpsolve('get_objective', solver)
    coefficients = lpsolve('get_variables', solver)[0]

    return obj_func, coefficients

def rabinKarp(pattern, text, q):
    m = len(pattern)
    n = len(text)
    p = 0
    t = 0
    h = 1
    i = 0
    j = 0
    d = 10
    indices = []

    for i in range(m-1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            for j in range(m):
                if text[i+j] != pattern[j]:
                    break

            j += 1
            if j == m:
                indices.append(i)

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i+m])) % q

            if t < 0:
                t = t + q

    return indices


# Testing politicalExample
obj, coeff = politicalExample()
print(f"Value of objective function: {obj}")
print(f"Value of coefficients function: {coeff}")

# Testing rabinKarp
userInput = input("Please enter your text: ")
pattern = input("Please enter the pattern that you want to match with the text: ")

listOfIndices = rabinKarp(pattern=pattern, text=userInput, q=13)
print(f"Pattern is found in the following position(s): {listOfIndices}")
