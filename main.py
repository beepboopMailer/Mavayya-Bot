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
from andari_kavitha import *
from hangMan import Hangman 
from english_words import english_words_lower_alpha_set
from botm import *



'''quiz_questions={
  "What is the capital of Sweden?": "Stockholm",
  "What is the largest state in India?": "Rajasthan",
  "Patagonia is in which continent?": "South America",
  "Who won the FIFA world cup in 2010?": "Spain",
  "Who wrote the secret history?": "Donna Tart"
}'''
from quote import quote

def mavayyaCalled(mess):
    mavayya = ["Mavayya", "mavayya", "Mamayya", "mavayya"]
    for i in mavayya:
        if i in mess:
            return True
    return False


def mavayyaQuote(mess, username):
    mavayya_maatalu = [
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
    admin = ["admin", "admeen", "aadmin", "yadmin", "mod", "mawd"]
    for i in admin:
        if "make" in mess.split() and i in mess.split():
            return True
    return False

def listToString(s): 
    # initialize an empty string
    str1 = "" 
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    # return string  
    return str1 


intents = discord.Intents.default()
intents.members = True
intents.emojis = True
intents.reactions = True

client = discord.Client(intents=intents)

telugu = Translator()

prog = {}

#hangman=Hangman()

@client.event
async def on_message(message):

    username = (message.author.nick) if message.author.nick else str(message.author).split("#")[0]

    global quizProgress
    quizProgress = False
    global ques
    ques = True
    mess = message.content
    
    
   
    
    if message.author == client.user:
        return

    

    elif mavayyaCalled(mess):
        await message.channel.send(mavayyaQuote(mess, username))

    elif Cursed(mess):
        await message.channel.send(f"yenti ra {username}, yemitaa maatalu?")

    #displays the avatar
    elif mess == "-avatar":
        await message.channel.send(message.author.avatar_url)

    elif YadminReq(mess):
        await message.channel.send(
            "Provide aadhar card, 10th class participation certificate, 2 passport size photos, then mod exam pass ga... Then interview pass ga... Internship ippistha."
        )

    elif message.channel.id == 923256242481266708:
        tel = telugu.translate(mess, src='en', dest='te')
        await message.channel.send(tel.text)

    elif mess == "call the cops":
        await message.channel.send(
            "ee maatram daaniki kaapulu chowdarilu enduku le amma")

    elif mess.lower().strip().startswith("!mecho"):
        mess = mess.lower().strip()[6:].strip(" \n")
        # print(mess)
        channelid, mess = mess.split(" ",1)
        # print(client.get_channel(int(channelid.strip(">#<"))))
        await client.get_channel(int(channelid.strip(">#<"))).send(mess)

    elif mess[0:2] == "!m":
        mes = mess[3::]
        recs = mes.split(',')

        await message.channel.send(random.choice(recs))

    elif mess.strip(" \n").lower().startswith("!q"):
      
      mess_ = mess.strip(" \n").lower().strip("!q")
      if not mess_:
        mess_ = random.choice(["love", "life", "inspire", "humor", "good", "truth"])
      q_ = {"quote": ""}
      quotes = quote(search = mess_,limit=random.randint(1,100))
      if quotes:
        try:
          while not q_["quote"]:
            q_ = random.choice(quotes)
            if len(q_["quote"])>1900:
              q_ = {"quote": ""}
          await message.channel.send("'{}' \n ---- \n {} : {}".format(q_["quote"], q_["author"], q_["book"]))
        except Exception as e:
          print(e,quotes, sep = "\n")
      else:
        await message.channel.send("couldn't get quote for search term {}. \n try with another term".format(mess_))

    elif message.channel.id in GlobVariables.channels:
      await get_kavitha(message)


    elif mess.startswith("!botm"):
      # l=mess.strip()
      l = mess.strip().split(" ", 1)
      gr_link=l[-1]
      b=BOTM(gr_link)
      b.setDetails()
      await message.channel.send(b.botm["title"])

    elif mess.strip(" \n").lower().startswith("!b"):
      mess = mess.strip(" \n").lower()
      try:
        temp = eval(BuddyRead(mess.strip(), username)())
        # print(temp)
        embed=discord.Embed.from_dict(temp["embeds"][-1])
      except Exception as exc_:
        await message.channel.send(
            "Sorry, couldn't process Book request. Exception: {}"
            .format(exc_))
      if mess.startswith("!br") and (message.channel.id in [900145851844935681, 911854338803109929, 876497506849144892]):
          try:
            msg = await message.channel.send(temp["content"],
                                                  embed=embed)
            await msg.add_reaction("✅")
            await message.delete()
          except Exception as exc_:
                await message.channel.send(
                    "Sorry, couldn't process Buddy read request. Exception: {}"
                    .format(exc_))
      else:
        embed.remove_field(1) #end date
        embed.remove_field(0) #start date
        msg = await message.channel.send("ఇదిగో, ఈ పుస్తకం చదువుకో",
                                                  embed=embed)

    
    
      
    '''elif mess=="m.hangman" and message.channel.id==911854338803109929:
      
      await message.channel.send("Game started!")
      
    
      
    
      
    if hangman.began==True and message.channel.id==911854338803109929:
      if hangman.wordSolved(hangman.dash)==False:
        await message.channel.send(listToString(hangman.guess(hangman.word,hangman.dash,hangman.chances,mess)))
        hangman.chances-=1
        if  hangman.wordSolved(hangman.dash)==True:
          await message.channel.send("You won!")
        if hangman.chances==0:
          await message.channel.send(f"You ran out of chances! The word was {hangman.word}.")
          hangman.began=False
      else:
        hangman.began=False'''
        







#welcome message when a member joins
@client.event
async def on_member_join(member):
    if member.guild.id == 876134376247820308:
        time.sleep(1)
        channel = client.get_channel(890388908813213727)
        roles = client.get_channel(876485505192165396)
        await channel.send(
            f"ఏమ్మా {member.mention} బాగున్నావా? ఏ పుస్తకం చదువుతున్నావు ఈ మధ్య?\n**అలాగే full server access కావాలంటే {roles.mention} లో \"🔓\" option దొరుకుతుంది చూడు!**"
        )


'''@client.event
async def on_message_delete(message):
  time.sleep(5)
  botspam=client.get_channel(876497595441229824)
  await botspam.send("ye ra, nee thappulanni ila lokaniki thelikunda daachestunnava?")'''


@client.event
async def on_raw_reaction_add(payload):
    hall_of_fame = client.get_channel(911854338803109929)
    channel=client.get_channel(payload.channel_id)
    mess = await channel.fetch_message(payload.message_id)
    user = mess.author
    # print(mess.reactions)
    stars = [x for x in mess.reactions if (x.emoji == "⭐")]
    if stars and stars[-1].count==2:
        pop = discord.Embed(title=f"{mess.content}", color=user.color)
        pop.set_author(name=f"{user}", icon_url=user.avatar_url)
        await hall_of_fame.send(embed=pop)

@client.event
async def on_ready():
  await client.get_channel(911854338803109929).send("Nen online ochesa")

#keeping the bot online

from itertools import cycle
from discord.ext import tasks
status = cycle(['with Python','JetHub'])

@client.event
async def on_ready():
  change_status.start()
  print("Your bot is ready")

@tasks.loop(seconds=30)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))


my_secret = os.environ['TOKEN']
keep_alive()
client.run(my_secret)
