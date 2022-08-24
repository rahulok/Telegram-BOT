from firebase import firebase
import telebot
import requests
from pytz import timezone
from datetime import datetime

API_KEY = 'TGAPIKEY'
try:
    bot = telebot.TeleBot(API_KEY)
    f = firebase.FirebaseApplication('https://tg-bot-hidingtheurl',None)
except:
    print('Some error occured while connecting to api')
c = 187

def get_request(message):
    return True

try:
    @bot.message_handler(func=get_request)
    def send_info(message):
      userinput = message.text
      if userinput[0] == '/':
        return
      global c
      c = c+1
      ind_time = str(datetime.now(timezone("Asia/Kolkata")).strftime("%m-%d-%Y %H:%M:%S"))

      data = {
      'ReqNo' : str(c),
      'Request': message.text,
      'User' : message.from_user.first_name,
      'Time': ind_time
      }
      f.post('/Requests',data)
      print('Request no. ' + str(c) + ' by ' + message.from_user.first_name + ' Request: ' + message.text)

      output = ""
      if userinput.isdigit():
        try:
          api_url = "https://api.postalpincode.in/pincode/" + userinput
          response = requests.get(api_url).json()[0]
        except:
          output = 'Bad input'
          bot.send_message(message.chat.id, output)
          return
        if response['Status'] == 'Error':
          output = 'Enter a valid pin'
        else:
          output = 'State: ' + response['PostOffice'][0]['State'] + '\n'
          output = output + response['Message'] + '\n'
          for x in response['PostOffice']:
            output = output+ x['Name'] + '\n'
      elif len(userinput)<3:
        output = "That's a really short city"
      else:
        try:
          api_url = "https://api.postalpincode.in/postoffice/" + userinput
          response = requests.get(api_url).json()[0]
        except:
          output = 'Bad input'
          bot.send_message(message.chat.id, output)
          return
        if response['Status'] == 'Error':
          output = 'Place not recognised'
        elif int(response['Message'].split(':')[-1]) > 100:
          counter = 0
          output = 'Too many results ('+response['Message'].split(':')[-1]+'), showing the first fifty\n'
          for x in response['PostOffice']:
            counter = counter+1
            output = output+ x['Name'] + '(' + x['State'] + ')' + ': ' + x['Pincode'] +'\n'
            if counter == 50:
              break
        else:
          output = response['Message'] + '\n'
          for x in response['PostOffice']:
            output = output+ x['Name'] + '(' + x['State'] + ')' + ': ' + x['Pincode'] +'\n'
      bot.send_message(message.chat.id, output)
except:
    print('Some error occured')

try:
    bot.polling()
except:
    print('Some error occured while pooling')
