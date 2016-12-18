from model import *
import sys
from io import StringIO


#scope tests:

F = Function
FD = FunctionDefinition
FC = FunctionCall
BO = BinaryOperation
R = Reference
C = Conditional
N = Number
UO = UnaryOperation
P = Print

def test_scope_simple():
    parent = Scope()
    temp = Number(10)
    parent["a"] = temp
    assert parent["a"] is temp
    temp2 = Number(-2)
    parent["b"] = temp2
    assert parent["b"] is temp2
    

def test_scope_take_from_parent():
    parent = Scope()
    scope = Scope(parent)
    temp = Number(10)
    parent["a"] = temp
    assert scope["a"] is temp

def test_scope_have_func():
    parent = Scope()
    temp = Function([], [])
    parent["f"] = temp
    assert parent["f"] is temp

#Number tests:


def test_number():
    scope = Scope()
    n = Number(43)
    assert n.evaluate(scope) is n 

#Print test:

def test_print_number(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    Print(Number(43)).evaluate(scope)
    assert sys.stdout.getvalue() == "43\n"

#Read test:
def test_read(monkeypatch):
    monkeypatch.setattr(sys, "stdin", StringIO('43\n'))
    monkeypatch.setattr(sys, "stdout", StringIO())
    
    scope = Scope()
    r = Read('a').evaluate(scope)
    Print(R('a')).evaluate(scope)
    assert sys.stdout.getvalue() == "43\n"

#UnaryOperation tests:

def test_unaryoperation_not(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    n = Number(1)
    not_n = UnaryOperation('!', n).evaluate(scope)
    Print(not_n).evaluate(scope)
    assert sys.stdout.getvalue() == '0\n'

def test_unaryoperation_minus(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    n = Number(43)
    not_n = UnaryOperation('-',n).evaluate(scope)
    Print(not_n).evaluate(scope)
    assert sys.stdout.getvalue() == '-43\n'

def test_unaryoperation_evaluate(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    n = Number(0)
    ev = UnaryOperation('-', UnaryOperation('!', n))
    Print(ev).evaluate(scope)
    assert sys.stdout.getvalue() == '-1\n'

#BinaryOperation tests:

def test_binaryoperation(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    a = Number(43)
    b = Number(10)
    summ = BinaryOperation(a, '+', b)
    Print(summ).evaluate(scope)
    con = BinaryOperation(a, '&&', Number(0))
    Print(con).evaluate(scope)
    assert sys.stdout.getvalue() == '53\n0\n'

def test_unaryoperation_evaluate(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    a = Number(43)
    b = Number(10)
    summ = BinaryOperation(a, '-', b)
    eq = BinaryOperation(summ, '==', Number(33))
    Print(eq).evaluate(scope)
    assert sys.stdout.getvalue() == '1\n'

#Function tests:

def test_function(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    func = Function([],[BO(Number(10), '+', Number(33))])
    res = func.evaluate(scope)
    P(res).evaluate(scope)
    assert sys.stdout.getvalue() == '43\n'

def test_function_many_arguments(monkeypatch):
    monkeypatch.setattr(sys,"stdout", StringIO())
    scope = Scope()
    scope["a"] = Number(33)
    scope["b"] = Number(10)
    func = Function(("a","b"),[BO(Reference("a"), '+', Reference("b"))])
    res = func.evaluate(scope)
    P(res).evaluate(scope)
    assert sys.stdout.getvalue() == '43\n'

def test_function_big_body(monkeypatch):
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

def test_function_empty(monkeypatch):
    scope = Scope()
    F(('a'), []).evaluate(scope)

#FunctionDefiniction tests:
def test_function_definition():
    #monkeypatch.setattr(sys,"stdout", StringIO())
    scope = Scope()
    func = Function([],[BO(Number(10), '+', Number(33))])
    func2 = FD("func", func).evaluate(scope)
    assert scope["func"] is func
    assert func2 is func

#Reference tests:

def test_reference_number(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    a = Number(43)
    scope["a"] = a
    a2 = Reference("a").evaluate(scope)
    assert a is a2

def test_reference_function(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    f = Function([], [])
    scope["f"] = f
    f2 = Reference("f").evaluate(scope)
    assert f is f2


#Conditional tests:
def test_conditional_empty(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    C(BO(BO(N(3), '%', N(3)), '==', N(0)), [], [Print(N(1))]).evaluate(scope)
    C(BO(BO(N(3), '%', N(4)), '==', N(0)), [], [Print(N(1))]).evaluate(scope)
    assert sys.stdout.getvalue() == '1\n'

def test_conditional_simple(monkeypatch):
    monkeypatch.setattr(sys,"stdout", StringIO())
    scope = Scope()
    C(BO(N(3), '==', N(3)), [P(N(1))], [Print(N(0))]).evaluate(scope)
    C(BO(N(2), '==', N(3)), [P(N(1))], [Print(N(0))]).evaluate(scope)
    assert sys.stdout.getvalue() == '1\n0\n'

def test_conditional_empty2(monkeypatch):
    monkeypatch.setattr(sys,"stdout", StringIO())
    scope = Scope()
    C(BO(N(3), '==', N(3)), [P(N(1))], []).evaluate(scope)
    C(BO(N(2), '==', N(3)), [P(N(2))], []).evaluate(scope)
    C(BO(N(3), '==', N(3)), [], []).evaluate(scope)
    C(BO(N(2), '==', N(3)), [], []).evaluate(scope)
    C(BO(N(3), '==', N(3)), [], [P(N(3))]).evaluate(scope)
    C(BO(N(2), '==', N(3)), [], [P(N(4))]).evaluate(scope)
    assert sys.stdout.getvalue() == '1\n4\n'

def test_conditional_big_body(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    scope = Scope()
    C(BO(N(3), '==', N(3)),
      [P(N(1)), P(N(2))],
      [P(N(3)), P(N(4))]).evaluate(scope)
    C(BO(N(2), '==', N(3)),
      [P(N(1)), P(N(2))],
      [P(N(3)), P(N(4))]).evaluate(scope)
    assert sys.stdout.getvalue() == '1\n2\n3\n4\n'

#FunctionCall tests:

def test_FunctionCall_simple(monkeypatch):
    monkeypatch.setattr(sys, "stdout", StringIO())
    parent = Scope()
    FD('average',
       F(('a', 'b'),
         [BO(BO(R('a'), '+', R('b')),
             '/', N(2))])).evaluate(parent)
    P(FC(R('average'),
         [Number(4), Number(6)])).evaluate(parent)
    assert sys.stdout.getvalue() == '5\n'

def test_FunctionCall_with_conditional(monkeypatch):
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


def test_FunctionCall_with_recursion(monkeypatch):
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

def test_FunctionCall_with_recursion2(monkeypatch):
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

def test_FunctionCall_very_tricky(monkeypatch):
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

