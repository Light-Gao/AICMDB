class Foo:
    def echo(self, *args):
        for arg in args:
            print(arg)
    def show(self, *args):
        print(args)
    def say(self, *args):
        print(*args)

if __name__ == '__main__':
    f = Foo()
    msg = ['my', 'name', 'is', 'Light', ',', 'and', 'you?']
    f.echo(*msg)
    f.show(*msg)
    f.show(msg)
    f.say(*msg)
    f.say(msg)