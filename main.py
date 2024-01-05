import discord
import requests
import json
import sqlite3
import re
import os
import uuid
from webserver import keep_alive

bot = discord.Bot(intents=discord.Intents.all())

listt= ["♥","♦","♠","♣","♪","∞","→","↓","↑","←","✓","∆","§","¶","Ω","₹","∅","x","»","«"]


@bot.event
async def on_ready():
  db =sqlite3.connect("db.sqlite")
  c=db.cursor()
  links=" "
  c.execute("SELECT id FROM users")
  res = c.fetchone()
  if res:
      res=res[0]
      author = bot.get_user(res)
      c.execute("SELECT times FROM users WHERE id=?",  (res,))
      r=c.fetchone()[0]
      guild= bot.get_guild(1187891841660625008)
      author = guild.get_member(res)
      times = 96
      vip = discord.utils.find(lambda r: r.name == 'VIP', guild.roles)
      vipp = discord.utils.find(lambda r: r.name == 'VIP +', guild.roles)
      if vip in author.roles:
          times = 146
      elif vipp in author.roles:
          times=196
      roles = [discord.utils.find(lambda r: r.name==p, guild.roles) for p in listt]
      timesagain = 0
      for role in roles:
          if role in author.roles:
              timesagain+=300
      for i in range(r,times+timesagain):
          header={
               "accept": "*/*",
               "accept-language": "en-US,en;q=0.9",
               "content-type": "application/json",
               "sec-ch-ua": "\"Opera GX\";v=\"105\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
               "sec-ch-ua-mobile": "?0",
               "sec-ch-ua-platform": "\"Windows\"",
               "sec-fetch-dest": "empty",
               "sec-fetch-mode": "cors",
               "sec-fetch-site": "cross-site"
              }
          data={
              "partnerUserId": str(uuid.uuid4()),
              }
          try:
              datadump=json.dumps(data)
              response = requests.post("https://api.discord.gx.games/v1/direct-fulfillment", headers=header, data=datadump)
              print(response.text, response.json())
              link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{response.json()['token']}"
              links= links+f"{link} \n"
          except Exception as e:
              channel = bot.get_channel(1187895495646007336)
              await channel.send("تم العثور على مشكلة لمرة ثانية, يرجى فتح تكت في اقرب وقت.")
              break
      with open('temp_nitro.txt', 'a') as file:
          file.writelines(links)
          file.close()
      with open('temp_nitro.txt', 'rb') as f:
          await author.send(file=discord.File(f))
          f.close()
      os.remove('temp_nitro.txt')
      channel = bot.get_channel(1187895521390632960)
      await channel.send(f"تم الارسال {times} نيترو مجانا لـ {author.mention}")
      c.execute("DELETE from users WHERE id=?", (res,))
      db.commit()
      db.close()

  print(f"logged in {bot.user}")

def tax(amount):
    ptax = round(amount*5/100)

    taxx = int(round(ptax * (20) / (19) + (1)))
    return taxx


with open('proxy_list.txt', 'r') as proxy_file:
    proxies = [line.strip() for line in proxy_file.readlines()]
proxy_index = 0  # Initialize the proxy index
@bot.event
async def on_message(message):
    global proxy_index
    if message.content == "$get":
        if message.channel.id == 1187895495646007336:
            try:
                author = message.author
                await author.send("رسالة تست")
                links=" "
                times = 0
                msg = " "
                vip = discord.utils.find(lambda r: r.name == 'VIP', message.guild.roles)
                vipp = discord.utils.find(lambda r: r.name == 'VIP +', message.guild.roles)
                if vipp in message.author.roles:
                    times=196
                    msg = f"**شكراً لك لتعاملك مع خادمنا، فيحال أن خدمتنا نالت إعجابك يرجى وضع تقييمك للخدمة بـ <#1188071801272668261> <a:heart_130:1190626706600509551>  \n هل مللت من الإنتظار وتحتاج الى عدد أكثر من الروابط؟  \n يمكنك تفقد <#1188449870164541510>** \n- {author.mention} \nكعضو vip+ بالخادم، ستحصل على 100 نيترو إضافياً، سيتم ارسال الروابط الى الخاص بعد قليل."
                elif vip in message.author.roles:
                    msg = f"**شكراً لك لتعاملك مع خادمنا، فيحال أن خدمتنا نالت إعجابك يرجى وضع تقييمك للخدمة بـ <#1188071801272668261> <a:heart_130:1190626706600509551>  \n هل مللت من الإنتظار وتحتاج الى عدد أكثر من الروابط؟  \n يمكنك تفقد <#1188449870164541510>** \n- {author.mention} \n كعضو vip بالخادم، ستحصل على 50 نيترو إضافياً، سيتم ارسال الروابط الى الخاص بعد قليل."
                    times=146
                else:
                    times=96
                    msg = f"**شكراً لك لتعاملك مع خادمنا، فيحال أن خدمتنا نالت إعجابك يرجى وضع تقييمك للخدمة بـ <#1188071801272668261> <a:heart_130:1190626706600509551>  \n هل مللت من الإنتظار وتحتاج الى عدد أكثر من الروابط؟  \n يمكنك تفقد <#1188449870164541510>** \n- {author.mention}"
                roles = [discord.utils.find(lambda r: r.name==p, message.guild.roles) for p in listt]
                timesagain = 0
                for role in roles:
                    if role in author.roles:
                        timesagain+=300
                        msg= f"**شكراً لك لتعاملك مع خادمنا، فيحال أن خدمتنا نالت إعجابك يرجى وضع تقييمك للخدمة بـ <#1188071801272668261><a:heart_130:1190626706600509551>  \n هل مللت من الإنتظار وتحتاج الى عدد أكثر من الروابط؟  \n يمكنك تفقد <#1188449870164541510>** \n- {author.mention} \nبما أنك عضو مميز ولديك رمز, سوف تحصل على {timesagain} نيترو اضافياً، سيتم ارسال الروابط الى الخاص بعد قليل"
                await message.channel.send(msg)
                for i in range(times+timesagain):
                    header={
                        "accept": "*/*",
                        "accept-language": "en-US,en;q=0.9",
                        "content-type": "application/json",
                        "sec-ch-ua": "\"Opera GX\";v=\"105\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": "\"Windows\"",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "cross-site"
                    }
                    data={
                        "partnerUserId": str(uuid.uuid4()),
                    }
                    datadump = json.dumps(data)
                    current_proxy = proxies[proxy_index % len(proxies)]
                    proxy = {
                    'http': f'http://{current_proxy}'
                    }
                    try:
                        response = requests.post("https://api.discord.gx.games/v1/direct-fulfillment", headers=header, data=datadump)
                        print(response.text, response.json())
                        link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{response.json()['token']}"
                        links= links+f"{link} \n"
                        proxy_index+=1
                    except Exception as e:
                      print(e)
                      await message.channel.send("تم العثور على مشكلة. سوف يتم اعادة تشغيل البوت. (سوف تستغرق وقت اكثر.)")
                      db = sqlite3.connect("db.sqlite")
                      c=db.cursor()
                      c.execute("INSERT INTO users(id, times) VALUES(?,?)", (author.id, i,))
                      db.commit()
                      db.close()
                      with open('temp_nitro.txt', 'a') as file:
                          file.writelines(links)
                          file.close()
                      with open('temp_nitro.txt', 'rb') as f:
                          await author.send(file=discord.File(f))
                          f.close()
                      os.remove('temp_nitro.txt')
                      print(e)
                      os.system("kill 1")
                      os.system("python main.py")
                print(links)
                with open('temp_nitro.txt', 'a') as file:
                    file.writelines(links)
                    file.close()
                with open('temp_nitro.txt', 'rb') as f:
                    await author.send(file=discord.File(f))
                    f.close()
                os.remove('temp_nitro.txt')
                channel = bot.get_channel(1187895521390632960)
                await channel.send(f"تم الارسال {times} نيترو مجانا لـ {author.mention}")
            except discord.errors.Forbidden as e:
                await message.channel.send(f"{author.mention} قفلت خاصك و لهذا لا يمكنني ارسال الروابط")
        else:
            await message.channel.send("nice try, but it only works in <#1187895495646007336> :nerd:")
    elif message.content== "$help":
        embed = discord.Embed(title="Help menu", description = " ")
        embed.add_field(name="`$get`", value="لأخذ النيترو")
        embed.set_footer(text="Bot version: RELEASE V1.0 | developed by SIDAL.py")
        await message.channel.send(embed=embed)
    elif str(message.content).startswith("$buy"):
      if message.channel.name.startswith('ticket'):
          text_after_buy = message.content[len("$buy"):].strip()
          vippprice= 49999
          vipprice= 24999
          if str(text_after_buy).upper() in ['VIP +', "VIP"]:
              await message.channel.send(f"يرجى تحويل مبلغ {vippprice if str(text_after_buy).upper() == 'VIP +' else vipprice} لـ <@1174642054282883094>")
              def check(msg):
                  try:
                      price = tax(vippprice) if str(text_after_buy).upper() == "VIP +" else tax(vipprice)
                      finalprice = vippprice + price if str(text_after_buy).upper() == "VIP +" else vipprice + price
                      return msg.mentions[0].id == 1174642054282883094 and msg.author.id == 282859044593598464 and str(round(finalprice)) in msg.content 
                  except IndexError:
                      return False
              await bot.wait_for('message', check=check)
              role = discord.utils.find(lambda r: r.name == str(text_after_buy).upper(), message.guild.roles)

              await message.author.add_roles(role)
              await message.channel.send("شكرًا للاشتراء من خادمنا, تم منحك الرتبة بنجاح ! ✅")
          else:
              await message.channel.send("الرجاء اختيار رتبة من القائمة التالية: VIP +, VIP")
      else:
          await message.channel.send("لا يمكنك الشراء في الرومات الاخرى الا بالتكتتات")
    elif str(message.content).startswith("$give"):
        if message.author.id in [994347081294684240, 1174642054282883094, 856181442011070485]:
          try:
              pattern = r'\$give\s+<@!?(\d+)>\s+(\d+)'
              match = re.match(pattern, message.content)
              user= " "
              times = 0
              if match:
                  user = match.group(1)
                  times = match.group(2)
                  print(times)
                  print(user)
                  if int(times) <= 0:
                      await message.channel.send("لا يمكنك اعطاء كمية سالبة او معدومة !")
                  else:
                        await message.channel.send("جاري اعطاء نيترو للمستخدم")
                        print(times)
                        links= " "
                        for i in range(int(times)):
                          print(int(times))
                          print(i)
                          header={
                              "accept": "*/*",
                              "accept-language": "en-US,en;q=0.9",
                              "content-type": "application/json",
                              "sec-ch-ua": "\"Opera GX\";v=\"105\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
                              "sec-ch-ua-mobile": "?0",
                              "sec-ch-ua-platform": "\"Windows\"",
                              "sec-fetch-dest": "empty",
                              "sec-fetch-mode": "cors",
                              "sec-fetch-site": "cross-site"
                           }
                          data= {
                              "partnerUserId": str(uuid.uuid4()),
                          }
                          datadump = json.dumps(data)
                          response = requests.post("https://api.discord.gx.games/v1/direct-fulfillment", headers=header, data=datadump)
                          print(response)
                          print(response.text, response.json())
                          link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{response.json()['token']}"
                          links= links+f"{link} \n"
                        author = bot.get_user(int(user))
                        with open('temp_nitro.txt', 'a') as file:
                          file.writelines(links)
                          file.close()
                        with open('temp_nitro.txt', 'rb') as f:
                          await author.send(file=discord.File(f))
                          f.close()
                        os.remove('temp_nitro.txt')
              else:
                  await message.channel.send("invalid format, $give @user <amount>")
          except Exception as e:
                await message.channel.send("invalid format, $give @user <amount>")
        else:
            await message.channel.send("هذه الكوماند موجودة للادمين بس :nerd:")
        
keep_alive()
try:
  bot.run("MTE4Nzg5OTk5MTcwOTE5MjI2Mg.G0FoZO.z6pY8sLkw1S1vXzQxtat04bUXDGZ-MWv5yGa_g")
except discord.errors.HTTPException:
  os.system("kill 1")
  os.system("python main.py")
