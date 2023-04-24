from pdb import post_mortem
from flask import Flask, render_template, request
from html import entities
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
import six
import sys



sys.modules['sklearn.externals.six'] = six
os.chdir(os.path.dirname(os.path.abspath(__file__)))


app = Flask(__name__, template_folder='templates')


#-------------------------------------------------------------------


#verisetinin okunmasi
data = pd.read_csv('.\\student-mat.csv')

#Final notunun harf notuna donusturulmesi
data['G3H'] = (data['G3'])

def define_G3H(df):

    G3H = []

    for row in df['G3H']:

        if row >= (0.9 * df['G3H'].max()):
            G3H.append('A')

        elif row >= (0.8 * df['G3H'].max()):
            G3H.append('B')

        elif row >= (0.7 * df['G3H'].max()):
            G3H.append('C')  

        elif row >= (0.6 * df['G3H'].max()):
            G3H.append('D')

        elif row >= (0.5 * df['G3H'].max()):
            G3H.append('E') 

        elif row < (0.5 * df['G3H'].max()):
            G3H.append('F')  
                     
    print(type(G3H))
    df['G3H'] = G3H
    return df

data = define_G3H(data)

##------------


data['G1H'] = (data['G1'])

def define_G1H(df):

    G1H = []

    for row in df['G1']:

        if row >= (0.9 * df['G1H'].max()):
            G1H.append('A')

        elif row >= (0.8 * df['G1H'].max()):
            G1H.append('B')

        elif row >= (0.7 * df['G1H'].max()):
            G1H.append('C')  

        elif row >= (0.6 * df['G1H'].max()):
            G1H.append('D')

        elif row >= (0.5 * df['G1H'].max()):
            G1H.append('E') 

        elif row < (0.5 * df['G1H'].max()):
            G1H.append('F')  
                     
    print(type(G1H))
    df['G1H'] = G1H
    return df

data = define_G1H(data)

##------------
#gereksiz buldugum datalarin cikartilmasi
data.drop(["school","age","famsize","Pstatus","reason","traveltime","failures","activities","higher","romantic","famrel","freetime","goout","Dalc","Walc","health","absences"], axis=1, inplace=True)


#1 ve 0 a donusturulmesi
d = {'yes': 1, 'no': 0}
data['schoolsup'] = data['schoolsup'].map(d)
data['famsup'] = data['famsup'].map(d)
data['paid'] = data['paid'].map(d)
data['nursery'] = data['nursery'].map(d)
data['internet'] = data['internet'].map(d)


d = {'F': 1, 'M': 0}
data['sex'] = data['sex'].map(d)

d = {'U': 1, 'R': 0}
data['address'] = data['address'].map(d)

d = {'teacher': 0, 'health': 1, 'services': 2,'at_home': 3,'other': 4}
data['Mjob'] = data['Mjob'].map(d)
data['Fjob'] = data['Fjob'].map(d)

d = {'mother': 0, 'father': 1, 'other': 2}
data['guardian'] = data['guardian'].map(d)

d = {'F': 0,'E': 1,'D': 2,'C': 3, 'B': 4, 'A': 5}
data['G3H'] = data['G3H'].map(d)

d = {'F': 0,'E': 1,'D': 2,'C': 3, 'B': 4, 'A': 5}
data['G1H'] = data['G1H'].map(d)



student_features = data.columns.tolist()
#student_features.remove('grades') 
#student_features.remove('G3H')
student_features.remove('G3H')
student_features.remove('G2')
student_features.remove('G1H')
student_features.remove('G3') 
#student_features.remove('G2') #-----iptal olan g2 notu-----

print('-------')
print(student_features)
print('-------')

##

X = data[student_features].copy()
X.columns


y=data[['G3H']].copy()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=42)


grade_classifier = tree.DecisionTreeClassifier(max_leaf_nodes=len(X.columns), random_state=0)
grade_classifier.fit(X_train, y_train)


##------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html',toplam="|")

    
@app.route('/hesapla')
def hesapla():
    return render_template('hesapla.html',toplam="|")

@app.route('/send',methods=['POST'])
def send():
    
    if request.method =='POST':

        cinsiyet = request.form.to_dict()['cinsiyet']
        bolge = request.form.to_dict()['bolge']
        medu = request.form.to_dict()['medu']
        fedu = request.form.to_dict()['fedu']
        mjob = request.form.to_dict()['mjob']
        fjob = request.form.to_dict()['fjob']
        veli = request.form.to_dict()['veli']
        stime = request.form.to_dict()['stime']
        ssup = request.form.to_dict()['ssup']
        fsup = request.form.to_dict()['fsup']
        paid = request.form.to_dict()['paid']
        nursery = request.form.to_dict()['nursery']
        internet = request.form.to_dict()['internet']

        g1 = request.form.to_dict()['g1']

        
        if g1=='':
           return render_template('/hesapla.html',toplam="Not Girmediniz")

        if int(g1)>100:
            return render_template('/hesapla.html',toplam="0-100 arasinda bir not giriniz")
        else:    
            print(g1)

            if int(g1)>=90 and int(g1)<=100:
                g1 = int(g1)/5
            elif int(g1)>=80 and int(g1)<90:
                g1 = int(g1)/5
            elif int(g1)>=70 and int(g1)<80:
                g1 = int(g1)/5
            elif int(g1)>=60 and int(g1)<70:
                g1 = int(g1)/5
            elif int(g1)>=50 and int(g1)<60:
                g1 = int(g1)/5
            elif int(g1)<50:
                g1 = int(g1)/5

            g1=int(g1)
            print(g1)
            print("\n*****************\n")

            print(cinsiyet)
            print(bolge)
            print(medu)
            print(fedu)
            print(mjob)
            print(fjob)
            print(veli)
            print(stime)
            print(ssup)
            print(fsup)
            print(paid)
            print(nursery)
            print(internet)
            print(g1)

            print("\n*****************\n")


            d = {'sex': [cinsiyet], # 0 - kadin / 1 - erkek
            'address': [bolge], # 0 - kirsal / 1 - kentsel
            'Medu':[medu],     # 0 - yok / 1 - ilkogretim / 2 - 5-9.sinif / 3 - lise / 4 - lisans   
            'Fedu':[fedu],     # 0 - yok / 1 - ilkogretim / 2 - 5-9.sinif / 3 - lise / 4 - lisans 
            'Mjob':[mjob],     # 0 - ogretmen / 1 - saglik / 2 - hizmet / 3 - evde / 4 - diger
            'Fjob':[fjob],     # 0 - ogretmen / 1 - saglik / 2 - hizmet / 3 - evde / 4 - diger
            'guardian':[veli], # 0 - anne / 1 - baba / 3 - diger
            'studytime':[stime],# 1 - 2 saatten az / 2 - 2-5 saat / 3 - 5-10 saat / 4 - 10 saatten fazla
            "schoolsup":[ssup],# 0 - hayir / 1 - evet (ekstra egitim destegi)
            "famsup":[fsup],   # 0 - hayir / 1 - evet (aile egitim destegi)
            "paid":[paid],     # 0 - hayir / 1 - evet (ekstra ucretli ders)
            "nursery":[nursery],  # 0 - hayir / 1 - evet (anaokuluna gitti mi)
            "internet":[internet], # 0 - hayir / 1 - evet (internet erisimi var mi)
            "G1":[g1]       # 20 uzerinden notu
            #"G2":[16]      # 20 uzerinden notu IPTAL
            }      
            print (d)
            df = pd.DataFrame(data=d)

            predictions = grade_classifier.predict(df)

            print('\n****************************\n')

            if predictions[0]==0:
                print("Ogrenci notu : F")# 50 den az
                predictions = 'F  50 den az'
            elif predictions[0]==1:
                print("Ogrenci notu : E")# 50 - 60 arasi
                predictions = 'E   50 - 60 arasi'
            elif predictions[0]==2:
                print("Ogrenci notu : D")# 60 - 70 arasi
                predictions = 'D   60 - 70 arasi'
            elif predictions[0]==3:
                print("Ogrenci notu : C")# 70 - 80 arasi
                predictions = 'C   70 - 80 arasi'
            elif predictions[0]==4:
                print("Ogrenci notu : B")# 80 - 90 arasi
                predictions = 'B   80 - 90 arasi'
            elif predictions[0]==5:
                print("Ogrenci notu : A")# 90 - 100 arasi
                predictions = 'A   90 - 100 arasi'

            print('\n****************************\n')

    return render_template('/hesapla.html',toplam=predictions,)  



##------------------------------------------------------------------------------------------------




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


