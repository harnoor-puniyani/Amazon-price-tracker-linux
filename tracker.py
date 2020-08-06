import time
from selenium.webdriver.common.keys import Keys
from  amazon_config import(
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY
)
class GenerateReport:
    def __init__(self):
        pass        
class AmazonAPI:
    def __init__(self , search_term , filters,base_url , currency):
        self.base_url=base_url
        self.search_term=search_term
        options =get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency=currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print('starting script..')
        print(f'Looking for {self.search_term} products')
        links = self.get_products_link()
        if not links:
            print('stopped script!')
            return
        print(f'GOT {len(links)} links to products')
        print('Getting info about prodicts....')
        products = self.get_products_info(links)
        time.sleep(3)
        self.driver.quit()

    def get_products_info(self,links):
        asins = self.get_asins(links)
        products =[]
        for asin in asins:
            product = self.get_single_product_info(asin)
            return


    def get_single_product_info(self,asin):
        print(f'product id {asin} getting data...')
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}/?language=en_IN')
        time.sleep(2)
        title = self.get_product_title()
        seller=self.get_product_seller()
        price=self.get_product_price()

    def get_product_price(self):
        try:
            return '99'
            # self.driver.find_element_by_id('priceblock_ourprice').text()
        except Exception as e:
            print(e)
            print(f"can't get price of the product : {self.driver.get.current_url}")
            return None

    def get_product_seller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text()
        except Exception as e:
            print(e)
            print(f"can't get seller info for {self.driver.get.current_url}")
            return None
    

    def get_product_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text()
        except Exception as e:
            print(e)
            print(f'Cannot get title of a product - {self.driver.get.current_url}')
            return None

    def shorten_url(self,asin):
        return self.base_url +'/dp/' + asin

    def get_asins(self,links):   
        return [self.get_asin(link)for link in links]

    def get_asin(self ,products_link):
        return products_link[products_link.find('/dp/') + 4:products_link.find('/ref')]

    def get_products_link(self):
        self.driver.get(self.base_url)
        element=self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        time.sleep(2)
        result_list=self.driver.find_elements_by_class_name('s-result-list')
        print(f'result_list= {result_list}')
        links=[]
        try:
            results=result_list[0].find_elements_by_xpath(
                '//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception  as e:
            print("Didn't get any products...")
            print(e)
            print(links)
            return links



if __name__=='__main__':
    print('Heyyy! 👀') 
    amazon = AmazonAPI(NAME,FILTERS,BASE_URL,CURRENCY)
    amazon.run()