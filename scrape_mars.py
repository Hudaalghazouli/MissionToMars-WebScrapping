from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

def scrape_all(browser):
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)



    news_title, news_paragraph = scrape_news(browser)

    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featureImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemisphere(browser),
        "lastUpdated": dt.datetime.now()
    }
    browser.quit()

    return marsData



def scrape_news(browser):
    url = 'https://redplanetscience.com/'

    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1) 

    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    last_new = soup.select_one('div.list_text')

    last_new_text= last_new.find('div',class_='content_title').get_text()

    last_new_paragraph = last_new.find('div',class_='article_teaser_body').get_text()

    return last_new_text, last_new_paragraph



def scrape_feature_img(browser):

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    image_link = browser.find_by_tag('button')[1]
    image_link.click()
    html = browser.html
    soup_image = BeautifulSoup(html, 'html.parser')
    image_url_find = soup_image.find('img',class_='fancybox-image').get('src')
    image_url = f'https://spaceimages-mars.com/{image_url_find}'

    return image_url


def scrape_facts_page(browser):

    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    html = browser.html

    fact_soup = BeautifulSoup(html, 'html.parser')
    factsLocation = fact_soup.find('div', class_='diagram mt-4')

    factTable = factsLocation.find('table')
    
    facts = ""
    facts += str(factTable)

    return facts


def scrape_hemisphere(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_url = []

    for i in range(4):
    
        hemisphereInfo={}
        
        browser.find_by_css('a.product-item img')[i].click()
        
        sample = browser.links.find_by_text('Sample').first
        
        hemisphereInfo['img_url'] = sample['href']
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_url.append(hemisphereInfo)
        browser.back()
    
    return hemisphere_image_url
    

if __name__ == "__main__":
    print(scrape_all)