#-*- coding:UTF-8 -*-
'''
Created on 2017年12月1日

@author: why
'''
__metaclass__  = type
class Bird:
    def __init__(self):
        self.hungry = True
    def eat(self):
        if self.hungry:
            print 'Aaaah...'
            self.hungry = False
        else:
            print 'No,thanks!'

class SongBird(Bird):
    def __init__(self):
        super(SongBird, self).__init__()
        self.sound='Squawk!'
    def sing(self):
        print self.sound
        
b = Bird()
b.eat()
b.eat()
b.eat()
sb = SongBird()
sb.sing()
sb.sing()
try:
    sb.eat()
except(AttributeError),e:
    print e 
sb.eat()




