from src.app import add,subtract,mul,div,welcome

def test_add():
    assert add(2,3)==5
    assert add(0,0)==0
    assert add(-1,1)==0
def test_subtract():
    assert subtract(2,0)==2
    assert subtract(0,2)==-2
    assert subtract(-1,-1)==0
def test_mul():
    assert mul(0,1)==0
    assert mul(-1,2)==-2
    assert mul(3,3)==9
def test_div():
    assert div(2,4)==0.5
    assert div(0,2)==0
    assert div(2,0) == "Error: Division by zero" # This will raise a ZeroDivisionError
def test_welcome():
    assert welcome("Alice") == "Welcome, Alice!"
    assert welcome("Bob") == "Welcome, Bob!"
    assert welcome("Charlie") == "Welcome, Charlie!"
    assert welcome("Mona") == "Welcome, Mona!"
