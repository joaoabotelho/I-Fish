from threading import Thread

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        thread.join()
        return thread
    return wrapper

def abc():
    a = input()
    print(a)

t1 = Thread(target=abc)
t1.start()
t1.join()
