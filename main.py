import telebot
import requests

API_KEY = '5658169924:AAE4mAeZY1p2WFG7OeO5jbd2uNqGxVHGTus'
bot = telebot.TeleBot(API_KEY)

c = 27

def get_request(message):
    return True

@bot.message_handler(func=get_request)
def send_info(message):
  global c
  print('Request no. ' + str(c) + ' by ' + message.from_user.first_name + '. Request: ' + message.text)
  c = c+1
  userinput = message.text
  if userinput[0] == '/':
    return
  output = ""
  if '\n' in userinput:
      output = 'Bad input'
  elif userinput.isdigit():
    api_url = "https://api.postalpincode.in/pincode/" + userinput
    response = requests.get(api_url).json()[0]
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
    api_url = "https://api.postalpincode.in/postoffice/" + userinput
    response = requests.get(api_url).json()[0]
    if response['Status'] == 'Error':
      output = 'Place not recognised'
    elif int(response['Message'].split(':')[-1]) > 100:
      counter = 0
      output = 'Too many results ('+response['Message'].split(':')[-1]+'), showing the first fifty\n'
      for x in response['PostOffice']:
        counter = counter+1
        output = output+ x['Name'] + ': ' + x['Pincode'] + '\n'
        if counter == 50:
          break
    else:
      output = response['Message'] + '\n'
      for x in response['PostOffice']:
        output = output+ x['Name'] + ': ' + x['Pincode'] + '\n'
  bot.send_message(message.chat.id, output)

bot.polling()
