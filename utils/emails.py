import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
def every_n(lst, n):
    """Yield successive n-sized chunks from lst."""
 
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
def email_send(subject,content):
        #The mail addresses and password
        sender_address = 'cheap404price@gmail.com'
        sender_pass = 'tnawxolbwtzdivqk'
        receivers_address = [

            # 'fabianastudillo789@gmail.com',
            # 'angelacastillolema@hotmail.com',
            # 'melissa.barrera.moral@gmail.com',
            # 'daniela.coliqueo@gmail.com',
            # 'jpeyran@gmail.com',
            # 'bruceproxd@gmail.com',
            # 'my_rousse@hotmail.com',
            # 'barbara.bustos.cm@gmail.com',
            # 'camilaev123@gmail.com',
            # 'Jochuamora42@gmail.com',
            # 'mariapaz_ortega@hotmail.com',
            # 'jheresi88@gmail.com',
            # 'sepulveda_100@hotmail.com',
            # 'retamal170394@gmail.com',
            # 'fabiancsm12@gmail.com',
            # 'catituhola@gmail.com',
            # 'ramverconsultores@gmail.com',
            # 'alan_broo@hotmail.com',
            # 'lissygarridom@gmail.com',
            # 'rosa.salin@gmail.com',
            # 'isap2121@gmail.com',
            # 'autos24@gmail.com',


            # 'fe.lopezm865@gmail.com',
            # 'sebian1920@hotmail.com',
            # 'ptroncoso@camanchaca.cl',
            # 'nsalazar041@gmail.com',
            # 'nicolevegaarancibia@gmail.com',
            # 'nicozagal2@gmail.com',
            # 'carlos_hinostroza@hotmail.cl',
            # 'Issa.castillo.a@gmail.com',
            # 'zarzuri50@gmail.com',
            # 'felipeantonios637@gmail.com',
            # 'mandgoba@hotmail.com',
            # 'nicolas.gota454@gmail.com',
            # 'vszurit@gmail.com',
            # 'gotita18@gmail.com',
            # 'manue.co.es@gmail.com',
            # 'jaja_viera@hotmail.com',
            # 'm.esquivel.tapia@gmail.com',
            # 'nicolas.o.mendez@gmail.com',
            # 'michelpalomino90@gmail.com',
            # 'nikor658@gmail.com',
            # 'krolak76@gmail.com',
            # 'jesus.enrique99520@gmail.com',
            # 'reneemilio2002@gmail.com',
            # 'enlaces.lir@gmail.com',
            # 'basthi.log@gmail.com',
            # 'hbritocm@gmail.com',
            # 'wually10@gmail.com',
            # 'ivandariodiazramos@gmail.com',
            # 'r.diiaz@gmail.com',
            # 'aldom.cl@gmail.com',
            'bastididierr@gmail.com',
            ]
        #Setup the MIME
        
        html = """      
                <html>
                <body>
                    <h1>Prueba ref:06 ) </h1>
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
                    
                    <p>Por favor marca este email como importante y antes de comprar el producto que te interese te recomiendo
                    ver si el precio no esta inflado, en paginas como <a href="https://www.knasta.cl">https://www.knasta.cl</a> o <a href="https://www.solotodo.cl ">https://www.solotodo.cl</a>
                    </p>
                     <p>
                     <b>Esta es una fase de pruebas lo más probable es que te llegen correos durante el dia
                     de la misma categoria dos veces o más, si tienes dudas llena este <a href="https://docs.google.com/forms/d/e/1FAIpQLSdn5UJGUgoM7niOAnKjIPz8hA0J1GfS-ruC722imQNTTR8WvQ/viewform?usp=sf_link">Google Forms</a>
                      </b
                    </p>
                <p>Nos vemos!! :)</p>
                </body>
                </html>
                """.format(content)

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        
        datetime_hour_for_now =  datetime.timedelta(hours=4)
        date_now = "{:%d-%m-%Y %H:%M:%S}".format(datetime.datetime.now() - datetime_hour_for_now )
        subject = "{} {}".format(subject,date_now)

        
        for email_list in list(every_n(receivers_address,20)):
            message = MIMEMultipart( "alternative", None, [ MIMEText(html,'html')])
            message['From'] = sender_address
            message['Subject'] = subject
            message['Cco'] = ", ".join(email_list)
            text = message.as_string()
            
            print("====================================")
            session.sendmail(sender_address, receivers_address, text)
            break
        
        

        session.quit()
        print('Correo enviado')