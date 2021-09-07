
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
# MODAL id kampyleInviteContainer
# En caso no funcionar en  el sv https://stackoverflow.com/questions/45370018/selenium-working-with-chrome-but-not-headless-chrome?rq=1
class Bot():
    def __init__(self, *args, **kwargs ):
        options = Options()
      
        options.add_argument('--headless')
        options.add_argument('--ignore-certificate-errors-spki-list') 
        options.add_argument('log-level=3')
        options.add_argument('window-size=1920x1080')
        options.add_argument("--incognito")
        # options.add_argument("--disable-gpu")
        # options.add_argument("-disable-software-rasterizer")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver,10)
        self.url = ''
        self.email_content = ''
        self.exists_discounts = False
        self.exists_exception = False
        self.discount = 70
        self.max_page_retry  = 0
        self.try_count = 3
        self.counter_page = 0

    
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
    def email_send(self,subject,content):
        #The mail addresses and password
        sender_address = 'bbasti390@gmail.com'
        sender_pass = 'jdjtzycowlaawmgd'
        receivers_address = ['bastididierr@gmail.com','anaisacvdo@gmail.com']
        #Setup the MIME
        
        html = """      
                <html>
                <body>
                    <h1>Tu descuentos :) </h1>
                    <table style="width:100%,border:.5px solid black">
                        <tr>
                            <th style="border:.5px solid black">MARCA</th>
                            <th style="border:.5px solid black">Producto</th>
                            <th style="border:.5px solid black">URL</th>
                            <th style="border:.5px solid black">Precio</th>
                            <th style="border:.5px solid black">Dcto</th>
                        
                        </tr>
                    {}
        
                    </table>
                    
                    <p>Por favor, antes de comprar el producto que te interese te recomiendo
                    ver si el precio no esta inflado, en paginas como https://www.knasta.cl o https://www.solotodo.cl
                    </p>
                <p>Nos vemos!! :)</p>
                </body>
                </html>
                """.format(content)
        message = MIMEMultipart( "alternative", None, [ MIMEText(html,'html')])
        message['From'] = sender_address
        message['Cco'] = ", ".join(receivers_address)

        datetime_hour_for_now =  datetime.timedelta(hours=4)
        date_now = "{:%d-%m-%Y %H:%M:%S}".format(datetime.datetime.now() - datetime_hour_for_now )
        subject_with_date = "{} {}".format(subject,date_now)
        message['Subject'] = subject_with_date

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receivers_address, text)
        session.quit()
        print('Correo enviado')

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
        
                # self.wait.until(EC.element_to_be_clickable((By.XPATH, "//b[starts-with(@id, 'testId-pod-displaySubTitle')]")))
           
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
    
                # self.wait.until(EC.element_to_be_clickable((By.XPATH, "//b[contains(@class, 'pod-title')]")))
                brand_product = product.find_elements_by_xpath(".//b[contains(@class, 'pod-title')]")

                # self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[starts-with(@class, 'copy10')]")))
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
                                                <td  style="border:.5px solid black"><a href={}>Link</a</td>
                                                <td  style="border:.5px solid black">{}</td>
                                                <td  style="border:.5px solid black">{}%</td>
                                            </tr>""".format(brand,product_name,link_ref,price,dcto_bag)
            # TODO: VER QUE HACE AL MOMENTO DE ENCONTRAR UN ERROR SI SIGUE NORMAN SIN EL BREAK
        
            print("FINALIZO SCAN")
        
            
                # object_product = {
                #     'name':product_name,
                #     'dcto':dcto_bag,
                #     'link':link_ref,
                #     'brand':brand,
                #     'price':price,
                # }
                # list_product.append(object_product)
            
                    
            
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
                        
                    print("INDEX --> ",i )
                    # TODO: simular error en la pagina 2 para hacer un reeset y vuelva ejecutar el bot 
                    # abajo esta para sabeer que tipo de excep es
                    # TODO: luego borrar este if dejar e oslo el else
                    # if i ==1:
                    #     self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-pod='catalyst-pod-----']")))
                    #     container_product = self.driver.find_elements_by_xpath( "//div[@data-pod='catalyst-pod']")
                    # else:
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
            # self.driver.quit()

            print("EXCEPT: for_products_container()")
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno        
            self.url = self.driver.current_url
            self.try_count -= 1
            self.exists_exception = True
            print(f"ExecptionType: {exception_type}\n ARCHIVO: {filename}\n LINEA:{ line_number } \n ERROR: {exception_object}") 

    def iniciar_bot(self,url): 
        try:
        

    
            
            
            if len(self.url) == 0:
                self.url = url
            while True:
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
                    break
                
            
            if self.exists_discounts:

                self.driver.quit()
                
                # # end_timer = time.time()
                # print("TIMER: ",end_timer - self.start_timer)
                print("ENVIO DESCUENTOS")
                category_name =self.url.split("/")[-1].split("?")[0].capitalize().replace("-"," ")
                self.email_send(f"DESCUENTOS!! {category_name} ",self.email_content)
            
         
            
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
    man_category = [
        'https://www.falabella.com/falabella-cl/category/cat1720006/Zapatos?isPLP=1',
        'https://www.falabella.com/falabella-cl/category/cat5260002/Ropa-interior?isPLP=1',
        'https://www.falabella.com/falabella-cl/category/cat1320008/Moda-Hombre?isPLP=1',
        'https://www.falabella.com/falabella-cl/category/cat6930003/Ropa-deportiva-hombre?isPLP=1',
        'https://www.falabella.com/falabella-cl/category/cat2036/Fitness?isPLP=1',
        'https://www.falabella.com/falabella-cl/category/cat6050003/Accesorios-Hombre?isPLP=1',
        'https://www.falabella.com/falabella-cl/category/cat7660002/Belleza?facetSelected=true&f.product.attribute.G%C3%A9nero=Hombre&isPLP=1',
    ]
    test_category = [
        'https://www.falabella.com/falabella-cl/category/cat5260002/Ropa-interior-y-pijamas?isPLP=1',
        'https://www.falabella.com/falabella-cl/category/cat5260002/Ropa-interior?isPLP=1'
    ]
    start = time.time()
    for url in  test_category:
        Bot().iniciar_bot(url)
    finish = time.time()
    print("TIEMPO: ------------------------------>",(finish - start)/60)

        