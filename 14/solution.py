# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
import itertools
import re
from string import ascii_uppercase, digits

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

# Thanks Peter Norvig for the idea
def compile_lambda(formula, verbose=False):
    formula = formula.replace(' = ', ' == ')
    letters = "".join(sorted(set(re.findall('[A-Z]', formula))))
    nonzero = sorted(set(re.findall(r'\b([A-Z])[A-Z]', formula)))
    body = re.sub('[A-Z]+', compile_word, formula)
    body = ' and '.join(nonzero + [body])
    fn = 'lambda {}: {}'.format(','.join(letters), body)
    if verbose: print(fn)
    assert len(letters) <= 10
    return eval(fn), letters

def compile_word(matchobj):
    word = matchobj.group()
    terms = reversed([mult(10**i, L) for (i, L) in enumerate(reversed(word))])
    return '(' + '+'.join(terms) + ')'

def mult(factor, var): return var if factor == 1 else str(factor) + '*' + var

def find_solutions(formula):
    fn, letters = compile_lambda(formula)
    for digits in itertools.permutations(range(10), len(letters)):
        try:
            if fn(*digits):
                yield formula.translate(str.maketrans(letters, "".join(map(str, digits))))
        except ArithmeticError:
            pass

def solution(expr):
    solns = list(find_solutions(expr))
    if len(solns) == 0:
        return "IMPOSSIBLE"
    return ";".join(sorted(solns))

def main():
    t = read_int()

    for i in range(t):
        expr = input().strip()
        s = solution(expr)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
