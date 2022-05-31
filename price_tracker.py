from selenium import webdriver
import time
import smtplib

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

server.login("example@gmail.com" , "password")

driver = webdriver.Chrome()

def url_list_control(url_list):   #return True if all urls are working, return false if not
    link_num=0
    for i in range(len(url_list)):
        time.sleep(1)
        try:
            driver.get(url_list[i])
            link_num+=1
        except:
            print("hatali link : ", url_list[i])
            return False

    print("no broken link",link_num,"link found")
    return True




def product_price(website,html):   #get html and return price of product

    if website=="amazon" :
        index = html.find("a-offscreen") #index of "a" from "a-offscreen"
        starting_index= html.find(">",index)
        ending_index= html.find("<",index)

        price=html[starting_index+1:ending_index] #declare price as string to return
        price=price.strip()
        return(price)

    elif website=="hepsiburada" :
        index = html.find("markupText:'currentPriceBeforePoint") #index of "a" from "a-offscreen"
        starting_index= html.find(">",index)
        ending_index= html.find("<",index)

        price=html[starting_index+1:ending_index] #declare price as string to return
        price=price.strip()
        return(price)


    elif website=="trendyol" :
        index = html.find("class=\"prc-dsc\"") #index of "a" from "a-offscreen"
        starting_index= html.find(">",index)
        ending_index= html.find("<",index)
        
        price=html[starting_index+1:ending_index] #declare price as string to return
        price=price.strip()
        return(price)

    #<ins content="219.00">219,00 <span content="TRY">TL</span></ins>
    elif website=="n11" :
        index = html.find("ins content=") #index of "a" from "a-offscreen"
        starting_index= html.find(">",index)
        ending_index= html.find("<",index)
        
        price=html[starting_index+1:ending_index] #declare price as string to return
        price=price.strip()
        return(price)




    
def product_name(website,html):    #get html and return name of product

    #<span id="productTitle" class="a-size-large product-title-word-break"> DECOBELLA 90512 GreenLeaves Pencere Sinekliği 130x150 Cm </span>
    if(website=="amazon"):
        index = html.find("id=\"productTitle\"") #index of "p" from "producTitle"
        starting_index= html.find(">",index)
        ending_index= html.find("<",index)

        name=html[starting_index+1:ending_index] #declare a name string to return name
        name=name.strip()
        return(name)    

    #<h1 itemprop="name" class="product-name best-price-trick" id="product-name" data-bind="markupText: 'productName', event: {mouseup: handleMouseUpForProductName}"> Artop Briket Mangal Kömürü 10 kg Özel Kutu </h1>
    elif website=="hepsiburada" :
        index = html.find("id=\"product-name\"") #index of "a" from "a-offscreen"
        starting_index= html.find(">",index)
        ending_index= html.find("<",index)

        name=html[starting_index+1:ending_index] #declare a name string to return name
        name=name.strip()
        return(name)    

    #<h1 class="pr-new-br" data-drroot="h1"><a href="/magic-saver-bag-x-b110588">Magic Saver Bag</a><span> 8’li Vakumlu Poşet Set-1 8697623589603 </span></h1>
    elif website=="trendyol" :
        index = html.find("class=\"pr-new-br\"") #index of "a" from "a-offscreen"
        starting_index = html.find(">",index) #go first >
        starting_index = html.find(">",starting_index+1) #go other > after the first one
        ending_index= html.find("<",starting_index) #go < after the last >, so we can get "Magic Saver Bag" which is the first part of name
        str=html[starting_index+1+5:ending_index]
        starting_index = html.find("<span>",ending_index)
        ending_index= html.find("</span>",starting_index)

        name=str+html[starting_index+1:ending_index]
        name=name.strip()
        return(name)

    #<h1 class="proName"> Nokia 2610 3 MB Tuşlu Cep Telefonu </h1>
    elif website=="n11" :
        index = html.find("class=\"proName\"") #index of "a" from "a-offscreen"
        starting_index= html.find(">",index)
        ending_index= html.find("<",index)
        
        name=html[starting_index+1:ending_index] #declare a name string to return name
        name=name.strip()
        return(name)    




file=open("html.txt","r")
text=file.read()
url_list = text.split('\n')

        
i=0
while(i<len(url_list)):  #url_list teki boşlukları kaldırdık
    if(url_list[i]==""):
        url_list.remove(url_list[i])
    else:
        i+=1
        

dictionary={}  



if(url_list_control(url_list)==True):   #dictionary oluştur
    for url in url_list:
        driver.get(url)
        html = driver.page_source
        
        time.sleep(1)
        
        if "www.amazon" in url:  # control if url from amazon (not included after amazon word to be able to work for all amazons)
            website="amazon"
            dictionary[url]=[website,product_name(website,html),product_price(website,html)]

        elif "www.hepsiburada.com" in url :  # control if url from hepsiburada
            website="hepsiburada"
            dictionary[url]=[website,product_name(website,html),product_price(website,html)]

        elif "www.trendyol.com" in url:  # control if url from trendyol
            website="trendyol"
            dictionary[url]=[website,product_name(website,html),product_price(website,html)]

        elif "urun.n11.com" in url :  # control if url from n11
            website="n11"
            dictionary[url]=[website,product_name(website,html),product_price(website,html)]





print(dictionary)




while(True):  #sonsuz kontrol
    for url in url_list:
        driver.get(url)
        html = driver.page_source

        if(product_price(html) != dictionary[url][2]):
            server.sendmail("from@gmail.com", "to@gmail.com", "price changed!, new price : ", dictionary[url][2])  # mail gönder
            dictionary[url][2]=product_price(html)   #yeni fiyatı güncelle
        

        else:
            print("no new price for : ", dictionary[url][1])


    





"""
AMAZON :

<span id="productTitle" class="a-size-large product-title-word-break"> DECOBELLA 90512 GreenLeaves Pencere Sinekliği 130x150 Cm </span>

<span class="a-offscreen">19,97TL</span>

https://www.amazon.com.tr/Sennheiser-508598-400S-Siyah-Kulakl%C4%B1k/dp/B07N2261R6





HEPSİBURADA:

<span data-bind="markupText:'currentPriceBeforePoint'">12.827</span>

<span itemprop="name" class="product-name" data-bind="markupText: 'productName'">
        Artop Briket Mangal Kömürü 10 kg Özel Kutu
    </span>


<h1 itemprop="name" class="product-name best-price-trick" id="product-name" data-bind="markupText: 'productName', event: {mouseup: handleMouseUpForProductName}"> Artop Briket Mangal Kömürü 10 kg Özel Kutu </h1>








TRENDYOL :

<span class="prc-dsc">262,49 TL</span>



<h1 class="pr-new-br" data-drroot="h1"><a href="/magic-saver-bag-x-b110588">Magic Saver Bag</a><span> 8’li Vakumlu Poşet Set-1 8697623589603 </span></h1>



N11:


<ins content="219.00">219,00 <span content="TRY">TL</span></ins>

<h1 class="proName"> Nokia 2610 3 MB Tuşlu Cep Telefonu </h1>



"""
