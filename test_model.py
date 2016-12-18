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


class TestScope:
    def test_scope_simple(self):
        parent = Scope()
        temp = Number(10)
        parent["a"] = temp
        assert parent["a"] is temp
        temp2 = Number(-2)
        parent["b"] = temp2
        assert parent["b"] is temp2

    def test_scope_take_from_parent(self):
        parent = Scope()
        scope = Scope(parent)
        temp = Number(10)
        parent["a"] = temp
        assert scope["a"] is temp

    def test_scope_have_func(self):
        parent = Scope()
        temp = Function([], [])
        parent["f"] = temp
        assert parent["f"] is temp


class TestNumber:

    def test_number(self):
        scope = Scope()
        n = Number(43)
        assert n.evaluate(scope) is n


class TestPrint:

    def test_print_number(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        Print(Number(43)).evaluate(scope)
        assert sys.stdout.getvalue() == "43\n"


class TestRead:
    def test_read(self, monkeypatch):
        monkeypatch.setattr(sys, "stdin", StringIO('43\n'))
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        r = Read('a').evaluate(scope)
        Print(R('a')).evaluate(scope)
        assert sys.stdout.getvalue() == "43\n"


class TestUnaryOperation:

    def test_unaryoperation_not(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        n = Number(1)
        not_n = UnaryOperation('!', n).evaluate(scope)
        Print(not_n).evaluate(scope)
        assert sys.stdout.getvalue() == '0\n'

    def test_unaryoperation_minus(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        n = Number(43)
        not_n = UnaryOperation('-', n).evaluate(scope)
        Print(not_n).evaluate(scope)
        assert sys.stdout.getvalue() == '-43\n'

    def test_unaryoperation_evaluate(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        n = Number(0)
        ev = UnaryOperation('-', UnaryOperation('!', n))
        Print(ev).evaluate(scope)
        assert sys.stdout.getvalue() == '-1\n'


class TestBinaryOperation:

    def test_binaryoperation(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        a = Number(43)
        b = Number(10)
        summ = BinaryOperation(a, '+', b)
        Print(summ).evaluate(scope)
        con = BinaryOperation(a, '&&', Number(0))
        Print(con).evaluate(scope)
        assert sys.stdout.getvalue() == '53\n0\n'

    def test_unaryoperation_evaluate(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        a = Number(43)
        b = Number(10)
        summ = BinaryOperation(a, '-', b)
        eq = BinaryOperation(summ, '==', Number(33))
        Print(eq).evaluate(scope)
        assert sys.stdout.getvalue() == '1\n'


class TestFunction:

    def test_function(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        func = Function([], [BO(Number(10), '+', Number(33))])
        res = func.evaluate(scope)
        P(res).evaluate(scope)
        assert sys.stdout.getvalue() == '43\n'

    def test_function_many_arguments(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        scope["a"] = Number(33)
        scope["b"] = Number(10)
        func = Function(("a", "b"), [BO(Reference("a"), '+', Reference("b"))])
        res = func.evaluate(scope)
        P(res).evaluate(scope)
        assert sys.stdout.getvalue() == '43\n'

    def test_function_big_body(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        scope["a"] = Number(33)
        scope["b"] = Number(10)
        func = F(("a", "b"), [P(R("a")),
                              BO(R("a"), '-', R("b")),
                              BO(R("a"), '+', R("b"))])
        res = func.evaluate(scope)
        P(res).evaluate(scope)
        assert sys.stdout.getvalue() == '33\n43\n'

    def test_function_empty(self, monkeypatch):
        scope = Scope()
        F(('a'), []).evaluate(scope)


class TestFunctionDefiniction:

    def test_function_definition_simple(self):
        scope = Scope()
        func = Function([], [BO(Number(10), '+', Number(33))])
        func2 = FD("func", func).evaluate(scope)
        assert scope["func"] is func
        assert func2 is func


class TestReference:

    def test_reference_number(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        a = Number(43)
        scope["a"] = a
        a2 = Reference("a").evaluate(scope)
        assert a is a2

    def test_reference_function(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        f = Function([], [])
        scope["f"] = f
        f2 = Reference("f").evaluate(scope)
        assert f is f2


class TestConditional:
    def test_conditional_empty(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        C(BO(BO(N(3), '%', N(3)),
             '==', N(0)), [], [Print(N(1))]).evaluate(scope)
        C(BO(BO(N(3), '%', N(4)),
             '==', N(0)), [], [Print(N(1))]).evaluate(scope)
        assert sys.stdout.getvalue() == '1\n'

    def test_conditional_simple(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        scope = Scope()
        C(BO(N(3), '==', N(3)), [P(N(1))], [Print(N(0))]).evaluate(scope)
        C(BO(N(2), '==', N(3)), [P(N(1))], [Print(N(0))]).evaluate(scope)
        assert sys.stdout.getvalue() == '1\n0\n'

    def test_conditional_empty2(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
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
        C(BO(N(3), '==', N(3)),
          [P(N(1)), P(N(2))],
          [P(N(3)), P(N(4))]).evaluate(scope)
        C(BO(N(2), '==', N(3)),
          [P(N(1)), P(N(2))],
          [P(N(3)), P(N(4))]).evaluate(scope)
        assert sys.stdout.getvalue() == '1\n2\n3\n4\n'


class TestFunctionCall:

    def test_FunctionCall_simple(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        parent = Scope()
        FD('average',
           F(('a', 'b'),
             [BO(BO(R('a'), '+', R('b')),
                 '/', N(2))])).evaluate(parent)
        P(FC(R('average'),
             [Number(4), Number(6)])).evaluate(parent)
        assert sys.stdout.getvalue() == '5\n'

    def test_FunctionCall_with_conditional(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        parent = Scope()
        FD('max',
           F(('a', 'b'),
             [Conditional(BO(R('a'), '>=', R('b')),
              [R('a')],
              [R('b')])])).evaluate(parent)
        P(FC(R('max'),
             [Number(6), Number(5)])).evaluate(parent)
        assert sys.stdout.getvalue() == '6\n'

    def test_FunctionCall_with_recursion(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        parent = Scope()
        FD('factorial',
           F(('a'),
             [C(BO(R('a'), '<=', Number(1)),
                [R('a')],
                [BO(FC(R('factorial'),
                       [BO(R('a'), '-', N(1))]),
                    '*', R('a'))])])).evaluate(parent)
        P(FC(R('factorial'),
             [Number(5)])).evaluate(parent)
        assert sys.stdout.getvalue() == '120\n'

    def test_FunctionCall_with_recursion2(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        parent = Scope()
        FD('fib',
           F(('a'),
             [C(BO(R('a'), '<=', N(1)),
                [R('a')],
                [BO(FC(R('fib'),
                       [BO(R('a'), '-', N(1))]),
                    '+', FC(R('fib'),
                            [BO(R('a'), '-', N(2))]))])])).evaluate(parent)
        P(FC(R('fib'),
             [Number(8)])).evaluate(parent)
        assert sys.stdout.getvalue() == '21\n'

    def test_FunctionCall_very_tricky(self, monkeypatch):
        monkeypatch.setattr(sys, "stdout", StringIO())
        parent = Scope()
        FD('strange_max',
           F(('a', 'b'),
             [C(BO(R('a'), '<=', R('b')),
                [R('b')], [FC(R('strange_max'),
                              [R('b'), R('a')])])])).evaluate(parent)
        P(FC(R('strange_max'),
             [Number(6), Number(5)])).evaluate(parent)
        assert sys.stdout.getvalue() == '6\n'
