def hello_world():
    print("Hello, World!")

def test_hello_world(capfd):
    hello_world()
    captured = capfd.readouterr()
    assert captured.out == "Hello, World!\n"