from .expr import *

from itertools import chain, zip_longest
import itertools

def interleave_longest(*iterables):
    o = object()
    i = chain.from_iterable(zip_longest(*iterables, fillvalue=o))
    return [x for x in i if x is not o]

some_nonnumbers = [Undefined, True_, False_, Infinity, -Infinity, Infinity*ConstI, -ConstI*Infinity,
    UnsignedInfinity, Undefined, Tuple(), Tuple(Tuple()), Tuple(0), Tuple(0, 0), Tuple(0, 1), Tuple(1, 2, 3),
    Set(), Set(Set()), Set(0), Set(0, 1), Set(-1, 0, 1), ZZ, RR, QQ, CC,
    Matrix2x2(1, 0, 0, 1)]

some_primes = [2,3,5,7,11,13,17,19,101,1009,10007]

some_integers = [Expr(_n) for _n in [0,1,-1,2,-2,3,-3,4,-4,5,-5,6,-6,7,8,9,
    10,11,12,24,30,32,40,41,42,60,64,100,120,127,128,255,256,257,720,
    1000,1729,10**4,10**5,10**6,10**9,10**12,10**15,10**30]]

some_fractions = [Div(1,2),-Div(1,2),Div(3,2),-Div(3,2),Div(5,2),Div(7,2),Div(1,3),Div(2,3),Div(4,3),Div(1,4),Div(3,4),Div(5,4),Div(1,5),Div(1,6),Div(1,24)]

some_algebraic_irrationals = [Sqrt(2), -Sqrt(2), Sqrt(2)/2, -Sqrt(2)/2, GoldenRatio, 1/GoldenRatio, Sqrt(2)+1, Sqrt(2)-1]

some_transcendentals = [Pi, 2*Pi, Pi/2, 3*Pi/2, -Pi, -Pi/2, 2*Pi/3, -2*Pi/3, Pi/4, -Pi/4, 3*Pi/4, -3*Pi/4, Pi/6, 5*Pi/6, Log(2), Log(3), ConstE]

some_complex_algebraics = [ConstI, -ConstI, 2*ConstI, -2*ConstI, ConstI/2, -ConstI/2,
    1+ConstI, 1-ConstI, -1+ConstI, -1-ConstI,
    2+ConstI, 2-ConstI, -2+ConstI, -2-ConstI,
    1+2*ConstI, 1-2*ConstI, -1+2*ConstI, -1-2*ConstI,
    Div(1,2)+ConstI, Div(1,2)-ConstI, Div(3,2)+ConstI,
    (1+ConstI)/2, (1-ConstI)/2, (-1+ConstI)/2, (-1-ConstI)/2,
    Exp(Pi*ConstI/3), Exp(2*Pi*ConstI/3), Exp(Pi*ConstI/6), Exp(5*Pi*ConstI/6),
    Exp(Pi*ConstI/4), Exp(-Pi*ConstI/4), Exp(3*Pi*ConstI/4), Exp(-3*Pi*ConstI/4)]

some_complex_transcendentals = [Pi*ConstI, 2*Pi*ConstI, -Pi*ConstI, Div(1,2)+Pi*ConstI, Div(1,2)-Pi*ConstI, Pi+ConstE*ConstI]

some_rationals = interleave_longest(some_integers, some_fractions)
some_algebraics = interleave_longest(some_integers, some_fractions, some_algebraic_irrationals, some_complex_algebraics)
some_reals = interleave_longest(some_integers, some_fractions, some_algebraic_irrationals, some_transcendentals)
some_extended_reals = interleave_longest(some_integers, some_fractions, some_algebraic_irrationals, some_transcendentals, [Infinity, -Infinity])
some_complexes = interleave_longest(some_integers, some_fractions, some_algebraic_irrationals, some_complex_algebraics, some_transcendentals, some_complex_transcendentals)
some_everything = interleave_longest(some_nonnumbers, some_complexes)

some_upper_half_plane = [ConstI, 2*ConstI, ConstI/2, 1+ConstI, 1+2*ConstI, 1+ConstI/2, -1+ConstI, -1+2*ConstI, -1+ConstI/2, 2+ConstI, 3+ConstI,
    Div(1,2)+ConstI, Div(1,2)+2*ConstI, Div(1,2)+ConstI/2, Div(1,3)+ConstI, Div(1,3)+2*ConstI, Div(1,3)+ConstI/2, Sqrt(2)+Pi*I, -Sqrt(2)+I/Pi]

def And_terms(expr):
    if expr.head() == And:
        for x in expr.args():
            for t in And_terms(x):
                yield t
    else:
        yield expr

# todo: design a real algorithm
def custom_cartesian(*lists):
    if len(lists) == 1:
        for v in lists[0]:
            yield (v,)
    elif len(lists) == 2:
        N = 0
        A = len(lists[0])
        B = len(lists[1])
        for N in range(max(A,B)):
            for i in range(N+1):
                a = i
                b = N - i
                if 0 <= a < A and 0 <= b < B:
                    yield lists[0][a], lists[1][b]
    elif len(lists) == 3:
        N = 0
        A = len(lists[0])
        B = len(lists[1])
        C = len(lists[2])
        for N in range(max(A,B,C)):
            for i in range(N+1):
                for j in range(N+1):
                    a = i
                    b = N - i
                    c = N - i - j
                    if 0 <= a < A and 0 <= b < B and 0 <= c < C:
                        yield lists[0][a], lists[1][b], lists[2][c]
    elif len(lists) == 4:
        N = 0
        A = len(lists[0])
        B = len(lists[1])
        C = len(lists[2])
        D = len(lists[3])
        for N in range(max(A,B,C,D)):
            for i in range(N+1):
                for j in range(N+1):
                    for k in range(N+1):
                        a = i
                        b = N - i
                        c = N - i - j
                        d = N - i - j - k
                        if 0 <= a < A and 0 <= b < B and 0 <= c < C and 0 <= d < D:
                            yield lists[0][a], lists[1][b], lists[2][c], lists[3][d]
    else:
        for v in itertools.product(*lists):
            yield v

additive_ops = set([Pos, Neg, Add, Sub])
ring_arithmetic_ops = set([Pos, Neg, Add, Sub, Mul])
field_arithmetic_ops = set([Pos, Neg, Add, Sub, Mul, Div])
arithmetic_ops = set([Pos, Neg, Add, Sub, Mul, Div, Sqrt, Pow])
number_part_ops = set([Sign, Abs, Re, Im, Conjugate, Floor, Ceil])

positive_real_constants = set([Pi, ConstE, ConstGamma, ConstCatalan, GoldenRatio])
irrational_constants = set([Pi, ConstE, GoldenRatio])
complex_constants = positive_real_constants.union(set([ConstI]))

set_logic_ops = set([Not, And, Or, Implies, Equal, NotEqual, Element, NotElement, Less, LessEqual, Greater, GreaterEqual])

def infer_not_domain(inferences, x, dom):
    if dom.head() == Union:
        for dom2 in dom.head_args_flattened(Union):
            infer_not_domain(inferences, x, dom2)
        return
    def add(x, dom):
         inferences.add(NotElement(x, dom))
    add(x, dom)
    # singleton set
    if dom.head() == Set and len(dom.args()) == 1:
        inferences.add(NotEqual(x, dom.args()[0]))
    if dom == CC:
        add(x, RR)
        add(x, QQ)
        add(x, ZZ)
        add(x, PP)
        add(x, HH)
        add(x, AlgebraicNumbers)
    elif dom == RR:
        add(x, QQ)
        add(x, ZZ)
        add(x, PP)
    elif dom == QQ:
        add(x, ZZ)
        add(x, PP)
    elif dom == ZZ:
        add(x, PP)
    elif dom == AlgebraicNumbers:
        add(x, QQ)
        add(x, ZZ)

def infer_domain(inferences, x, dom):
    if dom.head() == Intersection:
        for dom2 in dom.head_args_flattened(Intersection):
            infer_domain(inferences, x, dom2)
        return
    def add(x, dom):
         inferences.add(Element(x, dom))
    add(x, dom)
    # singleton set
    if dom.head() == Set and len(dom.args()) == 1:
        inferences.add(Equal(x, dom.args()[0]))
    if dom == RR:
        add(x, CC)
    elif dom == QQ:
        add(x, RR)
        add(x, CC)
        add(x, AlgebraicNumbers)
    elif dom == ZZ:
        add(x, QQ)
        add(x, RR)
        add(x, CC)
        add(x, AlgebraicNumbers)
    elif dom == HH:
        add(x, CC)
    elif dom == PP:
        add(x, ZZGreaterEqual(2))
        add(x, ClosedOpenInterval(2, Infinity))
        add(x, ZZ)
        add(x, QQ)
        add(x, RR)
        add(x, CC)
        add(x, AlgebraicNumbers)
    elif dom == AlgebraicNumbers:
        add(x, CC)
    elif dom.head() in (ZZGreaterEqual, ZZLessEqual, Range):
        add(x, ZZ)
        add(x, QQ)
        add(x, RR)
        add(x, CC)
        add(x, AlgebraicNumbers)
    elif dom.head() == OpenInterval:
        add(x, RR)
        add(x, CC)
        a, b = dom.args()
        inferences.add(Less(a, x))
        inferences.add(Less(x, b))
        inferences.add(Greater(x, a))
        inferences.add(Greater(b, x))
        for v in (-1, 0, 1):
            if GreaterEqual(a, v).simple() == True_:
                inferences.add(Greater(x, v))
                inferences.add(Less(v, x))
            if LessEqual(b, v).simple() == True_:
                inferences.add(Less(x, v))
                inferences.add(Greater(v, x))
    elif dom.head() == ClosedInterval:
        a, b = dom.args()
        inferences.add(LessEqual(a, x))
        inferences.add(LessEqual(x, b))
        inferences.add(GreaterEqual(x, a))
        inferences.add(GreaterEqual(b, x))
        # todo: simplify based on other assumptions?
        if Element(a, RR).simple() == True_ and Element(b, RR).simple() == True_:
            add(x, RR)
            add(x, CC)
        for v in (-1, 0, 1):
            if GreaterEqual(a, v).simple() == True_:
                inferences.add(GreaterEqual(x, v))
                inferences.add(LessEqual(v, x))
            if LessEqual(b, v).simple() == True_:
                inferences.add(LessEqual(x, v))
                inferences.add(GreaterEqual(v, x))
    elif dom.head() == OpenClosedInterval:
        a, b = dom.args()
        inferences.add(Less(a, x))
        inferences.add(LessEqual(x, b))
        inferences.add(Greater(x, a))
        inferences.add(GreaterEqual(b, x))
        if Element(b, RR).simple() == True_:
            add(x, RR)
            add(x, CC)
        for v in (-1, 0, 1):
            if GreaterEqual(a, v).simple() == True_:
                inferences.add(Greater(x, v))
                inferences.add(Less(v, x))
            if LessEqual(b, v).simple() == True_:
                inferences.add(LessEqual(x, v))
                inferences.add(GreaterEqual(v, x))
    elif dom.head() == ClosedOpenInterval:
        a, b = dom.args()
        inferences.add(LessEqual(a, x))
        inferences.add(Less(x, b))
        inferences.add(GreaterEqual(x, a))
        inferences.add(Greater(b, x))
        if Element(a, RR).simple() == True_:
            add(x, RR)
            add(x, CC)
        for v in (-1, 0, 1):
            if GreaterEqual(a, v).simple() == True_:
                inferences.add(GreaterEqual(x, v))
                inferences.add(LessEqual(v, x))
            if LessEqual(b, v).simple() == True_:
                inferences.add(Less(x, v))
                inferences.add(Greater(v, x))


class Brain(object):
    """
    A "brain" for performing symbolic computation.
    """

    def infer(self, thm):
        self.inferences.add(thm)
        if thm.head() == Element:
            x, dom = thm.args()
            infer_domain(self.inferences, x, dom)
            if dom.head() == SetMinus:
                inset, outset = dom.args()
                infer_domain(self.inferences, x, inset)
                infer_not_domain(self.inferences, x, outset)

    def __init__(self, variables=(), assumptions=None, fungrim=False, penalty={}):
        """
        Input: a list of symbols representing free variables and
        assumptions involving the free variables, which may be used
        in symbolic simplification.

        >>> brain = Brain(variables=[a,b,c],
        ...     assumptions=And(Element(a, CC), Element(b, ZZ),
        ...         Element(c, QQ), NotEqual(a, 1)))
        >>>

        """
        self.simple_cache = {}
        self.penalty = penalty

        # Init computational types
        from flint import arb, acb, fmpz, fmpq, ctx
        self._arb = arb
        self._acb = acb
        self._fmpz = fmpz
        self._fmpq = fmpq
        self._flint_ctx = ctx

        # Init assumptions
        self.variables = frozenset(variables)
        self.inferences = set()
        if assumptions is None:
            self.assumptions = frozenset()
        else:
            self.assumptions = frozenset(assumptions.head_args_flattened(And))
        # Simple inferences (mostly based on the domain)
        for asm in self.assumptions:
            # asm = asm.simple()
            self.infer(asm)

    def __repr__(self):
        s = ""
        s += "Variables: " + str(self.variables) + "\n"
        s += "Inferences: (%i)" % len(self.inferences) + "\n"
        for thm in self.inferences:
            s += "  " + str(thm) + "\n"
        return s

    def real_enclosure(self, x):
        """
        Performs numerical evaluation and returns an enclosure of x as an arb.
        Success proves that x is a real number.
        Returns None on failure.
        """
        try:
            val = x.n(as_arb=True)
            if type(val) == self._arb:
                return val
        except (NotImplementedError, ValueError, ImportError):
            pass
        return None

    def complex_enclosure(self, x):
        """
        Performs numerical evaluation and returns an enclosure of x as an acb.
        Success proves that x is a complex number.
        Returns None on failure.
        """
        try:
            val = x.n(as_arb=True)
            assert val.is_finite()
            if type(val) == self._acb:
                return val
            if type(val) == self._arb:
                return self._acb(val)
        except (NotImplementedError, ValueError, ImportError):
            pass
        return None

    def simple(self, expr):
        """
        Given a symbolic expression expr, return an equivalent expression,
        hopefully simplified.
        """
        if expr in self.inferences:
            return True_

        if expr.is_atom():
            return expr

        if expr in self.simple_cache:
            v = self.simple_cache[expr]
            if v is None:
                return expr
            return v

        input_expr = expr
        self.simple_cache[input_expr] = None

        head = expr.head()
        if head is not None and head.is_symbol():
            s = head._symbol
            f = "simple_" + s
            if hasattr(self, f):
                args = expr.args()
                expr2 = getattr(self, f)(*args)
                expr = expr2
            else:
                args = expr.args()
                args = [self.simple(x) for x in args]
                expr = head(*args)

        self.simple_cache[input_expr] = expr

        return expr

    def is_zero(self, x):
        """
        Check if x is the number zero.
        Return True, False, or None for unknown.
        """
        if x.is_integer():
            return int(x) == 0
        if Equal(x, 0) in self.inferences:
            return True
        if NotEqual(x, 0) in self.inferences:
            return False
        if Greater(x, 0) in self.inferences:
            return False
        if Less(x, 0) in self.inferences:
            return False
        if self.is_integer(x) == False:
            return False
        if self.is_positive(x):
            return False
        val = self.complex_enclosure(x)
        if val is not None and val != 0:
            return False
        if self.is_infinity(x):
            return False
        # todo: try normal form here?
        return None

    def is_not_zero(self, x):
        """
        Check if x is not the number zero.
        Return True, False, or None for unknown.
        """
        v = self.is_zero(x)
        if v is None:
            return v
        return not v

    def is_infinity(self, x):
        """
        Checks if x is an infinity (UnsignedInfinity or c*Infinity for some
        nonzero complex number c). Returns True, False, or None for unknown.
        """
        if x == Infinity:
            return True
        if x == UnsignedInfinity:
            return True
        if x == Undefined:
            return False
        if Element(x, CC) in self.inferences:
            return False
        if x.head() in (Pos, Neg):
            arg, = x.args()
            if self.is_infinity(arg):
                return True
        if x.head() == Mul:
            args = x.args()
            if any(self.is_infinity(arg) for arg in args):
                if all(self.is_infinity(arg) or (self.is_complex(arg) and self.is_not_zero(arg)) for arg in x.args()):
                    return True
        val = self.complex_enclosure(x)
        if val is not None:
            return False
        return None

    def is_nonnegative(self, x):
        """
        Check if x is an object satisfying x >= 0.
        Return True, False, or None for unknown.
        """
        if x.is_integer():
            return int(x) >= 0
        if x in positive_real_constants:
            return True
        if GreaterEqual(x, 0) in self.inferences:
            return True
        if Greater(x, 0) in self.inferences:
            return True
        if Less(x, 0) in self.inferences:
            return False
        if self.is_real(x):
            if x.head() in (Pos, Add, Mul, Exp, Sqrt):
                if all(self.is_nonnegative(arg) for arg in x.args()):
                    return True
            if x.head() == Div:
                p, q = x.args()
                if self.is_nonnegative(p) and self.is_positive(q):
                    return True
            if x.head() == Pow:
                base, exp = x.args()
                if self.is_positive(base):
                    return True
        val = self.complex_enclosure(x)
        if val is not None:
            real, imag = val.real, val.imag
            if imag == 0 and real >= 0:
                return True
            if imag != 0 or real < 0:
                return False
        return None

    def is_positive(self, x):
        """
        Check if x is an object satisfying x > 0.
        Returns True, False, or None for unknown.
        """
        if x.is_integer():
            return int(x) > 0
        if x in positive_real_constants:
            return True
        if Greater(x, 0) in self.inferences:
            return True
        if LessEqual(x, 0) in self.inferences:
            return False
        if Less(x, 0) in self.inferences:
            return False
        if self.is_real(x):
            if x.head() in (Exp, Cosh):
                t, = x.args()
                if self.is_real(t):
                    return True
            if x.head() in (Pos, Add, Mul, Sqrt):
                if all(self.is_positive(arg) for arg in x.args()):
                    return True
            if x.head() == Div:
                p, q = x.args()
                if self.is_positive(p) and self.is_positive(q):
                    return True
            if x.head() == Pow:
                base, exp = x.args()
                if self.is_positive(base):
                    return True
        val = self.complex_enclosure(x)
        if val is not None:
            real, imag = val.real, val.imag
            if imag == 0 and real > 0:
                return True
            if imag != 0 or real <= 0:
                return False
        return None

    def is_negative(self, x):
        """
        Check if x is an object satisfying x < 0.
        Returns True, False, or None for unknown.
        """
        if x.is_integer():
            return int(x) < 0
        if x in positive_real_constants:
            return False
        if Less(x, 0) in self.inferences:
            return True
        if GreaterEqual(x, 0) in self.inferences:
            return False
        if Greater(x, 0) in self.inferences:
            return False
        val = self.complex_enclosure(x)
        if val is not None:
            real, imag = val.real, val.imag
            if imag == 0 and real < 0:
                return True
            if imag != 0 or real >= 0:
                return False
        return None

    def is_nonpositive(self, x):
        """
        Check if x is an object satisfying x <= 0.
        Returns True, False, or None for unknown.
        """
        if x.is_integer():
            return int(x) <= 0
        if x in positive_real_constants:
            return False
        if LessEqual(x, 0) in self.inferences:
            return True
        if Less(x, 0) in self.inferences:
            return True
        if Greater(x, 0) in self.inferences:
            return False
        val = self.complex_enclosure(x)
        if val is not None:
            real, imag = val.real, val.imag
            if imag == 0 and real <= 0:
                return True
            if imag != 0 or real > 0:
                return False
        return None

    def is_integer(self, x):
        """
        Checks if x is an integer. Returns True, False, or None for unknown.
        """
        if x.is_integer():
            return True
        if Element(x, ZZ) in self.inferences:
            return True
        if NotElement(x, ZZ) in self.inferences:
            return False
        if x.head() in (Pos, Neg, Add, Sub, Mul):
            if all(self.is_integer(arg) for arg in x.args()):
                return True
        if x.head() == Pow:
            base, exp = x.args()
            if self.is_integer(base) and self.is_integer(exp) and self.is_nonnegative(exp):
                return True
        if x.head() == Factorial:
            n, = x.args()
            if self.is_integer(n) and self.is_nonnegative(n):
                return True
        if x in complex_constants:
            return False
        val = self.complex_enclosure(x)
        if val is not None:
            # todo: with increased precision when needed
            if not val.contains_integer():
                return False
        if self.is_infinity(x) or x == Undefined:
            return False
        return None

    # todo: irrational + rational, irrational * rational, irrational / rational, rational / irrational
    # todo: square roots
    # todo: exp, log, sin, cos, tan of rational numbers
    def is_rational(self, x):
        """
        Check if x is a rational number.
        Returns True, False, or None for unknown.
        """
        if self.is_integer(x):
            return True
        if Element(x, QQ) in self.inferences:
            return True
        if NotElement(x, QQ) in self.inferences:
            return False
        if x == Pi or x == ConstE:
            return False
        if x.head() in (Pos, Neg, Add, Sub, Mul):
            if all(self.is_rational(arg) for arg in x.args()):
                return True
        if x.head() == Div:
            p, q = x.args()
            if self.is_rational(p) and self.is_rational(q) and self.is_not_zero(q):
                return True
        if x.head() == Pow:
            base, exp = x.args()
            if self.is_rational(base) and self.is_integer(exp) and (self.is_not_zero(base) or self.is_nonnegative(exp)):
                return True
        if x.head() == Sqrt:
            # todo: implement an algorithm
            v, = x.args()
            if v.is_integer():
                v = int(v)
                if v < 0:
                    return False
                if v <= 100:
                    return v in [0,1,4,9,16,25,36,49,64,81,100]
        if self.is_infinity(x) or x == Undefined:
            return False
        return None

    def is_algebraic(self, x):
        """
        Check if x is an algebraic number.
        Returns True, False, or None for unknown.
        """
        if self.is_integer(x):
            return True
        if Element(x, AlgebraicNumbers) in self.inferences:
            return True
        if NotElement(x, AlgebraicNumbers) in self.inferences:
            return False
        if x == Pi or x == ConstE:
            return False
        if x == ConstI or x == GoldenRatio:
            return True
        if x.head() in (Pos, Neg, Add, Sub, Mul):
            if all(self.is_algebraic(arg) for arg in x.args()):
                return True
        if x.head() == Div:
            p, q = x.args()
            if self.is_algebraic(p) and self.is_algebraic(q) and self.is_not_zero(q):
                return True
        if x.head() == Pow:
            base, exp = x.args()
            if self.is_algebraic(base):
                if self.is_rational(exp) and (self.is_not_zero(base) or self.is_nonnegative(exp)):
                    return True
                # Gelfond-Schneider
                if self.is_algebraic(exp) and self.is_rational(exp) == False and self.is_not_zero(base) and self.equal(base, Expr(1)) == False:
                    return False
            # transcendental ^ rational
            if self.is_complex(base) and (self.is_algebraic(base) == False) and self.is_rational(exp) and self.is_not_zero(exp):
                return False
        if x.head() == Sqrt:
            v, = x.args()
            return self.is_algebraic(v)
        if x.head() == Exp:
            v, = x.args()
            if self.is_algebraic(v) and self.is_not_zero(v):
                return False
            if self.is_rational(self.simple(v / (Pi * ConstI))):
                return True
        if x.head() in (Sin, Cos, Tan, Cot, Csc, Sec):
            v, = x.args()
            if self.is_algebraic(v) and self.is_not_zero(v):
                return False
        if x.head() == Log:
            v, = x.args()
            if self.is_algebraic(v) and (self.equal(v, Expr(1)) == False):
                return False
        if self.is_infinity(x) or x == Undefined:
            return False
        return None

    def is_real(self, x):
        """
        Check if x is a real number.
        Return True, False, or None for unknown.
        """
        if self.is_rational(x):  # todo: remove this?
            return True
        if Element(x, RR) in self.inferences:
            return True
        if NotElement(x, RR) in self.inferences:
            return False
        if x in (Pi, ConstGamma, ConstE, ConstCatalan):
            return True
        if x == ConstI:
            return False
        if x.head() in (Pos, Neg, Add, Sub, Mul, Exp, Sin, Cos):
            if all(self.is_real(arg) for arg in x.args()):
                return True
        if x.head() == Div:
            p, q = x.args()
            if self.is_real(p) and self.is_real(q) and self.is_not_zero(q):
                return True
        if x.head() == Sqrt:
            arg, = x.args()
            if self.is_real(arg) and self.is_nonnegative(arg):
                return True
        if x.head() == Log:
            arg, = x.args()
            if self.is_real(arg) and self.is_positive(arg):
                return True
        if x.head() == Pow:
            base, exp = x.args()
            if self.is_real(base) and self.is_real(exp):
                if self.is_positive(base) and self.is_positive(exp):
                    return True
                if self.is_not_zero(base) and self.is_integer(exp):
                    return True
                if self.is_integer(exp) and self.is_nonnegative(exp):
                    return True
        v = self.complex_enclosure(x)
        if v is not None:
            if v.imag == 0:
                return True
            if v.imag != 0:
                return False
        if self.is_infinity(x) or x == Undefined:
            return False
        return None

    def is_complex(self, x):
        """
        Check if x is a complex number.
        Return True, False, or None for unknown.
        """
        if self.is_real(x):  # todo: remove this?
            return True
        if x == ConstI:
            return True
        if Element(x, CC) in self.inferences:
            return True
        if NotElement(x, CC) in self.inferences:
            return False
        if x.head() in (Pos, Neg, Add, Sub, Mul, Sqrt, Exp, Sin, Cos):
            if all(self.is_complex(arg) for arg in x.args()):
                return True
        if x.head() == Div:
            p, q = x.args()
            if self.is_complex(p) and self.is_complex(q) and self.is_not_zero(q):
                return True
        if x.head() == Pow:
            base, exp = x.args()
            # todo: more generally for re(exp) > 0
            if self.is_complex(base) and self.is_complex(exp) and \
                (self.is_not_zero(base) or (self.is_real(exp) and self.is_positive(exp))):
                return True
        if x.head() == Log:
            arg, = x.args()
            if self.is_complex(arg) and self.is_not_zero(arg):
                return True
        if self.is_infinity(x) or x == Undefined:
            return False
        return None

    # todo: identify different types; bools, tuples, sets, matrices, ...
    def equal(self, a, b):
        """
        Check if a and b are equal (represent exactly the same mathematical
        object). Returns True, False, or None for unknown.
        """
        assert isinstance(a, Expr)
        assert isinstance(b, Expr)
        if a == b:
            return True
        if a.is_integer() and b.is_integer():
            return False

        if Equal(a, b) in self.inferences:
            return True
        if Equal(b, a) in self.inferences:
            return True
        if NotEqual(a, b) in self.inferences:
            return False
        if NotEqual(b, a) in self.inferences:
            return False

        # try numerical exclusion test
        val1 = self.complex_enclosure(a)
        if val1 is not None:
            val2 = self.complex_enclosure(b)
            if val2 is not None:
                if not val1.overlaps(val2):
                    return False
                val3 = self.complex_enclosure(a - b)
                if not val3.contains(0):
                    return False

        # try exact computation
        from .algebraic import alg_get_degree_limit, alg_set_degree_limit
        from .algebraic import alg_get_bits_limit, alg_set_bits_limit
        
        orig_degree = alg_get_degree_limit()
        orig_bits = alg_get_bits_limit()
        try:
            alg_set_degree_limit(200)
            alg_set_bits_limit(100000)

            val1 = self.evaluate_alg_or_None(a)
            if val1 is not None:
                val2 = self.evaluate_alg_or_None(b)
                if val2 is not None:
                    return val1 == val2

        finally:
            alg_set_degree_limit(orig_degree)
            alg_set_bits_limit(orig_bits)

        # try domain exclusions
        aq = self.is_rational(a)
        bq = self.is_rational(b)
        if aq is not None and bq is not None and aq != bq:
            return False
        if aq and bq:
            aq = self.is_integer(a)
            bq = self.is_integer(b)
            if aq is not None and bq is not None and aq != bq:
                return False

        aq = self.is_complex(a)
        bq = self.is_complex(b)
        if aq is not None and bq is not None and aq != bq:
            return False
        if aq and bq:
            aq = self.is_real(a)
            bq = self.is_real(b)
            if aq is not None and bq is not None and aq != bq:
                return False

        aq = self.is_infinity(a)
        bq = self.is_infinity(b)
        if aq is not None and bq is not None and aq != bq:
            return False
        return None

    def greater(self, a, b):
        v = self.simple(Greater(a, b))
        if v == True_:
            return True
        if v == False_:
            return False
        return None

    def less(self, a, b):
        v = self.simple(Less(a, b))
        if v == True_:
            return True
        if v == False_:
            return False
        return None

    def greater_equal(self, a, b):
        v = self.simple(GreaterEqual(a, b))
        if v == True_:
            return True
        if v == False_:
            return False
        return None

    def less_equal(self, a, b):
        v = self.simple(LessEqual(a, b))
        if v == True_:
            return True
        if v == False_:
            return False
        return None

    def is_extended_real(self, x):
        if x == Infinity:
            return True
        if x == -Infinity:
            return True
        v = self.is_real(x)
        if v:
            return True
        if v is False and self.is_complex(x):
            return False
        return None

    def element(self, x, S):
        """
        Check if x is an element of S.
        Returns True, False, or None for unknown.
        """
        assert isinstance(x, Expr)
        if Element(x, S) in self.inferences:
            return True
        if NotElement(x, S) in self.inferences:
            return False
        if S == CC:
            return self.is_complex(x)
        if S == RR:
            return self.is_real(x)
        if S == QQ:
            return self.is_rational(x)
        if S == ZZ:
            return self.is_integer(x)
        if S == HH:
            c1 = self.is_complex(x)
            if not c1:
                return c1
            return self.is_positive(Im(x))
        if S == PP:
            z = self.is_integer(x)
            if not z:
                return z
            if x.is_integer() and int(x) <= 20:
                return int(x) in [2,3,5,7,11,13,17,19]
            return None
        if S == AlgebraicNumbers:
            return self.is_algebraic(x)
        head = S.head()
        if head == ZZGreaterEqual:
            a, = S.args()
            v = self.is_integer(x)
            if not v:
                return v
            return self.less_equal(a, x)
        if head == ZZLessEqual:
            b, = S.args()
            v = self.is_integer(x)
            if not v:
                return v
            return self.less_equal(x, b)
        if head == Range:
            a, b = S.args()
            v = self.is_integer(x)
            if not v:
                return v
            v = self.less_equal(a, x)
            if not v:
                return v
            return self.less_equal(x, b)
        if head in (ClosedInterval, OpenInterval, ClosedOpenInterval, OpenClosedInterval):
            a, b = S.args()
            v = self.is_extended_real(a)
            if not v:
                return None
            v = self.is_extended_real(b)
            if not v:
                return None
            v = self.is_extended_real(x)
            if not v:
                return v
            if head != ClosedInterval and a == b:
                return False
            if head == ClosedInterval or head == ClosedOpenInterval:
                v = self.less_equal(a, x)
                if not v:
                    return v
            else:
                v = self.less(a, x)
                if not v:
                    return v
            if head == ClosedInterval or head == OpenClosedInterval:
                v = self.less_equal(x, b)
                return v
            else:
                v = self.less(x, b)
                return v
        # todo: check for comprehensions
        if head == Set:
            check = [self.equal(x, y) for y in S.args()]
            if True in check:
                return True
            if all(c == False for c in check):
                return False
            return None
        # todo: check for comprehensions
        if head == Union:
            if len(S.args()) == 0:
                return False
            check = [self.element(x, T) for T in S.args()]
            if True in check:
                return True
            if all(c == False for c in check):
                return False
            return None
        # todo: check for comprehensions
        if head == Intersection:
            assert len(S.args()) >= 1
            check = [self.element(x, T) for T in S.args()]
            if all(c == True for c in check):
                return True
            if False in check:
                return False
            return None
        if head == SetMinus:
            assert len(S.args()) == 2
            T, U = S.args()
            v1 = self.element(x, T)
            if v1 == False:
                return False
            v2 = self.element(x, U)
            if v1 == True and v2 == False:
                return True
            if v1 == True and v2 == True:
                return False
            return None
        return None

    def simple_Not(self, x):
        """
        Return an expression equivalent to Not(x), simplified if possible.
        """
        x = self.simple(x)
        if x == True_:
            return False_
        if x == False_:
            return True_
        if x.head() == NotEqual and len(x.args()) == 2:
            return Equal(*x.args())
        if x.head() == Equal and len(x.args()) == 2:
            return NotEqual(*x.args())
        if x.head() == NotElement and len(x.args()) == 2:
            return Element(*x.args())
        if x.head() == Element and len(x.args()) == 2:
            return NotElement(*x.args())
        return Not(x)

    def simple_And(self, *args):
        # todo: identify For-expression iteration, etc.
        # todo: early termination
        # todo: postponed simplifications
        args = [self.simple(arg) for arg in args]
        if False_ in args:
            return False_
        args = [arg for arg in args if arg != True_]
        if len(args) == 0:
            return True_
        if len(args) == 1:
            return args[0]
        return And(*args)

    def simple_Or(self, *args):
        # todo: identify For-expression iteration, etc.
        # todo: early termination
        # todo: postponed simplifications
        args = [self.simple(arg) for arg in args]
        if True_ in args:
            return True_
        args = [arg for arg in args if arg != False_]
        if len(args) == 0:
            return False_
        if len(args) == 1:
            return args[0]
        return Or(*args)

    def simple_Implies(self, *args):
        args = [self.simple(arg) for arg in args]
        assert len(args) == 2
        P, Q = args
        if P == False_:
            return True_
        if P == True_:
            return Q
        return Implies(*args)

    def simple_Equal(self, *args):
        args = [self.simple(arg) for arg in args]
        assert len(args) >= 2   # define Equal for len = 0, 1 ?
        # all equal
        if all(self.equal(args[0], arg) for arg in args[1:]):
            return True_
        # any not equal
        for i in range(len(args)):
            for j in range(i + 1, len(args)):
                a = args[i]
                b = args[j]
                if self.equal(a, b) == False:
                    return False_
        # todo: remove duplicates?
        return Equal(*args)

    def simple_NotEqual(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) != 2:
            return NotEqual(*args) # XXX
        # all equal
        if all(self.equal(args[0], arg) for arg in args[1:]):
            return False_
        # any not equal
        for i in range(len(args)):
            for j in range(i + 1, len(args)):
                a = args[i]
                b = args[j]
                if self.equal(a, b) == False:
                    return True_
        # todo: remove duplicates?
        return NotEqual(*args)

    def simple_Element(self, *args):
        args = [self.simple(arg) for arg in args]
        head = Element
        assert len(args) == 2
        v = self.element(args[0], args[1])
        if v == True:
            if head == Element:
                return True_
            else:
                return False_
        if v == False:
            if head == Element:
                return False_
            else:
                return True_
        return Element(*args)

    def simple_NotElement(self, *args):
        args = [self.simple(arg) for arg in args]
        head = NotElement
        assert len(args) == 2
        v = self.element(args[0], args[1])
        if v == True:
            if head == Element:
                return True_
            else:
                return False_
        if v == False:
            if head == Element:
                return False_
            else:
                return True_
        return NotElement(*args)

    def simple_LessEqual(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            a, b = args
            if a.is_integer() and b.is_integer():
                if int(a) <= int(b):
                    return True_
                else:
                    return False_
            if self.is_real(a) and self.is_real(b):
                v = self.real_enclosure(a - b)
                if v is not None:
                    if v <= 0:
                        return True_
                    if v > 0:
                        return False_
            if self.is_extended_real(a) and self.is_extended_real(b):
                if self.equal(a, b):
                    return True_
                if a == -Infinity:
                    return True_
                if b == Infinity:
                    return True_
                if self.is_real(a) and b == -Infinity:
                    return False_
                if self.is_real(b) and a == Infinity:
                    return False_
                if a == Infinity and b == -Infinity:
                    return False_
        return LessEqual(*args)

    def simple_Less(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            a, b = args
            if a.is_integer() and b.is_integer():
                if int(a) < int(b):
                    return True_
                else:
                    return False_
            if self.is_real(a) and self.is_real(b):
                v = self.real_enclosure(a - b)
                if v is not None:
                    if v < 0:
                        return True_
                    if v >= 0:
                        return False_
            if self.is_extended_real(a) and self.is_extended_real(b):
                if self.equal(a, b):
                    return False_
                if a == -Infinity and self.is_real(b):
                    return True_
                if a == -Infinity and b == Infinity:
                    return True_
                if self.is_real(a) and b == Infinity:
                    return True_
                if a == Infinity:
                    return False_
                if b == -Infinity:
                    return False_
        return Less(*args)

    def simple_GreaterEqual(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            a, b = args
            if a.is_integer() and b.is_integer():
                if int(a) >= int(b):
                    return True_
                else:
                    return False_
            if self.is_real(a) and self.is_real(b):
                v = self.real_enclosure(a - b)
                if v is not None:
                    if v >= 0:
                        return True_
                    if v < 0:
                        return False_
            if self.is_extended_real(a) and self.is_extended_real(b):
                if self.equal(a, b):
                    return True_
                if b == -Infinity:
                    return True_
                if a == Infinity:
                    return True_
                if self.is_real(b) and a == -Infinity:
                    return False_
                if self.is_real(a) and b == Infinity:
                    return False_
                if b == Infinity and a == -Infinity:
                    return False_
        return GreaterEqual(*args)

    def simple_Greater(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            a, b = args
            if a.is_integer() and b.is_integer():
                if int(a) > int(b):
                    return True_
                else:
                    return False_
            if self.is_real(a) and self.is_real(b):
                v = self.real_enclosure(a - b)
                if v is not None:
                    if v > 0:
                        return True_
                    if v <= 0:
                        return False_
            if self.is_extended_real(a) and self.is_extended_real(b):
                if self.equal(a, b):
                    return False_
                if b == -Infinity and self.is_real(a):
                    return True_
                if b == -Infinity and a == Infinity:
                    return True_
                if self.is_real(b) and a == Infinity:
                    return True_
                if b == Infinity:
                    return False_
                if a == -Infinity:
                    return False_
        return Greater(*args)

    def simple_Pos(self, x):
        return self.simple(x)

    def simple_Parentheses(self, x):
        return self.simple(x)

    def simple_Brackets(self, x):
        return self.simple(x)

    def simple_Braces(self, x):
        return self.simple(x)

    def simple_Neg(self, x):
        x = self.simple(x)
        if x.head() == Neg:
            v, = x.args()
            return v
        if x.head() == Sub:
            a, b = x.args()
            return Sub(b, a)
        if x.is_integer():
            v = int(x)
            return Expr(-v)
        return Neg(x)

    def complexity(self, expr):
        if expr in self.penalty:
            return self.penalty[expr]
        if expr.is_integer():
            v = int(expr)
            return 1 + v.bit_length() + (v<0)
        if expr.is_atom():
            if expr in [True_, False_]:
                return 1
            if expr in [Add, Sub, Neg, Pos, Mul]:
                return 10
            if expr in [Div, Sqrt, GoldenRatio, ConstI]:
                return 20
            if expr in [Pi, ConstE, Pow, Exp, Log, Sin, Cos, Tan, Sinh, Cosh, Tanh]:
                return 100
            if expr in [Gamma, Erf, Erfc, Erfi, RiemannZeta, ConstGamma, ConstCatalan]:
                return 1000
            return 1000000
        head = expr.head()
        args = expr.args()
        a = self.complexity(head)
        b = sum(self.complexity(arg) for arg in args)
        return a + 2*b + 1

    def evaluate_fmpq(self, expr):
        if expr.is_integer():
            return self._fmpq(int(expr))
        elif expr.head() == Neg:
            x, = expr.args()
            return -self.evaluate_fmpq(x)
        elif expr.head() == Sub:
            x, y = expr.args()
            return self.evaluate_fmpq(x) - self.evaluate_fmpq(y)
        elif expr.head() == Add:
            s = self._fmpq(0)
            for x in expr.args():
                s += self.evaluate_fmpq(x)
            return s
        elif expr.head() == Mul:
            s = self._fmpq(1)
            for x in expr.args():
                s *= self.evaluate_fmpq(x)
            return s
        elif expr.head() == Div:
            x, y = expr.args()
            return self.evaluate_fmpq(x) / self.evaluate_fmpq(y)
        elif expr.head() == Pow:
            x, y = expr.args()
            y = self.simple(y)
            if y.is_integer():
                return self.evaluate_fmpq(x) ** int(y)
        raise NotImplementedError

    def evaluate_fmpq_poly(self, expr, var):
        from flint import fmpq_poly, fmpq
        if expr == var:
            return fmpq_poly([0,1])
        elif expr.is_integer():
            return fmpq_poly([fmpq(int(expr))])
        elif expr.head() == Neg:
            x, = expr.args()
            return -self.evaluate_fmpq_poly(x, var)
        elif expr.head() == Sub:
            x, y = expr.args()
            return self.evaluate_fmpq_poly(x, var) - self.evaluate_fmpq_poly(y, var)
        elif expr.head() == Add:
            s = fmpq_poly()
            for x in expr.args():
                s += self.evaluate_fmpq_poly(x, var)
            return s
        elif expr.head() == Mul:
            s = fmpq_poly([1])
            for x in expr.args():
                s *= self.evaluate_fmpq_poly(x, var)
            return s
        elif expr.head() == Div:
            x, y = expr.args()
            return self.evaluate_fmpq_poly(x, var) / self.evaluate_fmpq(y)
        elif expr.head() == Pow:
            x, y = expr.args()
            x = self.evaluate_fmpq_poly(x, var)
            y = self.evaluate_fmpq(y)
            if y.q == 1 and y.p >= 0:
                return x ** int(y.p)
            else:
                raise NotImplementedError
        else:
            v = self.evaluate_fmpq(expr)
            return fmpq_poly([v])

    def evaluate_fmpq_mat(self, expr):
        from flint import fmpq_mat, fmpq
        if expr.head() == Matrix2x1:
            a, b = expr.args()
            a = self.evaluate_fmpq(a)
            b = self.evaluate_fmpq(b)
            return fmpq_mat([[a],[b]])
        if expr.head() == Matrix2x2:
            a, b, c, d = expr.args()
            a = self.evaluate_fmpq(a)
            b = self.evaluate_fmpq(b)
            c = self.evaluate_fmpq(c)
            d = self.evaluate_fmpq(d)
            return fmpq_mat([[a,b],[c,d]])
        if expr.head() == Matrix:
            args = expr.args()
            if len(args) == 1 and args[0].head() in (List, Tuple):
                rows = args[0].args()
                eval_rows = []
                for row in rows:
                    if row.head() not in (List, Tuple):
                        raise NotImplementedError
                    row = [self.evaluate_fmpq(x) for x in row.args()]
                    eval_rows.append(row)
                return fmpq_mat(eval_rows)
            if len(args) == 3 and args[1].head() == For and args[2].head() == For:
                i, a, b = args[1].args()
                j, c, d = args[2].args()
                elem = args[0]
                a = self.simple(a)
                b = self.simple(b)
                c = self.simple(c)
                d = self.simple(d)
                if a.is_integer() and b.is_integer() and c.is_integer() and d.is_integer():
                    a = int(a)
                    b = int(b)
                    c = int(c)
                    d = int(d)
                    rows = []
                    for ii in range(a, b+1):
                        rows.append([])
                        for jj in range(c, d+1):
                            # xxx
                            val = elem.replace({i:Expr(ii), j:Expr(jj)})
                            val = self.evaluate_fmpq(val)
                            rows[-1].append(val)
                    return fmpq_mat(rows)
        if expr.head() == Neg:
            A, = args()
            return -self.evaluate_fmpq_mat(A)
        if expr.head() == Sub:
            A, B = args()
            return self.evaluate_fmpq_mat(A) - self.evaluate_fmpq_mat(B)
        if expr.head() == Add and len(expr.args()) >= 1:
            args = expr.args()
            A = self.evaluate_fmpq_mat(args[0])
            for B in args[1:]:
                A += self.evaluate_fmpq_mat(B)
            return A
        if expr.head() == Mul and len(expr.args()) >= 1:
            args = expr.args()
            A = self.evaluate_fmpq_mat(args[0])
            for B in args[1:]:
                A *= self.evaluate_fmpq_mat(B)
            return A
        if expr.head() == Pow:
            mat, exp = expr.args()
            exp = self.simple(exp)
            if exp.is_integer():
                mat = self.evaluate_fmpq_mat(mat)
                return mat ** int(exp)
        if expr.head() == HilbertMatrix:
            n, = expr.args()
            n = self.simple(n)
            if n.is_integer() and int(n) >= 0:
                n = int(n)
                return fmpq_mat.hilbert(n, n)
        raise NotImplementedError

    def evaluate_alg(self, expr):
        from .algebraic import alg
        if expr.is_atom():
            if expr.is_integer():
                return alg(int(expr))
            if expr == ConstI:
                return alg.i()
            if expr == GoldenRatio:
                return alg.phi()
            raise ValueError
        head = expr.head()
        if head == Pos:
            x, = expr.args()
            return self.evaluate_alg(x)
        elif head == Neg:
            x, = expr.args()
            return -self.evaluate_alg(x)
        elif head == Sub:
            x, y = expr.args()
            return self.evaluate_alg(x) - self.evaluate_alg(y)
        elif head == Add:
            s = alg(0)
            for x in expr.args():
                s += self.evaluate_alg(x)
            return s
        elif head == Mul:
            s = alg(1)
            for x in expr.args():
                s *= self.evaluate_alg(x)
            return s
        elif head == Div:
            x, y = expr.args()
            return self.evaluate_alg(x) / self.evaluate_alg(y)
        elif head == Sqrt:
            x, = expr.args()
            return self.evaluate_alg(x).sqrt()
        elif head == Pow:
            x, y = expr.args()
            x = self.evaluate_alg(x)
            y = self.evaluate_alg(y)
            return x ** y
        elif head == Sign:
            x, = expr.args()
            return self.evaluate_alg(x).sgn()
        elif head == Re:
            x, = expr.args()
            return self.evaluate_alg(x).real
        elif head == Im:
            x, = expr.args()
            return self.evaluate_alg(x).imag
        elif head == Abs:
            x, = expr.args()
            return abs(self.evaluate_alg(x))
        elif head in (Exp, Cos, Sin, Tan, Cot, Sec, Csc):
            x, = expr.args()
            v = self.simple(x / Pi)
            v = self.evaluate_alg(v)
            if head == Exp:
                v = v.imag
            if v.is_rational():
                v = v.fmpq()
                if head == Exp:
                    return alg.exp_pi_i(v)
                elif head == Cos:
                    return alg.cos_pi(v)
                elif head == Sin:
                    return alg.sin_pi(v)
                elif head == Tan:
                    return alg.tan_pi(v)
                elif head == Cot:
                    return alg.cot_pi(v)
                elif head == Sec:
                    return alg.sec_pi(v)
                elif head == Csc:
                    return alg.csc_pi(v)
        else:
            raise NotImplementedError

    def evaluate_alg_or_None(self, expr):
        try:
            return self.evaluate_alg(expr)
        except (ValueError, NotImplementedError):
            return None

    def alg_to_expression(self, x):
        from .algebraic import alg

        x = alg(x)

        if x.is_rational():
            x = x.fmpq()
            p = x.p
            q = x.q
            if q == 1:
                return Expr(int(p))
            elif p < 0:
                return Neg(Div(int(-p), int(q)))
            else:
                return Div(int(p), int(q))

        if x.degree() == 2:
            fmpz = self._fmpz
            a, b, c = x.as_quadratic()
            if b == 0:
                return Expr(a)
            A = Expr(a)
            if c > 0:
                B = Sqrt(c)
            elif c == -1:
                B = ConstI
            else:
                B = Mul(Sqrt(-c), ConstI)
            if b == 1:
                if a == 0:
                    return B
                else:
                    return Add(A, B)
            elif b == -1:
                if a == 0:
                    return Neg(B)
                else:
                    return Sub(A, B)
            elif b > 0:
                if a == 0:
                    return Mul(b, B)
                else:
                    return Add(A, Mul(b, B))
            else:
                if a == 0:
                    return Neg(Mul(-b, B))
                else:
                    return Sub(A, Mul(-b, B))

        from flint import fmpz_poly, fmpq

        pol = x.minpoly()
        d = pol.degree()
        # identify roots of unity
        n = pol.is_cyclotomic()
        if n > 0:
            pol2 = fmpz_poly.cyclotomic(n)
            if pol == pol2:
                # todo: this can be faster
                for k in range(1, n+1):
                    v = alg.exp_two_pi_i(fmpq(k, n))
                    if v == x:
                        return self.simple_Exp_two_pi_i_k_n(k, n)
        # identify rational multiples of roots of unity
        if pol[d-1] != 0:
            q = pol[d].root(d)
            if q**d == pol[d]:
                if pol[d-1] % q**(d-1) == 0:
                    p = pol[d-1] // q**(d-1)
                    v = fmpq(p,q)
                    u = x / v
                    if u.minpoly().is_cyclotomic():
                        return v * self.alg_to_expression(u)

        fmpq = self._fmpq
        # try depression
        deg = x.degree()
        pol = x.minpoly()
        a = pol[deg]
        b = pol[deg-1]
        if b != 0:
            shift = fmpq(-b, deg * a)
            res = self.alg_to_expression(x - shift)
            if res is not None:
                return res + shift

        # try deflation
        pol, n = pol.deflation()
        if n > 1:
            neg = False
            if x.is_real() and x < 0:
                x = -x
                neg = True
            v = x ** n
            vroot = v.root(n)
            A = self.alg_to_expression(v)
            if A is not None:
                if n == 2:
                    A = Sqrt(A)
                else:
                    A = Pow(A, Div(1, n))
                for k in range(n):
                    s = alg.exp_two_pi_i(self._fmpq(k,n))
                    if s * vroot == x:
                        if neg:
                            t = self._fmpq(k,n) + self._fmpq(1,2)
                            k, n = t.p, t.q
                        B = self.simple_Exp_two_pi_i_k_n(k, n)
                        if B == Expr(1):
                            return A
                        if B == Expr(-1):
                            return Neg(A)
                        if B == ConstI:
                            return A * B
                        if B == -ConstI:
                            return -(A * B)
                        return B * A

        if x.degree() == 3:
            fmpz = self._fmpz
            d, c, b, a = map(int, list(x.minpoly()))
            D0 = b**2 - 3*a*c
            D1 = 2*b**3 - 9*a*b*c + 27*a**2*d
            C3 = (D1 + alg(D1**2 - 4*D0**3).sqrt()) / 2
            if C3 == 0:
                C3 = (D1 - alg(D1**2 - 4*D0**3).sqrt()) / 2
            C = self.alg_to_expression(C3)
            assert C is not None
            C = Pow(C, Div(1, 3))
            w1 = self.simple_Exp_two_pi_i_k_n(1, 3)
            w2 = self.simple_Exp_two_pi_i_k_n(2, 3)
            x0 = (int(b) + C + int(D0) / C) / (-3*a)
            x1 = (int(b) + w1*C + w2 * int(D0) / C) / int(-3*a)
            x2 = (int(b) + w2*C + w1 * int(D0) / C) / int(-3*a)
            if self.evaluate_alg(x0) == x:
                return x0
            if self.evaluate_alg(x1) == x:
                return x1
            if self.evaluate_alg(x2) == x:
                return x2
        if x.degree() == 4:
            # see: http://eqworld.ipmnet.ru/en/solutions/ae/ae0108.pdf

            fmpz = self._fmpz
            fmpq = self._fmpq
            from flint import fmpz_poly, fmpq_poly
            pol = x.minpoly()

            e,d,c,b,a = map(fmpq, list(pol))

            shift = -b/(4*a)
            reduced = fmpq_poly(pol)(fmpq_poly([shift,1]))
            reduced /= reduced[4]
            p = reduced[2]
            q = reduced[1]
            r = reduced[0]

            # biquadratic!
            if q == 0:
                raise ValueError("should not be biquadratic!")
                roots = alg.polynomial_roots([r,p,1])
                for cand, _ in roots:
                    cand = Sqrt(self.alg_to_expression(cand))
                    for sign in [1,-1]:
                        if sign == 1:
                            cand2 = shift + cand
                        else:
                            cand2 = shift - cand
                        if self.evaluate_alg(cand2) == x:
                            return cand2


            resroots = alg.polynomial_roots([-q*q, p*p-4*r, 2*p, 1])

            resroots2 = []
            for r, m in resroots:
                for i in range(m):
                    resroots2.append(r)

            resroots3 = []
            for r in resroots2:
                v = r.sqrt()
                if v.degree() <= 2:
                    resroots3.append(self.alg_to_expression(v))
                else:
                    resroots3.append(Sqrt(self.alg_to_expression(r)))

            a, b, c = resroots3
            xs = [a+b+c, a+b-c, a-b+c, a-b-c, -a+b+c, -a+b-c, -a-b+c, -a-b-c]
            for xn in xs:
                xn = xn / 2
                xn += shift
                if self.evaluate_alg(xn) == x:
                    return xn

        if not x.is_real():
            re = self.alg_to_expression(x.real)
            if re is not None:
                im = self.alg_to_expression(x.imag)
                if im is not None:
                    if im == Expr(0):
                        return re
                    elif re == Expr(0):
                        return im*ConstI
                    else:
                        return re + im*ConstI
        return None

    def simple_Exp_two_pi_i_k_n(self, k, n):
        k = k % (2 * n)
        if k == 0:
            return Expr(1)
        if n == 2 * k:
            return Expr(-1)
        if n == 4 * k:
            return ConstI
        if 3 * n == 4 * k:
            return -ConstI
        if n == 8 * k:
            return Sqrt(2)/2 * (1 + ConstI)
        if 3 * n == 8 * k:
            return Sqrt(2)/2 * (-1 + ConstI)
        if 5 * n == 8 * k:
            return Sqrt(2)/2 * (-1 - ConstI)
        if 7 * n == 8 * k:
            return Sqrt(2)/2 * (1 - ConstI)
        if n == 3 * k:
            return (-1 + Sqrt(3)*ConstI)/2
        if 2 * n == 3 * k:
            return (-1 - Sqrt(3)*ConstI)/2
        if n == 6 * k:
            return (1 + Sqrt(3)*ConstI)/2
        if 5 * n == 6 * k:
            return (1 - Sqrt(3)*ConstI)/2
        u = 2 * self._fmpq(k, n)
        p = int(u.p)
        q = int(u.q)
        if p == 1:
            return Exp(Pi*ConstI/q)
        else:
            return Exp(p*Pi*ConstI/q)

    def simple_Add(self, *terms):
        """
        
        """
        if len(terms) == 0:
            return Expr(0)
        if len(terms) == 1:
            return self.simple(terms[0])
        # todo: we want to avoid recursive Add simplifies if possible...
        terms = [self.simple(x) for x in terms]
        if not all(self.is_complex(x) for x in terms):
            # todo: simplifications for this case
            return Add(*terms)
        constant_term = self._fmpz(0)
        term_coeff = {}
        def iter_term_coeff(terms):
            for x in terms:
                if x.is_integer():
                    yield Expr(1), self._fmpz(int(x))
                    continue
                head = x.head()
                if head == Add:
                    for t, c in iter_term_coeff(x.args()):
                        yield t, c
                elif head == Sub:
                    x, y = x.args()
                    for t, c in iter_term_coeff([x]):
                        yield t, c
                    for t, c in iter_term_coeff([y]):
                        yield t, -c
                elif head == Neg:
                    x, = x.args()
                    for t, c in iter_term_coeff([x]):
                        yield t, -c
                elif head == Mul:
                    factors = x.args()
                    # todo: make this more robust
                    if len(factors) >= 2:
                        try:
                            v = self.evaluate_fmpq(factors[0])
                        except NotImplementedError:
                            v = None
                        if v is None:
                            yield x, self._fmpz(1)
                        else:
                            red = self.simple_Mul(*factors[1:])
                            for t, c in iter_term_coeff([red]):
                                yield t, c * v
                    else:
                        yield x, self._fmpz(1)
                elif head == Div:
                    p, q = x.args()
                    if q.is_integer():
                        for t, c in iter_term_coeff([p]):
                            yield t, c / self._fmpq(int(q))
                    else:
                        yield x, self._fmpz(1)
                else:
                    yield x, self._fmpz(1)
        for t, c in iter_term_coeff(terms):
            # todo: detect rationals
            #if t.is_integer() and c.is_integer():
            #    t = int(t)
            #    c = int(c)
            #    constant_term += t * c
            #    continue
            if t in term_coeff:
                term_coeff[t] += c
            else:
                term_coeff[t] = c
        terms = []
        for t, c in term_coeff.items():
            if c == 0:
                continue
            elif c == 1:
                terms.append(t)
            elif c == -1:
                if t == Expr(1):
                    terms.append(Expr(-1))
                else:
                    terms.append(Neg(t))
            else:
                if isinstance(c, self._fmpq):
                    p = int(c.p)
                    q = int(c.q)
                    if q == 1:
                        terms.append(self.simple_Mul(t, Expr(p)))
                    else:
                        terms.append(self.simple_Mul(t, Div(p, q)))
                else:
                    c = int(c)
                    terms.append(self.simple_Mul(t, Expr(c)))
        terms = sorted(terms, key=lambda x: (not self.is_real(x), self.complexity(x), str(x)))
        if constant_term != 0:
            terms = [Expr(int(constant_term))] + terms
        if len(terms) == 0:
            return Expr(0)
        if len(terms) == 1:
            return terms[0]
        if len(terms) == 2 and terms[1].head() == Neg:
            x, = terms[1].args()
            return Sub(terms[0], x)
        return Add(*terms)

    def simple_Sub(self, x, y):
        if self.is_complex(x) and self.is_complex(y):
            return self.simple_Add(x, Neg(y))
        return Sub(self.simple(x), self.simple(y))

    '''
    def simple_Mul(self, *factors):
        u = Mul(*factors)
        v = self.simple_Mul2(*factors)
        try:
            a = u.n(as_arb=True)
            b = v.n(as_arb=True)
            if not a.overlaps(b):
                print(u)
                print(a)
                print(v)
                print(b)
                assert 0
        except (NotImplementedError, ValueError):
            pass
        return v
    '''

    def simple_Mul(self, *factors):
        """
        Simple product.
        """
        if len(factors) == 0:
            return Expr(1)
        if len(factors) == 1:
            return self.simple(factors[0])
        # todo: we want to avoid recursive Mul simplifies if possible...
        factors = [self.simple(x) for x in factors]
        if not all(self.is_complex(x) for x in factors):
            # todo: simplifications for this case
            return Mul(*factors)
        for x in factors:
            if x == Expr(0):
                return Expr(0)
        prefactor = self._fmpz(1)
        base_exp = {}
        def iter_base_exp(factors):
            for x in factors:
                head = x.head()
                if head == Mul:
                    for b, e in iter_base_exp(x.args()):
                        yield b, e
                elif head == Div:
                    p, q = x.args()
                    for b, e in iter_base_exp([p]):
                        yield b, e
                    for b, e in iter_base_exp([q]):
                        yield b, self.simple_Neg(e)
                elif head == Exp:
                    v, = x.args()
                    yield ConstE, v
                elif head == Pow:
                    b, e = x.args()
                    #b = self.simple(b)
                    if e.is_integer():
                        for b2, e2 in iter_base_exp([b]):
                            yield b2, self.simple_Mul(e2, e)
                    else:
                        yield b, e
                elif head == Sqrt:
                    v, = x.args()
                    yield v, Div(1, 2)
                elif head == Neg:
                    v, = x.args()
                    yield Expr(-1), Expr(1)
                    for b, e in iter_base_exp([v]):
                        yield b, e
                else:
                    yield x, Expr(1)
        for b, e in iter_base_exp(factors):
            if b.is_integer() and e.is_integer():
                bb = int(b)
                ee = int(e)
                if -2 <= ee <= 2 or bb == -1:
                    if bb == -1:
                        if ee % 2:
                            prefactor = -prefactor
                    elif ee >= 0:
                        prefactor *= self._fmpz(bb)**ee
                    else:
                        prefactor *= self._fmpq(1,bb**(-ee))
                    continue
            if b in base_exp:
                base_exp[b] += e
            else:
                base_exp[b] = e
        factors = []
        den_factors = []
        for b, e in base_exp.items():
            # todo: simple_Pow here?
            e = self.simple(e)
            if b == ConstE:
                if e == Expr(0):
                    pass
                elif e == Expr(1):
                    factors.append(b)
                else:
                    factors.append(Exp(e))
                continue
            if e.is_integer():
                e = int(e)
                if e == 0:
                    continue
                elif e == 1:
                    factors.append(b)
                elif e == -1:
                    den_factors.append(b)
                elif e >= 2:
                    factors.append(Pow(b, e))
                else:
                    den_factors.append(Pow(b, -e))
            elif e.head() == Neg:
                e, = e.args()
                den_factors.append(Pow(b, e))
            elif e == Div(1, 2):
                factors.append(Sqrt(b))
            else:
                factors.append(Pow(b, e))
        if isinstance(prefactor, self._fmpq):
            prefactor_den = Expr(int(prefactor.q))
            prefactor = Expr(int(prefactor.p))
        else:
            prefactor = Expr(int(prefactor))
            prefactor_den = Expr(1)
        factors = sorted(factors, key=lambda x: (not self.is_real(x), self.complexity(x), str(x)))
        den_factors = sorted(den_factors, key=lambda x: (self.is_real(x), self.complexity(x), str(x)))
        if prefactor != Expr(1):
            factors = [prefactor] + factors
        if prefactor_den != Expr(1):
            den_factors = [prefactor_den] + den_factors
        if len(factors) == 0:
            num = Expr(1)
        elif len(factors) == 1:
            num = factors[0]
        else:
            num = Mul(*factors)
        if len(den_factors) == 0:
            den = Expr(1)
        elif len(den_factors) == 1:
            den = den_factors[0]
        else:
            den = Mul(*den_factors)
        if den == Expr(1):
            return num
        else:
            return Div(num, den)

    def simple_Div(self, x, y):
        if self.is_complex(x) and self.is_complex(y) and self.is_not_zero(y):
            return self.simple_Mul(x, Pow(y, -1))
        x = self.simple(x)
        y = self.simple(y)
        if self.is_complex(x) and self.is_complex(y) and self.is_not_zero(y):
            return self.simple_Mul(x, Pow(y, -1))
        return Div(x, y)

    def simple_Pow(self, x, y):
        x = self.simple(x)
        y = self.simple(y)
        # todo: want to combine this with power simplification in Mul...
        if self.is_complex(x) and self.is_complex(y):
            if x.is_integer() and y.is_integer():
                a = int(x)
                b = int(y)
                if 0 <= b <= 2:
                    return Expr(a**b)
            if y == Expr(0):
                return Expr(1)
            if y == Expr(1):
                return x
            if x == Expr(1):
                return Expr(1)
            if x == Expr(0):
                if self.is_positive(y):
                    return Expr(0)
                if self.is_negative(y):
                    return UnsignedInfinity
        if x == ConstE:
            # todo: maybe don't want this much ... ?
            #v = self.simple(y / (Pi * ConstI / 120))
            #if v.is_integer():
            #    a = self.simple(Cos(v * Pi / 120))
            #    b = self.simple(Sin(v * Pi / 120))
            #    return self.simple(a + b * ConstI)
            return Exp(y)
        return Pow(x, y)

    def simple_Exp(self, x):
        return self.simple_Pow(ConstE, x)

    def simple_Sin(self, x):
        x = self.simple(x)
        if x == Expr(0):
            return x
        if self.is_complex(x):
            v = self.simple(x / Pi)
            if self.is_integer(v):
                return Expr(0)
            v = self.simple(x * (120 / Pi))
            if v.is_integer():
                v = int(v)
                v = v % 240
                def _sin(v):
                    if v > 60:
                        v = 120 - v
                    if v == 0: return Expr(0)
                    if v == 10: return (Sqrt(2)*(Sqrt(3)-1))/4   # todo: sqrt(6)?
                    if v == 12: return (Sqrt(5)-1)/4
                    if v == 15: return Sqrt(2-Sqrt(2))/2
                    if v == 20: return Div(1,2)
                    if v == 30: return Sqrt(2)/2
                    if v == 36: return (Sqrt(5)+1)/4
                    if v == 40: return Sqrt(3)/2
                    if v == 45: return Sqrt(Sqrt(2)+2)/2
                    if v == 50: return (Sqrt(2)*(Sqrt(3)+1))/4
                    if v == 60: return Expr(1)
                    if v > 30:
                        return Cos(self.simple(Pi*(60-v)/120))
                    else:
                        return Sin(self.simple(Pi*v/120))
                if v >= 120:
                    return self.simple(-_sin(v-120))
                else:
                    return _sin(v)
            if self.is_negative(x):
                return -Sin(self.simple(-x))
            v = self.simple(x / ConstI)
            if self.is_real(v):
                return self.simple(Sinh(v) * ConstI)
        return Sin(x)

    def simple_Cos(self, x):
        x = self.simple(x)
        if x == Expr(0):
            return Expr(1)
        if self.is_complex(x):
            v = self.simple(x * (120 / Pi))
            if v.is_integer():
                return self.simple(Sin((int(v)+60)*Pi/120))
            if self.is_negative(x):
                return Cos(self.simple(-x))
            v = self.simple(x / ConstI)
            if self.is_real(v):
                return self.simple(Cosh(v))
        return Cos(x)

    # todo: have this call simple_Pow, implementing all simplifications there?
    def simple_Sqrt(self, x):
        """
        Return an expression equivalent to Sqrt(x), simplified if possible.
        """
        x = self.simple(x)
        if x in (Expr(0), Expr(1), Infinity, UnsignedInfinity, Undefined):
            return x
        if x == Expr(-1):
            return ConstI
        if x == -Infinity:
            return ConstI * Infinity
        if x.is_integer():
            # todo: call an actual square root function
            v = int(x)
            real = v >= 0
            v = abs(v)
            if v < 1e100:
                r = int(round(v ** 0.5))
                if r * r == v:
                    return Expr(r) if real else Expr(r)*ConstI
        # todo: wanted?
        if self.is_negative(x):
            return self.simple_Sqrt(-x) * ConstI
        # todo: generalize
        if x.head() == Pow:
            base, exp = x.args()
            if exp.is_integer():
                exp = int(exp)
                if exp % 2 == 0 and exp > 0 and self.is_real(base) and self.is_nonnegative(base):
                    if exp == 2:
                        return base
                    else:
                        return Pow(base, exp // 2)
        return Sqrt(x)

    def simple_Abs(self, x):
        """
        Return an expression equivalent to Abs(x), simplified if possible.
        """
        x = self.simple(x)
        if x.is_integer():
            v = int(x)
            if v >= 0:
                return x
            else:
                return Expr(-v)
        if x == Undefined:
            return x
        if self.is_infinity(x):
            return Infinity
        val = self.complex_enclosure(x)
        if val is not None:
            real, imag = val.real, val.imag
            if imag == 0:
                if real >= 0:
                    return x
                if real < 0:
                    return self.simple(-x)
            if real == 0:
                if imag >= 0:
                    return self.simple(-ConstI * x)
                if imag < 0:
                    return self.simple(ConstI * x)
        if self.is_nonnegative(x):
            return x
        if self.is_nonpositive(x):
            return self.simple(-x)
        if x.head() == Exp:
            v, = x.args()
            # todo: is_imaginary
            if self.is_complex(v):
                if self.is_real(self.simple(v / ConstI)):
                    return Expr(1)
        return Abs(x)

    def simple_Re(self, x):
        x = self.simple(x)
        if self.is_integer(x):
            return x
        if not self.is_complex(x):
            return Re(x)
        if self.is_real(x):
            return x
        if x.head() == Add:
            return self.simple_Add(*[self.simple_Re(t) for t in x.args()])
        if x.head() == Sub:
            a, b = x.args()
            return self.simple_Sub(self.simple_Re(a), self.simple_Re(b))
        if x.head() == Neg:
            a, = x.args()
            return self.simple_Neg(self.simple_Re(a))
        if x.head() == Mul:
            real = []
            nonreal = []
            for t in x.args():
                if self.is_real(t):
                    real.append(t)
                else:
                    nonreal.append(t)
            if real:
                return self.simple(Mul(*real) * Re(Mul(*nonreal)))
        if x.head() == Div:
            a, b = x.args()
            if self.is_not_zero(b):
                if self.is_real(b):
                    if self.is_real(a):
                        return a / b
                    return self.simple(Re(a) / b)
        if x.head() == Exp:
            a, = x.args()
            return self.simple(Exp(Re(a)) * Cos(Im(a)))
        v = self.complex_enclosure(x)
        if v is not None:
            if v.real == 0:
                return Expr(0)
        return Re(x)

    def simple_Im(self, x):
        x = self.simple(x)
        if not self.is_complex(x):
            return Im(x)
        if self.is_real(x):
            return Expr(0)
        if x == ConstI:
            return Expr(1)
        if x.head() == Add:
            return self.simple_Add(*[self.simple_Im(t) for t in x.args()])
        if x.head() == Sub:
            a, b = x.args()
            return self.simple_Sub(self.simple_Im(a), self.simple_Im(b))
        if x.head() == Neg:
            a, = x.args()
            return self.simple_Neg(self.simple_Im(a))
        if x.head() == Mul:
            real = []
            nonreal = []
            for t in x.args():
                if self.is_real(t):
                    real.append(t)
                else:
                    nonreal.append(t)
            if real:
                return self.simple(Mul(*real) * Im(Mul(*nonreal)))
        if x.head() == Exp:
            a, = x.args()
            return self.simple(Exp(Re(a)) * Sin(Im(a)))
        xdivi = self.simple(x / ConstI)
        if self.is_real(xdivi):
            return xdivi
        return Im(x)

    def simple_Arg(self, x):
        x = self.simple(x)
        if not self.is_complex(x):
            return Arg(x)
        if x == Expr(0):
            return x
        if self.is_nonnegative(x):
            return Expr(0)
        if self.is_negative(x):
            return Pi
        if self.is_positive(x / ConstI):
            return Pi / 2
        if self.is_negative(x / ConstI):
            return self.simple(-Pi / 2)
        return Arg(x)

    def simple_Floor(self, x):
        x = self.simple(x)
        if self.is_integer(x):
            return x
        # xxx: dynamic precision / bounds
        v = self.real_enclosure(Floor(x))
        if v.is_exact() and abs(v) < self._arb("1e1000"):
            v = v.unique_fmpz()
            return Expr(v)
        return Floor(x)

    def simple_Ceil(self, x):
        x = self.simple(x)
        if self.is_integer(x):
            return x
        # xxx: dynamic precision / bounds
        v = self.real_enclosure(Ceil(x))
        if v.is_exact() and abs(v) < self._arb("1e1000"):
            v = v.unique_fmpz()
            return Expr(v)
        return Ceil(x)

    def simple_DirichletCharacter(self, *args):
        args = [self.simple(x) for x in args]
        if len(args) == 3:
            q, p, n = args
            if q.is_integer() and p.is_integer() and n.is_integer():
                q = int(q)
                p = int(p)
                n = int(n)
                from flint import dirichlet_char
                try:
                    char = dirichlet_char(q, p)
                except (AssertionError, ValueError, OverflowError):
                    return DirichletCharacter(*args)
                a = char.chi_exponent(n)
                if a is None:
                    return Expr(0)
                b = char.group().exponent()
                return self.simple_Exp_two_pi_i_k_n(a, b)
        return DirichletCharacter(*args)

    def simple_Zeros(self, *args):
        if len(args) == 3:
            expr, foriter, cond = args
        elif len(args) == 2:
            expr, foriter = args
            cond = True_
        else:
            return Zeros(*args)

        if foriter.head() == ForElement:
            var, domain = foriter.args()
            # xxx: better function for this
            inferences = set()
            infer_domain(inferences, var, domain)
            if Element(var, CC) in inferences:
                orig_cond = cond
                cond = And(Element(var, domain), cond)
                try:
                    poly = self.evaluate_fmpq_poly(expr, var)
                except NotImplementedError:
                    poly = None
                if poly is None:
                    expr = self.simple(expr)
                    try:
                        poly = self.evaluate_fmpq_poly(expr, var)
                    except NotImplementedError:
                        poly = None
                if poly is not None:
                    if poly == 0:
                        if len(args) == 2:
                            return Set(var, ForElement(var, domain))
                        else:
                            return Set(var, ForElement(var, domain), orig_cond)
                    from .algebraic import alg
                    roots = alg.polynomial_roots(poly)
                    roots = [r for (r, multiplicity) in roots]
                    roots_expr = []
                    for r in roots:
                        r = self.alg_to_expression(r)
                        if r is None:
                            return Zeros(*args)   # unable to express
                        r_cond = cond.replace({var:r})
                        r_cond = self.simple(r_cond)
                        if r_cond == True_:
                            roots_expr.append(r)
                        elif r_cond == False_:
                            pass
                        else:
                            return Zeros(*args)   # unable to decide?
                    return Set(*roots_expr)

        return Zeros(*args)

    def simple_Det(self, A):
        try:
            mat = self.evaluate_fmpq_mat(A)
            return Expr(mat.det())
        except (NotImplementedError, ZeroDivisionError):
            pass
        return Det(A)

    def simple_Spectrum(self, A):
        try:
            mat = self.evaluate_fmpq_mat(A)
            from .algebraic import alg
            eig = alg.matrix_eigenvalues(mat)
            eig = [r for (r, multiplicity) in eig]
            eig_expr = []
            for r in eig:
                r = self.alg_to_expression(r)
                if r is None:
                    return Spectrum(A)
                eig_expr.append(r)
            return Set(*eig_expr)
        except (NotImplementedError, ZeroDivisionError):
            pass
        return Spectrum(A)

    def simple_SingularValues(self, A):
        try:
            mat = self.evaluate_fmpq_mat(A)
            # todo: recognize symmetric matrices
            mat = mat * mat.transpose()
            from .algebraic import alg
            eig = alg.matrix_eigenvalues(mat)
            eig = [r.sqrt() for (r, multiplicity) in eig]
            eig_expr = []
            for r in eig:
                r = self.alg_to_expression(r)
                if r is None:
                    return SingularValues(A)
                eig_expr.append(r)
            return Set(*eig_expr)
        except (NotImplementedError, ZeroDivisionError):
            pass
        return SingularValues(A)

    def simple_Sum(self, *args):
        if len(args) == 2 or len(args) == 3:
            if len(args) == 2:
                expr, forargs = args
                cond = True_
            else:
                expr, forargs, cond = args
            if forargs.head() == For and len(forargs.args()) == 3:
                var, a, b = forargs.args()
                a = self.simple(a)
                b = self.simple(b)
                if a.is_integer() and b.is_integer():
                    a = int(a)
                    b = int(b)
                    if b - a < 100:
                        if cond == True_:
                            terms = [expr.replace({var:i}) for i in range(a,b+1)]
                        else:
                            terms = []
                            for i in range(a,b+1):
                                include = self.simple(cond.replace({var:i}))
                                if include == True_:
                                    terms.append(expr.replace({var:i}))
                                elif include == False_:
                                    continue
                                else:
                                    return Sum(*args)
                        return self.simple(Add(*terms))
        return Sum(*args)

    def simple_Where(self, *args):
        expr = args[0]
        defs = list(args[1:])

        # todo: semantic substitutions (stopping at new bound variables)
        def replace_func(expr, func, func_args, func_value):
            if expr.head() == func:
                args = expr.args()
                if len(args) != len(func_args):
                    raise ValueError("function called with wrong number of arguments")
                return func_value.replace(dict(zip(func_args, args)))
            if expr.is_atom():
                return expr
            head = replace_func(expr.head(), func, func_args, func_value)
            args = [replace_func(arg, func, func_args, func_value) for arg in expr.args()]
            return head(*args)

        try:

            for i in range(len(defs)):
                definition = defs[i]
                assert definition.head() in (Def, Equal)
                var, value = definition.args()
                value = self.simple(value)
                # normal assignment
                if var.is_symbol():
                    for j in range(i+1, len(defs)):
                        defs[j] = defs[j].replace({var:value})
                    expr = expr.replace({var:value})
                # destructuring assignment (todo: more cases)
                elif var.head() in (Tuple, List, Matrix2x2):
                    if value.head() in (Tuple, List, Matrix2x2):
                        xs = var.args()
                        xvals = value.args()
                        if len(xs) == len(xvals) and all(x.is_symbol() for x in xs):
                            replace_map = dict(zip(xs, xvals))
                            for j in range(i+1, len(defs)):
                                defs[j] = defs[j].replace(replace_map)
                            expr = expr.replace(replace_map)
                        else:
                            raise NotImplementedError
                # function assignment
                elif var.head() not in all_builtins:
                    func = var.head()
                    func_args = var.args()
                    func_value = value
                    for j in range(i+1, len(defs)):
                        defs[j] = replace_func(defs[j], func, func_args, func_value)
                    expr = replace_func(expr, func, func_args, func_value)

                else:
                    raise NotImplementedError

            expr = self.simple(expr)
            return expr

        except NotImplementedError:
            pass

        return Where(*args)

    def simple_RiemannZeta(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            s, = args
            if s.is_integer():
                fmpq = self._fmpq
                fmpz = self._fmpz
                n = int(s)
                if n == 1:
                    return UnsignedInfinity
                if n <= 0 and n >= -20:
                    return Expr((-1)**(-n) * fmpq.bernoulli(-n+1) / (-n+1))
                if n == 2:
                    return Pi**2 / 6
                if n >= 4 and n % 2 == 0 and n <= 20:
                    c = (-1)**(n//2+1) * fmpq.bernoulli(n) / (2 * fmpz.fac_ui(n)) * 2**n
                    return self.simple(Expr(c) * Pi**n)
            if s == Infinity:
                return Expr(1)
            if s.head() == RiemannZetaZero:
                n, = s.args()
                if self.is_integer(n) and self.is_not_zero(n):
                    return Expr(0)
        if len(args) == 2:
            s, r = args
            if r.is_integer() and int(r) >= 0:
                r = int(r)
                if r == 0:
                    return self.simple(RiemannZeta(s))
                if r == 1 and s == Expr(0):
                    return -(Log(2*Pi)/2)
                if s == Expr(1):
                    return UnsignedInfinity
                if s == Infinity:
                    return Expr(0)
        return RiemannZeta(*args)

    def simple_Cases(self, *args):
        # todo: push new assumptions when simplifying cases!
        unknown = []
        for arg in args:
            val, cond = arg.args()
            cond = self.simple(cond)
            if cond == True_:
                return self.simple(val)
            if cond == False_:
                continue
            unknown.append((val, cond))
        if len(unknown) == 1:
            if unknown[0][1] == Otherwise:
                return self.simple(unknown[0][0])
        return Cases(*unknown)

    def simple_AiryAi(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            if args[1] == Expr(0):
                args = [args[0]]
        if len(args) == 1:
            x, = args
            if x == Expr(0):
                return (Gamma(Div(1,3)) / (2*3**Div(1,6)*Pi))
            if x == Infinity:
                return Expr(0)
            if x == -Infinity:
                return Expr(0)
            if x.head() == AiryAiZero:
                if len(x.args()) == 1 and self.simple(Element(x.args()[0], ZZGreaterEqual(1))) == True_:
                    return Expr(0)
        if len(args) == 2:
            x, r = args
            if r.is_integer():
                n = int(r)
                if x == Expr(0):
                    if n % 3 == 2:
                        return Expr(0)
                    if n == 1:
                        return -(1/(3**Div(1,3) * Gamma(Div(1,3))))
                if self.is_complex(x):
                    if n == 2:
                        return (x * AiryAi(x)).simple()
                    if n == 3:
                        return (AiryAi(x) + x * AiryAi(x, 1)).simple()
                    if n == 4:
                        return (x**2 * AiryAi(x) + 2 * AiryAi(x, 1)).simple()
                    # todo: could implement higher derivatives
            if x.head() == AiryAiZero:
                if len(x.args()) == 2 and self.simple(Element(x.args()[0], ZZGreaterEqual(1))) == True_:
                    if self.equal(r, x.args()[1]) and self.simple(Element(r, ZZGreaterEqual(0))) == True_:
                        return Expr(0)
        return AiryAi(*args)

    def simple_AiryBi(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            if args[1] == Expr(0):
                args = [args[0]]
        if len(args) == 1:
            x, = args
            if x == Expr(0):
                return (3**Div(1,3) * Gamma(Div(1,3))) / (2*Pi)
            if x == Infinity:
                return Infinity
            if x == -Infinity:
                return Expr(0)
            if x.head() == AiryBiZero:
                if len(x.args()) == 1 and self.simple(Element(x.args()[0], ZZGreaterEqual(1))) == True_:
                    return Expr(0)
        if len(args) == 2:
            x, r = args
            if r.is_integer():
                n = int(r)
                if x == Expr(0):
                    if n % 3 == 2:
                        return Expr(0)
                    if n == 1:
                        return 3**Div(1,6) / Gamma(Div(1,3))
                if self.is_complex(x):
                    if n == 2:
                        return (x * AiryBi(x)).simple()
                    if n == 3:
                        return (AiryBi(x) + x * AiryBi(x, 1)).simple()
                    if n == 4:
                        return (x**2 * AiryBi(x) + 2 * AiryBi(x, 1)).simple()
                    # todo: could implement higher derivatives
            if x.head() == AiryBiZero:
                if len(x.args()) == 2 and self.simple(Element(x.args()[0], ZZGreaterEqual(1))) == True_:
                    if self.equal(r, x.args()[1]) and self.simple(Element(r, ZZGreaterEqual(0))) == True_:
                        return Expr(0)
        return AiryBi(*args)

    def simple_Erf(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            x, = args
            if x == Expr(0):
                return Expr(0)
            if x == Infinity:
                return Expr(1)
            if x == -Infinity:
                return Expr(-1)
            if self.is_negative(x):
                return -Erf(self.simple(-x))
            return Erf(x)
        return Erf(*args)

    def simple_Erfc(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            x, = args
            if x == Expr(0):
                return Expr(1)
            if x == Infinity:
                return Expr(0)
            if x == -Infinity:
                return Expr(2)
            return Erfc(x)
        return Erfc(*args)

    def simple_HurwitzZeta(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            s, a = args
            if self.is_complex(s) and self.is_complex(a):
                if s == Expr(1):
                    return UnsignedInfinity
                if s == Expr(0):
                    return self.simple(Div(1,2) - a)
                if self.simple(Element(s, ZZLessEqual(0))) == True_:
                    n = Neg(s)
                    return self.simple(-BernoulliPolynomial(n+1, a) / (n+1))
                if self.simple(Element(s, ZZGreaterEqual(2))) == True_ and self.simple(Element(a, ZZLessEqual(0))) == True_:
                    return UnsignedInfinity
                if a.is_integer():
                    n = int(a)
                    if n == 1:
                        return self.simple(RiemannZeta(s))
                    if n >= 2 and n <= 50:
                        return self.simple(RiemannZeta(s) - Add(*(1/k**s for k in range(1, n))))
                if self.is_rational(a):
                    bval = {(s,       Div(1,2)) : (2**s-1)*RiemannZeta(s),
                            (Expr(2), Div(1,4)) : Pi**2 + 8*ConstCatalan,
                            (Expr(2), Div(3,4)) : Pi**2 - 8*ConstCatalan,
                            (Expr(3), Div(1,4)) : 28*RiemannZeta(3) + Pi**3,
                            (Expr(3), Div(3,4)) : 28*RiemannZeta(3) - Pi**3,
                            (Expr(3), Div(1,6)) : 91*RiemannZeta(3) + 2*Sqrt(3)*Pi**3,
                            (Expr(3), Div(5,6)) : 28*RiemannZeta(3) - 2*Sqrt(3)*Pi**3}
                    for sval, aval in bval:
                        if s == sval:
                            v = self.simple(a - aval)
                            if v.is_integer():
                                n = int(v)
                                if n >= 0 and n <= 20:
                                    return self.simple(bval[(s, aval)] - Add(*(1/(k+aval)**s for k in range(n))))
                                if n >= -20 and n < 0:
                                    return self.simple(bval[(s, aval)] + Add(*(1/(k-(-n)+aval)**s for k in range(-n))))
        return HurwitzZeta(*args)

    def simple_DigammaFunction(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            if args[1] == Expr(0):
                args = [args[0]]
        if len(args) == 1:
            z, = args
            if z == Infinity:
                return Infinity
            if z.is_integer():
                n = int(z)
                if n <= 0:
                    return UnsignedInfinity
                if n == 1:
                    return -ConstGamma
                if n <= 100:
                    return self._fmpq.harmonic(n-1) - ConstGamma
            try:
                x = self.evaluate_fmpq(z)
                p = x.p
                q = x.q
                if q != 1 and q <= 12 and abs(x) <= 100:
                    n = p // q
                    p = p % q
                    assert 1 <= p < q
                    s = -ConstGamma - Log(2*q) - (Pi/2)*Cot(Pi*p/q)
                    s += 2 * sum(Cos(2*Pi*k*p/q)*Log(Sin(Pi*k/q)) for k in range(1, (q-1)//2+1))
                    if n > 0:
                        x = self._fmpq(p, q)
                        s += sum(1/(x+k) for k in range(n))
                    elif n < 0:
                        x = self._fmpq(p, q)
                        s -= sum(1/(x-k) for k in range(1, -n+1))
                    return self.simple(s)
            except NotImplementedError:
                pass
        if len(args) == 2:
            z, r = args
            if r.is_integer():
                if int(r) >= 1:
                    if z == Infinity:
                        return Expr(0)
                    if self.is_complex(z):
                        pole = self.simple(Element(z, ZZLessEqual(0)))
                        if pole == True_:
                            return UnsignedInfinity
                        if pole == False_:
                            return self.simple((-1)**(r+1) * Factorial(r) * HurwitzZeta(r + 1, z))
        return DigammaFunction(*args)

    def _gamma_fmpq(self, x):
        # https://arxiv.org/abs/math/0403510
        p = x.p
        q = x.q
        G = lambda a, b: Gamma(Div(a, b))
        n = p // q
        if abs(n) > 100:
            return G(p, q)
        p = p % q
        if n != 0:
            c = x - n
            r = 1
            if n > 0:
                for k in range(n):
                    r *= (c + k)
            else:
                for k in range(-n):
                    r /= (c + n + k)
            return self.simple(r * self._gamma_fmpq(c))
        if q not in [2,3,4,5,6,8,10,12,15,20,24,30,60]:
            return G(p, q)
        S = Sqrt
        A = 5 + S(5)
        B = 5 - S(5)
        C = S(5 + 2*S(5))
        D = S(5 - 2*S(5))
        def gamma(ppi, qpi, p2, q2, p3, q3, p5, q5, r, s):
            f = Pow(Pi, Div(ppi, qpi)) * Pow(2, Div(p2, q2)) * Pow(3, Div(p3, q3)) * Pow(5, Div(p5, q5))
            f = self.simple(f)
            return Mul(f, r, s)
        if q == 2:
            if p == 1:
                return Sqrt(Pi)
        if q == 3:
            if p == 2:
                return 2*Pi/(Sqrt(3) * G(1,3))
        if q == 4:
            if p == 3:
                return Sqrt(2) * Pi / G(1,4)
        if q == 5:
            if p == 3:
                return Pi * S(2) / S(5) * S(B) * G(2, 5)**-1
            if p == 4:
                return Pi * S(2) / S(5) * S(A) * G(1, 5)**-1
        if q == 6:
            if p == 1:
                return Gamma(Div(1,3))**2 * Sqrt(3) / (Sqrt(Pi) * Pow(2,Div(1,3)))
            if p == 5:
                return 2*Pow(Pi,Div(3,2)) * Pow(2,Div(1,3)) / (Sqrt(3) * Gamma(Div(1,3))**2)
        if q == 8:
            if p == 3:
                return Sqrt(Pi) * S(S(2)-1) * G(1,4)**-1 * G(1,8)
            if p == 5:
                return Sqrt(Pi) * 2**Div(3,4) * G(1,4) * G(1,8)**-1
            if p == 7:
                return Pi * 2**Div(3,4) * S(S(2)+1) * G(1,8)**-1
        if q == 10:
            if p == 1:
                return gamma(-1, 2, -7, 10, 0, 1, 0, 1, S(A), G(1,5) * G(2,5))
            if p == 3:
                return gamma(1, 2, -3, 5, 0, 1, -1, 2, B, G(1,5) * G(2,5)**-1)
            if p == 7:
                return Sqrt(Pi) * 2**Div(3,5) * G(1,5)**-1 * G(2,5)
            if p == 9:
                return gamma(3, 2, 7, 10, 0, 1, -1, 2, S(A), G(1,5)**-1 * G(2,5)**-1)
        if q == 12:
            if p == 1:
                return gamma(-1, 2, -1, 4, 3, 8, 0, 1, S(S(3)+1), G(1,3) * G(1,4))
            if p == 5:
                return gamma(1, 2, 1, 4, -1, 8, 0, 1, S(S(3)-1), G(1,4) * G(1,3)**-1)
            if p == 7:
                return gamma(1, 2, 1, 4, 1, 8, 0, 1, S(S(3)-1), G(1,3) * G(1,4)**-1)
            if p == 11:
                return gamma(3, 2, 3, 4, -3, 8, 0, 1, S(S(3)+1), G(1,3)**-1 * G(1,4)**-1)
        if q == 15:
            if p == 2:
                return gamma(0, 1, -1, 1, -7, 20, -1, 3, S(B) * S(S(15)-D), G(1,3)**-1 * G(2,5) * G(1,15))
            if p == 4:
                return gamma(0, 1, -3, 2, -3, 10, -1, 2, S(A) * S(S(15)-C) * S(S(15)-D), G(1,5)**-1 * G(2,5) * G(1,15))
            if p == 7:
                return gamma(0, 1, -1, 1, 9, 20, -1, 6, S(B) * S(S(15)+D), G(1,3) * G(1,5) * G(1,15)**-1)
            if p == 8:
                return gamma(1, 1, 1, 2, -9, 20, -1, 3, S(S(15)-C), G(1,3)**-1 * G(1,5)**-1 * G(1,15))
            if p == 11:
                return 2 * Pi * 3**Div(3,10) * G(1,5) * G(2,5)**-1 * G(1,15)**-1
            if p == 13:
                return gamma(1, 1, 1, 2, 7, 20, -1, 6, S(S(15)+C), G(1,3) * G(2,5)**-1 * G(1,15)**-1)
            if p == 14:
                return gamma(1, 1, -1, 2, 0, 1, -1, 2, S(A) * S(S(15)+C) * S(S(15)+D), G(1,15)**-1)
        if q == 20:
            if p == 3:
                return gamma(1, 2, -21, 20, 0, 1, -7, 8, B * S(S(10)-S(B)), G(2,5)**-1 * G(1,20))
            if p == 7:
                return gamma(1, 2, -3, 20, 0, 1, -3, 8, S(S(10)-S(A)), G(1,5)**-1 * G(1,20))
            if p == 9:
                return gamma(1, 1, -1, 5, 0, 1, -1, 2, S(S(10)-S(A)) * S(S(10)-S(B)), G(1,5)**-1 * G(2,5)**-1 * G(1,20))
            if p == 11:
                return 2**Div(1,5) * Sqrt(A) * G(1,5) * G(2,5) * G(1,20)**-1
            if p == 13:
                return gamma(1, 2, 3, 20, 0, 1, -1, 8, S(B) * S(S(10)+S(B)), G(1,5) * G(1,20)**-1)
            if p == 17:
                return gamma(1, 2, 1, 20, 0, 1, -1, 8, S(A) * S(S(10)+S(A)), G(2,5) * G(1,20)**-1)
            if p == 19:
                return gamma(1, 1, 0, 1, 0, 1, -1, 2, S(A) * S(S(10)+S(A)) * S(S(10)+S(B)), G(1,20)**-1)
        if q == 24:
            if p == 5:
                return gamma(1, 2, -1, 6, -1, 2, 0, 1, S(S(2)-1) * S(S(3)-1), G(1,3)**-1 * G(1,24))
            if p == 7:
                return gamma(1, 2, -1, 4, -3, 8, 0, 1, S(S(3)-1) * S(S(3)-S(2)), G(1,4)**-1 * G(1,24))
            if p == 11:
                return gamma(1, 1, 1, 12, -3, 8, 0, 1, S(S(2)-1) * S(S(3)-S(2)), G(1,3)**-1 * G(1,4)**-1 * G(1,24))
            if p == 13:
                return gamma(0, 1, 2, 3, 3, 8, 0, 1, S(S(3)+1), G(1,3) * G(1,4) * G(1,24)**-1)
            if p == 17:
                return gamma(1, 2, 1, 1, 3, 8, 0, 1, S(S(2)+1), G(1,4) * G(1,24)**-1)
            if p == 19:
                return gamma(1, 2, 11, 12, 1, 2, 0, 1, S(S(3)+S(2)), G(1,3) * G(1,24)**-1)
            if p == 23:
                return gamma(1, 1, 3, 4, 0, 1, 0, 1, S(S(2)+1) * S(S(3)+1) * S(S(3)+S(2)), G(1,24)**-1)
        if q == 30:
            if p == 1:
                return gamma(-1, 2, -16, 15, 9, 20, -1, 6, S(A) * S(S(15)+C), G(1,3) * G(1,5))
            if p == 7:
                return gamma(-1, 2, -22, 15, 3, 20, -1, 6, S(B) * S(S(15)+D), G(1,3) * G(2,5))
            if p == 11:
                return gamma(1, 2, -11, 15, -1, 20, -1, 3, S(A) * S(S(15)-C), G(1,3)**-1 * G(1,5))
            if p == 13:
                return gamma(1, 2, -41, 30, 7, 20, -2, 3, B * S(S(15)-D), G(1,3) * G(2,5)**-1)
            if p == 17:
                return gamma(1, 2, -2, 15, -7, 20, -1, 3, S(B) * S(S(15)-D), G(1,3)**-1 * G(2,5))
            if p == 19:
                return gamma(1, 2, -23, 30, 1, 20, -2, 3, A * S(S(15)-C), G(1,3) * G(1,5)**-1)
            if p == 23:
                return gamma(3, 2, -1, 30, -3, 20, -5, 6, B * S(S(15)+D), G(1,3)**-1 * G(2,5)**-1)
            if p == 29:
                return gamma(3, 2, -13, 30, -9, 20, -5, 6, A * S(S(15)+C), G(1,3)**-1 * G(1,5)**-1)
        if q == 60:
            if p == 11:
                return gamma(1, 2, -5,4, -1,2, -17,24,  S(A) * S(S(15) - C) * S(S(10) - S(A)), G(1,3)**-1 * G(1,60))
            if p == 13:
                return gamma(1, 2, -13, 10, -3, 20, -3, 8,  S(B) * S(S(3) + 1) * S(S(5) - S(3)) * S(S(15) - D), G(2,5)**-1 * G(7,60))
            if p == 17:
                return gamma(1, 2, -3, 4, -1, 2, -11, 24, S(B) * S(S(15) - D) * S(S(10) - S(B)), G(1,3)**-1 * G(7,60))
            if p == 19:
                return gamma(1, 2, -7, 5, -9, 20, -5, 8, S(A) * S(S(3) - 1) * S(S(5) - S(3)) * S(S(15) - C), G(1,5)**-1 * G(1,60))
            if p == 23:
                return gamma(1, 1, -11, 20, -3, 20, -7, 12, S(B) * S(S(3) + 1) * S(S(5) - S(3)) * S(S(10) - S(B)), G(1,3)**-1 * G(2,5)**-1 * G(7,60))
            if p == 29:
                return gamma(1, 1, -23, 20, -9, 20, -7, 12, S(A) * S(S(3) - 1) * S(S(5) - S(3)) * S(S(10) - S(A)), G(1,3)**-1 * G(1,5)**-1 * G(1,60))
            if p == 31:
                return gamma(0, 1, -1, 10, 9, 20, -1, 6, S(A) * S(S(15) + C), G(1,3) * G(1,5) * G(1,60)**-1)
            if p == 37:
                return gamma(0, 1, -7, 10, 3, 20, -1, 6, S(B) * S(S(15) + D), G(1,3) * G(2,5) * G(7,60)**-1)
            if p == 41:  # typo corrected
                return gamma(1, 2, 3, 20, 9, 20, -1, 8, S(A) * S(S(10) + S(A)), G(1,5) * G(1,60)**-1)
            if p == 43:
                return gamma(1, 2, -1, 2, 1, 2, -7, 24, S(B) * S(S(3)-1) * S(S(5) + S(3)), G(1,3) * G(7,60)**-1)
            if p == 47: # typo corrected
                return gamma(1, 2, 1, 20, 3, 20, -3, 8, S(B) * S(S(10) + S(B)), G(2,5) * G(7,60)**-1)
            if p == 49:
                return gamma(1, 2, 0, 1, 1, 2, -1, 24, S(A) * S(S(3) + 1) * S(S(5) + S(3)), G(1,3) * G(1,60)**-1)
            if p == 53:
                return gamma(1, 1, -5, 4, 0, 1, -3, 4, B * S(S(3) - 1) * S(S(5) + S(3)) * S(S(15) + D) * S(S(10) + S(B)), G(7,60)**-1)
            if p == 59:
                return gamma(1, 1, -5, 4, 0, 1, -3, 4, A * S(S(3) + 1) * S(S(5) + S(3)) * S(S(15) + C) * S(S(10) + S(A)), G(1,60)**-1)
        return G(p, q)

    def simple_Gamma(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            fmpz = self._fmpz
            z, = args
            if z.is_integer():
                n = int(z)
                if n <= 0:
                    return UnsignedInfinity
                if n <= 100:
                    return Expr(fmpz.fac_ui(n - 1))
            if z == Infinity:
                return Infinity
            if self.is_rational(z):
                m = self.simple(z * 60)
                if m.is_integer():
                    return self._gamma_fmpq(self.evaluate_fmpq(z))
                m = self.simple(z * 24)
                if m.is_integer():
                    return self._gamma_fmpq(self.evaluate_fmpq(z))

        return Gamma(*args)

    def simple_Factorial(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            fmpz = self._fmpz
            z, = args
            if z.is_integer():
                n = int(z)
                if n < 0:
                    return UnsignedInfinity
                if n <= 100:
                    return Expr(fmpz.fac_ui(n))
        return Factorial(*args)

    def simple_RisingFactorial(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 2:
            a, n = args
            if n.is_integer():
                n = int(n)
                if n <= 100 and a.is_integer():
                    v = self._fmpz(int(a)).rising(n)
                    return Expr(v)
                if n <= 30 and self.is_complex(a):
                    return self.simple(Mul(*(a+k for k in range(n))))

        return RisingFactorial(*args)


    def simple_hypergeometric(self, As, Bs, z, regularized=False):
        """
        Step 1 of hypergeometric evaluation; applies generic transformations
        and dispatches to step 2 if possible.
        """
        As = [self.simple(a) for a in As]
        Bs = [self.simple(b) for b in Bs]
        z = self.simple(z)
        all_complex = all(self.is_complex(a) for a in (As + Bs + [z]))
        prefactor = Expr(1)
        try:
            if all_complex:

                # We define F(..., 0) = 1 regardless of any parameter poles
                # Todo: is this a wise definition?
                at_zero = self.is_zero(z)
                if at_zero:
                    val = Expr(1)
                    if regularized:
                        for b in Bs:
                            # todo: unnecessary; div by UnsignedInfinity ought to be simplified
                            if b.is_integer() and int(b) <= 0:
                                return Expr(0)
                            val *= (1 / Gamma(b))
                    return self.simple(val)

                # Look for certain termination
                # Possible outcomes: None, parameter a_i = n
                terminating = None
                for a in As:
                    if a.is_integer():
                        an = int(a)
                        if an <= 0:
                            if terminating is None:
                                terminating = an
                            else:
                                terminating = max(terminating, an)

                # Possible issue: if there is some termination point a_j > a_i
                # with a corresponding pole b_k > a_i which could not be detected
                # with certainty, we are potentially adding too many
                # terms, incorrectly adding a pole. This must be avoided.
                if terminating is not None and not regularized:
                    if any(self.simple(Element(b, Range(terminating + 1, 0))) != False_ for b in Bs):
                        if any(self.simple(Element(a, Range(terminating + 1, 0))) != False_ for a in As):
                            terminating = None

                # Todo: fast code here (use recurrences when possible)
                if terminating is not None:
                    if terminating >= -30:
                        terms = []
                        for k in range(-terminating + 1):
                            P = [RisingFactorial(a, k) for a in As]
                            P += [z**k]
                            P += [1/Factorial(k)]
                            if regularized:
                                for b in Bs:
                                    # todo: unnecessary; div by UnsignedInfinity ought to be simplified
                                    if b.is_integer() and int(b) + k <= 0:
                                        P += [Expr(0)]
                                    else:
                                        P += [1/Gamma(b + k)]
                            else:
                                for b in Bs:
                                    P += [1/RisingFactorial(b, k)]
                            term = self.simple(Mul(*P))
                            terms.append(term)
                        return self.simple(Add(*terms))

                # Eliminate redundant parameters
                remove_Bi = set()
                for i in range(len(Bs)):
                    b = Bs[i]
                    if self.simple(Element(b, ZZLessEqual(0))) == False_:
                        for j in range(len(As)):
                            if self.equal(As[j], b):
                                del As[j]
                                remove_Bi.add(i)
                                break

                Bs_removed = [b for (i, b) in enumerate(Bs) if i in remove_Bi]
                Bs = [b for (i, b) in enumerate(Bs) if i not in remove_Bi]
                if Bs_removed and regularized:
                    prefactor = Mul(*(1/Gamma(b) for b in Bs_removed))

                # Now try step 2
                res = self.simple_hypergeometric_2(As, Bs, z, regularized)
                if res is not None:
                    if prefactor != Expr(1):
                        res = self.simple(prefactor * res)
                    return res

        except NotImplementedError:
            pass

        p = len(As)
        q = len(Bs)
        if q == 0:
            regularized = False

        # we define this regardless of whether z is complex
        if p == 0 and q == 0:
            res = self.simple(prefactor * Exp(z))

        if regularized:
            if p == 0 and q == 1:
                res = Hypergeometric0F1Regularized(Bs[0], z)
            elif p == 1 and q == 1:
                res = Hypergeometric1F1Regularized(As[0], Bs[0], z)
            elif p == 1 and q == 2:
                res = Hypergeometric1F2Regularized(As[0], Bs[0], Bs[1], z)
            elif p == 2 and q == 1:
                res = Hypergeometric2F1Regularized(As[0], As[1], Bs[0], z)
            elif p == 2 and q == 2:
                res = Hypergeometric2F2Regularized(As[0], As[1], Bs[0], Bs[1], z)
            elif p == 3 and q == 2:
                res = Hypergeometric3F2Regularized(As[0], As[1], As[2], Bs[0], Bs[1], z)
            else:
                res = HypergeometricPFQRegularized(As, Bs, z)
        else:
            if p == 0 and q == 1:
                res = Hypergeometric0F1(Bs[0], z)
            elif p == 1 and q == 1:
                res = Hypergeometric1F1(As[0], Bs[0], z)
            elif p == 1 and q == 2:
                res = Hypergeometric1F2(As[0], Bs[0], Bs[1], z)
            elif p == 2 and q == 0:
                res = Hypergeometric2F0(As[0], As[1], Bs[0], z)
            elif p == 2 and q == 1:
                res = Hypergeometric2F1(As[0], As[1], Bs[0], z)
            elif p == 2 and q == 2:
                res = Hypergeometric2F2(As[0], As[1], Bs[0], Bs[1], z)
            elif p == 3 and q == 2:
                res = Hypergeometric3F2(As[0], As[1], As[2], Bs[0], Bs[1], z)
            else:
                res = HypergeometricPFQ(As, Bs, z)
        if prefactor == Expr(1):
            return res
        else:
            return prefactor * res

    def simple_hypergeometric_2(self, As, Bs, z, regularized=False):
        """
        Step 2 of hypergeometric evaluation: attempt to find closed forms
        for special cases. Assumes step 1 has done preprocessing (verify
        that all parameters are complex; remove redundant parameters;
        handle finite cases). Returns None if no good closed form is found.
        """
        p = len(As)
        q = len(Bs)

        if p == 0 and q == 0:
            return self.simple(Exp(z))

        if p == 1 and q == 0:
            return self.simple((1-z)**(-As[0]))

        # print("CASE", As, Bs, regularized)

        # explicit evaluation of 0F1
        # todo: regularization
        # todo: do we want bessel functions?
        if p == 0 and q == 1:
            b = Bs[0]
            if b.is_integer():
                n = int(b)
                if n <= 0:
                    if not regularized and self.is_not_zero(z):
                        return UnsignedInfinity
                    if regularized:
                        return self.simple(z**(1-n) * Hypergeometric0F1Regularized(2-n, z))

            n = self.simple(2 * b)
            if n.is_integer():
                n = int(n)
                if n % 2 == 1 and abs(n) <= 7:
                    # todo: implement this in a much better way
                    fmpq = self._fmpq
                    def _0f1(b, z):
                        if b == fmpq(1,2):
                            return self.simple(Cosh(2 * Sqrt(z)))
                        if b == fmpq(-1,2):
                            return self.simple(Cosh(2 * Sqrt(z)) - 2 * Sqrt(z) * Sinh(2 * Sqrt(z)))
                        if b == fmpq(3,2):
                            return self.simple(Sinh(2 * Sqrt(z)) / (2 * Sqrt(z)))
                        if b > fmpq(3,2):
                            return (b-2)*(b-1)/z * (_0f1(b-2,z) - _0f1(b-1,z))
                        if b < fmpq(-1,2):
                            return _0f1(b+1,z) + z/(b*(b+1)) * _0f1(b+2,z)
                    val = _0f1(fmpq(n, 2), z)
                    if n >= 3:
                        # division by zero in the formulas
                        val = Cases((val, NotEqual(z, 0)), Tuple(1, Equal(z, 0)))
                        val = self.simple(val)  # todo. div not simplifying enough
                    if regularized:
                        return self.simple(val / Gamma(b))
                    else:
                        return self.simple(val)

        # Gauss 2F1
        if p == 2 and q == 1:
            if z == Expr(1):
                a, b, c = As[0], As[1], Bs[0]
                if self.is_complex(a) and self.is_complex(b) and self.is_complex(c) and self.simple(NotElement(c, ZZLessEqual(0))) == True_:
                    v = Greater(Re(c-a-b), 0)
                    v = self.simple(v)
                    if v == True_:
                        if regularized:
                            return self.simple(Gamma(c-a-b) / (Gamma(c-a) * Gamma(c - b)))
                        else:
                            return self.simple(Gamma(c) * Gamma(c-a-b) / (Gamma(c-a) * Gamma(c-b)))

        return None

    def simple_Hypergeometric0F1(self, *args):
        try:
            b, z = args
        except ValueError:
            return Hypergeometric0F1(*args)
        return self.simple_hypergeometric([], [b], z)

    def simple_Hypergeometric0F1Regularized(self, *args):
        try:
            b, z = args
        except ValueError:
            return Hypergeometric0F1Regularized(*args)
        return self.simple_hypergeometric([], [b], z, regularized=True)

    def simple_Hypergeometric1F1(self, *args):
        try:
            a, b, z = args
        except ValueError:
            return Hypergeometric1F1(*args)
        return self.simple_hypergeometric([a], [b], z)

    def simple_Hypergeometric1F1Regularized(self, *args):
        try:
            a, b, z = args
        except ValueError:
            return Hypergeometric1F1Regularized(*args)
        return self.simple_hypergeometric([a], [b], z, regularized=True)

    def simple_Hypergeometric2F1(self, *args):
        try:
            a, b, c, z = args
        except ValueError:
            return Hypergeometric2F1(*args)
        return self.simple_hypergeometric([a, b], [c], z)

    def simple_Hypergeometric2F1Regularized(self, *args):
        try:
            a, b, c, z = args
        except ValueError:
            return Hypergeometric2F1Regularized(*args)
        return self.simple_hypergeometric([a, b], [c], z, regularized=True)

    def simple_HypergeometricPFQ(self, *args):
        try:
            a, b, z = args
            # todo: check iterators
            if a.head() in (List, Tuple) and b.head() in (List, Tuple):
                return self.simple_hypergeometric(a.args(), b.args(), z)
        except ValueError:
            pass
        return HypergeometricPFQ(*args)

    def simple_HypergeometricPFQRegularized(self, *args):
        try:
            a, b, z = args
            # todo: check iterators
            if a.head() in (List, Tuple) and b.head() in (List, Tuple):
                return self.simple_hypergeometric(a.args(), b.args(), z, regularized=True)
        except ValueError:
            pass
        return HypergeometricPFQRegularized(*args)


    def simple_ModularJ(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            tau, = args
            try:
                v = self.evaluate_alg(tau)
                v, transform = v.reduce_sl2z(v)
            except ValueError:
                v = None
            if v is not None and v.degree() == 2:
                a, b, c = v.as_quadratic()
                h = self._fmpq(1,2)
                # Produce exact values.
                # https://en.wikipedia.org/wiki/J-invariant#Special_values
                # Todo: implement an algorithm!
                modjtab = {
                    (-h, h, -3) : Expr(0),
                    (0, 1, -1) : Expr(1728),
                    (0, 2, -1) : Expr(66**3),
                    (0, 3, -1) : 64*(2+Sqrt(3))**2*(21+20*Sqrt(3))**3,
                    (0, 4, -1) : 27*(724+513*Sqrt(2))**3,
                    (0, 1, -2) : Expr(20**3),
                    (0, 2, -2) : 1000*(19+13*Sqrt(2))**3,
                    (0, 2, -3) : 13500*(30+17*Sqrt(3))**3,
                    (-h, 1, -1) : 27*(724-513*Sqrt(2))**3,
                    (0, 1, -6) : 432 * (14 + 9*Sqrt(2))**3 * (2 - Sqrt(2)),
                    (-h, h, -7) : Expr(-15**3),
                    (-h, h, -11) : Expr(-32**3),
                    (-h, h, -19) : Expr(-96**3),
                    (-h, h, -43) : Expr(-960**3),
                    (-h, h, -67) : Expr(-5280**3),
                    (-h, h, -163) : Expr(-640320**3),
                }
                val = modjtab.get((a, b, c))
                if val is not None:
                    return val
        return ModularJ(*args)

    def simple_DedekindEtaEpsilon(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 4:
            a, b, c, d = args
            if a.is_integer() and b.is_integer() and c.is_integer() and d.is_integer():
                fmpz = self._fmpz
                def epsilon_arg(a, b, c, d):
                    if a*d - b*c != 1:
                        raise ValueError
                    if c < 0 or (c == 0 and d < 0):
                        a, b, c, d = -a, -b, -c, -d
                    if c == 0:
                        return b % 24
                    aa = a % 24
                    bb = b % 24
                    cc = c % 24
                    dd = d % 24
                    def kronecker(a, b):
                        if b < 0:
                            return kronecker(a, -b)
                        if b == 1:
                            return fmpz(1)
                        return fmpz(a).jacobi(b)
                    if cc % 2 == 1:
                        u = kronecker(a, c)
                        aa = aa*bb + 2*aa*cc - 3*cc + cc*dd*(1-aa*aa)
                    else:
                        u = kronecker(c, a)
                        aa = aa*bb - aa*cc + 3*aa - 3 + cc*dd*(1-aa*aa)
                    assert u in (-1, 1)
                    if u == -1:
                        aa += 12
                    aa = aa % 24
                    return aa
                try:
                    r = epsilon_arg(int(a), int(b), int(c), int(d))
                except ValueError:
                    return Undefined
                r = self.simple_Exp_two_pi_i_k_n(r, 24)
                return r

        return DedekindEtaEpsilon(*args)

    def simple_ModularLambda(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            tau, = args
            try:
                v = self.evaluate_alg(tau)
                v, transform = v.reduce_sl2z(v)
            except ValueError:
                v = None
            if v is not None and v.degree() == 2:
                a, b, c = v.as_quadratic()
                h = self._fmpq(1,2)
                # http://mathworld.wolfram.com/EllipticLambdaFunction.html
                # Todo: fill in more values
                modlamtab = {
                    (0, 1, -1) : Expr(1)/2,
                    (-h, h, -3) : -self.simple_Exp_two_pi_i_k_n(1, 3),
                    (0, 2, -1) : 17 - 12*Sqrt(2),
                    (0, 1, -2) : (Sqrt(2) - 1)**2,
                    (0, 1, -3) : ((Sqrt(3)-1)**2/8),
                    (0, 1, -5) : (Div(1,2)-Sqrt(Sqrt(5)-2)),
                    (0, 1, -6) : (2-Sqrt(3))**2*(Sqrt(3)-Sqrt(2))**2,
                    (0, 1, -7) : ((3-Sqrt(7))**2/32),
                    (0, 2, -2) : ((1+Sqrt(2)-Sqrt(2*Sqrt(2)+2))**4),
                    (0, 3, -1) : ((Sqrt(2)-3**Div(1,4))**2*(Sqrt(3)-1)**2/4),
                    (0, 1, -10) : ((Sqrt(10)-3)**2*(Sqrt(2)-1)**4),
                    (0, 2, -3) : (Sqrt(3)-Sqrt(2))**4 * (Sqrt(2)-1)**4,
                    (0, h, -6) : 1 - (2-Sqrt(3))**2*(Sqrt(2)+Sqrt(3))**2,
                    (0, h, -10) : 1 - (1+Sqrt(2))**4*(Sqrt(10)-3)**2,
                }
                val = modlamtab.get((a, b, c))
                if val is not None:
                    transform = [n%2 for n in transform]
                    if transform == [1, 0, 0, 1]: val = val
                    if transform == [0, 1, 1, 0]: val = 1-val
                    if transform == [1, 0, 1, 1]: val = 1/val
                    if transform == [0, 1, 1, 1]: val = 1/(1-val)
                    if transform == [1, 1, 1, 0]: val = 1-1/val
                    if transform == [1, 1, 0, 1]: val = val/(val-1)
                    return self.simple(val)

        return ModularLambda(*args)

    def simple_DedekindEta(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            tau, = args
            try:
                v = self.evaluate_alg(tau)
                v, transform = v.reduce_sl2z(v)
            except ValueError:
                v = None
            if v is not None and v.degree() == 2:
                a, b, c = v.as_quadratic()
                h = self._fmpq(1,2)
                if a == -h:
                    t = b * Sqrt(c)
                    val = Exp(-Pi*ConstI/24) * DedekindEta(2*t)**3 / (DedekindEta(t) * DedekindEta(4*t))
                    val = self.simple(val)
                else:
                    etai = Gamma(Div(1,4)) / (2 * Pi**Div(3,4))
                    modetatab = {
                        (0, 1, -1) : etai,
                        (0, 2, -1) : etai / 2**Div(3,8),
                        (0, 3, -1) : etai / (3**Div(3,8) * (2+Sqrt(3))**Div(1,12)),
                        (0, 4, -1) : etai / (2**Div(13,16) * (1+Sqrt(2))**Div(1,4)),
                        (0, 5, -1) : etai / Sqrt(5*GoldenRatio),
                        (0, 6, -1) : (1/6**Div(3,8)) * ((5-Sqrt(3))/2 - 3**Div(3,4)/Sqrt(2))**Div(1,6) * etai,
                        (0, 7, -1) : (1/Sqrt(7)) * (-Div(7,2) + Sqrt(7) + Div(1,2)*Sqrt(-7+4*Sqrt(7)))**Div(1,4) * etai,
                        (0, 8, -1) : (1/2**Div(41,32)) * Sqrt(2**Div(1,4) - 1) / (1+Sqrt(2))**Div(1,8) * etai,
                        (0, 16, -1) : (1/2**Div(113,64)) * (2**Div(1,4)-1)**Div(1,4) / (1+Sqrt(2))**Div(1,16) * Sqrt(-2**Div(5,8) + Sqrt(1+Sqrt(2))) * etai,
                        (0, 1, -3) : 3**Div(1,8) / 2**Div(4,3) * Gamma(Div(1,3))**Div(3,2) / Pi,
                        (-h, h, -3) : Exp(-Pi*ConstI/24) * 3**Div(1,8) * Gamma(Div(1,3))**Div(3,2) / (2*Pi),
                    }
                    val = modetatab.get((a, b, c))
                if val is not None:
                    a, b, c, d = transform
                    tau = v.expr()
                    val = DedekindEtaEpsilon(a, b, c, d) * Sqrt(c*tau + d) * val
                    return self.simple(val)

        return DedekindEta(*args)

    def simple_EllipticK(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            z, = args
            if z == Expr(0):
                return Pi / 2
            if z == Expr(1):
                return Infinity
            if z == Expr(-1):
                return Gamma(Div(1,4))**2 / (4*Sqrt(2*Pi))
            if z == Expr(2):
                return Gamma(Div(1,4))**2 / (4*Sqrt(2*Pi)) * (1-ConstI)
            if self.equal(z, Div(1, 2)):
                return Gamma(Div(1,4))**2 / (4*Sqrt(Pi))
            # todo: implement evaluation at more singular values
            if self.equal(z, 17-12*Sqrt(2)):
                return (2+Sqrt(2))*Gamma(Div(1,4))**2 / (16*Sqrt(Pi))
            if self.equal(z, (4-3*Sqrt(2))/8):
                return Gamma(Div(1,4))**2 / (4*2**Div(1,4) * Sqrt(Pi))
        return EllipticK(*args)

    def simple_EllipticE(self, *args):
        args = [self.simple(arg) for arg in args]
        if len(args) == 1:
            z, = args
            if z == Expr(0):
                return Pi / 2
            if z == Expr(1):
                return Expr(1)
            if z == Expr(-1):
                return Sqrt(2) * (Gamma(Div(1,4))**2 / (8*Sqrt(Pi)) + Pi**Div(3,2) / Gamma(Div(1,4))**2)
            if z == Expr(2):
                return (Sqrt(2)*Pi**Div(3,2)/Gamma(Div(1,4))**2 * (1+ConstI))
            if self.equal(z, Div(1, 2)):
                return (Gamma(Div(1,4))**2 / (8*Sqrt(Pi)) + Pi**Div(3,2) / Gamma(Div(1,4))**2)
            # todo: implement evaluation at singular values
        return EllipticE(*args)





    def some_values(self, variables, assumptions, num=10, as_dict=False, max_candidates=100000):
        """
        Attempt to generate values satisfying given assumptions (constraints).

        This is meant to be used to generate test parameters, not to solve
        equations. The method may fail to generate any suitable test values;
        this does not imply that no solutions exist.

        Input:

        variables - Python list of symbols representing variables
        assumptions - single expression giving conditions (can be And(...))
        num - maximal number of instances to generate
        as_dict - yield dict of variable assignments, not just the values

        Examples:

            >>> b = Brain()
            >>> for v in b.some_values([x, y], And(Element(x, ZZ), Element(y, QQ)), as_dict=True):
            ...     print(v)
            ... 
            {x: 0, y: 0}
            {x: 0, y: Div(1, 2)}
            {x: 1, y: 0}
            {x: 0, y: 1}
            {x: 1, y: Div(1, 2)}
            {x: -1, y: 0}
            {x: 0, y: Neg(Div(1, 2))}
            {x: 1, y: 1}
            {x: -1, y: Div(1, 2)}
            {x: 2, y: 0}

        """
        # preprocess assumptions: decouple And; factor by variables
        assert isinstance(assumptions, Expr)
        variables = list(variables)
        assumptions = list(assumptions.head_args_flattened(And))
        assumptions_by_var = {}
        for var in variables:
            for a in assumptions:
                if var in a.subexpressions():
                    assumptions_by_var[var] = assumptions_by_var.get(var, [])
                    assumptions_by_var[var].append(a)
        base_sets = {var:some_everything for var in variables}
        for var in variables:
            if var in assumptions_by_var:
                for a in assumptions_by_var[var]:
                    if a.head() == Element and a.args()[0] == var:
                        S = a.args()[1]
                        if S == PP:
                            base_sets[var] = some_primes
                        elif S == ZZ:
                            base_sets[var] = some_integers
                        elif S == QQ:
                            base_sets[var] = some_rationals
                        elif S == RR:
                            base_sets[var] = some_reals
                        elif S == CC:
                            base_sets[var] = some_complexes
                        elif S == HH:
                            base_sets[var] = some_upper_half_plane
                        elif S == AlgebraicNumbers:
                            base_sets[var] = some_algebraics
                        elif S.head() in (ZZLessEqual, ZZGreaterEqual, Range):
                            base_sets[var] = some_integers
                        elif S.head() in (ClosedInterval, OpenInterval, OpenClosedInterval, ClosedOpenInterval):
                            base_sets[var] = some_extended_reals
        base_sets = [base_sets[var] for var in variables]
        found = 0
        count = 0
        for values in custom_cartesian(*base_sets):
            assignment = {var:val for (var,val) in zip(variables, values)}
            # todo: when the assumptions for the variables are pure domain statements with simple domains, we could skip the checks
            ok = all(self.simple(a.replace(assignment)) == True_ for a in assumptions)
            if count > max_candidates:
                break
            count += 1
            if ok:
                if found == num:
                    break
                found += 1
                if as_dict:
                    yield assignment
                else:
                    yield values

    def match(self, expr, rule, free_variables=[], assumptions=None):
        if assumptions is None:
            assumptions = True_

        match_values = {}

        def match_recursive(expr, rule):
            if rule in free_variables:
                if rule in match_values:
                    if expr != match_values[rule]:
                        raise ValueError
                else:
                    match_values[rule] = expr
                return
            if expr == rule:
                return
            expr_head = expr.head()
            rule_head = rule.head()
            expr_args = expr.args()
            rule_args = rule.args()
            if expr_head != rule_head or expr_head is None or len(expr_args) != len(rule_args):
                raise ValueError
            for a, b in zip(expr_args, rule_args):
                match_recursive(a, b)

        try:
            match_recursive(expr, rule)
        except ValueError:
            return None

        #print("MATCH", rule, match_values)

        # todo: some_values search for matching assumptions if missing variables?

        assumptions = assumptions.replace(match_values)
        assumptions = self.simple(assumptions)

        #print("ASSUMPTIONS", assumptions)

        if assumptions == True_:
            return match_values
        else:
            return None

    def rewrite_fungrim(self, expr, id, recursive=True):
        from .formulas import entries_dict
        entry = entries_dict[id]
        variables = entry.get_arg_with_head(Variables)
        if variables is None:
            variables = []
        else:
            variables = variables.args()
        formula = entry.get_arg_with_head(Formula)
        if formula is None:
            raise ValueError("unsupported kind of entry for rewriting")
        formula = formula.args()[0]
        assumptions = entry.get_arg_with_head(Assumptions)
        if assumptions is None:
            assumptions = True_
        else:
            assumptions = assumptions.args()[0]
        if formula is None or formula.head() != Equal or len(formula.args()) != 2:
            raise ValueError("unsupported kind of entry for rewriting")
        lhs, rhs = formula.args()

        def match_local(expr):
            match = self.match(expr, lhs, variables, assumptions)
            if match is not None:
                return rhs.replace(match)
            if expr.is_atom():
                return expr
            head = expr.head()
            args = expr.args()
            return head(*(match_local(arg) for arg in args))

        if recursive:
            return match_local(expr)
        else:    
            match = self.match(expr, lhs, variables, assumptions)
            if match is not None:
                return rhs.replace(match)
            return expr



class FungrimBrain(Brain):

    def __init__(self, *args, **kwargs):
        Brain.__init__(self, *args, **kwargs)

        # Init Fungrim patterns
        self.expr_db = {}
        self.match_db = {}

        from . import formulas
        from .expr import all_entries
        for entry in all_entries:
            formula = entry.get_arg_with_head(Formula)
            if formula is None:
                continue

            variables = entry.get_arg_with_head(Variables)

            # Constant expression
            if variables is None:
                content = formula.args()[0]
                self.infer(content)
                # self.expr_db[content] = True_
                if content.head() == Equal:
                    args = content.args()
                    best = args[0]
                    cost = self.complexity(best)
                    for arg in args[1:]:
                        cost2 = self.complexity(arg)
                        if cost2 < cost:
                            best = arg
                            cost = cost2
                    for arg in args:
                        if arg != best:
                            self.expr_db[arg] = best
            # Nonconstant expression for matching
            else:
                content = formula.args()[0]
                if content.head() == Equal and len(content.args()) == 2:
                    eid = entry.id()
                    lhs_head = content.args()[0].head()
                    if lhs_head in self.match_db:
                        self.match_db[lhs_head].add(eid)
                    else:
                        self.match_db[lhs_head] = set([eid])

    def simple(self, expr):
        """
        Given a symbolic expression expr, return an equivalent expression,
        hopefully simplified.
        """
        if expr in self.inferences:
            return True_

        if expr.is_atom():
            return expr

        if expr in self.simple_cache:
            v = self.simple_cache[expr]
            if v is None:
                return expr
            return v

        input_expr = expr
        self.simple_cache[input_expr] = None


        def fungrim_simplify(expr):
            if expr in self.expr_db:
                return self.expr_db[expr]
            if expr.is_atom():
                return expr

            head = expr.head()
            expr = head(*(self.simple(arg) for arg in expr.args()))
            if head in self.match_db:
                exprs = set((self.rewrite_fungrim(expr, id, recursive=False), id) for id in self.match_db[head])
                #for e in exprs:
                #    print(e, self.complexity(e[0]))
                expr2, id = min(exprs, key=lambda v: self.complexity(v[0]))
                if expr2 != expr and self.complexity(expr2) < self.complexity(expr):
                    expr = self.simple(expr2)
            return expr

        if self.expr_db:
            expr = fungrim_simplify(expr)

        head = expr.head()
        if head is not None and head.is_symbol():
            s = head._symbol
            f = "simple_" + s
            if hasattr(self, f):
                args = expr.args()
                expr2 = getattr(self, f)(*args)
                if self.expr_db and expr2 != expr:
                    expr2 = fungrim_simplify(expr2)
                expr = expr2

        self.simple_cache[input_expr] = expr

        return expr


class TestBrain(object):

    def __init__(self):
        pass

    def run(self):
        for method in dir(self):
            if method.startswith("test_"):
                print(method, "...", end=" ")
                getattr(self, method)()
                print("OK!")

    def test_init(self):
        b = Brain([x,y], And(Element(x, CC), Element(y, SetMinus(QQ, ZZ))))

    def test_domain_inference(self):
        b = Brain([x], Element(x, ZZ))
        assert b.simple(Element(x, ZZ)) == True_
        assert b.simple(Element(x, QQ)) == True_
        assert b.simple(Element(x, RR)) == True_
        assert b.simple(Element(x, CC)) == True_
        assert b.simple(Element(x, AlgebraicNumbers)) == True_
        assert b.simple(Element(x, PP)) == Element(x, PP)

        b = Brain([x], Element(x, QQ))
        assert b.simple(Element(x, QQ)) == True_
        assert b.simple(Element(x, RR)) == True_
        assert b.simple(Element(x, CC)) == True_
        assert b.simple(Element(x, AlgebraicNumbers)) == True_
        assert b.simple(Element(x, ZZ)) == Element(x, ZZ)
        assert b.simple(Element(x, PP)) == Element(x, PP)

        b = Brain([x], Element(x, RR))
        assert b.simple(Element(x, RR)) == True_
        assert b.simple(Element(x, CC)) == True_
        assert b.simple(Element(x, AlgebraicNumbers)) == Element(x, AlgebraicNumbers)
        assert b.simple(Element(x, QQ)) == Element(x, QQ)
        assert b.simple(Element(x, ZZ)) == Element(x, ZZ)
        assert b.simple(Element(x, PP)) == Element(x, PP)

        b = Brain([x], Element(x, AlgebraicNumbers))
        assert b.simple(Element(x, CC)) == True_
        assert b.simple(Element(x, AlgebraicNumbers)) == True_
        assert b.simple(Element(x, QQ)) == Element(x, QQ)
        assert b.simple(Element(x, RR)) == Element(x, RR)
        assert b.simple(Element(x, ZZ)) == Element(x, ZZ)
        assert b.simple(Element(x, PP)) == Element(x, PP)

        b = Brain([x], Element(x, PP))
        assert b.simple(Element(x, PP)) == True_
        assert b.simple(Element(x, ZZ)) == True_
        assert b.simple(Element(x, QQ)) == True_
        assert b.simple(Element(x, RR)) == True_
        assert b.simple(Element(x, CC)) == True_
        assert b.simple(Element(x, AlgebraicNumbers)) == True_

        b = Brain([x], Element(x, SetMinus(RR, QQ)))
        assert b.simple(Element(x, CC)) == True_
        assert b.simple(Element(x, RR)) == True_
        assert b.simple(Element(x, QQ)) == False_
        assert b.simple(NotElement(x, QQ)) == True_

    def test_simple(self):
        b = Brain()
        assert b.simple(Element(Add(3, 5), ZZ)) == True_
        assert b.simple(And(Not(False_), Or(True_, False_))) == True_

    def test_is_positive(self):
        b = Brain()
        assert b.is_positive(Expr(3)) is True
        assert b.is_positive(Pi) is True
        assert b.is_positive(1 + Sqrt(2)) is True
        assert b.is_positive(Expr(-3)) is False
        assert b.is_positive(Pi - 3) is True
        assert b.is_positive(Pi - 4) is False

    def test_is_algebraic(self):
        b = Brain()
        assert b.is_algebraic(ConstI) is True
        assert b.is_algebraic(Sqrt(2)) is True
        assert b.is_algebraic(Sqrt(2)+1) is True
        assert b.is_algebraic(Pi) is False
        assert b.is_algebraic(Exp(2)) is False
        assert b.is_algebraic(Log(2)) is False
        assert b.is_algebraic(Sin(2)) is False
        assert b.is_algebraic(Sin(Sqrt(Pi))) is None
        assert b.is_algebraic(2**Sqrt(2)) is False
        assert b.is_algebraic(Exp(3*ConstI*Pi/7)) is True
        b = Brain([q], And(Element(q, QQ), NotEqual(q, 0)))
        assert b.is_algebraic(Exp(q)) is False
        assert b.is_algebraic(Sin(q)) is False
        assert b.is_algebraic(Log(q)) is None
        assert b.is_algebraic(Pi + ConstE) is None

    def test_element(self):
        b = Brain()
        assert b.element(Expr(3), ZZ) is True
        assert b.element(Expr(3) * Expr(-4) + Pow(5, 2) - Expr(1), ZZ) is True
        assert b.element(Factorial(10**20), ZZ) is True
        assert b.element(Pi, ZZ) is False
        assert b.element(Pi, Set(Pi)) is True
        assert b.element(Pi, Union(ZZ, Set(Pi))) is True
        assert b.element(Pi, SetMinus(RR, QQ)) is True
        assert b.element(Div(3, 2), ZZ) in (False, None)  # todo: implement calculation

        points = [-Infinity, Expr(-3), Expr(0), Expr(3), Infinity, ConstI]
        np = range(len(points))
        bad = points.index(ConstI)
        for ia in np:
            for ib in np:
                # todo: order comparisons with complex numbers -> False consistently?
                v = b.less(points[ia], points[ib])
                if bad in (ia, ib):
                    assert v in (False, None)
                else:
                    assert v == (ia < ib)

                v = b.less_equal(points[ia], points[ib])
                if bad in (ia, ib):
                    assert v in (False, None)
                else:
                    assert v == (ia <= ib)

                v = b.greater(points[ia], points[ib])
                if bad in (ia, ib):
                    assert v in (False, None)
                else:
                    assert v == (ia > ib)

                v = b.greater_equal(points[ia], points[ib])
                if bad in (ia, ib):
                    assert v in (False, None)
                else:
                    assert v == (ia >= ib)

                for ix in np:
                    v = b.element(points[ix], ClosedInterval(points[ia], points[ib]))
                    if bad in (ia, ib):
                        assert v is None
                    elif ix == bad:
                        assert v is False
                    else:
                        assert v == (ia <= ix and ix <= ib)

                    v = b.element(points[ix], OpenInterval(points[ia], points[ib]))
                    if bad in (ia, ib):
                        assert v is None
                    elif ix == bad:
                        assert v is False
                    else:
                        assert v == (ia < ix and ix < ib)

                    v = b.element(points[ix], OpenClosedInterval(points[ia], points[ib]))
                    if bad in (ia, ib):
                        assert v is None
                    elif ix == bad:
                        assert v is False
                    else:
                        assert v == (ia < ix and ix <= ib)

                    v = b.element(points[ix], ClosedOpenInterval(points[ia], points[ib]))
                    if bad in (ia, ib):
                        assert v is None
                    elif ix == bad:
                        assert v is False
                    else:
                        assert v == (ia <= ix and ix < ib)

        assert b.element(Expr(3), ZZGreaterEqual(2)) is True
        assert b.element(Expr(3), ZZGreaterEqual(3)) is True
        assert b.element(Expr(3), ZZGreaterEqual(4)) is False
        assert b.element(Pi, ZZGreaterEqual(4)) is False

        assert b.element(Expr(3), ZZLessEqual(2)) is False
        assert b.element(Expr(3), ZZLessEqual(3)) is True
        assert b.element(Expr(3), ZZLessEqual(4)) is True
        assert b.element(Pi, ZZLessEqual(4)) is False

        assert b.element(Expr(2), Range(2, 5)) is True
        assert b.element(Expr(3), Range(2, 5)) is True
        assert b.element(Expr(5), Range(2, 5)) is True
        assert b.element(Expr(1), Range(2, 5)) is False
        assert b.element(Expr(6), Range(2, 5)) is False
        assert b.element(Pi, Range(2, 5)) is False
        assert b.element(Expr(2), Range(2, 1)) is False

        b = Brain([z], Element(z, CC))
        assert b.element(Log(z), CC) is None
        b = Brain([z], And(Element(z, CC), NotEqual(z, 0)))
        assert b.element(Log(z), CC) is True

    def test_equal(self):
        b = Brain()
        assert b.equal(Pi, Pi) is True
        assert b.equal(x, x) is True
        assert b.equal(1+x, 1+x) is True
        assert b.equal(1+x, x+1) is None
        assert b.equal(Pi, Expr(2)) is False
        assert b.equal(Expr(3), Expr(3)) is True
        assert b.equal(Expr(3), Expr(-3)) is False
        assert b.equal(Expr(3), Pi) is False
        assert b.equal(Expr(3), ConstI) is False

    def test_Sqrt(self):
        b = Brain()
        assert b.simple(Sqrt(0)) == Expr(0)
        assert b.simple(Sqrt(1)) == Expr(1)
        assert b.simple(Sqrt(2)) == Sqrt(2)
        assert b.simple(Sqrt(4)) == Expr(2)
        assert b.simple(Sqrt(-1)) == ConstI
        assert b.simple(Sqrt(-4)) == 2*ConstI
        assert b.simple(Sqrt(Infinity)) == Infinity
        assert b.simple(Sqrt(UnsignedInfinity)) == UnsignedInfinity
        assert b.simple(Sqrt(Undefined)) == Undefined
        assert b.simple(Sqrt(Pi**2)) == Pi
        assert b.simple(Sqrt(Pi**3)) == Sqrt(Pi**3)
        assert b.simple(Sqrt(Pi**4)) == Pi**2
        b = Brain([x], Element(x, ClosedOpenInterval(0, Infinity)))
        assert b.simple(Sqrt(x**2)) == x
        assert b.simple(Sqrt(x**4)) == x**2
        b = Brain([x], Element(x, RR))
        assert b.simple(Sqrt(x**2)) == Sqrt(x**2)
        # todo: check element (...)

    def test_Abs(self):
        b = Brain()
        assert b.simple(Abs(0)) == Expr(0)
        assert b.simple(Abs(1)) == Expr(1)
        assert b.simple(Abs(2)) == Expr(2)
        assert b.simple(Abs(-2)) == Expr(2)
        assert b.simple(Abs(-Pi)) == Pi
        assert b.simple(Abs(Infinity)) == Infinity
        assert b.simple(Abs(-Infinity)) == Infinity
        assert b.simple(Abs(UnsignedInfinity)) == Infinity
        assert b.simple(Abs(ConstI*UnsignedInfinity)) == Infinity
        assert b.simple(Abs(2*ConstI)) == b.simple(-ConstI*(2*ConstI))   # XXX
        assert b.simple(Abs(-2*ConstI)) == b.simple(ConstI*(-2*ConstI))   # XXX
        assert b.simple(Abs(Exp(ConstI*Pi/7))) == Expr(1)
        b = Brain([x], Element(x, OpenInterval(0, Infinity)))
        assert b.simple(Abs(x)) == x
        b = Brain([x], Element(x, OpenClosedInterval(0, Infinity)))
        assert b.simple(Abs(x)) == x
        b = Brain([x], Element(x, OpenInterval(-Infinity, 0)))
        assert b.simple(Abs(x)) == -x
        b = Brain([x], Element(x, OpenClosedInterval(-Infinity, 0)))
        assert b.simple(Abs(x)) == -x

    def test_Add(self):
        b = Brain()
        assert b.simple(Add(2, 3)) == Expr(5)
        assert b.simple(Add(-1, 1)) == Expr(0)
        assert b.simple(Add(0, 0, 0)) == Expr(0)
        assert b.simple(Add(0, 0, 1)) == Expr(1)
        assert b.simple(Add(-1, Pi, 1)) == Pi

    def test_Mul(self):
        b = Brain()
        assert b.simple(Pi**2 / Pi) == Pi
        assert b.simple(Pi / Pi**2) == 1/Pi
        assert b.simple(Pi**2 / (Pi - 2*Pi)**2) == Expr(1)
        assert b.simple(Pi**2 / (Pi - 2*Pi)**3) == b.simple(-1/Pi)

    def test_Zeros(self):
        b = Brain()
        assert b.simple(Zeros(x**2+1, ForElement(x, CC))) == Set(ConstI, Neg(ConstI))
        assert b.simple(Zeros(x**2+1, ForElement(x, RR))) == Set()
        assert b.simple(Zeros(x**2+1, ForElement(x, CC), Greater(Im(x), 0))) == Set(ConstI)
        # xxx
        assert b.simple(Zeros(0, ForElement(x, CC))) != Set()
        assert b.simple(Zeros(0, ForElement(x, CC), NotEqual(x, 0))) != Set()

    def test_Where(self):
        b = Brain()
        assert b.simple(Where(x**2, Def(x, Pi))) == Pi**2
        assert b.simple(Where(x*y, Def(x, 5), Def(y, x+1))) == Expr(30)
        assert b.simple(Where(f(3)*f(4), Def(f(x), x**2))) == Expr(144)
        assert b.simple(Where(x+y, Def([x,y], List(3,5)))) == Expr(8)

    def test_fungrim(self):
        b = FungrimBrain()
        assert b.simple(RiemannZeta(2) / Pi**2) == Div(1,6)
        assert b.simple((1+Sqrt(5))/2) == GoldenRatio
        assert b.simple(Sin(1)**2 + Cos(1)**2) == Expr(1)
        assert b.simple(Erf(Sin(1)**2 + Cos(1)**2) + Erfc(1)) == Expr(1)
        assert b.simple(2 * Integral(1/(2*x+3)**Div(3,2), For(x, 1, Infinity))) == b.simple(2 * Pow(5, Div(-1, 2)))

    def test_hypergeometric(self):
        N = 8
        for b in range(-N,N+1):
            for z in [0, -2, 2]:
                for r in [True, False]:
                    if r:
                        f = Hypergeometric0F1Regularized(Div(b, 2), z)
                    else:
                        f = Hypergeometric0F1(Div(b, 2), z)
                    g = f.eval()
                    try:
                        x1 = f.n(as_arb=True)
                        x2 = g.n(as_arb=True)
                    except ValueError:
                        x1 = x2 = Expr(0).n(as_arb=True)
                    if not x1.overlaps(x2):
                        raise ValueError
        N = 6
        for a in range(-N,N+1):
            for b in range(-N,N+1):
                for z in [0, -2, 2]:
                    for r in [True, False]:
                        if r:
                            f = Hypergeometric1F1Regularized(Div(a, 2), Div(b, 2), z)
                        else:
                            f = Hypergeometric1F1(Div(a, 2), Div(b, 2), z)
                        g = f.eval()
                        try:
                            x1 = f.n(as_arb=True)
                            x2 = g.n(as_arb=True)
                        except ValueError:
                            x1 = x2 = Expr(0).n(as_arb=True)
                        if not x1.overlaps(x2):
                            raise ValueError
        if 0:
            N = 6   # slow
        else:
            N = 3
        for a in range(-N,N+1):
            for b in range(-N,N+1):
                for c in range(-N,N+1):
                    for z in [0, 1, Div(1,4), 4]:
                        for r in [True, False]:
                            if r:
                                f = Hypergeometric2F1Regularized(Div(a, 2), Div(b, 2), Div(c, 2), z)
                            else:
                                f = Hypergeometric2F1(Div(a, 2), Div(b, 2), Div(c, 2), z)
                            g = f.eval()
                            try:
                                x1 = f.n(as_arb=True)
                                x2 = g.n(as_arb=True)
                            except ValueError:
                                x1 = x2 = Expr(0).n(as_arb=True)
                            if not x1.overlaps(x2):
                                raise ValueError
