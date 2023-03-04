from selenium import webdriver
import time



browser = webdriver.Chrome()
browser.maximize_window() 
browser.get("https://archive.twitter-trending.com/worldwide/01-01-2019")
time.sleep(10)
trends=[]
trends_2=[]
flag=True
i=1
while (flag):
    try:
        url=browser.current_url
        ads="google_vignette"
        if (url=="https://archive.twitter-trending.com/worldwide/31-12-2019"):
            flag=False
            print("doneeee")
        if ads in url:
            print(url)
            url=url.replace('#google_vignette','')
            print(url)
            browser.refresh()
            time.sleep(10)

        a=browser.find_element("xpath",'/html/body/div[2]/div[2]/div/div/div/div[5]/div[1]/div[1]/span[1]/div[2]/span[1]/span[2]').get_attribute("innerHTML")
        if (a=='-'):
            browser.refresh()
            continue
        else:
            trends.append(a)

        trends.append (browser.find_element("xpath",'/html/body/div[2]/div[2]/div/div/div/div[5]/div[1]/div[1]/span[1]/div[2]/span[2]/span[2]').get_attribute("innerHTML"))

        trends.append (browser.find_element("xpath",'/html/body/div[2]/div[2]/div/div/div/div[5]/div[1]/div[1]/span[1]/div[2]/span[3]/span[2]').get_attribute("innerHTML"))

        trends.append (browser.find_element("xpath",'/html/body/div[2]/div[2]/div/div/div/div[5]/div[1]/div[1]/span[1]/div[2]/span[4]/span[2]').get_attribute("innerHTML"))

        trends.append (browser.find_element("xpath",'/html/body/div[2]/div[2]/div/div/div/div[5]/div[1]/div[1]/span[1]/div[2]/span[5]/span[2]').get_attribute("innerHTML"))
            
        time.sleep(10)
            
        s=browser.find_element("xpath",'//*[@id="ust_menu_4"]/li[3]')
        s.click()
        time.sleep(10)

        print(i,"- " ,trends)
        with open(r"world wide.txt","a",encoding="utf8")as f:
            for trend in trends:
                f.write(trend)
                f.write("\n")
            trends_2.append(trend)
            

                    
        trends.clear()
        i+=1   
        time.sleep(15)
    except Exception:
        print("REEPEATEEEED")
        trends.clear()
        browser.refresh()
        time.sleep(5)
        continue
f.close()
      
        
    

    
    
# print("Page title is: ")
# print(browser.title)
# time.sleep(5)
print(trends_2)
print("-----------------------")
for x in trends_2:
    print(x)
print("done")
