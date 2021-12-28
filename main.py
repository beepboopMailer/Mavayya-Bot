
import discord
import random
import os
from keep_online import keep_alive
from googletrans import Translator
from boothulu import bad_words
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from buddyreads import *


'''quiz_questions={
  "What is the capital of Sweden?": "Stockholm",
  "What is the largest state in India?": "Rajasthan",
  "Patagonia is in which continent?": "South America",
  "Who won the FIFA world cup in 2010?": "Spain",
  "Who wrote the secret history?": "Donna Tart"
}'''


def mavayyaCalled(mess):
  mavayya=["Mavayya","mavayya","Mamayya","mavayya"]
  for i in mavayya:
    if i in mess:
      return True
  return False



def mavayyaQuote(mess,username):
  mavayya_maatalu=[
  f"entira {username} chusi kuda chudanattu velthunav...bagunava?",
  "manushulu manchollu ra, manashi antene manchodu!",
  "oka samanyudiga emi ivagalamu ra e samajaniki prema tho kudina oka kutumbam thappa...",
  "nuvvu, ee server nadipevallu, ee server ni abhimaaninche vallu, andaru baagundali ra!",
  "chakkaga oka navvu navvithe, meeku baguntundi, naku baaguntundi :grin:",
  "https://tenor.com/view/smile-prakash-raj-gif-reactions-mahesh-babu-gif-19508343",
  "aa bhagavantudni mana gurinchi korukovalsina avasaram em ledu ra... ala korukunte pakkodi gurinchi korukuvali :pray:",
  f"bhagavantudaa, nijayiti ga brathike {username} ni chiru navvu nunchi dooram cheyyaku...",
  f"yera {username} ela unnav, bagunnava?",
  "mee andarini ila server lo chutunte, entha haayi ga undho...",
  f"yera {username} , bhojanam chesava?",
  f"ఏరా {username}, నీ లిస్ట్ లో నుండి తీసేశావా నన్ను?",
  f"ఒరేయి {username}, దేవుణ్ణి ఏం కోరుకున్నావు రా?",
  f"అరేయి {username}, దాటగలిగే కష్టాల్నీనీ, ఆ కష్టాల్ని దాటే ధైర్యాన్నీ ఇవ్వమని దేవుణ్ణి అడగరా!"
  ]
 
  return random.choice(mavayya_maatalu)


def Cursed(mess):
 
  for i in bad_words:
    if i in mess.casefold().split():
      return True
  return False


def YadminReq(mess):
  admin=["admin","admeen","aadmin","yadmin","mod","mawd"]
  for i in admin:
    if "make" in mess.split() and i in mess.split():
      return True 
  return False




intents = discord.Intents.default()
intents.members = True
intents.emojis=True
intents.reactions=True


client=discord.Client(intents=intents)

telugu=Translator()


prog={}

@client.event
async def on_message(message):
  
  username=(message.author.nick) if message.author.nick else str(message.author).split("#")[0]

  global quizProgress
  quizProgress=False
  global ques
  ques=True
  mess=message.content

  if message.author==client.user:
    return

  if mavayyaCalled(mess):
    await message.channel.send(mavayyaQuote(mess,username))

  if Cursed(mess):
    await message.channel.send(f"yenti ra {username}, yemitaa maatalu?")
  
  #displays the avatar
  if mess == "-avatar":
    await message.channel.send(message.author.avatar_url)


  if YadminReq(mess):
    await message.channel.send("Provide aadhar card, 10th class participation certificate, 2 passport size photos, then mod exam pass ga... Then interview pass ga... Internship ippistha.")


  if message.channel.id==923256242481266708:
    tel=telugu.translate(mess,src='en',dest='te')
    await message.channel.send(tel.text)
   
  if mess=="call the cops":
    await message.channel.send("ee maatram daaniki kaapulu chowdarilu enduku le amma")

  if mess[0:2]=="!m":
    mes=mess[3::]
    recs=mes.split(',')

    await message.channel.send(random.choice(recs))

  
  if message.channel.id==900145851844935681 or message.channel.id==911854338803109929 or message.channel.id==876497506849144892:
    if mess.startswith("!br"):
      try:
        temp = eval(BuddyRead(mess.strip(), username)())
        # print(temp)
        msg = await message.channel.send(temp["content"], embed = discord.Embed.from_dict(temp["embeds"][-1]))
        await msg.add_reaction("✅")
        await message.delete()
      except Exception as e:
        await message.channel.send("Sorry, couldn't process Buddy read request. Exception: {}".format(e))

  elif mess[0:2]=="!b":
    spl=mess.split()

    gr_link=spl[1]
    book_page=urlopen(gr_link)
    gr_parser=BeautifulSoup(book_page,'html.parser')
    body=gr_parser.find('div',class_='readable stacked')
    des=body.find_all('span')
 
    await message.channel.send(des[1].text)

  
  '''if mess=="mama start quiz":
    if quizProgress==False:
      quizProgress=True
  if mess=="mama stop quiz":
    if quizProgress==True:
      quizProgress=False

  if mess=="1":
    if quizProgress:
      if ques:
        questions=list(quiz_questions.keys())
        q=random.choice(questions)
        ques=False
        await message.channel.send(q)
        
      else:
        if mess==list(quiz_questions[q]):
          await message.channel.send("correct answer")''''

  
  
      
    
 



#welcome message when a member joins
@client.event
async def on_member_join(member):
  if member.guild.id == 876134376247820308:
    time.sleep(1)
    channel = client.get_channel(890388908813213727)
    roles=client.get_channel(876485505192165396)
    await channel.send(f"ఏమ్మా {member.mention} బాగున్నావా? ఏ పుస్తకం చదువుతున్నావు ఈ మధ్య?\n**అలాగే full server access కావాలంటే {roles.mention} లో \"🔓\" option దొరుకుతుంది చూడు!**")

'''@client.event
async def on_message_delete(message):
  time.sleep(5)
  botspam=client.get_channel(876497595441229824)
  await botspam.send("ye ra, nee thappulanni ila lokaniki thelikunda daachestunnava?")'''


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent): 
  hall_of_fame=client.get_channel(911854338803109929)
  mess = await client.fetch_message(payload.message_id)
  if mess.reactions=="⭐":

    user = client.get_user(payload.user_id)

    pop=discord.Embed(title=f"{mess}",color=user.color)
    pop.set_author(name=f"{user}",icon_url=user.avatar_url)

    await hall_of_fame.send(f"{user.mention}, reacted with {payload.emoji}")
    #await hall_of_fame.send(embed=pop)
    




#keeping the bot online
my_secret = os.environ['TOKEN']
keep_alive()
client.run(my_secret)

