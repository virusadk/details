import telebot
from telebot import types # для указание типов
import requests
import xmltodict 
import pprint 
import json 
from bs4 import BeautifulSoup
import lxml
from PIL import Image
import sys
from PIL import ImageFilter
import pybase64


bot = telebot.TeleBot('7059069070:AAEXVrB__AyZ-Tw_l_gVhk2jQWwG1g2Sivk')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Как пользоваться")
    btn2 = types.KeyboardButton("❓ Поиск по артикулу")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот для твоей статьи для habr.com".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "👋 Как пользоваться"):
        bot.send_message(message.chat.id, text="Вскоре сдесь будет подробная инструкция")
    elif(message.text == "❓ Поиск по артикулу"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        
        bot.send_message(message.chat.id, text="Введите артикул", reply_markup=markup)
        bot.register_next_step_handler(message, get_article);
    

    elif(message.text == "Аналоги"):
        
        mesim = get_analog(article, brand)
        try:
            bot.send_message(message.chat.id, text=mesim, parse_mode="HTML")
        except:
            bot.send_message(message.chat.id, text='Аналогов не найдено', parse_mode="HTML")

    elif(message.text == "Искать другой артикул"):
        
        start(message)



    elif(message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "У меня нет имени..")
    
    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Поздороваться с читателями")
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")
def get_article(message): #получаем фамилию
    global article;
    article = message.text;
    print(article)
    brands = search(article)
    print(brands)
    if brands == []: 
        bot.send_message(message.chat.id, text='Данный артикул не найден')
    else:
        for br in brands:
            bre = br['Name']
            
            bot.send_message(message.chat.id, text=bre)
        bot.register_next_step_handler(message, get_brand);  




def get_brand(message):  
    global brand;
    brand = message.text;
   
    gurl = get_picture(article)
#     with open('test.txt', 'rb') as bs64_file:
#         bs64_data = bs64_file.read()

# # Decode base64
#     decoded_img_data = pybase64.b64decode((bs64_data))

# # Create image file from base64
#     with open('image.jpeg', 'wb') as img_file:
#         img_file.write(decoded_img_data)
    # try:
    #     resp = requests.get(gurl, stream=True).raw
    # except requests.exceptions.RequestException as e:  
    #     sys.exit(1)
 
    # try:
    #     img = Image.open(resp)
    # except IOError:
    #     print("Unable to open image")
    #     sys.exit(1)
    # # namephoto = f'{article}'
    # img.save(article, 'jpeg')
    # tatras = Image.open('sid.jpg')
    # # blurred_jelly = tatras.filter(ImageFilter.SHARPEN)
    # # blurred_jelly.save('{article}.jpg')
    # print(soup)
    bot.send_message(message.chat.id, text='Выполняется поиск.......')
    info = search_info()
    
    for des in info:
        article1 = des['Article']
        print(article)
        br = des['Brand']
        print(br)
        primenimost = des['Designation']
        print(primenimost)
        group = des['Group']
        print(group)
        
        mes = f'\U00002699 <b>{br} {article1}</b>\n'\
                \
              f'<i>{group}</i>\n'\
              f'<i>{primenimost}</i>\n'\
              f'\n'\
        
        skladi = ''
        stores = des['Stores']
        
        for sklad in stores:
            
            name = sklad['StoreName']
            kol = sklad['Quantity']
            price = sklad['Price']
            valuta = sklad['Currency']
            unit = sklad['Unit']
            kratno = sklad['Multiplicity']
            dostavka = sklad['DeliveryInfo']
            print(name,kol,unit,price,valuta,dostavka)
            if name == 'АС Барановичи':
                if int(kol) >= 1:
                    otz = '<i>Вналичии</i>'
                    sklad = f'\U0001F6D2<b>{name}</b> \n'\
                            f'<b>{otz}</b> \n'\
                            f'\U0001F3F7{kol}{unit} \U0001F4B7<b>{price}{valuta}</b>\n'
                else:
                    otz = '\U0001F6D2 <b>Нет вналичии</b>'
                    sklad = f'{name} {otz}\n'
            else:
                sklad = f'\U0001F4E6 <b>{name}</b>\n'\
                        f'\U0001F3F7<i>{kol}{unit}</i> \U0001F4B7<b>{price}{valuta}</b> \U0001F4C5<i>{dostavka}</i>\n'\
                      
                
            skladi = skladi + sklad
        if skladi == '':
            skladi = 'Нет позиций для заказа'
    itog = mes + skladi
    # soup = get_picture(article)
    # print(soup)
    # bot.send_message(message.chat.id, photo='{soup}', text=itog)
    # sp = r'soup'
    # optest = open(sp)
    # print(optest)
    
        # ph = pybase64.b64decode((gurl))
        # with open('image.jpeg', 'wb') as img_file:
        #     img_file.write(ph)
        # photo = open('image.jpeg', 'rb')
        # with open("image.jpeg", "rb") as file:
        #     f = file.read()
        # fixed_width = 2160
        # fixed_height = 3840
        # img = Image.open('image.jpeg')
        # # получаем процентное соотношение
        # # старой и новой ширины
        # # width_percent = (fixed_height / float(img.size[0]))
        # # # на основе предыдущего значения
        # # # вычисляем новую высоту
        # # height_size = int((float(img.size[0]) * float(width_percent)))
        # # меняем размер на полученные значения
        # new_image = img.resize((fixed_width, fixed_height))
        # blurred_jelly = new_image.filter(ImageFilter.SHARPEN)
        # blurred_jelly1 = blurred_jelly.filter(ImageFilter.SHARPEN)
        # blurred_jelly2 = blurred_jelly1.filter(ImageFilter.SHARPEN)
        # # blurred_jelly.save('{article}.jpg')
        # im = f'{article.jpeg}'
        # img = Image.open(im)
    try:
        resp = requests.get(gurl, stream=True).raw
    except requests.exceptions.RequestException as e:  
        sys.exit(1)
 
    try:
        img = Image.open(resp)
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn10 = types.KeyboardButton("Аналоги")
        btn11 = types.KeyboardButton("Документация")
        btn12 = types.KeyboardButton("Искать другой артикул")
        markup1.add(btn10, btn11, btn12)
        bot.send_photo(message.chat.id, img, caption=itog, parse_mode="HTML", reply_markup=markup1)
        
    except IOError:
        img = Image.open('1.jpg')
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn10 = types.KeyboardButton("Аналоги")
        btn11 = types.KeyboardButton("Документация")
        btn12 = types.KeyboardButton("Искать другой артикул")
        markup1.add(btn10, btn11, btn12)
        bot.send_photo(message.chat.id, img, caption=itog, parse_mode="HTML", reply_markup=markup1)
        print("Unable to open image")
        sys.exit(1)
    
        
    


def search_info():
    

    cookies = {
        'sid': 'b4tm52ksbw1ihp0o1l2dv4pj',
        'uss': 'a12a9d76-e494-4ede-beeb-9d8c5c4cf299',
        '__RequestVerificationToken': '5gqmGVDKJPEaiYCZrd6jTFtrqO1j6j2fyLK3MC1SU-5nHzSBL-VHiSxj3qdG7IJI14GApnFVutTHPuS9dZcRKJKHdb8ySXsyRewh-_bNM_w1',
        '_gcl_au': '1.1.1102377369.1711699614',
        '_fbp': 'fb.1.1711699613816.1335070960',
        'tmr_lvid': 'd68f60751c5589fde18a18a143fff4e3',
        'tmr_lvidTS': '1711699614931',
        '_ym_uid': '1711699615216095717',
        '_ym_d': '1711699615',
        '_tt_enable_cookie': '1',
        '_ttp': 'NQN8X5DNr5s4N_vNeXAzuqf3Qs1',
        '_gid': 'GA1.2.1245189497.1711972118',
        '_ym_isad': '1',
        'seconds_on_page_104054': '147',
        '_ga_6352MSYKNX': 'GS1.1.1711972120.4.1.1711972276.59.0.0',
        '_ga': 'GA1.1.615461343.1711699613',
        '_ga_ECXG0392JW': 'GS1.1.1711972123.4.1.1711972277.0.0.0',
        'tmr_detect': '0%7C1711972280331',
        'was_called_in_current_session_104054': '1',
        '_ga_83HJKTVF69': 'GS1.1.1711972121.3.1.1711972430.0.0.0',
        '.AspNet.ApplicationCookie': 'Cjt2MKDrouGGoWQz4mvb8p2fr_Ej7RlXGqA_QTqdgbR_TR7TGIyWTbywfXGdpB0HruHi-sbIIuPCEBIGebGMQySxPN74WE2UQwmQu6MRZ4TbpiQrRU2AmR94TP8f4ORVTFxYZS033-vLkkRZVYCnB91m9AUNNeqQcSNAA7716NQUMGyhprOKXGwyvRExEhhkPH4cdXXakNmw-44PqMFCu_SqLVl9AzZir5bYmMRgQuUXxCzONOkCVjRnkxXI1HtbR9kvvtqpUFMtSyPNdqmFFltdHPPS93FhuSe9ZEgdBMnTCc84xlWIY6bnT7dVLKmWCQ_gFhMwYie0So-rvhCLLkzLkGdCOYWcvcTaz24dCUol6eaem7-RddpioUZZsR18kAHXdqV-nvJvZB7GPISpegL5QHO46E5QMtn81zjxmPY4aGhNZ5zCCTDLrSi2WRooAS_UwvtR2d4uZJT_h0DUD1fWF7CFkMIZT983Sc7iScgE0Yd_NUy9127ZnYU8Yrki',
        'app': '7UxtR6vQDlKMgIXwkoTkCWKBk6gSwQKoMhnk7J4CSvCSVCnLYdSiuf76nwInGxAPAxFcAcfa44y7Ml3CnGKEDfRZS8ePw7Gb8iC7q6sFrsXseT_6XcTmPhYKLFbOmSwxH8qsfD8_8z0GV5jlkkSOPV5eDCtQ1_HDRG42C8r50MU5Eq19UqC1ihud4wdbR2ed_L1UKJ8XR3ZZ408A9bGD9AMGlzxGd4rTrNcJFrr__Yx0ih97V72W3jnN3mCyEVGv9YAuJUjqBH9BUoejEH-DTHG_fvX2gaP4Be0A6pHbW9X2F6xoxK5pK8Q-LO7NrSK_kDDv24gVTiYISh8jXdiBwxGBhIb9-827AI3eLHPCez6heX831PicsscMmB1RrRNLJptCa3JjFKWcodrmCwhuDTQO0SoCMyGVENy1FL9SHfbuePwlLYBPmDm1k3IGCXEWmvB8KqpQ6jtwfgNWhlAyh0Y6EKz2vsyc32nQR6ZnohrEX1JkC-Y2n9gW7Bo-OnmK',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'sid=b4tm52ksbw1ihp0o1l2dv4pj; uss=a12a9d76-e494-4ede-beeb-9d8c5c4cf299; __RequestVerificationToken=5gqmGVDKJPEaiYCZrd6jTFtrqO1j6j2fyLK3MC1SU-5nHzSBL-VHiSxj3qdG7IJI14GApnFVutTHPuS9dZcRKJKHdb8ySXsyRewh-_bNM_w1; _gcl_au=1.1.1102377369.1711699614; _fbp=fb.1.1711699613816.1335070960; tmr_lvid=d68f60751c5589fde18a18a143fff4e3; tmr_lvidTS=1711699614931; _ym_uid=1711699615216095717; _ym_d=1711699615; _tt_enable_cookie=1; _ttp=NQN8X5DNr5s4N_vNeXAzuqf3Qs1; _gid=GA1.2.1245189497.1711972118; _ym_isad=1; seconds_on_page_104054=147; _ga_6352MSYKNX=GS1.1.1711972120.4.1.1711972276.59.0.0; _ga=GA1.1.615461343.1711699613; _ga_ECXG0392JW=GS1.1.1711972123.4.1.1711972277.0.0.0; tmr_detect=0%7C1711972280331; was_called_in_current_session_104054=1; _ga_83HJKTVF69=GS1.1.1711972121.3.1.1711972430.0.0.0; .AspNet.ApplicationCookie=Cjt2MKDrouGGoWQz4mvb8p2fr_Ej7RlXGqA_QTqdgbR_TR7TGIyWTbywfXGdpB0HruHi-sbIIuPCEBIGebGMQySxPN74WE2UQwmQu6MRZ4TbpiQrRU2AmR94TP8f4ORVTFxYZS033-vLkkRZVYCnB91m9AUNNeqQcSNAA7716NQUMGyhprOKXGwyvRExEhhkPH4cdXXakNmw-44PqMFCu_SqLVl9AzZir5bYmMRgQuUXxCzONOkCVjRnkxXI1HtbR9kvvtqpUFMtSyPNdqmFFltdHPPS93FhuSe9ZEgdBMnTCc84xlWIY6bnT7dVLKmWCQ_gFhMwYie0So-rvhCLLkzLkGdCOYWcvcTaz24dCUol6eaem7-RddpioUZZsR18kAHXdqV-nvJvZB7GPISpegL5QHO46E5QMtn81zjxmPY4aGhNZ5zCCTDLrSi2WRooAS_UwvtR2d4uZJT_h0DUD1fWF7CFkMIZT983Sc7iScgE0Yd_NUy9127ZnYU8Yrki; app=7UxtR6vQDlKMgIXwkoTkCWKBk6gSwQKoMhnk7J4CSvCSVCnLYdSiuf76nwInGxAPAxFcAcfa44y7Ml3CnGKEDfRZS8ePw7Gb8iC7q6sFrsXseT_6XcTmPhYKLFbOmSwxH8qsfD8_8z0GV5jlkkSOPV5eDCtQ1_HDRG42C8r50MU5Eq19UqC1ihud4wdbR2ed_L1UKJ8XR3ZZ408A9bGD9AMGlzxGd4rTrNcJFrr__Yx0ih97V72W3jnN3mCyEVGv9YAuJUjqBH9BUoejEH-DTHG_fvX2gaP4Be0A6pHbW9X2F6xoxK5pK8Q-LO7NrSK_kDDv24gVTiYISh8jXdiBwxGBhIb9-827AI3eLHPCez6heX831PicsscMmB1RrRNLJptCa3JjFKWcodrmCwhuDTQO0SoCMyGVENy1FL9SHfbuePwlLYBPmDm1k3IGCXEWmvB8KqpQ6jtwfgNWhlAyh0Y6EKz2vsyc32nQR6ZnohrEX1JkC-Y2n9gW7Bo-OnmK',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Opera";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    params = {
        'article': article,
        'orgId': '2',
        'orderType': '2',
        'brand': brand,
        'login': 'info@allcar.by',
        'password': 'Autospace7757513',
        'application': 'json'
        
        
    }

    response = requests.get('https://auto1.by/WebApi/SearchByArticle',cookies=cookies,headers=headers,params=params)
    resultline1 = response.json()
    print(response)
    print(resultline1)
    return resultline1
    
def search(article):
    cookies = {
    'sid': 'b4tm52ksbw1ihp0o1l2dv4pj',
    'uss': 'a12a9d76-e494-4ede-beeb-9d8c5c4cf299',
    '__RequestVerificationToken': '5gqmGVDKJPEaiYCZrd6jTFtrqO1j6j2fyLK3MC1SU-5nHzSBL-VHiSxj3qdG7IJI14GApnFVutTHPuS9dZcRKJKHdb8ySXsyRewh-_bNM_w1',
    '_gid': 'GA1.2.564438751.1711699613',
    '_ga_6352MSYKNX': 'GS1.1.1711699613.1.0.1711699613.60.0.0',
    '_gcl_au': '1.1.1102377369.1711699614',
    '_fbp': 'fb.1.1711699613816.1335070960',
    'session_timer_104054': '1',
    '_ga': 'GA1.1.615461343.1711699613',
    '_ga_ECXG0392JW': 'GS1.1.1711699614.1.0.1711699614.0.0.0',
    'tmr_lvid': 'd68f60751c5589fde18a18a143fff4e3',
    'tmr_lvidTS': '1711699614931',
    '_ym_uid': '1711699615216095717',
    '_ym_d': '1711699615',
    '_ym_isad': '2',
    '_tt_enable_cookie': '1',
    '_ttp': 'NQN8X5DNr5s4N_vNeXAzuqf3Qs1',
    '_ym_visorc': 'b',
    'tmr_detect': '0%7C1711699618213',
    'b24_sitebutton_hello': 'y',
    'was_called_in_current_session_104054': '1',
    '_ga_83HJKTVF69': 'GS1.1.1711699614.1.1.1711699914.0.0.0',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'sid=b4tm52ksbw1ihp0o1l2dv4pj; uss=a12a9d76-e494-4ede-beeb-9d8c5c4cf299; __RequestVerificationToken=5gqmGVDKJPEaiYCZrd6jTFtrqO1j6j2fyLK3MC1SU-5nHzSBL-VHiSxj3qdG7IJI14GApnFVutTHPuS9dZcRKJKHdb8ySXsyRewh-_bNM_w1; _gid=GA1.2.564438751.1711699613; _ga_6352MSYKNX=GS1.1.1711699613.1.0.1711699613.60.0.0; _gcl_au=1.1.1102377369.1711699614; _fbp=fb.1.1711699613816.1335070960; session_timer_104054=1; _ga=GA1.1.615461343.1711699613; _ga_ECXG0392JW=GS1.1.1711699614.1.0.1711699614.0.0.0; tmr_lvid=d68f60751c5589fde18a18a143fff4e3; tmr_lvidTS=1711699614931; _ym_uid=1711699615216095717; _ym_d=1711699615; _ym_isad=2; _tt_enable_cookie=1; _ttp=NQN8X5DNr5s4N_vNeXAzuqf3Qs1; _ym_visorc=b; tmr_detect=0%7C1711699618213; b24_sitebutton_hello=y; was_called_in_current_session_104054=1; _ga_83HJKTVF69=GS1.1.1711699614.1.1.1711699914.0.0.0',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Opera";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'pattern': article,
        'orgId': '2',
        'orderType': '2',
        'login': 'info@allcar.by',
        'password': 'Autospace7757513',
        'application': 'json'
        
        
    }

    response = requests.get('https://auto1.by/WebApi/GetBrands', params=params, cookies=cookies, headers=headers)
    resultline = response.json()
    # my_dict = xmltodict.parse(response)
    # for brand in my_dict:
    #     test = brand['Brand']
    return resultline
    
    # print(my_dict)
    
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
#         #код сохранения данных, или их обработки
#         bot.send_message(call.message.user.id, 'Введите артикул');
def get_picture(article):
   



    cookies = {
        'sid': 'mdzfqfrqsfdsf1jnugxclkiv',
        'uss': 'f3013664-592e-484e-b5a5-af7eefeb1604',
        '__RequestVerificationToken': 'ytgor4TgCKKVVsifOioSm8C7fpLSRHyyGJVnqkn1lEGzi3R0wlvJo0RCnwVlraq2HM2tdiAdLEbk58mI11SoXXECC79KxKGxtylKY1YPwso1',
        '_gid': 'GA1.2.448986056.1712920910',
        '_gcl_au': '1.1.828200517.1712920910',
        '_fbp': 'fb.1.1712920910383.1569263708',
        '_ym_uid': '1712920911440191163',
        '_ym_d': '1712920911',
        'tmr_lvid': '83ae2c001903b1fc6aae6c26f74974b4',
        'tmr_lvidTS': '1712920911411',
        'session_timer_104054': '1',
        '_ym_isad': '2',
        '_ym_visorc': 'b',
        '_tt_enable_cookie': '1',
        '_ttp': 'fPOE4tgO-opiyEl8Nqj3X_kNhsA',
        'domain_sid': 'cWCIuad8T9ItflpoBTUTo%3A1712920913347',
        'was_called_in_current_session_104054': '1',
        '_gat': '1',
        '_dc_gtm_UA-38210263-4': '1',
        '_gat_UA-238453145-1': '1',
        'seconds_on_page_104054': '416',
        '_ga': 'GA1.1.48095384.1712920909',
        'tmr_detect': '0%7C1712921370488',
        '_ga_6352MSYKNX': 'GS1.1.1712920909.1.1.1712921381.28.0.0',
        '_ga_83HJKTVF69': 'GS1.1.1712920911.1.1.1712921381.0.0.0',
        '_ga_ECXG0392JW': 'GS1.1.1712920911.1.1.1712921381.0.0.0',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'sid=mdzfqfrqsfdsf1jnugxclkiv; uss=f3013664-592e-484e-b5a5-af7eefeb1604; __RequestVerificationToken=ytgor4TgCKKVVsifOioSm8C7fpLSRHyyGJVnqkn1lEGzi3R0wlvJo0RCnwVlraq2HM2tdiAdLEbk58mI11SoXXECC79KxKGxtylKY1YPwso1; _gid=GA1.2.448986056.1712920910; _gcl_au=1.1.828200517.1712920910; _fbp=fb.1.1712920910383.1569263708; _ym_uid=1712920911440191163; _ym_d=1712920911; tmr_lvid=83ae2c001903b1fc6aae6c26f74974b4; tmr_lvidTS=1712920911411; session_timer_104054=1; _ym_isad=2; _ym_visorc=b; _tt_enable_cookie=1; _ttp=fPOE4tgO-opiyEl8Nqj3X_kNhsA; domain_sid=cWCIuad8T9ItflpoBTUTo%3A1712920913347; was_called_in_current_session_104054=1; _gat=1; _dc_gtm_UA-38210263-4=1; _gat_UA-238453145-1=1; seconds_on_page_104054=416; _ga=GA1.1.48095384.1712920909; tmr_detect=0%7C1712921370488; _ga_6352MSYKNX=GS1.1.1712920909.1.1.1712921381.28.0.0; _ga_83HJKTVF69=GS1.1.1712920911.1.1.1712921381.0.0.0; _ga_ECXG0392JW=GS1.1.1712920911.1.1.1712921381.0.0.0',
        'Referer': 'https://auto1.by/search?pattern=vx2300',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Opera";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'pattern': article,
    }

    responsesearch = requests.get('https://auto1.by/search', params=params, cookies=cookies, headers=headers).text
    # print(responsesearch)
    soup = BeautifulSoup(responsesearch, 'lxml')
    
    # print(soup)
    # prov = []
    i = 0
    for tr in soup.find_all('a', class_ = 'paddingStyle'):
        
        # print(tr)
            tre = tr.get_text()
            # print(tre)
            
            if brand in tre:
                i += 1
                if i <= 1:
                
                    trem = f'{tr}'
                    print(trem)
                    trem1 = trem.split('href="')[1]
                    trem2 = trem1.split('">')[0]
                    urle = f'https://auto1.by{trem2}'


                    print(urle)
            

                    cookies = {
                        'sid': 'mdzfqfrqsfdsf1jnugxclkiv',
                        'uss': 'f3013664-592e-484e-b5a5-af7eefeb1604',
                        '__RequestVerificationToken': 'ytgor4TgCKKVVsifOioSm8C7fpLSRHyyGJVnqkn1lEGzi3R0wlvJo0RCnwVlraq2HM2tdiAdLEbk58mI11SoXXECC79KxKGxtylKY1YPwso1',
                        '_gcl_au': '1.1.828200517.1712920910',
                        '_fbp': 'fb.1.1712920910383.1569263708',
                        '_ym_uid': '1712920911440191163',
                        '_ym_d': '1712920911',
                        'tmr_lvid': '83ae2c001903b1fc6aae6c26f74974b4',
                        'tmr_lvidTS': '1712920911411',
                        '_tt_enable_cookie': '1',
                        '_ttp': 'fPOE4tgO-opiyEl8Nqj3X_kNhsA',
                        '_gid': 'GA1.2.1441901532.1713243833',
                        '_ym_isad': '2',
                        'domain_sid': 'cWCIuad8T9ItflpoBTUTo%3A1713243837996',
                        'b24_sitebutton_hello': 'y',
                        'session_timer_104054': '1',
                        '_ym_visorc': 'w',
                        'was_called_in_current_session_104054': '1',
                        'seconds_on_page_104054': '536',
                        '_ga_6352MSYKNX': 'GS1.1.1713267541.6.1.1713268110.32.0.0',
                        '_ga_83HJKTVF69': 'GS1.1.1713267541.6.1.1713268113.0.0.0',
                        '_ga': 'GA1.1.48095384.1712920909',
                        '_ga_ECXG0392JW': 'GS1.1.1713267541.6.1.1713268113.0.0.0',
                        'tmr_detect': '0%7C1713268117667',
                    }

                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Connection': 'keep-alive',
                        # 'Cookie': 'sid=mdzfqfrqsfdsf1jnugxclkiv; uss=f3013664-592e-484e-b5a5-af7eefeb1604; __RequestVerificationToken=ytgor4TgCKKVVsifOioSm8C7fpLSRHyyGJVnqkn1lEGzi3R0wlvJo0RCnwVlraq2HM2tdiAdLEbk58mI11SoXXECC79KxKGxtylKY1YPwso1; _gcl_au=1.1.828200517.1712920910; _fbp=fb.1.1712920910383.1569263708; _ym_uid=1712920911440191163; _ym_d=1712920911; tmr_lvid=83ae2c001903b1fc6aae6c26f74974b4; tmr_lvidTS=1712920911411; _tt_enable_cookie=1; _ttp=fPOE4tgO-opiyEl8Nqj3X_kNhsA; _gid=GA1.2.1441901532.1713243833; _ym_isad=2; domain_sid=cWCIuad8T9ItflpoBTUTo%3A1713243837996; b24_sitebutton_hello=y; session_timer_104054=1; _ym_visorc=w; was_called_in_current_session_104054=1; seconds_on_page_104054=536; _ga_6352MSYKNX=GS1.1.1713267541.6.1.1713268110.32.0.0; _ga_83HJKTVF69=GS1.1.1713267541.6.1.1713268113.0.0.0; _ga=GA1.1.48095384.1712920909; _ga_ECXG0392JW=GS1.1.1713267541.6.1.1713268113.0.0.0; tmr_detect=0%7C1713268117667',
                        'Referer': 'https://auto1.by/search?pattern=90407',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
                        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Opera";v="108"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    response3 = requests.get(
                        urle,
                        cookies=cookies,
                        headers=headers,
                    ).text
                    soup3 = BeautifulSoup(response3, 'lxml')   
                    # print(soup3)  
                    
                    for head in soup3.find_all('head', class_ = ''): 
                        
                        he = f'{head}'
                        print(he)
                        he1 = he.split('" property="og:image"/>')[0]
                        he2 = he1.split('name="twitter:description"/>')[1]
                        he3 = he2.split('name="twitter:image"/>')[1]
                        he4 = he3.split('<meta content="')[1]
                        print(he4) 
                
                        return he4
                    
def get_analog(article, brand):

    mesim = '' 

    cookies = {
    'sid': 'mdzfqfrqsfdsf1jnugxclkiv',
    'uss': 'f3013664-592e-484e-b5a5-af7eefeb1604',
    '__RequestVerificationToken': 'ytgor4TgCKKVVsifOioSm8C7fpLSRHyyGJVnqkn1lEGzi3R0wlvJo0RCnwVlraq2HM2tdiAdLEbk58mI11SoXXECC79KxKGxtylKY1YPwso1',
    '_gid': 'GA1.2.448986056.1712920910',
    '_gcl_au': '1.1.828200517.1712920910',
    '_fbp': 'fb.1.1712920910383.1569263708',
    '_ym_uid': '1712920911440191163',
    '_ym_d': '1712920911',
    'tmr_lvid': '83ae2c001903b1fc6aae6c26f74974b4',
    'tmr_lvidTS': '1712920911411',
    'session_timer_104054': '1',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    '_tt_enable_cookie': '1',
    '_ttp': 'fPOE4tgO-opiyEl8Nqj3X_kNhsA',
    'domain_sid': 'cWCIuad8T9ItflpoBTUTo%3A1712920913347',
    'was_called_in_current_session_104054': '1',
    '_gat': '1',
    '_dc_gtm_UA-38210263-4': '1',
    '_gat_UA-238453145-1': '1',
    'seconds_on_page_104054': '416',
    '_ga': 'GA1.1.48095384.1712920909',
    'tmr_detect': '0%7C1712921370488',
    '_ga_6352MSYKNX': 'GS1.1.1712920909.1.1.1712921381.28.0.0',
    '_ga_83HJKTVF69': 'GS1.1.1712920911.1.1.1712921381.0.0.0',
    '_ga_ECXG0392JW': 'GS1.1.1712920911.1.1.1712921381.0.0.0',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'sid=mdzfqfrqsfdsf1jnugxclkiv; uss=f3013664-592e-484e-b5a5-af7eefeb1604; __RequestVerificationToken=ytgor4TgCKKVVsifOioSm8C7fpLSRHyyGJVnqkn1lEGzi3R0wlvJo0RCnwVlraq2HM2tdiAdLEbk58mI11SoXXECC79KxKGxtylKY1YPwso1; _gid=GA1.2.448986056.1712920910; _gcl_au=1.1.828200517.1712920910; _fbp=fb.1.1712920910383.1569263708; _ym_uid=1712920911440191163; _ym_d=1712920911; tmr_lvid=83ae2c001903b1fc6aae6c26f74974b4; tmr_lvidTS=1712920911411; session_timer_104054=1; _ym_isad=2; _ym_visorc=b; _tt_enable_cookie=1; _ttp=fPOE4tgO-opiyEl8Nqj3X_kNhsA; domain_sid=cWCIuad8T9ItflpoBTUTo%3A1712920913347; was_called_in_current_session_104054=1; _gat=1; _dc_gtm_UA-38210263-4=1; _gat_UA-238453145-1=1; seconds_on_page_104054=416; _ga=GA1.1.48095384.1712920909; tmr_detect=0%7C1712921370488; _ga_6352MSYKNX=GS1.1.1712920909.1.1.1712921381.28.0.0; _ga_83HJKTVF69=GS1.1.1712920911.1.1.1712921381.0.0.0; _ga_ECXG0392JW=GS1.1.1712920911.1.1.1712921381.0.0.0',
        'Referer': 'https://auto1.by/search?pattern=vx2300',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Opera";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'pattern': article,
    }

    responsesearch = requests.get('https://auto1.by/search', params=params, cookies=cookies, headers=headers).text
    # print(responsesearch)
    soup = BeautifulSoup(responsesearch, 'lxml')
    # brand = 'NGK'
    # print(soup)
    # prov = []
    i = 0
    for tr in soup.find_all('a', class_ = 'paddingStyle'):
        
        # print(tr)
            tre = tr.get_text()
            # print(tre)
            
            if brand in tre:
                i += 1
                if i <= 1:
                
                    trem = f'{tr}'
                    # print(trem)
                    trem1 = trem.split('href="')[1]
                    trem2 = trem1.split('">')[0]
                    urle = f'https://auto1.by{trem2}'


                    print(urle)

            

                    cookies = {
                        'sid': 'mdzfqfrqsfdsf1jnugxclkiv',
                        'uss': 'f3013664-592e-484e-b5a5-af7eefeb1604',
                        '__RequestVerificationToken': 'ytgor4TgCKKVVsifOioSm8C7fpLSRHyyGJVnqkn1lEGzi3R0wlvJo0RCnwVlraq2HM2tdiAdLEbk58mI11SoXXECC79KxKGxtylKY1YPwso1',
                        '_gcl_au': '1.1.828200517.1712920910',
                        '_fbp': 'fb.1.1712920910383.1569263708',
                        '_ym_uid': '1712920911440191163',
                        '_ym_d': '1712920911',
                        'tmr_lvid': '83ae2c001903b1fc6aae6c26f74974b4',
                        'tmr_lvidTS': '1712920911411',
                        '_tt_enable_cookie': '1',
                        '_ttp': 'fPOE4tgO-opiyEl8Nqj3X_kNhsA',
                        '_gid': 'GA1.2.1441901532.1713243833',
                        '_ym_isad': '2',
                        'domain_sid': 'cWCIuad8T9ItflpoBTUTo%3A1713243837996',
                        'b24_sitebutton_hello': 'y',
                        'session_timer_104054': '1',
                        '_ym_visorc': 'w',
                        'was_called_in_current_session_104054': '1',
                        'seconds_on_page_104054': '536',
                        '_ga_6352MSYKNX': 'GS1.1.1713267541.6.1.1713268110.32.0.0',
                        '_ga_83HJKTVF69': 'GS1.1.1713267541.6.1.1713268113.0.0.0',
                        '_ga': 'GA1.1.48095384.1712920909',
                        '_ga_ECXG0392JW': 'GS1.1.1713267541.6.1.1713268113.0.0.0',
                        'tmr_detect': '0%7C1713268117667',
                    }

                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                        'Connection': 'keep-alive',
                        # 'Cookie': 'sid=mdzfqfrqsfdsf1jnugxclkiv; uss=f3013664-592e-484e-b5a5-af7eefeb1604; __RequestVerificationToken=ytgor4TgCKKVVsifOioSm8C7fpLSRHyyGJVnqkn1lEGzi3R0wlvJo0RCnwVlraq2HM2tdiAdLEbk58mI11SoXXECC79KxKGxtylKY1YPwso1; _gcl_au=1.1.828200517.1712920910; _fbp=fb.1.1712920910383.1569263708; _ym_uid=1712920911440191163; _ym_d=1712920911; tmr_lvid=83ae2c001903b1fc6aae6c26f74974b4; tmr_lvidTS=1712920911411; _tt_enable_cookie=1; _ttp=fPOE4tgO-opiyEl8Nqj3X_kNhsA; _gid=GA1.2.1441901532.1713243833; _ym_isad=2; domain_sid=cWCIuad8T9ItflpoBTUTo%3A1713243837996; b24_sitebutton_hello=y; session_timer_104054=1; _ym_visorc=w; was_called_in_current_session_104054=1; seconds_on_page_104054=536; _ga_6352MSYKNX=GS1.1.1713267541.6.1.1713268110.32.0.0; _ga_83HJKTVF69=GS1.1.1713267541.6.1.1713268113.0.0.0; _ga=GA1.1.48095384.1712920909; _ga_ECXG0392JW=GS1.1.1713267541.6.1.1713268113.0.0.0; tmr_detect=0%7C1713268117667',
                        'Referer': 'https://auto1.by/search?pattern=90407',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
                        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Opera";v="108"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    response3 = requests.get(urle, cookies=cookies, headers=headers).text
                    soup3 = BeautifulSoup(response3, 'lxml')
                    soup33 = soup3.get_text()
                    # print(soup3)
                    mesi = ''
                    for tr in soup3.find_all('script', class_ = ''):
                    
                    # print(tr)
                        tre = tr.get_text()
                        tref = f'{tr}'
                        # print(tref)
                        try:
                            tre1 = tref.split('inStockStores = ')[1]
                            tre2 = tre1.replace('OpenModal(inStockStores);','')
                            # print(tre2)
                            tre3 = tre2.split('"BytesArrayImage"')[0]
                            brandanalog1 = tre3.split('"Brand":"')[1]
                            brandanalog = brandanalog1.split('","Article"')[0]
                            articleanalog1 = tre3.split('","Article":"')[1]
                            articleanalog = articleanalog1.split('","Designation"')[0]
                            price1 = tre3.split(',"Price":')[1]
                            price = price1.split(',"Prc"')[0]
                            
                            print(brandanalog,articleanalog,price)
                            if article == articleanalog and brand == brandanalog:
                                pass
                            else:
                                if 'АС Барановичи' in tre3:
                                    nal = 'Вналичии ул.Тельмана, д.64'
                                    mes = f'<b>{brandanalog}  {articleanalog}   {price} BYN   {nal}</b>\n' 
                                    mesi = mesi +mes
                                if 'Мотехс-Барановичи' in tre3:
                                    nal = 'Вналичии Мотехс'
                                    mes = f'<b>{brandanalog}  {articleanalog}   {price} BYN   {nal}</b>\n' 
                                    mesi = mesi +mes
                                if 'Армтек-Барановичи' in tre3:
                                    nal = 'Вналичии Мотехс'
                                    mes = f'<b>{brandanalog}  {articleanalog}   {price} BYN   {nal}</b>\n' 
                                    mesi = mesi +mes
                                if 'АС Барановичи 50лет ВЛКСМ' in tre3:
                                    nal = 'Вналичии Мотехс'
                                    mes = f'<b>{brandanalog}  {articleanalog}   {price} BYN   {nal}</b>\n' 
                                    mesi = mesi +mes
                                if 'АС Минск' in tre3:
                                    nal = 'Под заказ на завтра'
                                    mes = f'<b>{brandanalog}  {articleanalog}   {price} BYN   {nal}</b>\n' 
                                    mesi = mesi +mes
                                else:
                                    nal = 'Под заказ'
                                    mes = f'{brandanalog}  {articleanalog}   {price} BYN   {nal}\n' 
                                    mesi = mesi +mes
                        except:
                             pass
    return mesi
        
            
bot.polling(none_stop=True)
