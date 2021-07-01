from collections.abc import Sequence
from collections import defaultdict
from collections import OrderedDict
import json

class OpenEnglishText: 
    
    def __init__(self,filename,format, mode): 
        self.filename = filename
        self.format = format
        self.mode = mode
    
    def __enter__(self):
        self.file = open(f"{self.filename}.{self.format}",self.mode)
        return self.file
        
    def __exit__(self, exc_type,exc_val,traceback): 
        text = Text(self.file)
        histogram = open(f"{self.filename}_histogram.jason","w") 
        json.dump(text.sort_words(reverse=True),histogram)
        histogram.close() 
        self.file.close()
        
 

class Text(Sequence):

    def __init__(self, text, idiom="en"):
        self.text = text.read()
        self._words = self.separete_words(fix_format=True)
        self._idiom = idiom 
        
    def __len__(self):
        return len(self.words)

    def __getitem__(self, item):
        return self.text.__getitem__(item)
    
    def __str__(self):
        return str(self.text)
    
    def __call__(self,other_text:list):
        new_words=other_text.words
        self.words.extend(list(new_words))
        
    def repetitions(self) -> dict:
        records =  defaultdict(int)
        for word in self.separete_words(): 
            records[word] += 1
        return dict(records)

    @property
    def idiom(self):
        return self._idiom 
    
    @idiom.setter
    def idiom(self, new_idiom): 
        self._idiom = new_idiom

    def sort_words(self,reverse=False) -> dict:      
        
        sorted_dict = OrderedDict(sorted(self.repetitions().items(),
                                         key=lambda x: x[1],
                                         reverse=reverse))
        return sorted_dict
    
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
                    ord("."): ""
                }
        words = self.separete_words()
        fixed_words = [word.translate(map_chars).lower() for word in words ]
        return fixed_words
    



def main():
    with OpenEnglishText("example","txt","r"): 
        pass

       
if __name__ == "__main__": 
    main() 


