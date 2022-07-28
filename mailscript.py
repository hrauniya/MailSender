import email,smtplib,ssl
import json

from email import encoders
from configparser import ConfigParser
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#instantiating configparser object
file='config.ini'
config=ConfigParser()
config.read(file)

class mail:


    port=465
    smtp_server="smtp.gmail.com"
    
    sender_address=config['senderdetails']['email']
    password=config['senderdetails']['password']
    reciever_address=config['recieverdetails']['email']
    files = config.get("attachments", "fullfilepath")
    file_list = json.loads(files)

    
  
    
    message=MIMEMultipart("alternative")

    with open('test.html', 'r') as file:
        htmlstring=file.read()
    

    
   

   

    def __init__(self,plaintext=config['bodymessage']['message'],htmlcontent=htmlstring):
        self.plaintext=plaintext
        self.htmlcontent=htmlcontent

        self.message["Subject"]="Testing"
        self.message["From"]=self.sender_address
        self.message["To"]=self.reciever_address

         
          

        self.message.attach(MIMEText(self.plaintext, "plain"))
        self.message.attach(MIMEText(self.htmlcontent, "html") )
        if self.file_list is not None:
            print("This is self.file_list",self.file_list)

            for file in self.file_list:
                print("This is the file",file)
                
                with open(file,"rb") as attachment:
                    attachment_part=MIMEBase("application","octet-stream")
                    attachment_part.set_payload(attachment.read())

                    encoders.encode_base64(attachment_part)

                    attachment_part.add_header(
                        "Content-Disposition",
                        f"attachment;filename={file}",
                    )

                    self.message.attach(attachment_part)


        self.context=ssl.create_default_context()

    def sendemail(self):
        with smtplib.SMTP_SSL(self.smtp_server,self.port,context=self.context) as server:
            server.login(self.sender_address, self.password)
            server.sendmail(self.sender_address,self.reciever_address,self.message.as_string())



auto=mail()
auto.sendemail()