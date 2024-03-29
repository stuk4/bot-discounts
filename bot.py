
from selenium import webdriver
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time
from selenium.common.exceptions import NoSuchElementException,TimeoutException,ElementClickInterceptedException
from  urllib3.exceptions import  MaxRetryError  
import sys
from utils.emails import email_send
# MODAL id kampyleInviteContainer
# En caso no funcionar en  el sv https://stackoverflow.com/questions/45370018/selenium-working-with-chrome-but-not-headless-chrome?rq=1
class Bot():
    def __init__(self, *args, **kwargs ) -> None:
        options = Options()
      
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors-spki-list') 
        options.add_argument('log-level=3')
        options.add_argument('window-size=1920x1080')
        options.add_argument("--incognito")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        # options.add_argument("--disable-gpu")
        # options.add_argument("-disable-software-rasterizer")
        self.driver = webdriver.Chrome(ChromeDriverManager(log_level=0).install(),options=options)
        self.wait = WebDriverWait(self.driver,10)
        self.url:str = ''
        self.email_content:str = ''
        self.exists_discounts:bool = False
        self.exists_exception:bool = False
        self.discount:int = 70
        self.max_page_retry:int  = 0
        self.try_count:int = 3
        self.counter_page:int = 0
        self.category_name:str = ""

    
        # Lo hago para tener el autocomplete del driver
        return super().__init__(*args, **kwargs)
    def check_exists_inside_by_xpath(self,element,xpath):
        element_check = None
        try:
            element_check = element.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return element_check
        return element_check
    def check_exists_by_timeout_xpath(self,xpath):
        try:
            # self.driver.find_element_by_xpath(xpath)
            WebDriverWait(self.driver,0).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
        except (TimeoutException,NoSuchElementException):
            return False
        return True

    def get_list_products_info(self,element_container):
        try:
            list_product = []
            
            print("ESCANEO PRODUCTOS: ",len(element_container))
           
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//b[starts-with(@id, 'testId-pod-displaySubTitle')]")))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'layout_grid-view')]")))

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//b[contains(@class, 'pod-title')]")))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[starts-with(@class, 'copy10')]")))
            for product in element_container:
              
                object_product = {}
                # Nombre del producto
                # print("INDEX PRODUCTOS: ",index)

                product_name_list = product.find_elements_by_xpath(".//b[starts-with(@id,'testId-pod-displaySubTitle')]")

                # Obtener descuento del producto
                # Hago un check para ver si existen descuentons en la pagina
                # Si no existen regresa un array vacio
                
                dcto_bags_list = self.check_exists_inside_by_xpath(product,".//span[contains(@id, 'DCTO')]")
            
                if dcto_bags_list is None:
                    dcto_bag = 0
                else:
                    try:
                        dcto_bag = int(dcto_bags_list.text.split("%")[0])
                    except ValueError:
                        dcto_bag = 0
        
                # Obtengo el link del producto
                # self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'layout_grid-view')]")))
            
                link = product.find_elements_by_xpath(".//a[contains(@class, 'layout_grid-view')]")
                brand_product = product.find_elements_by_xpath(".//b[contains(@class, 'pod-title')]")
                product_actual_price = product.find_elements_by_xpath(".//span[starts-with(@class,'copy10')]")
                # Defino mis variables, nombre,dcto y link
                product_name = product_name_list[0].text
                link_ref  = link[0].get_attribute('href')
                
                
        

                brand = brand_product[0].text
                if len(brand_product) != 0:
                    price = product_actual_price[0].text
                else:
                    price = ""

                if dcto_bag >= self.discount:
                    self.exists_discounts = True
                    self.email_content+= """ <tr>
                                                <td  style="border:.5px solid black">{}</td>
                                                <td  style="border:.5px solid black">{}</td>
                                                <td  style="border:.5px solid black"><a href={}>Link</a></td>
                                                <td  style="border:.5px solid black">{}</td>
                                                <td  style="border:.5px solid black">{}%</td>
                                            </tr>""".format(brand,product_name,link_ref,price,dcto_bag)

        
            print("FINALIZO SCAN")
        

            
                    
            
        except (NoSuchElementException,MaxRetryError,TimeoutException,Exception) as error: 
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno        
            print(f"ExecptionType: {exception_type}\n ARCHIVO: {filename}\n LINEA:{ line_number } \n ERROR: {exception_object}") 
            self.url = self.driver.current_url
            self.try_count -= 1
            self.exists_exception = True
            

            
    def for_products_container(self,max_page):
        try:
            
            for i in range(int(max_page)):
                    # Si termina las paginas termino el proceso ya que esta
                    # dentor el while
                    self.counter_page += 1
                    if self.counter_page == int(max_page):
                        print("LLEGO AL FINAL DE PAGINAS")
                        self.try_count = 0
                    if self.try_count == 0:
                        break
                        
                    # print("INDEX --> ",i )
                    self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-pod='catalyst-pod']")))
                    container_product = self.driver.find_elements_by_xpath( "//div[@data-pod='catalyst-pod']")

                    self.get_list_products_info(container_product)
                    # Si existe una exception en get_list_products_info, esta 
                    # se saldra en el if de a continuacion para reiniciar la pagina
                    if self.exists_exception:
                        break
                    if i != int(max_page) -1:
                        self.wait.until(EC.element_to_be_clickable((By.ID, "testId-pagination-bottom-arrow-right")))
                        # self.wait.until(EC.invisibility_of_element_located((By.ID, "kampyleInviteContainer")))
                        self.driver.find_element_by_id("testId-pagination-bottom-arrow-right").click()
                    self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'loader')]")))
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except (NoSuchElementException,MaxRetryError,TimeoutException,Exception,ElementClickInterceptedException)as error:
           

            print("EXCEPT: for_products_container()")
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno        
            self.url = self.driver.current_url
            self.try_count -= 1
            self.exists_exception = True
            print(f"ExecptionType: {exception_type}\n ARCHIVO: {filename}\n LINEA:{ line_number } \n ERROR: {exception_object}") 

    def iniciar_bot(self,url:str,discount:int,category_name): 
        try:
        

    
            
            self.discount = discount
            self.category_name = category_name
            if len(self.url) == 0:
                self.url = url
            while True:
                try:

                    print("TRY COUNT: ",self.try_count,"\nURL: ",self.url )
                    self.exists_exception = False
                    self.driver.get(self.url)

                    time.sleep(3)
                    print("============== PASO GET ===============")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print("SALTO")
                
                    if self.max_page_retry == 0:
                        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//*[starts-with(@id, 'testId-pagination-bottom')]")))
                        buttons_pagination = self.driver.find_elements_by_xpath("//*[starts-with(@id, 'testId-pagination-bottom')]")
                        if type(buttons_pagination) == list:
                            self.max_page_retry = buttons_pagination[1].text
                        else:
                            print("ERROR IF BUTTONS ")
                            self.driver.quit()

                    print("MAX PAGES: ",self.max_page_retry)
                    self.for_products_container(self.max_page_retry)
                    if self.try_count <= 0:
                        self.driver.quit()
                        break
                except Exception:
                    self.url = self.driver.current_url
                    self.try_count -= 1
                    if self.try_count <= 0:
                        self.driver.quit()
                        break
                    continue
            
            if self.exists_discounts:

                
                
                # # end_timer = time.time()
                # print("TIMER: ",end_timer - self.start_timer)
                print("ENVIO DESCUENTOS")
                category_name =self.url.split("/")[-1].split("?")[0].capitalize().replace("-"," ")
                email_send(f"DESCUENTOS {self.category_name}!! {category_name} ",self.email_content)
            

            
            print("TERMINO EL PROCESO")
        except Exception:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno        
            print(f"ExecptionType: {exception_type}\n ARCHIVO: {filename}\n LINEA:{ line_number } \n ERROR: {exception_object}") 
            self.url = self.driver.current_url
            self.try_count -= 1
            self.exists_exception = True
    



if   __name__ == '__main__':
    categories = [
        {
            "category_name":"Telefonos",
            "discount":50,
            "links":[
              
            ]
        },
        {
            "category_name":"Mujer",
            "discount":60,
            "links":[


            ]
        },
        {
            "category_name":"Hombre",
            "discount":60,
            "links":[

            ]
        }
        ,
        {
            "category_name":"Zapatos Mujer-Hombre",
            "discount":60,
            "links":[

            ]
        },
        {
            "category_name":"Tecnologia",
            "discount":50,
            "links":[


            ]
        },
        {
            "category_name":"Electro",
            "discount":50,
            "links":[       

            ]
        },
        {
            "category_name":"Muebles",
            "discount":45,
            "links":[       


            ]
        },
        {
            "category_name":"Dormitorio",
            "discount":45,
            "links":[       

               
            ]
        },
        {
            "category_name":"Cocina y baño",
            "discount":45,
            "links":[       

            ]
        }
        ,
        {
            "category_name":"Decoracion",
            "discount":45,
            "links":[       

            ]
        }
        ,
        {
            "category_name":"Jardin",
            "discount":45,
            "links":[       

            ]
        }
        ,
        {
            "category_name":"Deportes",
            "discount":45,
            "links":[       
         
            ]
        }
    ]


    categories_exclude = [
        {
            "category_name":"TV"
        }
    ]
    test_category = [

      
    ]
    print(type(categories[0]))
    start = time.time()
    for category  in  categories:
        print("Category:",category["category_name"])
        for url in category["links"]:
            Bot().iniciar_bot(url,category['discount'],category["category_name"])
    finish = time.time()
    print(f"TIEMPO {datetime.datetime.now()} : ------------------------------>",(finish - start)/60)

        
