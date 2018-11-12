from test3 import *

if __name__ == "__main__":
	srv = MyServer('localhost', 5554)
	srv.run()

	print('end')
	input()