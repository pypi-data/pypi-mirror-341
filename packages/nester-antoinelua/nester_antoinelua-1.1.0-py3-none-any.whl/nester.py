"""Python 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
print("hola")
hola
cast = ["Francis", "Malcolm", "Dewey", "Reese", "Jaime"]
print(cast)
['Francis', 'Malcolm', 'Dewey', 'Reese', 'Jaime']
print(len(cast))
5
print(cast[1])
Malcolm
cast.re
Traceback (most recent call last):
  File "<pyshell#5>", line 1, in <module>
    cast.re
AttributeError: 'list' object has no attribute 're'
cast.remove("Jaime")
print(cast)
['Francis', 'Malcolm', 'Dewey', 'Reese']
cast.insert(0, "Antoine")
print(cast)
['Antoine', 'Francis', 'Malcolm', 'Dewey', 'Reese']
movies = ["The Holy Grail", 1975]
movies = ["The Holy Grail", 1975, "The Life of Brian", 1979, "The Meaning of Life", 1983]
print(movies)
['The Holy Grail', 1975, 'The Life of Brian', 1979, 'The Meaning of Life', 1983]
for each_flick in movies:
    print(each_flick)

    
The Holy Grail
1975
The Life of Brian
1979
The Meaning of Life
1983
movies = ["The holy grail", 1975, "Therry Jones", 1991,
                  ["Graham Chapman", ["Michel Palin", "Jhon Cleese",
                        "Therry Gilliam", "Eric Idle", "Terry Jones"]]]
print(movies)
['The holy grail', 1975, 'Therry Jones', 1991, ['Graham Chapman', ['Michel Palin', 'Jhon Cleese', 'Therry Gilliam', 'Eric Idle', 'Terry Jones']]]
for each_item in movies:
    print(each_item)

    
The holy grail
1975
Therry Jones
1991
['Graham Chapman', ['Michel Palin', 'Jhon Cleese', 'Therry Gilliam', 'Eric Idle', 'Terry Jones']]
names = ["Hank", "Javier"]
isinstance(names, list)
True
num_names = len(names)
isinstance(num_names, list)
False
dir(__builtins__)
['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '_', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
for each_item in movies:
    if isinstance(each_item, list):
        for nested_item in each_item:
            print(nested_item)
    else:
        print(each_item)

        
The holy grail
1975
Therry Jones
1991
Graham Chapman
['Michel Palin', 'Jhon Cleese', 'Therry Gilliam', 'Eric Idle', 'Terry Jones']
for each_item in movies:
    if isinstance(each_item, list):
        for nested_item in each_item:
            if isinstance(nested_item, list):
                for another_nested_item in nested_item:
                    print(another_nested_item)
    else:
        print(each_item)

        
The holy grail
1975
Therry Jones
1991
Michel Palin
Jhon Cleese
Therry Gilliam
Eric Idle
Terry Jones
>>> for each_item in movies:
...     if isinstance(each_item, list):
...         for nested_item in each_item:
...             if isinstance(nested_item, list):
...                 for another_nested_item in nested_item:
...                     print(another_nested_item)
...             else:
...                 print(nested_item)
...     else:
...         print(each_item)
... 
...         
The holy grail
1975
Therry Jones
1991
Graham Chapman
Michel Palin
Jhon Cleese
Therry Gilliam
Eric Idle
Terry Jones
>>> 
>>> 
>>> def print_lol(the_list):
...     for each_item in the_list:
...         if isinstance(each_item, list):
...             print_lol(each_item)
...         else:
...             print(each_item)
... 
...             
>>> print_lol(movies)
The holy grail
1975
Therry Jones
1991
Graham Chapman
Michel Palin
Jhon Cleese
Therry Gilliam
Eric Idle
Terry Jones"""

movies = ["The holy grail", 1975, "Therry Jones", 1991,
                  ["Graham Chapman", ["Michel Palin", "Jhon Cleese",
                        "Therry Gilliam", "Eric Idle", "Terry Jones"]]]

def print_lol(the_list, level):
     for each_item in the_list:
        if isinstance(each_item, list):
              print_lol(each_item, level + 1)
        else:
             for i in range(level):
                 print("\t", end="")
             print(each_item, level)
             

print_lol(movies, 0)

