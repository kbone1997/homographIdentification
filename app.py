from flask import Flask,render_template,url_for
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast,AutoTokenizer, AutoModel
from jax import lib
import jyserver.Flask as jsf
import nltk
from nltk.corpus import wordnet
import re
import pandas as PD

#loading xlcs file
df = PD.read_excel("Bengali-Homograph-dataset.xlsx")

model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
bnbert_tokenizer = AutoTokenizer.from_pretrained("sagorsarker/bangla-bert-base")

article_bn = "আমি কাল বাসায় যাবো"
article_hi = "मैं तुम्हें जानता हूं"  #hindi
article_np = "म तिमीलाई चिन्छु" #nepali
article_mr = "मी तुला ओळखतो" #marathi
article_ta = "எனக்கு உன்னை தெரியும்" #tamil
article_te = "మీరు నాకు తెలుసు" #telegu
article_ur = "میں آپکو جانتا ہوں"

app = Flask(__name__)
result = []

@jsf.use(app)
class App:
    def __init__(self):
        print("nothing")
    def translateLan(self):
        print("inside translate")
        sourceLanguage = str(self.js.document.querySelector('#language').value)
        targetLanguage = str(self.js.document.querySelector('#TLanguage').value)
        print(sourceLanguage, targetLanguage)
        tokenizer.src_lang = sourceLanguage
        article_bn = str(self.js.document.getElementById('input').value)
        print(type(article_bn))
        encoded_ar = tokenizer(article_bn, return_tensors="pt")
        generated_tokens = model.generate(**encoded_ar, forced_bos_token_id=tokenizer.lang_code_to_id[targetLanguage])
        translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        print(type(translation))
        self.js.document.getElementById('output').value = translation
        line = str(translation)
        fileWrite = open('history.txt','a',encoding='utf-8')
        lineToBackUpBangla = article_bn
        fileWrite.write(lineToBackUpBangla)
        fileWrite.write("-------------->")
        fileWrite.write(line)
        fileWrite.write("\n")
        fileWrite.close()
        print("printing without respliting it")
        print(line)
        line = line.replace("[","").replace("]","").replace("\"","").replace(".","").replace("?","").replace(",","").replace("'","")
        wordMeaninglist = []
        synonymslist=[]
        antonymslist=[]
        print("printing after removing problems:")
        line1 = line.split(" ")
        print(line1)
        for x in line1:
            #print(x)
            testSy = x
            mean=wordnet.synsets(x)
            if len(mean) != 0:
                wordMeaning = []
                #word meaning section
                for x in mean:
                    #print(x.definition())
                    wordMeaning.append(x.definition())
                wordMeaninglist.append(wordMeaning)
            else:
                #print("n/a")
                wordMeaning = []
                wordMeaning.append("n/a")
                wordMeaninglist.append(wordMeaning)

            #synonyms section
            #print("printing x:")
            #print(testSy)
            synonyms=[]
            for syn in wordnet.synsets(testSy):
                for lemma in syn.lemmas():
                    synonyms.append(lemma.name())
            if len(synonyms) != 0:
                synonymslist.append(synonyms)
            else:
                synonymslist.append("n/a")

            #antonyms section
            #print("printing x:")
            #print(testSy)
            antonyms=[]
            for syn in wordnet.synsets(testSy):
                for lemma in syn.lemmas():
                    if lemma.antonyms():
                        antonyms.append(lemma.antonyms()[0].name())
            if len(antonyms) != 0:
                antonymslist.append(antonyms)
            else:
                antonymslist.append("n/a")
        print(wordMeaninglist)
        print(len(wordMeaninglist))
        print(synonymslist)
        print(len(synonymslist))
        print(antonymslist)
        print(len(antonymslist))
        open("temporary.txt", "w").close()
        fileWrite = open('temporary.txt','a')
        counter = 0
        for i in wordMeaninglist:
            fileWrite.write(line1[counter])
            fileWrite.write("-------------->")
            fileWrite.write(str(i))
            fileWrite.write("\n")
            counter+=1
        fileWrite.close()
        open("tempSym.txt", "w").close()
        fileWrite = open('tempSym.txt','a')
        counter = 0
        for i in synonymslist:
            fileWrite.write(line1[counter])
            fileWrite.write("-------------->")
            fileWrite.write(str(i))
            fileWrite.write("\n")
            counter+=1
        fileWrite.close()
        open("tempAnty.txt", "w").close()
        fileWrite = open('tempAnty.txt','a')
        counter = 0
        for i in antonymslist:
            fileWrite.write(line1[counter])
            fileWrite.write("-------------->")
            fileWrite.write(str(i))
            fileWrite.write("\n")
            counter+=1
        fileWrite.close()
        

    #checking for homograph
    def checkHomograph(self):
        homographCounter = 0
        print("inside man!")
        article_bn = self.js.document.getElementById('input').value
        testList = bnbert_tokenizer.tokenize(str(article_bn))
        print(testList)
        print(article_bn)
        words = df['Bengali word']
        print(words)
        for i in testList:
            print(i)
            if i in words.values:
                print("yes")
                homographCounter+=1
            else:
                print('nop')
        if homographCounter == 0:
            self.translateLan()
        else:
            print("before testing article bn")
            for i in testList:
                print(i)
                if i in words.values:
                    data = df.loc[df["Bengali word"] == i]
                    print(data)
                    # find by POS tag
                    # for pos in data["POS tag"]:
                    #     hg_pos = object  # part of speech of hg
                    #     if hg_pos == pos:
                    #         # Homograph tagged meaning is found
                    #         found = True
                    #         result[hg] = data.loc[data["POS tag"] == hg_pos]["English Meaning"].values[0]
                    #         break
                    # find by contextual data
                    print(data["Bangla Meaning"])
                    for context in data["Bangla Meaning"]:
                        # if bengali context meaning is found
                        if context in testList:
                            print(context)
                            result.append(data.loc[data["Bangla Meaning"] == context]["English Meaning"].values[0])
                            break
            print("printing result here")
            print(result)
            self.translateLan()

            

        

@app.route('/')
def index():
    return App.render(render_template('index.html'))

@app.route('/history')
def history():
    with open('history.txt',encoding='utf-8') as f:
        historyLines = f.read().splitlines()
    return App.render(render_template('history.html',len = len(historyLines), historyLines=historyLines))

@app.route('/meanings')
def meanings():
    with open('temporary.txt',encoding='utf-8') as f:
        wordmeanings = f.read().splitlines()
    with open('tempSym.txt',encoding='utf-8') as f:
        synonyms = f.read().splitlines()
    with open('tempAnty.txt',encoding='utf-8') as f:
        antonyms = f.read().splitlines()
    return App.render(render_template('meanings.html',len1 = len(wordmeanings),len2 = len(synonyms),len3 = len(antonyms),len4 = len(result),result=result, wordmeanings=wordmeanings,synonyms=synonyms,antonyms=antonyms))

@app.route('/login')
def login():
    return App.render(render_template('Login.html'))

@app.route('/Signup')
def signup():
    return App.render(render_template('Signup.html'))

if __name__ == "__main__":
    app.run(debug=True)