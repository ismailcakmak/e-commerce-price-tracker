# e-commerce-price-tracker

Hi, everyone. 

This program allows you to track prices from Amazon websites (.com .co.jp .com.tr etc) and leading Turkish e-commerce
websites like Hepsiburada, Trendyol and N11.

Just copy the links of product you want to track, and paste the link to txt file by line. 

I used Python, Selenium and Smtplib modules.


The working mechanim is basicly like that : 
 * detect and control of links in txt file, if they are not broken add them to "url_list" list.
 * then one by one, paste html code of urls to "html" string
 * extract price data from html code according to platform where html pulled
 * create dictonary formed like that {url:[plarform_name,product_name,product_price]}
 * Then start by checking the dictionary elements one by one, if there is a change in the product price, send an e-mail to the desired address.


Thanks..

my email : ismailcakmak@sabanciuniv.edu
