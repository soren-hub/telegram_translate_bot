
from collections.abc import Sequence
from collections import defaultdict
from collections import OrderedDict
import json


        
class Text(Sequence):

    def __init__(self, text:str, idiom="en"):
        self.text = text
        self._words = self.separete_words(fix_format=True)
        self._idiom = idiom 
        
    def __len__(self):
        return len(self._words)

    def __getitem__(self, item:int):
        return self._words.__getitem__(item)
    
    def __str__(self):
        return str(self.text)
    
    def __call__(self,other_text):
        new_words = other_text.separete_words(fix_format=True)
        self._words.extend(new_words)
        
    @property
    def idiom(self):
        return self._idiom 
    
    @idiom.setter
    def idiom(self, new_idiom:str): 
        self._idiom = new_idiom
    
        
    def repetitions(self) -> dict:
        records =  defaultdict(int)
        for word in self._words: 
            records[word] += 1
        return dict(records)


    def sort_words(self,reverse=False) -> dict:      
        sorted_dict = OrderedDict(sorted(self.repetitions().items(),
                                         key=lambda x: x[1],
                                         reverse=reverse))
        return dict(sorted_dict)
    
    def separete_words(self,fix_format=False) -> list:
        words = self.text.split(" ")
        all_words = [exception for word in words for exception in word.split()]
        if fix_format: 
            return self._fix_format_words()
        return all_words
    
    def _fix_format_words(self) -> list:
        map_chars = {
                    ord("?"): "", 
                    ord(":"): "", 
                    ord(","): "",
                    ord("."): "",
                    ord(")"): "",
                    ord("("): ""
                }
        words = self.separete_words()
        fixed_words = [word.translate(map_chars).lower() for word in words ]
        return fixed_words
    

class OpenEnglishText: 
    
    def __init__(self,filename:str,format:str, mode:str): 
        self.filename = filename
        self.format = format
        self.mode = mode
    
    def __enter__(self):
        self.file = open(f"{self.filename}.{self.format}",self.mode)
        return self.file
        
    def save_jason(self): 
        file = self.__enter__().read()
        text = Text(file)
        histogram_ordered = text.sort_words(reverse=True)
        with open(f"{self.filename}_histogram.jason","w") as histogram:
            json.dump(histogram_ordered,histogram)
         
     
    def __exit__(self, exc_type,exc_val,traceback): 
        self.save_jason()
        self.file.close()
        
        
def main():
    #os.system("cd ./Desktop/pytonic/ ")

    example_text=r"""If you create a class that directly extends dict, for example, you will obtain results
                    that are probably not what you are expecting. The reason for this is that in CPython
                    (a C optimization), the methods of the class don't call each other (as they should),
                    so if you override one of them, this will not be reflected by the rest, resulting in
                    unexpected outcomes. For example, you might want to override __getitem__, and
                    then when you iterate the object with a for loop, you will notice that the logic you
                    have put on that method is not applied.
                    """
    other_text = Text(example_text)
    
    
    with OpenEnglishText("example","txt","r") as file: 
        read_text = file.read()
        text = Text(read_text)
        #print(text)
        #print(text.sort_words(reverse=True))
        print(len(text))
        text(other_text)
        #print(text.words)
        print(len(text))
        
       
if __name__ == "__main__": 
    main() 


