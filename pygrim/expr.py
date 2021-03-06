# -*- coding: utf-8 -*-

int_types = (int, type(1<<128))

katex_function = []

int_cache = {}

def escape_title(name):
    # paren = name.find("(")
    # if paren >= 0:
    #     name = name[:paren].rstrip(" ")
    return name.replace(" ", "_")

class Expr(object):
    """
    Represents a symbolic expression.

    A symbolic expression is either an atom (symbol, integer or text)
    or a non-atomic expression representing a function application
    f(a, b, ...) where f and a, b, ... are symbolic expressions.

    The methods .is_atom(), and specifically .is_symbol(), .is_integer(),
    .is_text() are useful to check for atoms.

    For a non-atomic expression expr, expr.head() returns f and
    expr.args() returns (a, b, ...) as a Python tuple.
    For a non-atomic expression, these methods both return None.

    Expr objects are immutable and instances may be cached silently.

    Most arithmetic operators are overloaded to permit constructing
    expressions in natural syntax, but the == and != operators
    perform structural comparison.
    """

    def __new__(self, arg=None, symbol_name=None, call=None):
        """
        Expr(expr) creates a copy of expr (this may actually return
        the same object).

        Expr(5) creates an Integer atom with the value 5.
        Expr("text") creates a Text atom with the value "text".
        Expr(symbol_name="x") creates a Symbol atom with the label "x".

        Expr(call=(f, a, b)) creates the non-atomic expression f(a, b).
        """
        if isinstance(arg, Expr):
            return arg
        self = object.__new__(Expr)
        self._hash = None
        self._symbol = None
        self._integer = None
        self._text = None
        self._args = None
        if symbol_name is not None:
            self._symbol = symbol_name
        elif isinstance(arg, str):
            self._text = arg
        elif isinstance(arg, int_types):
            if isinstance(arg, bool):
                return [False_, True_][arg]
            self._integer = int(arg)
        elif call is not None:
            self._args = tuple(Expr(obj) for obj in call)
            assert len(self._args) >= 1
        elif isinstance(arg, list):
            return List(*(Expr(x) for x in arg))
        elif isinstance(arg, tuple):
            return Tuple(*(Expr(x) for x in arg))
        elif isinstance(arg, float):
            import math
            if math.isinf(arg):
                if arg > 0.0:
                    return Infinity
                else:
                    return -Infinity
            if math.isnan(arg):
                return Undefined
            if arg == 0.0:
                return Expr(0)
            m, e = math.frexp(arg)
            m = int(m * 2.0**53)
            e -= 53
            s = str(m)
            trailing = (m^(m-1)).bit_length()-1
            m >>= trailing
            e += trailing
            if 0 <= e <= 20:
                return Expr(m * 2**e)
            if -8 <= e < 0:
                return Expr(m) / Expr(2**-e)
            if m == 1:
                return Expr(2)**e
            if m == -1:
                return -Expr(2)**e
            return Expr(m) * Expr(2)**e
        elif isinstance(arg, complex):
            if arg.real == 0.0:
                if arg.imag == 1.0:
                    return ConstI
                if arg.imag == -1.0:
                    return -ConstI
                return Expr(arg.imag) * ConstI
            if arg.imag == 0.0:
                return Expr(arg.real)
            return Expr(arg.real) + Expr(arg.imag) * ConstI
        else:
            try:
                import flint
                if type(arg) is flint.fmpz:
                    return Expr(int(arg))
                elif type(arg) is flint.fmpq:
                    p = arg.p
                    q = arg.q
                    if q == 1:
                        return Expr(int(p))
                    elif p > 0:
                        return Div(Expr(int(p)), Expr(int(q)))
                    else:
                        return -Div(Expr(int(-p)), Expr(int(q)))
            except ImportError:
                pass
            raise ValueError("cannot create Expr from type %s", type(arg))
        return self

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if hash(self) != hash(other):
            return False
        if self._args is not None:
            if other._args is not None:
                return self._args == other._args
            return False
        if self._symbol is not None:
            if other._symbol is not None:
                return self._symbol == other._symbol
            return False
        if self._integer is not None:
            if other._integer is not None:
                return self._integer == other._integer
            return False
        if self._text is not None:
            if other._text is not None:
                return self._text == other._text
            return False
        return False

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        if self._hash is None:
            if self._symbol is not None:
                self._hash = hash(self._symbol)
            elif self._integer is not None:
                self._hash = hash(self._integer)
            elif self._text is not None:
                self._hash = hash(self._text)
            else:
                self._hash = hash(self._args)
        return self._hash

    def __int__(self):
        return int(self._integer)

    def is_atom(self):
        """Returns True if self is an atom (symbol, integer or text),
        False otherwise."""
        return self._args is None

    def is_symbol(self):
        return self._symbol is not None

    def is_integer(self):
        return self._integer is not None

    def is_text(self):
        return self._text is not None

    def head(self):
        if self._args is None:
            return None
        return self._args[0]

    def args(self):
        if self._args is None:
            return None
        return self._args[1:]

    def __call__(self, *args):
        return Expr(call=((self,) + args))

    def __pos__(self):
        return Pos(self)
    def __neg__(self):
        return Neg(self)
    def __abs__(self):
        return Abs(self)

    def __add__(self, other):
        return Add(Expr(self), Expr(other))
    def __radd__(self, other):
        return Add(Expr(other), Expr(self))

    def __sub__(self, other):
        return Sub(Expr(self), Expr(other))
    def __rsub__(self, other):
        return Sub(Expr(other), Expr(self))

    def __mul__(self, other):
        return Mul(Expr(self), Expr(other))
    def __rmul__(self, other):
        return Mul(Expr(other), Expr(self))

    def __div__(self, other):
        return Div(Expr(self), Expr(other))
    def __rdiv__(self, other):
        return Div(Expr(other), Expr(self))
    def __truediv__(self, other):
        return Div(Expr(self), Expr(other))
    def __rtruediv__(self, other):
        return Div(Expr(other), Expr(self))

    def __pow__(self, other):
        return Pow(Expr(self), Expr(other))
    def __rpow__(self, other):
        return Pow(Expr(other), Expr(self))

    def str(self, level=0, **kwargs):
        if self._symbol is not None:
            s = str(self._symbol)
        elif self._integer is not None:
            s = str(self._integer)
        elif self._text is not None:
            s = self._text.replace('"', '\\"')
            return '"' + s + '"'
        elif self._args is not None:
            fstr = self._args[0].str(level, **kwargs)
            argstrs = [arg.str(level+1, **kwargs) for arg in self._args[1:]]
            if self._args[0] == Entry:
                s = fstr + "(" + ",\n    ".join(argstrs) + ")"
            else:
                s = fstr + "(" + ", ".join(argstrs) + ")"
        else:
            raise ValueError("no content")
        return s

    def __str__(self):
        #if self.is_integer():
        #    return "Expr(%s)" % int(self)
        return self.str()

    def __repr__(self):
        #if self.is_integer():
        #    return "Expr(%s)" % int(self)
        return self.str()

    def _repr_latex_(self):
        return "$$" + self.latex() + "$$"

    def atoms(self, unique=False):
        """
        Generate all atoms in this expression. With unique=True, avoids
        repetitions.
        """
        if self.is_atom():
            yield self
        else:
            if unique:
                seen = set()
                for arg in self._args:
                    for atom in arg.atoms():
                        if atom not in seen:
                            yield atom
                            seen.add(atom)
            else:
                for arg in self._args:
                    for atom in arg.atoms():
                        yield atom

    def symbols(self, unique=False):
        """
        Generate all symbols in this expression. With unique=True, avoids
        repetitions.
        """
        if self.is_symbol():
            yield self
        elif not self.is_atom():
            if unique:
                seen = set()
                for arg in self._args:
                    for symbol in arg.symbols():
                        if symbol not in seen:
                            yield symbol
                            seen.add(symbol)
            else:
                for arg in self._args:
                    for symbol in arg.symbols():
                        yield symbol

    def free_variables(self, bound=None):
        """
        Return a list of the free variables in self, assuming that self
        is a mathematical formula.
        """
        variables = set()
        if bound is None:
            bound = set()
        else:
            bound = set(bound)

        def search(expr, bound):
            if expr.is_atom():
                if expr.is_symbol():
                    if expr._symbol not in all_builtins_set and expr not in bound:
                        variables.add(expr)
            else:
                head = expr.head()
                args = expr.args()
                # todo: deprecate subscript
                if head == Subscript:
                    a, b = args
                    if a.is_symbol() and b.is_integer():
                        search(a, bound)
                        return
                # todo: handle Fun - expressions
                # todo: variable-length tuple unpacking
                # todo: handle function defs in Where
                if head == Where or any(arg.head() in (For, ForElement) for arg in args):
                    """
                    print(head)
                    for arg in args:
                        print(arg)
                    print()
                    """
                    # we have to deal with variable bindings
                    bound_local = bound.copy()
                    remaining_args = []
                    for i, arg in enumerate(args):
                        # hack; needed because of Equal being used in old Where statements
                        if head == Where and i == 0:
                            remaining_args.append(arg)
                            continue
                        if arg.head() == For or arg.head() == ForElement or (head == Where and arg.head() in (Equal, Def)):
                            new_var = arg.args()[0]
                            if head == Where and arg.head() in (Equal, Def):
                                if not new_var.is_atom() and new_var.head().is_symbol():
                                    func_symb = new_var.head()
                                    if func_symb._symbol not in all_builtins_set:
                                        # Def(f(x, y), expr(x, y)) -- bind f and search locally in expr
                                        func_args = new_var.args()
                                        bound_local2 = bound_local.copy()
                                        for x in func_args:
                                            bound_local2.add(x)
                                        for data in arg.args()[1:]:
                                            search(data, bound_local2)
                                        bound_local.add(func_symb)
                                        continue

                            for data in arg.args()[1:]:
                                search(data, bound_local)

                            # Destructuring assignment (should be improved...)
                            if new_var.head() == Tuple:
                                # allow assigning to Def(Tuple(f(i), For(i, 1, n)), T)
                                if len(new_var.args()) == 2 and new_var.args()[1].head() == For:
                                    fi = new_var.args()[0]
                                    func_symb = fi.head()
                                    i, a, b = new_var.args()[1].args()
                                    if a.is_integer() and b.is_symbol():
                                        bound_local.add(b)
                                        bound_local.add(func_symb)
                                else:
                                    # Regular destructuring assignment
                                    for subvar in new_var.args():
                                        bound_local.add(subvar)
                            elif new_var.head() == Matrix2x2:
                                # Regular destructuring assignment
                                for subvar in new_var.args():
                                    bound_local.add(subvar)
                            else:
                                bound_local.add(new_var)
                        else:
                            remaining_args.append(arg)
                    for arg in remaining_args:
                        search(arg, bound_local)
                else:
                    search(head, bound)
                    for arg in args:
                        search(arg, bound)
        search(self, bound)
        return frozenset(variables)

    def replace(self, rules, semantic=False):
        """
        Replace subexpressions of self with exact matches in the given
        dictionary. If semantic=True, free variables will be replaced
        but bound variables will not.
        """
        if self in rules:
            return rules[self]
        if self.is_atom() or not rules:
            return self
        if not semantic:
            return Expr(call=(arg.replace(rules, semantic=False) for arg in self._args))
        expr = self
        head = expr.head()
        args = expr.args()
        # todo: handle Fun-expressions
        if head == Where or any(arg.head() in (For, ForElement) for arg in args):
            args = list(args)
            remaining_arg_indices = []
            for arg_index, arg in enumerate(args):
                # hack; needed because of Equal being used in old Where statements
                if head == Where and arg_index == 0:
                    remaining_arg_indices.append(arg_index)
                    continue
                if arg.head() == For or arg.head() == ForElement or (head == Where and arg.head() in (Equal, Def)):
                    for_args = list(arg.args())
                    new_var = for_args[0]
                    if head == Where and arg.head() in (Equal, Def):
                        if not new_var.is_atom() and new_var.head().is_symbol():
                            # Def(f(x, y), expr(x, y)) -- replace locally in expr (ignoring x, y), then bind f
                            func_symb = new_var.head()
                            func_args = new_var.args()
                            if func_symb._symbol not in all_builtins_set:
                                rules2 = rules.copy()
                                for x in func_args:
                                    if x in rules2:
                                        del rules2[x]
                                # replace in expr(x, y)
                                for_args = [new_var] + [a.replace(rules2, semantic) for a in for_args[1:]]
                                # bind f
                                if func_symb in rules:
                                    rules = rules.copy()
                                    del rules[func_symb]

                                args[arg_index] = arg.head()(*for_args)
                                continue

                    # Def(x, y) or For(x, a, b) -- 
                    for_args = [new_var] + [a.replace(rules, semantic) for a in for_args[1:]]

                    # Destructuring assignment
                    if new_var.head() == Tuple:
                        # Special destructuring assignment Def(Tuple(f(i), For(i, 1, n)), T)
                        if len(new_var.args()) == 2 and new_var.args()[1].head() == For:
                            fi = new_var.args()[0]
                            func_symb = fi.head()
                            i, a, b = new_var.args()[1].args()
                            # todo: possible variable in a / b ?
                            if b in rules:
                                rules = rules.copy()
                                del rules[b]
                            if func_symb in rules:
                                rules = rules.copy()
                                del rules[func_symb]
                        else:
                            # Regular destructuring assignment
                            for subvar in new_var.args():
                                if subvar in rules:
                                    rules = rules.copy()
                                    del rules[subvar]
                    elif new_var.head() == Matrix2x2:
                        # Regular destructuring assignment
                        for subvar in new_var.args():
                            if subvar in rules:
                                rules = rules.copy()
                                del rules[subvar]
                    else:
                        # Simple variable
                        if new_var in rules:
                            rules = rules.copy()
                            del rules[new_var]

                    args[arg_index] = arg.head()(*for_args)
                else:
                    remaining_arg_indices.append(arg_index)

            # Go back and complete the replace op after binding variables
            for arg_index in remaining_arg_indices:
                args[arg_index] = args[arg_index].replace(rules, semantic)

            return head(*args)
        else:
            head = head.replace(rules, semantic)
            args = [arg.replace(rules, semantic) for arg in args]
            return head(*args)


    def subexpressions(self, unique=False):
        """
        Generate all subexpressions of this expression (including the
        root expression). With unique=True, avoids repetitions.
        """
        yield self
        if not self.is_atom():
            if unique:
                seen = set()
                for arg in self._args:
                    for expr in arg.subexpressions():
                        if expr not in seen:
                            yield expr
                            seen.add(expr)
            else:
                for arg in self._args:
                    for expr in arg.subexpressions():
                        yield expr

    def subexpressions_with_head(self, head):
        if self.head() == head:
            yield self
        if not self.is_atom():
            for arg in self._args:
                for expr in arg.subexpressions_with_head(head):
                    yield expr

    def head_args_flattened(self, head):
        """
        Iterates over args with the given head, flattening nested applications.

            >>> from pygrim import *
            >>> list(And(And(a, b), c).head_args_flattened(And))
            [a, b, c]
            >>> list(And(And(a, b), c).head_args_flattened(Or))
            [And(And(a, b), c)]
        """
        if self.head() == head:
            for x in self.args():
                for t in x.head_args_flattened(head):
                    yield t
        else:
            yield self

    def latex(self, in_small=False, **kwargs):
        from .latex import latex
        return latex(self, in_small=in_small, **kwargs)

    def _can_render_html(self):
        if self.is_integer():
            return True
        if self.head() == Decimal:
            return True
        if self.head() == Div and self.args()[0].is_integer() and self.args()[1].is_integer():
            return True
        if self.head() == Tuple:
            return all(arg._can_render_html() for arg in self.args())
        if self.head() == Set:
            return all(arg._can_render_html() for arg in self.args())
        return False

    def html(self, display=False, avoid_latex=False, single=False):
        katex = katex_function[0]
        if self.is_atom():
            if avoid_latex and self.is_integer():
                return str(self._integer)
            return katex(self.latex(), display=display)
        if self.head() == Decimal and avoid_latex:
            text = self.args()[0]._text
            if "e" in text:
                mant, expo = text.split("e")
                expo = expo.lstrip("+")
                text = mant + " &middot; 10<sup>" + expo + "</sup>"
            return text
        if self.head() == Div and avoid_latex and self.args()[0].is_integer() and self.args()[1].is_integer():
            p, q = self.args()
            return "%s/%s" % (str(self.args()[0]._integer), str(self.args()[1]._integer))
        if self.head() == Neg and avoid_latex and self.args()[0]._can_render_html():
            return "-" + self.args()[0].html(display=display, avoid_latex=True)
        if self.head() == Tuple and avoid_latex and self._can_render_html():
            return "(" + ", ".join(a.html(display=display, avoid_latex=True) for a in self.args()) + ")"
        if self.head() == Set and avoid_latex and self._can_render_html():
            return "{" + ", ".join(a.html(display=display, avoid_latex=True) for a in self.args()) + "}"
        if self.head() == Table:
            return self.html_Table()
        if self.head() == Formula:
            return katex(self._args[1].latex())
        if self.head() == References:
            return self.html_References()
        if self.head() == Assumptions:
            return self.html_Assumptions()
        if self.head() == Description:
            return self.html_Description(display=display)
        if self.head() == CodeExample:
            return self.html_CodeExample()
        if self.head() == SymbolDefinition:
            return self.html_SymbolDefinition()
        if self.head() == Image:
            return self.html_Image(single=single)
        return katex(self.latex(), display=display)

    def html_Image(self, single=False):
        description, image = self.args()
        path = image.args()[0]._text
        s = ""
        s += """<div style="text-align:center; margin:0.6em 0.4em 0.0em 0.2em">"""
        s += """<span style="font-size:85%; color:#888">Image:</span> """
        s += description.html()

        # hack: duplicated constants in html head
        thumb_size = "140px"
        full_size = "500px"

        s += """<button style="margin:0 0 0 0.3em" onclick="toggleBig('%s', '../../img/%s/%s_small.svg', '../../img/%s/%s.svg')">Big &#x1F50D;</button>""" % (path, path, path, path, path)
        s += """<div style="text-align:center; padding-right:1em;">"""
        s += """<img id="%s", src="../../img/%s/%s_small.svg" style="width:%s; max-width:100%%; margin-top:0.3em; margin-bottom:0px"/>""" % (path, path, path, thumb_size)
        s += """</div>"""

        s += """</div>"""
        return s


    def html_Table(self):
        rel = self.get_arg_with_head(TableRelation)
        heads = self.get_arg_with_head(TableHeadings)
        if heads is None:
            heads = self.get_arg_with_head(TableValueHeadings)
        data = self.get_arg_with_head(List)
        split = self.get_arg_with_head(TableSplit)
        colheads = self.get_arg_with_head(TableColumnHeadings)
        headrows = []
        if split is None:
            split = 1
        else:
            split = split.args()[0]._integer
        if heads is None:
            cols = len(data.args()[0].args())
        else:
            cols = len(heads.args())
        num = len(data.args())
        innum = num // split
        s = """<div style="overflow-x:auto;">"""
        s += """<table align="center" style="border:0; background-color:#fff;">"""
        s += """<tr style="border:0; background-color:#fff">"""
        j = 0
        for outer in range(split):
            s += """<td style="border:0; background-color:#fff; vertical-align:top;">"""
            s += """<table style="float: left; margin-right: 1em;">"""
            if heads is not None:
                s += "<tr>"
                for col in heads.args():
                    # the nowrap is a hack to avoid "n \ k" breaking
                    s += """<th style="white-space:nowrap;">""" + col.html(display=False, avoid_latex=True) + "</th>"
                s += "</tr>"
            if outer == split-1:
                end = num
            else:
                end = innum*(outer+1)
            for row in data.args()[innum*outer : end]:
                s += "<tr>"
                if row.head() == TableSection:
                    s += """<td colspan="%i" style="text-align:center; font-weight: bold">%s</td>""" % (cols, row.args()[0]._text)
                else:
                    if colheads is not None:
                        col = colheads.args()[j]
                        s += "<th>" + col.html(display=False, avoid_latex=True) + "</th>"
                    for i, col in enumerate(row.args()):
                        s += "<td>" + col.html(display=False, avoid_latex=True) + "</td>"
                s += "</tr>"
                j += 1
            s += """</table>"""
            s += "</td>"
        s += "</tr></table></div>"
        if rel is not None:
            s += """<div style="text-align:center; margin-top: 0.5em">"""
            s += Description("Table data:", rel.args()[0], " such that ", rel.args()[1]).html(display=True)
            s += """</div>"""
        return s

    def html_References(self):
        s = ""
        s += """<div class="entrysubhead">References:</div>"""
        s += "<ul>"
        for ref in self._args[1:]:
            if ref.head() == SloaneA:
                continue
            s += "<li>%s</li>" % ref._text
        s += "</ul>"
        return s

    def html_Assumptions(self):
        s = ""
        #s += """<div class="entrysubhead">Assumptions:</div>"""

        #for arg in self.args():
        #    s += arg.html(display=True)
        #return s
        num = 1
        for arg in self.args():
            s += """<div style="text-align:center; margin:0.8em">"""
            if num == 1:
                strcond = "Assumptions"
            else:
                strcond = "Alternative assumptions"
            s += """<span style="font-size:85%; color:#888; margin-right:0.8em">""" + strcond + """:</span>"""
            s += arg.html(display=False)
            s += """</div>"""
            num += 1
        return s

    def _html_Description(self):
        s = ""
        for arg in self.args():
            if arg.is_text():
                if arg._text and arg._text[0] in (",", ".", ";"):
                    s = s.rstrip()
                s += arg._text
            elif (not arg.is_atom()) and arg.head() == SourceForm:
                s += """<span style="border: 1px solid #ddd; padding-left:0.3em; padding-right:0.2em"><tt>%s</tt></span>""" % str(arg.args()[0])
            elif (not arg.is_atom()) and arg.head() == EntryReference:
                id = arg.args()[0]._text
                s += """<a href="../../entry/%s/">%s</a>""" % (id, id)
            elif (not arg.is_atom()) and arg.head() == TopicReference:
                title = arg.args()[0]._text
                s += """<a href="../../topic/%s/">%s</a>""" % (escape_title(title), title)
            else:
                s += arg.html(avoid_latex=True)
            s += " "
        return s

    def html_Description(self, display=False):
        s = ""
        if display:
            s += """<div style="text-align:center; margin:0.6em">"""
        s += self._html_Description()
        if display:
            s += """</div>"""
        return s

    def html_CodeExample(self):
        #expr, *args = self.args()
        expr = self.args()[0]
        args = self.args()[1:]
        s = ""
        s += """<div style="text-align:left; margin:1em"><span style="margin-right:0.5em">&#9658;</span>"""
        s += Description(SourceForm(expr))._html_Description()
        s += """ <span style="color:#888; margin:0.5em">&mdash;</span> """
        s += Description(expr)._html_Description()
        s += """ <span style="color:#888; margin:0.5em">&mdash;</span> """
        s += Description(*args)._html_Description()
        s += "</div>"
        return s

    def html_SymbolDefinition(self):
        symbol, example, description = self.args()
        s = ""
        s += """<div style="text-align:center; margin:0.6em">"""
        s += """<span style="font-size:85%; color:#888">Symbol:</span> """
        s += """<tt><a href="../../symbol/%s/">%s</a></tt>""" % (symbol._symbol, symbol._symbol)
        s += """ <span style="color:#888">&mdash;</span> """
        s += example.html()
        s += """ <span style="color:#888">&mdash;</span> """
        s += description._text
        s += """</div>"""
        return s

    def get_arg_with_head(self, head):
        for arg in self.args():
            if not arg.is_atom() and (arg.head() == head):
                return arg
        return None

    def id(self):
        id = self.get_arg_with_head(ID)
        return id._args[1]._text

    def title(self):
        title = self.get_arg_with_head(Title)
        return title._args[1]._text

    def entry_html(self, single=False, entry_dir="../../entry/", symbol_dir="../../symbol/", default_visible=False):
        id = self.id()
        all_tex = []
        image_downloads = []
        s = ""
        s += """<div class="entry">"""
        if single:
            s += """<div style="padding-top:0.4em">"""
        else:
            s += """<div style="float:left; margin-top:0.0em; margin-right:0.3em">"""
            s += """<a href="%s%s/" style="margin-left:3pt; font-size:85%%">%s</a> <span></span><br/>""" % (entry_dir, id, id)
            s += """<button style="margin-top:0.2em; margin-bottom: 0.1em;" onclick="toggleVisible('%s:info')">Details</button>""" % id
            s += """</div>"""
            s += """<div>"""

        args = self.args()
        args = [arg for arg in args if arg.head() not in (ID, Variables)]

        for arg in args:
            if arg.head() == Image:
                src = arg.get_arg_with_head(ImageSource).args()[0]._text
                image_downloads.append(src)

        # First item is always visible
        s += args[0].html(display=True, single=single)
        s += "</div>"

        # Remaining items may be hidden beneath the fold
        if single:
            s += """<div id="%s:info" style="padding: 1em; clear:both">""" % id
        else:
            if default_visible:
                s += """<div id="%s:info" style="display:visible; padding: 1em; clear:both">""" % id
            else:
                s += """<div id="%s:info" style="display:none; padding: 1em; clear:both">""" % id

        if image_downloads:
            src = image_downloads[0]
            s += """<div style="text-align:center; margin-top:0; margin-bottom:1.1em">"""
            s += """<span style="font-size:85%; color:#888">Download:</span> """
            s += """<a href="../../img/%s/%s_small.png">png (small)</a>""" % (src, src)
            s += """ <span style="color:#888">&mdash;</span> """
            s += """<a href="../../img/%s/%s_medium.png">png (medium)</a>""" % (src, src)
            s += """ <span style="color:#888">&mdash;</span> """
            s += """<a href="../../img/%s/%s_large.png">png (large)</a>""" % (src, src)
            s += """ <span style="color:#888">&mdash;</span> """
            s += """<a href="../../img/%s/%s_small.pdf">pdf (small)</a>""" % (src, src)
            s += """ <span style="color:#888">&mdash;</span> """
            s += """<a href="../../img/%s/%s.pdf">pdf (medium/large)</a>""" % (src, src)
            s += """ <span style="color:#888">&mdash;</span> """
            s += """<a href="../../img/%s/%s_small.svg">svg (small)</a>""" % (src, src)
            s += """ <span style="color:#888">&mdash;</span> """
            s += """<a href="../../img/%s/%s.svg">svg (medium/large)</a>""" % (src, src)
            s += """</div>"""

        # Link SloaneA to OEIS references
        oeisrefs = set()
        for arg in args:
            refs = list(arg.subexpressions_with_head(SloaneA))
            for r in refs:
                X = r.args()[0]
                if X.is_integer():
                    oeisrefs.add(X)
                elif X.is_text():
                    X = X._text.lstrip("A")
                    if X.isdigit():
                        oeisrefs.add(int(X))

        if oeisrefs:
            oeisrefs = sorted(list(oeisrefs))
            oeisrefs = tuple("""Sequence <a href="https://oeis.org/A%06i">A%06i</a> in Sloane's On-Line Encyclopedia of Integer Sequences (OEIS)</a>""" % (r, r) for r in oeisrefs)
            refarg = -1
            for i in range(1,len(args)):
                if args[i].head() == References:
                    refarg = i
                    break
            if refarg == -1:
                args.append(References(*oeisrefs))
            else:
                args[refarg] = References(*(args[refarg].args() + oeisrefs))

        # Remaining items
        for arg in args[1:]:
            s += arg.html(display=True)
            s += "\n\n"

        # Generate TeX listing
        for arg in self.args():
            if arg.head() in (Formula, Assumptions):
                for arg2 in arg.args():
                    all_tex.append(arg2.latex())

        if all_tex:
            s += """<div class="entrysubhead">TeX:</div>"""
            s += "<pre>"
            s += "\n\n".join(all_tex)
            s += "</pre>"

        # Generate symbol table
        symbols = self.symbols(unique=True)
        symbols = [sym for sym in symbols if sym not in exclude_symbols]
        s += """<div class="entrysubhead">Definitions:</div>"""
        s += Expr.definitions_table_html(symbols, center=True, symbol_dir=symbol_dir)

        s += """<div class="entrysubhead">Source code for this entry:</div>"""
        s += "<pre>"
        s += self.str()
        s += "</pre>"

        s += "</div></div>\n"

        return s

    @staticmethod
    def definitions_table_html(symbols, center=False, entry_dir="../../entry/", symbol_dir="../../symbol/"):
        katex = katex_function[0]
        s = ""
        if center:
            s += """<table style="margin: 0 auto">"""
        else:
            s += """<table>"""
        # s += """<tr><th>Fungrim symbol</th> <th>Notation</th> <th>Domain</th> <th>Codomain</th> <th>Description</th></tr>"""
        s += """<tr><th>Fungrim symbol</th> <th>Notation</th> <th>Short description</th></tr>"""
        for symbol in symbols:
            if symbol in descriptions:
                example, domain, codomain, description = descriptions[symbol]
                s += """<tr><td><tt><a href="%s%s/">%s</a></tt>""" % (symbol_dir, symbol.str(), symbol.str())
                s += """<td>%s</td>""" % katex(example.latex(), False)
                # domstr = ",\, ".join(dom.latex() for dom in domain)
                # s += """<td>%s</td>""" % katex(domstr, False)
                # if codomain is None:
                #     s += """<td></td>"""
                # else:
                #     s += """<td>%s</td>""" % katex(codomain.latex(), False)
                s += """<td>%s</td></tr>""" % description
        s += """</table>"""
        return s

    def n(self, digits=20, **kwargs):
        from .numeric import neval
        return neval(self, digits, **kwargs)

    def simple(self, assumptions=None, variables=None, **kwargs):
        """
        Simple expression simplification: returns an expression that is
        mathematically equivalent to the original expression.

            >>> (-(-Expr(3))).simple()
            3
            >>> And(Element(3, ZZ), Element(Pi, SetMinus(RR, QQ))).simple()
            True_

        The following expression does not change; without assumptions,
        it is unknown whether arithmetic with x is associative!

            >>> Expr(1 + x + 1).simple()
            Add(Add(1, x), 1)

        Providing assumptions permits simplification:

            >>> Expr(1 + x + 1).simple(Element(x, CC))
            Add(2, x)

        This method is a simple wrapper around Brain.simple.
        """
        from .brain import Brain
        assert (assumptions is None or isinstance(assumptions, Expr))
        if variables is None:
            variables = self.free_variables()
            if assumptions is not None:
                variables = variables.union(assumptions.free_variables())
        b = Brain(variables=variables, assumptions=assumptions, **kwargs)
        return b.simple(self)

    def eval(self, *args, **kwargs):
        return self.simple(*args, **kwargs)

    def rewrite_fungrim(self, entry_id, assumptions=None, variables=None, recursive=True):
        # todo: combine with other code?
        from .brain import Brain
        assert (assumptions is None or isinstance(assumptions, Expr))
        if variables is None:
            variables = self.free_variables()
            if assumptions is not None:
                variables = variables.union(assumptions.free_variables())
        b = Brain(variables=variables, assumptions=assumptions)
        return b.rewrite_fungrim(self, entry_id, recursive=recursive)

    def test(self, variables, assumptions=None, num=100, verbose=True, raising=True):
        """
        Test that this formula holds for variables satisfying the given
        assumptions, by assigning random values to the listed
        free variables and attempting to simplify.

        These assumptions are not correct:

            >>> try:
            ...     Equal(Sqrt(x**2), x).test([x], Element(x, RR))
            ... except ValueError:
            ...     print("FAIL!")
            ...
            {x: 0}    ...  True
            {x: Div(1, 2)}    ...  True
            {x: Sqrt(2)}    ...  True
            {x: Pi}    ...  True
            {x: 1}    ...  True
            {x: Neg(Div(1, 2))}    ...  False
            FAIL!

        Valid assumptions:
        
            >>> _ = Equal(Sqrt(x**2), x).test([x], And(Element(x, RR), GreaterEqual(x, 0)))
            {x: Div(1, 2)}    ...  True
            ...
            Passed 69 instances (68 True, 1 Unknown, 0 False)

            >>> _ = Equal(Sqrt(x**2), x).test([x], And(Element(x, CC), Or(Greater(Re(x), 0), And(Equal(Re(x), 0), Greater(Im(x), 0)))))
            {x: Div(1, 2)}    ...  True
            ...
            Passed 91 instances (85 True, 6 Unknown, 0 False)

        """
        info = {"True": 0, "Unknown": 0, "False": 0}
        if len(variables) == 0:
            v = self.simple()
            if v == False_:
                if verbose:
                    print("False")
                if raising:
                    raise ValueError
                info["False"] += 1
            elif v == True_:
                if verbose:
                    print("True")
                info["True"] += 1
            else:
                if verbose:
                    print("Unknown")
                info["Unknown"] += 1
        else:
            from .brain import Brain
            b = Brain()
            import sys
            for assignment in b.some_values(variables, assumptions, num=num, as_dict=True):
                v = self.replace(assignment, semantic=True)
                if verbose:
                    print(assignment, "   ...  ", end="")
                    sys.stdout.flush()
                v = v.simple()
                if v == False_:
                    if verbose:
                        print("False")
                    info["False"] += 1
                    if raising:
                        raise ValueError
                elif v == True_:
                    if verbose:
                        print("True")
                    info["True"] += 1
                else:
                    if verbose:
                        print("Unknown")
                    info["Unknown"] += 1
        info["Total"] = info["True"] + info["False"] + info["Unknown"]
        if verbose:
            print("Passed", info["True"] + info["Unknown"], "instances (%i True, %i Unknown, %i False)" % (info["True"], info["Unknown"], info["False"]))
        return info

all_builtins = []
all_builtins_set = set()

def inject_builtin(string):
    for sym in string.split():
        globals()[sym] = Expr(symbol_name=sym)
        all_builtins.append(sym)
        all_builtins_set.add(sym)

variable_names = set()

def inject_vars(string):
    for s in string.split():
        for sym in [s, s + "_"]:
            e = Expr(symbol_name=sym)
            globals()[sym] = e
            variable_names.add(sym)

inject_builtin("""
Universe Sets Tuples
Fun Function MultivariateFunction
Funs Functions MultivariateFunctions
CartesianProduct CartesianPower
Restriction MultivariateRestriction
One Zero Characteristic
Matrices GeneralLinearGroup SpecialLinearGroup IdentityMatrix ZeroMatrix
Def Gen
All Exists
True_ False_
Parentheses Brackets Braces AngleBrackets
Ellipsis Call Subscript
Repeat Step
Unknown Undefined
Where
Set List Tuple
PowerSet
Union Intersection SetMinus Not And Or Equivalent Implies
Cardinality
Element Elements DistinctElements NotElement Subset SubsetEqual
EqualAndElement
Concatenation
Length Item
Rings CommutativeRings Fields
PP ZZ QQ RR CC HH AlgebraicNumbers ZZp QQp
ZZGreaterEqual ZZLessEqual Range
ClosedInterval OpenInterval ClosedOpenInterval OpenClosedInterval
Path CurvePath
RealBall
UnitCircle
OpenDisk ClosedDisk BernsteinEllipse
InteriorClosure Interior
Decimal
Equal NotEqual Greater GreaterEqual Less LessEqual
Pos Neg Add Sub Mul Div Mod Inv Pow
CongruentMod Odd Even
Max Min Sign Csgn Abs Floor Ceil Arg Re Im Conjugate RealAbs
NearestDecimal
EqualNearestDecimal
Minimum Maximum ArgMin ArgMax ArgMinUnique ArgMaxUnique
Solutions UniqueSolution
Supremum Infimum
Limit SequenceLimit RealLimit LeftLimit RightLimit ComplexLimit MeromorphicLimit
SequenceLimitInferior SequenceLimitSuperior
Derivative RealDerivative ComplexDerivative ComplexBranchDerivative MeromorphicDerivative
IsHolomorphic IsMeromorphic
Sum Product
PrimeSum DivisorSum PrimeProduct DivisorProduct
Integral
IndefiniteIntegralEqual RealIndefiniteIntegralEqual ComplexIndefiniteIntegralEqual
AsymptoticTo
FormalGenerator Polynomials PolynomialFractions RationalFunctions PowerSeries LaurentSeries SeriesCoefficient
Poles BranchPoints BranchCuts EssentialSingularities Zeros UniqueZero AnalyticContinuation
ComplexZeroMultiplicity
Residue
Infinity UnsignedInfinity
Sqrt NthRoot Log LogBase Exp
Sin Cos Tan Sec Cot Csc
Asin Acos Atan Atan2 Asec Acot Acsc
Sinh Cosh Tanh Sech Coth Csch
Asinh Acosh Atanh Asech Acoth Acsch
Sinc LambertW LambertWPuiseuxCoefficient
Pi ConstE ConstGamma ConstI GoldenRatio ConstCatalan ConstGlaisher
Binomial Factorial DoubleFactorial Gamma LogGamma DigammaFunction DigammaFunctionZero PolyGamma
RisingFactorial FallingFactorial HarmonicNumber StirlingSeriesRemainder
Erf Erfc Erfi
UpperGamma LowerGamma
BernoulliB BernoulliPolynomial EulerE EulerPolynomial
StirlingCycle StirlingS1 StirlingS2 BellNumber
RiemannZeta RiemannZetaZero
BesselJ BesselI BesselY BesselK HankelH1 HankelH2
BesselJZero BesselYZero
CoulombF CoulombG CoulombH CoulombC CoulombSigma
Hypergeometric0F1 Hypergeometric1F1 Hypergeometric2F1 Hypergeometric2F0 Hypergeometric3F2
HypergeometricU HypergeometricUStar
Hypergeometric0F1Regularized Hypergeometric1F1Regularized Hypergeometric2F1Regularized Hypergeometric3F2Regularized
Hypergeometric1F2 Hypergeometric1F2Regularized
Hypergeometric2F2 Hypergeometric2F2Regularized
HypergeometricPFQ
HypergeometricPFQRegularized
HypergeometricUStarRemainder
AiryAi AiryBi AiryAiZero AiryBiZero
LegendrePolynomial LegendrePolynomialZero GaussLegendreWeight
HermitePolynomial
ChebyshevT ChebyshevU
DedekindEta EulerQSeries DedekindEtaEpsilon DedekindSum
JacobiTheta JacobiThetaEpsilon JacobiThetaPermutation JacobiThetaQ
Divides
GCD LCM XGCD DivisorSigma MoebiusMu Totient SquaresR LiouvilleLambda
LegendreSymbol JacobiSymbol KroneckerSymbol
Fibonacci
PartitionsP HardyRamanujanA
KroneckerDelta
Lattice
WeierstrassP WeierstrassZeta WeierstrassSigma
PrimeNumber PrimePi
RiemannHypothesis
SinIntegral LogIntegral LandauG
Matrix2x2 Matrix2x1 Matrix
Spectrum Det SingularValues
SL2Z PSL2Z ModularGroupAction ModularGroupFundamentalDomain
ModularLambdaFundamentalDomain
ModularJ ModularLambda
PrimitiveReducedPositiveIntegralBinaryQuadraticForms
HilbertClassPolynomial
DirichletCharacter DirichletGroup PrimitiveDirichletCharacters
ConreyGenerator
DiscreteLog
Cases Otherwise
HurwitzZeta DirichletL GeneralizedBernoulliB LerchPhi PolyLog
RiemannXi StieltjesGamma KeiperLiLambda DeBruijnNewmanLambda
DirichletLZero
GeneralizedRiemannHypothesis
DirichletLambda GaussSum JacobiSum
MultiZetaValue
EisensteinG EisensteinE
AGM AGMSequence EllipticK EllipticE EllipticPi IncompleteEllipticF IncompleteEllipticE IncompleteEllipticPi
EllipticSingularValue
EllipticInvariantG EllipticRootE
CarlsonRF CarlsonRG CarlsonRJ CarlsonRD CarlsonRC CarlsonHypergeometricR CarlsonHypergeometricT
QSeriesCoefficient EqualQSeriesEllipsis
BetaFunction IncompleteBeta IncompleteBetaRegularized
BarnesG LogBarnesG LogBarnesGRemainder
SloaneA
HalphenConstant PolynomialDegree RationalFunctionDegree
HilbertMatrix
StandardIndeterminates StandardNoncommutativeIndeterminates
EvaluateIndeterminate CallIndeterminate
XX XXSeries XXNonCommutative
Evaluated Logic
Cyclotomic
SymmetricPolynomial
PolX
PolY
PolZ
Pol
SerX
SerY
SerQ
Ser
NonComX
NonComY
NonCom
Coefficient
Polynomial
One
Zero
Characteristic
Rings
CommutativeRings
Fields
QuotientRing

FormalPowerSeries
FormalLaurentSeries
FormalPuiseuxSeries

""")

inject_builtin("""
For ForElement Var
Entry Formula ID Assumptions References Variables DomainCodomain
CodeExample
Description Table TableRelation TableValueHeadings TableHeadings TableColumnHeadings TableSplit TableSection
Topic Title DefinitionsTable Section Subsection SeeTopics Entries EntryReference TopicReference
SourceForm SymbolDefinition
Image ImageSource
""")

# symbols we don't want to show in entry definition listings, because they are too common/generic
# todo: a better solution may be to hide long tables
exclude_symbols = set([Set, List, Tuple, And, Or, Implies, Equivalent, Not,
    Element, Elements, NotElement, Union, Intersection, SetMinus, Subset, SubsetEqual, For, ForElement,
    Repeat, Step, Parentheses, Brackets, Braces, AngleBrackets, Entry, ID, Formula, Variables,
    Assumptions, References, Description])


inject_vars("""a b c d e f g h i j k l m n o p q r s t u v w x y z""")
inject_vars("""A B C D E F G H I J K L M N O P Q R S T U V W X Y Z""")
inject_vars("""alpha beta gamma delta epsilon zeta eta theta iota kappa lamda mu nu xi pi rho sigma tau phi chi psi omega ell""")
inject_vars("""Alpha Beta GreekGamma Delta Epsilon Zeta Eta Theta Iota Kappa Lamda Mu Nu Xi GreekPi Rho Sigma Tau Phi Chi Psi Omega""")

described_symbols = []
descriptions = {}
long_descriptions = {}
domain_tables = {}

def describe(symbol, example, domain, codomain, description):
    described_symbols.append(symbol)
    descriptions[symbol] = (example, domain, codomain, description)

def describe2(symbol, example, description, domain_table=None, long_description=None):
    described_symbols.append(symbol)
    descriptions[symbol] = (example, None, None, description)
    if long_description is not None:
        long_descriptions[symbol] = long_description
    if domain_table is not None:
        domain_tables[symbol] = domain_table



description_x_predicate = Description("The expression", SourceForm(Var(x)),
    "declares", SourceForm(x), "as a locally bound variable within the scope of the arguments to this operator. ",
    "The corresponding predicate", P(x), "must define the domain of", x, "unambiguously; that is, it must include a statement such as",
    Element(x, S), "where", S, "is a known set.",
    "More generally,", SourceForm(Var(x, y, Ellipsis)), "defines a collection of variables", Tuple(x, y, Ellipsis),
    "all of which become locally bound, with a corresponding predicate", P(x, y, Ellipsis), ".")

description_xray = Description("An X-ray plot illustrates the geometry of a complex analytic function", f(z), ".",
    "Thick black curves show where", Equal(Im(f(z)), 0), "(the function is pure real).",
    "Thick red curves show where", Equal(Re(f(z)), 0), "(the function is pure imaginary).",
    "Points where black and red curves intersect are zeros or poles.",
    "Magnitude level curves", Equal(Abs(f(z)), C), "are rendered as thin gray curves, with brighter shades corresponding to larger", C, ".",
    "Blue lines show branch cuts.",
    "The value of the function is continuous with the branch cut on the side indicated with a solid line, and discontinuous on the side indicated with a dashed line.",
    "Yellow is used to highlight important regions.")


all_entries = []
all_topics = []

def def_Topic(*args):
    topic = Topic(*args)
    all_topics.append(topic)

def make_entry(*args):
    entry = Entry(*args)
    symd = entry.get_arg_with_head(SymbolDefinition)
    if symd is not None:
        id = entry.get_arg_with_head(ID)
        symbol, example, description = symd.args()
        described_symbols.append(symbol)
        descriptions[symbol] = (example, None, None, description._text)
        domain_tables[symbol] = id.args()[0]._text
    all_entries.append(entry)


class TestExpr:

    def __init__(self):
        pass

    def run(self):
        for method in dir(self):
            if method.startswith("test_"):
                print(method, "...", end=" ")
                getattr(self, method)()
                print("OK!")

    def test_free_variables(self):
        assert (x+y+1).free_variables() == set([x, y])
        assert (Pi+1).free_variables() == set()
        assert (x+Where(y, Def(y, 3))).free_variables() == set([x])
        assert (x+Where(y, Def(y, y))).free_variables() == set([x, y])
        assert (x+Where(y, Def(y, 3), Def(z, y))).free_variables() == set([x])
        assert Sum(f(n), For(n, a, b)).free_variables() == set([f, a, b])
        assert Sum(f(n), ForElement(n, S)).free_variables() == set([f, S])
        assert Where(t+y*u, Def(Tuple(t, u), v)).free_variables() == set([y, v])
        assert Where(f(b), Def(f(z), z+a)).free_variables() == set([a, b])
        assert Where(f(b), Def(f(z, x), z+x-a)).free_variables() == set([a, b])
        assert Where(f(b), Def(f(z, x), z+x-a+f)).free_variables() == set([a, b, f])
        assert Where(Sum(a_(i) * b, For(i, 1, n)), Def(Tuple(a_(i), For(i, 1, n)), T)).free_variables() == set([T, b])
        assert Where(a*d-b*c, Def(Matrix2x2(a, b, c, d), M)).free_variables() == set([M])

    def test_replace(self):
        assert (x+y+1).replace({x:z}) == (z+y+1)
        assert (x+y).replace({x:y, y:x}) == y+x
        assert Where(y, Def(y, 3)).replace({y:5}) == Where(5, Def(5, 3))
        assert Where(y, Def(y, 3)).replace({y:5}, semantic=True) == Where(y, Def(y, 3))
        assert Where(y, Def(y, y)).replace({y:5}, semantic=True) == Where(y, Def(y, 5))
        assert Where(x, Def(x, y), Def(y, x)).replace({x:5, y:3}, semantic=True) == Where(x, Def(x, 3), Def(y, x))
        assert Where(x+z, Def(x, y), Def(y, x)).replace({x:5, y:3, z:2}, semantic=True) == Where(x+2, Def(x, 3), Def(y, x))
        assert Where(a+b, Def(Tuple(a, b, c), T(a))).replace({a:2, T:S, b:8}, semantic=True) == Where(a+b, Def(Tuple(a, b, c), S(2)))
        assert Where(Sum(a_(i) * b, For(i, 1, n)), Def(Tuple(a_(i), For(i, 1, n)), T)).replace({a_:f, i:7, b:5, n:8, T:S}, semantic=True) == \
                Where(Sum(a_(i) * 5, For(i, 1, n)), Def(Tuple(a_(i), For(i, 1, n)), S))
        assert Where(f(b), Def(f(z), z+a)).replace({f:g}, semantic=True) == Where(f(b), Def(f(z), z+a))
        assert Where(f(b), Def(f(z), z+a)).replace({f:g, z:w}, semantic=True) == Where(f(b), Def(f(z), z+a))
        assert Where(f(b), Def(f(z), z+a), Def(b, f(a))).replace({f:g, z:w}, semantic=True) == Where(f(b), Def(f(z), z+a), Def(b, f(a)))
        assert Where(f(b), Def(f(z), z+a)).replace({f:g, z:w, a:b, b:a}, semantic=True) == Where(f(a), Def(f(z), z+b))
        assert Where(a*d-b*c+e, Def(Matrix2x2(a, b, c, d), M)).replace({a:2, M:S, e:7}, semantic=True) == Where(a*d-b*c+7, Def(Matrix2x2(a, b, c, d), S))
        assert Sum(f(n), For(n, a, b)).replace({a:1,b:10}, semantic=True) == Sum(f(n), For(n, 1, 10))
        assert Sum(f(n), For(n, a, b)).replace({a:1,b:10,f:g}, semantic=True) == Sum(g(n), For(n, 1, 10))
        assert Sum(f(n), For(n, a, b)).replace({a:1,b:10,f:g,n:m}, semantic=True) == Sum(g(n), For(n, 1, 10))
        assert Sum(f(n), For(n, a, b), Q(n,a)).replace({a:1,b:10,f:g,n:m,Q:R}, semantic=True) == Sum(g(n), For(n, 1, 10), R(n,1))
        assert Set(x+y, ForElement(x, S)).replace({x:y}, semantic=True) == Set(x+y, ForElement(x, S))
        assert Set(x+y, ForElement(x, S), P(x)).replace({x:y}, semantic=True) == Set(x+y, ForElement(x, S), P(x))
        assert Set(x+y, ForElement(x, S), P(x)).replace({x:y, S:x, P:Q, y:5}, semantic=True) == Set(x+5, ForElement(x, x), Q(x))

