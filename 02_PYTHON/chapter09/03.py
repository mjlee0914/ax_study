import sys

args = sys.argv[1:] # sys.argv = ["test.py", "10", "20", "30"]
print(int(args[0]) + int(args[1])) # powershell에 un run 03.py 100 200 입력하고 실행하면 ['03.py', '100', '200'] 출력, 기본 문자열로 출력되므로 int로 변경


