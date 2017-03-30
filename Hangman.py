# HW 4 - Murtaza Meerza

from tkinter import *
from tkinter.messagebox import showinfo

def mask(string,exceptions):
    ans = ''
    for ice in string:
        if ice in exceptions:
            ans+=ice
        else:
            ans+='?'
    return ans
                                        
class hangman(Frame):
    def __init__(self,entword,parent=None):
        Frame.__init__(self,parent)
        
        #Correct and Wrong Keys Collectors
        self.corkeys = ''
        self.wrokeys = ''

        # Screen - Word
        self.word = entword.upper()
        self.ans = Entry(self)
        self.ans.grid(row=0,column=2,columnspan=4)
        Label(self,text='Word:').grid(row=0,column=0,columnspan=2)

        # Masking Word etc
        hword = mask(self.word,'')
        self.ans.insert(END,mask(self.word,''))

        # Screen - Right
        Label(self,text='Right:').grid(row=1,column=0,columnspan=2)
        self.right = Entry(self)
        self.right.grid(row=1,column=2,columnspan=4)
        # Screen - Wrong
        Label(self,text='Wrong:').grid(row=2,column=0,columnspan=2)
        self.wrong = Entry(self)
        self.wrong.grid(row=2,column=2,columnspan=4)
        
        
        # Buttons
        labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(len(labels)):
            # make custom function for each button
            def cmd(key=labels[i]):
                self.click(key)
            b = Button(self,command=cmd,text=labels[i],width=5,height=3)
            # grid it
            b.grid(row=i//6+3,column=i%6)
            
            
    def click(self,key):
        if key in self.word:
            if key not in self.corkeys:
                self.corkeys+= key
                self.right.insert(END,key)
                self.ans.delete(0,END)
                self.ans.insert(END,mask(self.word,self.corkeys))
        elif key not in self.word:
            if key not in self.wrokeys:
                self.wrokeys += key
                self.wrong.insert(END,key)
        if self.ans.get() == self.word:
            messagebox.showinfo('Hangman','You Win!')
        elif len(self.wrong.get()) == 6:
            messagebox.showinfo('Hangman','You Lose!')
                       
if __name__=='__main__':
    import doctest
    print(doctest.testfile('hw4TEST.py'))                

    

        
    
            
            
            
            






        
        
        
