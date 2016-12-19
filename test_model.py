from model import *
import sys
from io import StringIO
import pytest


F = Function
FD = FunctionDefinition
FC = FunctionCall
BO = BinaryOperation
R = Reference
C = Conditional
N = Number
UO = UnaryOperation
P = Print


def is_same(number, expected_value, monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    Print(number).evaluate(scope)
    return sys.stdout.getvalue() == str(expected_value) + "\n"


class TestScope:
    def test_scope_simple(self):
        parent = Scope()
        numb1 = Number(10)
        parent["a"] = numb1
        assert parent["a"] is numb1
        numb2 = Number(-2)
        parent["b"] = numb2
        assert parent["b"] is numb2

    def test_scope_take_from_parent(self):
        parent = Scope()
        scope = Scope(parent)
        numb = Number(10)
        parent["a"] = numb
        assert scope["a"] is numb

    def test_scope_have_func(self):
        parent = Scope()
        numb = Function([], [])
        parent["f"] = numb
        assert parent["f"] is numb


class TestNumber:

    def test_number(self):
        scope = Scope()
        n = Number(43)
        assert n.evaluate(scope) is n 


class TestPrint:

    def test_print_number(self, monkeypatch):
        n = Number(43)
        assert is_same(n, 43, monkeypatch)
    
    def test_print_evaluate(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        res = Print(BO(N(30), "+", N(13))).evaluate(scope)
        assert is_same(res, 43, monkeypatch)
        assert sys.stdout.getvalue() == "43\n"

class TestRead:
    def test_read(self, monkeypatch):
        monkeypatch.setattr(sys, "stdin", StringIO('43\n'))
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        read_res = Read('a').evaluate(scope)
        Print(R('a')).evaluate(scope)
        assert sys.stdout.getvalue() == "43\n"
        assert is_same(read_res, 43, monkeypatch)


class TestUnaryOperation:

    def test_unaryoperation_not(self, monkeypatch):
        scope = Scope()
        n = Number(1)
        not_n = UnaryOperation('!', n).evaluate(scope)
        assert is_same(not_n, 0, monkeypatch)

    def test_unaryoperation_minus(self, monkeypatch):
        scope = Scope()
        n = Number(43)
        minus_n = UnaryOperation('-',n).evaluate(scope)
        assert is_same(minus_n, -43, monkeypatch)

    def test_unaryoperation_evaluate(self, monkeypatch):
        scope = Scope()
        n = Number(0)
        ev = UnaryOperation('-', UnaryOperation('!', n))
        assert is_same(ev, -1, monkeypatch)


class TestBinaryOperation:

    def test_binaryoperation(self, monkeypatch):
        scope = Scope()
        a = Number(43)
        b = Number(10)
        summ = BinaryOperation(a, '+', b)
        assert is_same(summ, 53, monkeypatch)
        con = BinaryOperation(a, '&&', Number(0))
        assert is_same(con, 0, monkeypatch)

    def test_unaryoperation_evaluate(self, monkeypatch):
        scope = Scope()
        a = Number(43)
        b = Number(10)
        summ = BinaryOperation(a, '-', b)
        eq = BinaryOperation(summ, '==', Number(33))
        assert is_same(eq, 1, monkeypatch)


class TestFunction:

    def test_function_empty_arguments(self, monkeypatch):
        scope = Scope()
        func = Function([], [BO(Number(10), '+', Number(33))])
        res = func.evaluate(scope)
        assert is_same(res, 43, monkeypatch)

    def test_function_many_arguments(self, monkeypatch):
        scope = Scope()
        scope["a"] = Number(33)
        scope["b"] = Number(10)
        func = Function(("a","b"),[BO(Reference("a"), '+', Reference("b"))])
        res = func.evaluate(scope)
        assert is_same(res, 43, monkeypatch)

    def test_function_big_body(self, monkeypatch):
        monkeypatch.setattr(sys,"stdout", StringIO())
        scope = Scope()
        scope["a"] = Number(33)
        scope["b"] = Number(10)
        func = F(("a", "b"), [P(R("a")),
                              BO(R("a"), '-', R("b")),
                              BO(R("a"), '+', R("b"))])
        res = func.evaluate(scope)
        P(res).evaluate(scope)
        assert sys.stdout.getvalue() == '33\n43\n'

    def test_function_empty_body(self, monkeypatch):
        scope = Scope()
        F(('a'), []).evaluate(scope)
        

class TestFunctionDefiniction:

    def test_function_definition_simple(self):
        scope = Scope()
        func = Function([],[BO(Number(10), '+', Number(33))])
        func2 = FD("func", func).evaluate(scope)
        assert scope["func"] is func
        assert func2 is func


class TestReference:

    def test_reference_number(self, monkeypatch):
        scope = Scope()
        a = Number(43)
        scope["a"] = a
        a2 = Reference("a").evaluate(scope)
        assert a is a2

    def test_reference_function(self, monkeypatch):
        scope = Scope()
        func = Function([], [])
        scope["function"] = func
        func2 = Reference("function").evaluate(scope)
        assert func is func2


class TestConditional:
    def test_conditional_empty(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        C(BO(BO(N(3), '%', N(3)), '==', N(0)), [], [Print(N(1))]).evaluate(scope)
        C(BO(BO(N(3), '%', N(4)), '==', N(0)), [], [Print(N(1))]).evaluate(scope)
        assert sys.stdout.getvalue() == '1\n'

    def test_conditional_simple(self, monkeypatch):
        monkeypatch.setattr(sys,"stdout", StringIO())
        scope = Scope()
        C(BO(N(3), '==', N(3)), [P(N(1))], [Print(N(0))]).evaluate(scope)
        C(BO(N(2), '==', N(3)), [P(N(1))], [Print(N(0))]).evaluate(scope)
        assert sys.stdout.getvalue() == '1\n0\n'

    def test_conditional_return(self, monkeypatch):
        monkeypatch.setattr(sys,"stdout", StringIO())
        scope = Scope()
        res1 = C(BO(N(3), '==', N(3)), [N(1)], [N(0)]).evaluate(scope)
        res2 = C(BO(N(2), '==', N(3)), [N(1)], [N(0)]).evaluate(scope)
        assert is_same(res1, 1, monkeypatch)
        assert is_same(res2, 0, monkeypatch)

    def test_conditional_empty2(self, monkeypatch):
        monkeypatch.setattr(sys,"stdout", StringIO())
        scope = Scope()
        C(BO(N(3), '==', N(3)), [P(N(1))], []).evaluate(scope)
        C(BO(N(2), '==', N(3)), [P(N(2))], []).evaluate(scope)
        C(BO(N(3), '==', N(3)), [], []).evaluate(scope)
        C(BO(N(2), '==', N(3)), [], []).evaluate(scope)
        C(BO(N(3), '==', N(3)), [], [P(N(3))]).evaluate(scope)
        C(BO(N(2), '==', N(3)), [], [P(N(4))]).evaluate(scope)
        assert sys.stdout.getvalue() == '1\n4\n'

    def test_conditional_big_body(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        res1 = C(BO(N(3), '==', N(3)),
          [P(N(1)), P(N(2))],
          [P(N(3)), P(N(4))]).evaluate(scope)
        #assert is_same(res1, 2, monkeypatch)
        res2 = C(BO(N(2), '==', N(3)),
          [P(N(1)), P(N(2))],
          [P(N(3)), P(N(4))]).evaluate(scope)
        #assert is_same(res2, 4, monkeypatch)
        assert sys.stdout.getvalue() == '1\n2\n3\n4\n'


class TestFunctionCall:

    def test_FunctionCall_with_simple(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        parent = Scope()
        FD('max',
           F(('a', 'b'),
             [Conditional(BO(R('a'), '>=', R('b')),
              [R('a')],
              [R('b')])])).evaluate(parent)
        n = FC(R('max'),
               [Number(6), Number(5)]).evaluate(parent)
        assert is_same(n, 6, monkeypatch)

    def test_FunctionCall_very_tricky(self, monkeypatch):
        parent = Scope()
        FD('strange_max',
           F(('a', 'b'),
             [C(BO(R('a'), '<=', R('b')),
                [R('b')], [FC(R('strange_max'),
                              [R('b'), R('a')])])])).evaluate(parent)
        n = FC(R('strange_max'),
               [Number(6), Number(5)]).evaluate(parent)
        assert is_same(n, 6, monkeypatch)


class TestIntegration:

    def test_factorial(self , monkeypatch):
        parent = Scope()
        FD('factorial',
           F(('a'),
             [C(BO(R('a'), '<=', Number(1)),
                [R('a')],
                [BO(FC(R('factorial'),
                       [BO(R('a'), '-', N(1))]),
                    '*', R('a'))])])).evaluate(parent)
        n = FC(R('factorial'),
               [Number(5)]).evaluate(parent)
        assert is_same(n, 120, monkeypatch)

    def test_fibonacci(self, monkeypatch):
        parent = Scope()
        FD('fib',
           F(('a'),
             [C(BO(R('a'), '<=', N(1)),
                [R('a')],
                [BO(FC(R('fib'),
                       [BO(R('a'), '-', N(1))]),
                    '+', FC(R('fib'),
                            [BO(R('a'), '-', N(2))]))])])).evaluate(parent)
        n = FC(R('fib'),
               [Number(8)]).evaluate(parent)
        assert is_same(n, 21, monkeypatch)

    def test_average(self, monkeypatch):
        parent = Scope()
        FD('average',
           F(('a', 'b'),
             [BO(BO(R('a'), '+', R('b')),
                 '/', N(2))])).evaluate(parent)
        n = FC(R('average'),
               [Number(4), Number(6)]).evaluate(parent)
        assert is_same(n, 5, monkeypatch)
