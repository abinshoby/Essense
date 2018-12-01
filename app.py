from flask import Flask
from flask import render_template
from  predict_text_meaning import predict,load_map,load_model,load_data
from flask import *
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import re
from pyvirtualdisplay import Display
from requests import get
from bs4 import BeautifulSoup
from flask_caching import Cache


app = Flask(__name__)

o=""
#@app.route('/')

# def index():
#     return render_template('index.html',pred=predict)
# @app.route('/pred', methods=['POST'])
# def pred():
#     data=request.form['inp'];
#     return predict(data)
def scrap_image(word):
    path = str(os.popen("pwd").read()).strip("\n") + "/geckodriver" #/home/abin/PycharmProjects/Essence/geckodriver
    print('geck',path)
    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Firefox(executable_path=path)  # /usr/local/bin/geckodriver
    word = word.encode('utf-8').decode('utf-8')
    word = word.replace(" ", "+")
    driver.get(
        "https://www.google.com/search?safe=active&tbm=isch&source=hp&biw=1366&bih=638&ei=LHLZW5_pIMye9QOAz6_YCg&q="+word+"&oq=special+&gs_l=img.1.0.35i39k1j0l9.1980.4399.0.5731.9.9.0.0.0.0.181.1041.0j7.7.0....0...1ac.1.64.img..2.7.1038.0...0.vIIm7tH2ToI"
       )
    try:
        html = driver.find_element_by_tag_name("html").get_attribute("innerHTML")
        driver.close()
        display.stop()

        return html

        # org = []
        # for w in l:
        #     org.append(w.replace('\u200c', '').replace('\u200d', ''))

        # return org
    except  WebDriverException  as e:
        driver.close()
        display.stop()
        return -1

def scrap_search(word):
    path = str(os.popen("pwd").read()).strip("\n") + "/geckodriver"
    print('geck', path)
    display = Display(visible=0, size=(800, 600))
    display.start()
    #driver=None
    driver = webdriver.Firefox(executable_path=path)  # /usr/local/bin/geckodriver
    #driver=webdriver.Chrome(executable_path=path)
    word = word.encode('utf-8').decode('utf-8')
    word=word.replace(" ","+")
    driver.get( "https://www.google.co.in/search?q="+word+"&oq="+word+"&aqs=chrome.0.69i59.8573j1j8&sourceid=chrome&ie=UTF-8")
    try:
        print('result found')
        html = driver.find_element_by_tag_name("html").get_attribute("innerHTML")
        driver.close()
        display.stop()
        print('result found')
        return html

        # org = []
        # for w in l:
        #     org.append(w.replace('\u200c', '').replace('\u200d', ''))

        # return org
    except  WebDriverException  as e:
        driver.close()
        display.stop()
        print('error no result')
        return -1
# def scrap_by_bs(word):
#     url = "https://www.google.co.in/search?q="+word+"&oq="+word+"&aqs=chrome.0.69i59.8573j1j8&sourceid=chrome&ie=UTF-8"
#
#     response = get(url)
#     html_soup = BeautifulSoup(response.text, 'html.parser')
#     containers = html_soup.find_all('html')
#     return str(containers[0])


@app.route('/')
def first():
    return render_template('Search.html')#predict.html
@app.route('/req', methods=['POST'])
def req():
    inp =  request.form['inp'];
    if(len(inp)>0):
        pr=predict([inp.strip()],model,word_map,data_train)
        if(pr=="that one"):
            pr=inp.strip()
        html=scrap_search(pr)
        if(html==-1):
            out = json.dumps({'status': 'NOTOK', 'suggestion': '', 'result': ''});
        else:
        # print(html)
            out= json.dumps({'status':'OK','suggestion':pr,'result':html});



        return  out
    else:
        print("no inp")
        return json.dumps({'status':'OK','suggestion':''});
@app.route('/images' ,methods=['POST'])
def image():
    pr=request.form['inp']
    print(pr)
    html = scrap_image(pr)
    if (html == -1):
        out = json.dumps({'status': 'NOTOK', 'suggestion': '', 'result': ''});
    else:
        # print(html)
        out = json.dumps({'status': 'OK', 'suggestion': pr, 'result': html});

    return out



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
if __name__ == '__main__':
    model=load_model()
    word_map=load_map()
    data_train=load_data()
    app.run(debug=True)