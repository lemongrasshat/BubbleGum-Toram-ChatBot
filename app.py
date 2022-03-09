
'''

█▓▒░░BUBBLEGUM░░▒▓█ 

This is Toram Info bot made by SNAW.

FEATURES:
#Food buff system to track food buffs. Auto deletion after user leaves the group.
#Info search for statting and refining
#Searching for bosses around same level using Coryn.club data

If you encountered any error(that is not solvable by simple debugging) Contact me :
Line ID: @snaw.gg
or just message me on github.

You are free to do changes as you please.

'''
import os
import requests
import psycopg2
from flask import Flask, request, abort
from bs4 import BeautifulSoup
import re
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

#
# █▓▒░░EDIT BELOW░░▒▓█
#   █ # and ''' represents comments
#   █ DONT FORGET THE QUOTATION MARKS
#   !
line_bot_api = LineBotApi('ENTER YOUR CHANNEL ACCESS TOKEN HERE')
handler = WebhookHandler('ENTER CHANNEL SECRET HERE')
DATABASE_URL = "ENTER YOUR POSTGRES URL HERE"
APPROVED_GROUP_ID=["ENTER YOUR GROUP IDS HERE"] # These are group id where your bot will work
APPROVED_ADMIN_ID=["ENTER YOUR ADMIN IDS HERE"] # These are admin userId
#   !
#   █
#   █ 
#
# To add new feature of levelling 
# for recommendaed and add materials searching command
# New Levelling command(not implemented): !lvling2 [current] [achieved] have to add limits
# Material search command : !mats materailsname/shortform(m/w/med/b)
# █▓▒░░EDIT ABOVE░░▒▓█


app = Flask(__name__)
app.debug=True #for debugging purposes

class bubblegum:
    def __init__(self) -> None:
        self.GROUP_ID=None
        self.USER_ID=None
        self.CURRENT_ERRORS=[]
        self.CURRENTMAXLEVEL=235
        self.foodnames=["ACCURACY","AGI","AGGRO+","AGGRO-","AMPR","ATK","CRIT","DARK_RES","DEX","DEF","DODGE","DROP_RATE","EARTH_RES","EXP_GAIN","FRAC_BARRIER",
        "FIRE_RES","HP","INT","LIGHT_RES","MAGIC_BARRIER","MAGIC_RES","MATK","MDEF","MP","PHYS_BARRIER","PHY_RESIST","STR","SA_DARK","SA_EARTH","SA_FIRE",
        "SA_LIGHT","SA_NEUTRAL","SA_WATER","SA_WIND","WATER_RES","WEAP_ATK"]
        #If you have changed values in foodnames make sure to change it in FoodValueCalculator function too
        self.commands=["!fs","!help","!myfood","!statting","!refining","!Fs","!Help","!Myfood","!Statting","!Refining","!FS","!HELP","!MYFOOD","!STATTING","!mats","!MATS","!Mats"]
        self.MaterialTerms=["mana","m","beast","b","medicine","med","cloth","c","metal","met","wood","w"]
        self.Commands1=[
        "\n□□□□□□□□□□□□□□□", 
        "\n⭕ !fs <food name>",
        "\n➡ Searches for Food buff",
        "\n➡ Example: !fs int",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n⭕ !lvlyt <lvl-number>",
        "\n➡ Searches for mobs from popular youtubers data list",
        "\n➡ Example: !lvlyt 230",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n⭕ !lvl <lvl-number>",
        "\n➡ Searches for boss and miniboss on coryn",
        "\n➡ Example: !lvl 230",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n⭕ !mats <material_name>",
        "\n➡ 🆕 Shows Farming spots for materials: mana(m),medicine(med),cloth(c),beast(b),metal(met),wood(w)",
        "\n➡ Example(both short and long form works!): !mats mana or !mats m",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n⭕ !refining",
        "\n➡ Shows refining guide",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n⭕ !statting",
        "\n➡ Shows statting guide and sim.",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        
        "\n⭕ !myfood",
        "\n➡ Shows Your foodbuffs",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n⭕ !myfood delete <fuid>",
        "\n➡ Deletes your food forever",
        "\n➡ Example: !myfood delete 9999",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n⭕ !myfood add <IGN> <FoodName> <Level>",
        "\n➡ Adds your food ",
        "\n➡ Example: !myfood add testname drop_rate 3",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n⭕ !myfood update <fuid> <newlevel>",
        "\n➡ Updates your food",
        "\n➡ Example: !myfood update 9999 8"
        "\n■■■■■■■■■■■■■■■■■■\n",

        ]
        self.commandfoodname="\nAllowed Food Names: ACCURACY , AGI , AGGRO+ , AGGRO- , AMPR, ATK , CRIT , DARK_RES , DEX , DEF, DODGE , DROP_RATE , EARTH_RES , EXP_GAIN , FRAC_BARRIER , FIRE_RES , HP , INT , LIGHT_RES , MAGIC_BARRIER , MAGIC_RES , MATK , MDEF , MP , PHYS_BARRIER , PHY_RESIST , STR , SA_DARK , SA_EARTH , SA_FIRE , SA_LIGHT , SA_NEUTRAL , SA_WATER , SA_WIND,WATER_RES,WEAP_ATK" 
        self.commands2=[
        "\n ========== ",
        "\n 🔐Admin only🔐 ",
        "\n ========== ",
        "\n□□□□□□□□□□□□□□□",
        "\n🔐!myfood a list",
        "\n➡ Shows list of yet to be approved food",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n🔐!myfood approve <fuid>",
        "\n➡ Approves the food",
        "\n■■■■■■■■■■■■■■■■■■\n",
        "\n□□□□□□□□□□□□□□□",
        "\n🔐 !myfood reject <fuid>",
        "\n➡ Removes it from approval list"
        "\n■■■■■■■■■■■■■■■■■■\n",
        ]
    def getHTMLdocument(self,url):
        response = requests.get(url)
        return response.text

    def InformBotFix(self,replyTK):
        #This is function to inform some people who don't have id they can do it following Fixtext Method.
        FixText='''You can't access bot commands try the fix below:
        Bot fix:
        Add Bot as friend.
        Message it something if popup comes allow it or sometimes nothing may appear both ways are fine
        If you are unable to access site then use vpn'''
        line_bot_api.reply_message(replyTK,TextSendMessage(text=FixText))

    def CorynDataColletor_level(self,lvlvalue):
        #method to get data from coryn.club : Information portal for toram .
        #I am not including experience data in finaltext but you can add it if you want.
        finaltext=""
        try:
            url = "https://coryn.club/leveling.php?lv={0}".format(lvlvalue)  
            html_document = self.getHTMLdocument(url)
            soup = BeautifulSoup(html_document, 'html.parser')
            text=soup.find_all("div",{"class":"table-grid item-leveling"})
            #Boss Data extractor 
            levelsoup=BeautifulSoup(str(text[0]),'html.parser')
            bossdata=levelsoup.find_all("div",{"class":"level-row"},limit=4)
            finaltext+="Bosses\n=================\n"
            for bossitems in bossdata:
                bosssoup=BeautifulSoup(str(bossitems),'html.parser')
                BossName=""
                BossLevel=""
                ExpData=""
                for item in bosssoup.find_all("div",{"class":"level-col-2"}):
                    BossName=item.get_text()

                for item in bosssoup.find_all("div",{"class":"level-col-1"}):
                    BossLevel=item.get_text()

                for item in bosssoup.find_all("div",{"class":"level-col-3"}):
                    ExpData=item.get_text()
                #finaltext+="\n"+"Name:"+BossName.strip()+"\n"+"Level:"+BossLevel.strip()+"\n"+"Experience:"+ExpData.strip()+"\n"
                finaltext+="\n"+"Name:"+BossName.strip()+"\n"+"Level:"+BossLevel.strip()+"\n"

            #miniboss data extractor
            levelsoup=BeautifulSoup(str(text[1]),'html.parser')
            bossdata=levelsoup.find_all("div",{"class":"level-row"},limit=4)
            finaltext+="\nMiniBosses\n=================\n"
            for bossitems in bossdata:
                bosssoup=BeautifulSoup(str(bossitems),'html.parser')
                BossName=""
                BossLevel=""
                ExpData=""
                for item in bosssoup.find_all("div",{"class":"level-col-2"}):
                    BossName=item.get_text()

                for item in bosssoup.find_all("div",{"class":"level-col-1"}):
                    BossLevel=item.get_text()

                for item in bosssoup.find_all("div",{"class":"level-col-3"}):
                    ExpData=item.get_text()
                #finaltext+="\n"+"Name:"+BossName.strip()+"\n"+"Level:"+BossLevel.strip()+"\n"+"Experience:"+ExpData.strip()+"\n"
                finaltext+="\n"+"Name:"+BossName.strip()+"\n"+"Level:"+BossLevel.strip()+"\n"
            return finaltext
        except Exception:
            return "ERROR_LEVELLING_DATA"

    def GetLevelValue(self,SearchInquiry):
        SplitSearchInquiry=self.QueryCleaner(SearchInquiry)
        if(len(SplitSearchInquiry)>2):
            return "ERROR_LEVELLING_DATA"
        elif(SplitSearchInquiry[1].isdigit()==True):
            if(int(SplitSearchInquiry[1])>0 ):
                return SplitSearchInquiry[1]
        else:
            return "ERROR_LEVELLING_DATA"

    def ValidFoodNameChecker(self,food_name):
        #Checks if foodname is valid you can change those names in foodnames list above
        if food_name in self.foodnames:
            return True
        else:
            return False

    
    def LevellingQueryValidator(self,SplitSearchInquiry):
        length=len(SplitSearchInquiry) 
        if(length==2):
            if(SplitSearchInquiry[0]=="!lvlyt"):
                if(SplitSearchInquiry[1].isdigit()==True):
                    if(int(SplitSearchInquiry[1])<=self.CURRENTMAXLEVEL and int(SplitSearchInquiry[1])>0):
                        return True
                    else:
                        self.CURRENT_ERRORS.append("Enter level number between 1-"+str(self.CURRENTMAXLEVEL))
                        return False
                else:
                    self.CURRENT_ERRORS.append("Number is not digit!")
                    return False
        elif(length>2):
            if(SplitSearchInquiry[0]=="!lvlyt"):
                self.CURRENT_ERRORS.append("⚠ There are some 👉extra  fields in your command! Proper query is   ▶ !lvlyt <Number> ◀\n")
                return False
            else:
                self.CURRENT_ERRORS.append("ERROR_LVLVYT_NOTPROPER")
                return False
        else:
            self.CURRENT_ERRORS.append("⚠ There are some 👉missing  fields in your command! Proper query is   ▶ !lvlyt <Number> ◀ \n")
            return False
    
    def PopularLevellingManager(self,Searchquery):
        #!lvlyt function 
        SplitSearchInquiry=self.QueryCleaner(Searchquery)
        if(self.LevellingQueryValidator(SplitSearchInquiry)==True):
            text=self.PopularLevellingCollector(int(SplitSearchInquiry[1]))
            return text 
        else:
            if "ERROR_LVLVYT_NOTPROPER" in self.CURRENT_ERRORS:
                pass 
            else:
                ErrorText=""
                for errors in self.CURRENT_ERRORS:
                    ErrorText+=errors
                return ErrorText
            
    def MaterialQueryValidator(self,SplitSearchInquiry):
        length=len(SplitSearchInquiry)
        if(length==2):
            if(SplitSearchInquiry[0]=="!mats"):
                if(SplitSearchInquiry[1] in self.MaterialTerms):
                    return True
                else:
                    self.CURRENT_ERRORS.append("Please Enter Valid Material search query proper terms are :\n mana(m),medicine(med),cloth(c),beast(b),metal(met),wood(w)")
                    return False
        elif(length>2):
            if(SplitSearchInquiry[0]=="!mats"):
                self.CURRENT_ERRORS.append("⚠ There are some 👉extra  fields in your command! Proper query is   ▶ !mats <material_name> ◀\n")
                return False
            else:
                self.CURRENT_ERRORS.append("ERROR_MATS_NOTPROPER")
                return False
        else:
            self.CURRENT_ERRORS.append("⚠ There are some 👉missing  fields in your command! Proper query is   ▶ !mats <material_name> ◀ \n")
            return False

    def MatsDataCollector(self,MatType):

        if(MatType=="m"):
            MatType="mana"
        elif(MatType=="med"):
            MatType="medicine"
        elif(MatType=="met"):
            MatType="metal"
        elif(MatType=="c"):
            MatType="cloth"
        elif(MatType=="b"):
            MatType="beast"
        elif(MatType=="w"):
            MatType="wood"    

        text=""
        text+="Material Farming Spots\n"
        text+="\n"
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        try:
            Query="""select * from "matfarm" where matfarm."Type" = %s  """
            curr.execute(Query,(MatType,))
            Result=curr.fetchall()
            if not Result:
                return "Error While searching_emp"
            else:
                for row in Result:
                    text+="===================\n"
                    text+="Mob: " +str(row[1])+"\n"+"Location: " +str(row[2])+"\n"+"Best Farmer: " +str(row[3])+"\n"+"Popularity: "+str(row[4])+"\n"+"Availability: "+str(row[6])
                    text+="\n=+=+=+=+=+=+=+=+=+=+\n\n"
                return text
        except psycopg2.Error as e:
            app.logger.info(e)
            return "Error While searching"
        finally:
            curr.close()
            conn.close()

    def MaterialQueryManager(self,Searchquery):
        SplitSearchInquiry=self.QueryCleaner(Searchquery)
        if(self.MaterialQueryValidator(SplitSearchInquiry)==True):
            text=self.MatsDataCollector(SplitSearchInquiry[1])
            return text
        else:
            if "ERROR_MATS_NOTPROPER" in self.CURRENT_ERRORS:
                pass 
            else:
                ErrorText=""
                for errors in self.CURRENT_ERRORS:
                    ErrorText+=errors
                return ErrorText
    
    
    def PopularLevellingCollector(self,level):
        # BELOW CODE IS TO BALANCE OUT LEVEL VALUES
        #Food search query function
        #!lvlyt function 
        text=""
        text+="===================\n"
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        try:
            
            Query="""select * from toram_levelling_data where %s between lvlmin and lvlmax order by lvlmax desc limit 3;"""
            curr.execute(Query,(level,))
            Result=curr.fetchall()
            if not Result:
                return "Error While searching_emp "
            else:
                for row in Result:
                    text+="Level: " +str(row[0])+" - "+str(row[1])+"\n"+" Mob: " +str(row[2])+"\n"+" Location: " +str(row[3])+"\n"+" Description: " +str(row[4])
                    text+="\n------------------\n"
                return text
        except psycopg2.Error as e:
            return "Error While searching"
        finally:
            curr.close()
            conn.close()

    def SearchQueryResult(self,food_name):
        #Food search query function
        text=""
        text+="===================\n"
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        try:
            Query="""select * from fuid_fooddata where food_name=%s order by foodlvl desc limit 5"""
            curr.execute(Query,(food_name,))
            Result=curr.fetchall()
            if not Result:
                return "No food found! ಥ_ಥ"
            else:
                for row in Result:
                    Query="""select * from fuid_user_ign where fuid=%s"""
                    curr.execute(Query,(row[0],))
                    FuidResult=curr.fetchone()
                    text+="IGN: "+FuidResult[2]+"\nFoodName: "+row[1]+"\nFood Level: "+str(row[2]) +"\nFood Value: "+str(row[3])+"\n"
                    text+="\n------------------\n"
                return text
        except:
            return "Error While searching"
        finally:
            curr.close()
            conn.close()
        
    def GetFoodAvailableType(self):
        #Extra function to see all the food data available.
        #Suggesstion of Zeal
        text=""
        text+="Available Food Type:"
        text+="\n=================\n"
        FoodNamesList=[]
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        try:
            Query="""select food_name from fuid_fooddata"""
            curr.execute(Query)
            Result=curr.fetchall()
            for row in Result:
                if row[0] not in FoodNamesList:
                    FoodNamesList.append(row[0])
            for items in FoodNamesList:
                text+=items+"\n"
            return text
        except:
            return "Error while searching code:41023"

    def SearchQueryManager(self,SearchInquiry):
        SplitSearchInquiry=self.QueryCleaner(SearchInquiry)
        length=len(SplitSearchInquiry)
        if(length==2):
            if(SplitSearchInquiry[0].isdigit()==False and SplitSearchInquiry[1].isdigit()==False):
                if(SplitSearchInquiry[0].lower()=="!fs"):
                    if(self.ValidFoodNameChecker(SplitSearchInquiry[1].upper())==True):
                        text=self.SearchQueryResult(SplitSearchInquiry[1].upper())
                        return text
                    elif(SplitSearchInquiry[1]=="all"):
                        text=self.GetFoodAvailableType()
                        return text
                    elif(self.ValidFoodNameChecker(SplitSearchInquiry[1].upper())==False):
                        text="⚠ Not a valid foodname . type !help for foodnames ◀ "
                        return text
        elif(length>2):
            text="⚠ There are some 👉extra  fields in your command! Proper query is   ▶ !fs <foodname> ◀ or ▶ !fs all ◀\n"
            return text
        else:
            text="⚠ There are some 👉missing  fields in your command! Proper query is   ▶ !fs <foodname> ◀ or ▶ !fs all ◀\n"
            return text

    def GetCurrentFuid(self):
        #This method is used to get FUID to automate FUID
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        try:
            #Query = "select * from food_Data where food_name like %s limit 5"
            Query="select * from \"fuid_manager\""
            curr.execute(Query)
            result=curr.fetchall()
            if not result:
                return "No food! :("
            else:
                CurrentFuid=0
                for row in result:
                    CurrentFuid=int(row[0])
                return CurrentFuid
        except:
            return 0
        finally:
            curr.close()
            conn.close()

    def FoodValueCalculator(self,foodlvl, foodname):
        #Calculate FoodValue for foodlvl
        #If you have changed values in foodnames make sure to change it in FoodValueCalculator function too
        cur_fn = foodname
        if cur_fn == "STR" or cur_fn == "AMPR" or  cur_fn == "AGI" or cur_fn == "VIT" or cur_fn == "INT" or cur_fn == "DEX" or cur_fn == "CRIT" or cur_fn == "DARK_RES" or cur_fn == "WATER_RES" or cur_fn == "EARTH_RES" or cur_fn == "LIGHT_RES" or cur_fn == "FIRE_RES" or cur_fn == "WIND_RES" :
            new_fl = int(foodlvl)
            if new_fl < 5 :
                foodlvl = new_fl * 2
                return foodlvl
            else:
                foodlvl = 4 * new_fl - 10
                return foodlvl
        elif cur_fn == "MAGIC_BARRIER" or cur_fn == "PHY_BARRIER" or cur_fn == "HP" :
            new_fl = int(foodlvl)
            if new_fl < 5 :
                foodlvl = new_fl * 400
                return foodlvl
            else:
                foodlvl = 600 * new_fl - 1000
                return foodlvl    
        elif cur_fn == "ATK" or cur_fn == "MATK" or cur_fn == "DODGE" or cur_fn == "ACCURACY" or cur_fn == "WEAP_ATK" or cur_fn == "AGGRO+" or cur_fn == "AGGRO-" :
            new_fl = int(foodlvl)
            if new_fl < 5 :
                foodlvl = new_fl * 6
                return foodlvl
            else:
                foodlvl = 14 * new_fl - 40
                return foodlvl
        elif cur_fn == "MP" :
            new_fl = int(foodlvl)
            if new_fl < 5 :
                foodlvl = new_fl * 60
                return foodlvl
            else:
                foodlvl = 140 * new_fl - 400
                return foodlvl
        elif cur_fn == "EXP_GAIN" or cur_fn == "DROP_RATE" or cur_fn == "SA_FIRE" or cur_fn == "SA_WATER" or cur_fn == "SA_EARTH" or cur_fn == "SA_WIND" or cur_fn == "SA_LIGHT" or cur_fn == "SA_DARK" or cur_fn == "SA_NEUTRAL" :
            new_fl = int(foodlvl)
            if new_fl < 5 :
                foodlvl = new_fl
                return foodlvl
            else:
                foodlvl = new_fl * 2 - 5
                return foodlvl
        elif cur_fn == "DEF" or cur_fn == "MDEF" :
            new_fl = int(foodlvl)
            if new_fl < 5 :
                foodlvl = new_fl * 20
                return foodlvl
            else:
                foodlvl = 40 * new_fl - 100
                return foodlvl
        elif cur_fn == "PHY_RESIST" or cur_fn == "MAGIC_RES" :
            new_fl = int(foodlvl)
            if new_fl < 5 :
                foodlvl = new_fl * 4
                return foodlvl
            else:
                foodlvl = 6 * new_fl - 10
                return foodlvl

    def IsFuidValid(self,query):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        #app.logger.info(query)
        try:
            #Query = "select * from food_Data where food_name like %s limit 5"
            Query="""select * from fuid_user_ign where fuid=%s"""
            curr.execute(Query,(query,))
            FuidList=curr.fetchall()
            #app.logger.info(FuidList)
            if not FuidList:
                #app.logger.info("not in fuidlist")
                #app.logger.info(FuidList)
                return False
            else:
                #app.logger.info("in fuidlist")
                #app.logger.info(FuidList)
                return True
        except psycopg2.Error as e:
            return False
        finally:
            curr.close()
            conn.close()

    def IsFuidValidInApprovalList(self,query):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        #app.logger.info(query)
        try:
            #Query = "select * from food_Data where food_name like %s limit 5"
            Query="""select * from fuid_approval_table where fuid=%s"""
            curr.execute(Query,(query,))
            FuidList=curr.fetchall()
            if not FuidList:
                return False
            else:
                return True
        except psycopg2.Error as e:
            return False
        finally:
            curr.close()
            conn.close()        

    def IsUseridInDatabase(self,userid):
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        try:
            #Query = "select * from food_Data where food_name like %s limit 5"
            Query="""select * from fuid_user_ign where userid=%s"""
            curr.execute(Query,(userid,))
            FuidList=curr.fetchall()
            if not FuidList:
                return False
            else:
                return True
        except psycopg2.Error as e:
            return False
        finally:
            curr.close()
            conn.close()

    def MyFoodQueryHandler(self,CleanQuery):
        '''I am checking actual query on length based first then actually
            checking with matching template
            so that's why first check is length.
            It's kind of dumb approach tho
        '''
        length=len(CleanQuery)
        #app.logger.info(CleanQuery)
        if length==1:
            #this is query-> !myfood
            #Used to show query bound to userID
            text=""
            text+="Your Food"
            text+="\n===============\n"
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            curr=conn.cursor()
            try:
                #Query = "select * from food_Data where food_name like %s limit 5"
                Query="""select * from fuid_user_ign where userid like %s """
                curr.execute(Query,(self.USER_ID,))
                FuidList=curr.fetchall()
                if not FuidList:
                    return "No food assigned to you! :( Type !help for commands and more"
                else:
                    for row in FuidList:
                        Query="""select * from fuid_fooddata where fk_fuid like %s """
                        curr.execute(Query,(row[0],))
                        QueryResult=curr.fetchone()
                        text+="IGN: "+row[2] +"\nFuid: "+QueryResult[0]+"\nFood_name: "+QueryResult[1]+"\nFoodlvl: "+str(QueryResult[2])+"\nFoodvalue: "+str(QueryResult[3])+"\n"
                        text+="----------------\n"
                    return text
            except psycopg2.Error as e:
                return "ERROR_MYFOOD_SEARCH"
            finally:
                curr.close()
                conn.close()
        elif(CleanQuery[1].lower()=="update"):
            #this is query-> !myfood update <fuid> <lvl>
            #Used to update your food
            QueryName=CleanQuery[1].lower()
            IsUpdateDone=True
            if self.IsFuidValid(CleanQuery[2])==False:
                return "Fuid Doesn't exist! unless you got a time machine! ( ´･_･)ﾉ(._.`)"
            elif(QueryName=="update"):
                IntFoodlvl=int(CleanQuery[3])
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                curr=conn.cursor()
                try:
                    #Query = "select * from food_Data where food_name like %s limit 5"
                    #add method to get food name
                    Query="""select * from fuid_user_ign where (userid=%s and fuid=%s) """
                    curr.execute(Query,(self.USER_ID,CleanQuery[2],))
                    FuidList=curr.fetchone()
                    if not FuidList:
                        IsUpdateDone=False
                        return "Don't Try to update others value! ಠ_ಠ "
                    else:
                        Query="""select * from fuid_fooddata where fk_fuid=%s"""
                        curr.execute(Query,(CleanQuery[2],))
                        FoodList=curr.fetchone()
                        IntFoodValue=self.FoodValueCalculator(IntFoodlvl,FoodList[1])
                        Query="""update fuid_fooddata set foodlvl=%s,foodvalue=%s where fk_fuid=%s"""
                        curr.execute(Query,(IntFoodlvl,IntFoodValue,CleanQuery[2],))
                except psycopg2.Error as e:
                    IsUpdateDone=False
                finally:
                    if IsUpdateDone==True:
                        conn.commit()
                    curr.close()
                    conn.close()
                if(IsUpdateDone==True):
                    return "Update Completed!"
                else:
                    return "Update Failed!"
            else:
                return "Wrong update query format. Type !help for commands"
        elif(CleanQuery[1].lower()=="add"):
                #this is query-> !myfood add <ign> <fuid> <lvl>
                #Used to add your food
                #It also checks if you already have one so adding two requires admin persion
                #which you can add in APPROVED_ADMIN_ID at line 13
                QueryName=CleanQuery[1].lower()
                if self.IsUseridInDatabase(self.USER_ID):
                    FoodName=CleanQuery[3].upper()
                    IntFoodLevel=int(CleanQuery[4])
                    NewFuid=self.GetCurrentFuid()
                    NewFuid=int(NewFuid)
                    NewFuid=NewFuid+1
                    FoodValue=self.FoodValueCalculator(IntFoodLevel,FoodName)
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    IsCommitSuccessfullyDone=True
                    curr=conn.cursor()
                    try:
                        #Query = "select * from food_Data where food_name like %s limit 5"
                        strFuid=str(NewFuid)
                        Query="""UPDATE fuid_manager SET lastfuid=%s"""
                        curr.execute(Query,(NewFuid,))
                        #Query = "select * from food_Data where food_name like %s limit 5"
                        Query="""INSERT INTO fuid_approval_table(fuid, userid, ign, food_name, foodlvl, foodvalue) VALUES (%s, %s, %s, %s, %s, %s)"""
                        curr.execute(Query,(NewFuid,self.USER_ID,CleanQuery[2].lower(),CleanQuery[3].upper(),IntFoodLevel,FoodValue,))
                    except psycopg2.Error as e:
                        IsCommitSuccessfullyDone=False
                        return "Error While adding"+e.pgerror+e.diag.message_detail
                        #return "ERROR_MYFOODQUERYHANDLER_INSERT"
                    finally:
                        if(IsCommitSuccessfullyDone==True):
                            conn.commit()
                        curr.close()
                        conn.close()
                    if(IsCommitSuccessfullyDone==True):
                        Successtext="It seems you have one or more food in database however you need approval of captain or snaw to add extra food! ᕦ(ò_óˇ)ᕤ , Don't worry your food has been added in approval database (✿◡‿◡) Better tag them. \nYOUR FUID:"+str(NewFuid)+ "\n"
                        return Successtext
                    else:
                        Failedtext="It seems you have one or more food in database however you need approval of captain or snaw to add extra food! ᕦ(ò_óˇ)ᕤ , \n (╯‵□′)╯︵┻━┻ also your food wasn't added in approval database\n"
                        return Failedtext
                else:
                    FoodName=CleanQuery[3].upper()
                    IntFoodLevel=int(CleanQuery[4])
                    NewFuid=self.GetCurrentFuid()
                    NewFuid=int(NewFuid)
                    NewFuid=NewFuid+1
                    FoodValue=self.FoodValueCalculator(IntFoodLevel,FoodName)
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    IsCommitSuccessfullyDone=True
                    curr=conn.cursor()
                    try:
                        #Query = "select * from food_Data where food_name like %s limit 5"
                        strFuid=str(NewFuid)
                        Query="""INSERT INTO fuid_user_ign(fuid, userid, ign) VALUES (%s, %s, %s)"""
                        curr.execute(Query,(strFuid,self.USER_ID,CleanQuery[2].lower(),))
                        Query="""UPDATE fuid_manager SET lastfuid=%s"""
                        curr.execute(Query,(NewFuid,))
                        #Query = "select * from food_Data where food_name like %s limit 5"
                        Query="""INSERT INTO fuid_fooddata(fk_fuid, food_name, foodlvl, foodvalue) VALUES (%s, %s, %s, %s)"""
                        curr.execute(Query,(NewFuid,CleanQuery[3].upper(),IntFoodLevel,FoodValue,))
                    except psycopg2.Error as e:
                        IsCommitSuccessfullyDone=False
                        return "Error While adding (´。＿。｀)"
                        #return "ERROR_MYFOODQUERYHANDLER_INSERT"
                    finally:
                        if(IsCommitSuccessfullyDone==True):
                            conn.commit()
                        curr.close()
                        conn.close()
                    if(IsCommitSuccessfullyDone==True):
                        return "Food has been added! (⌐■_■)"
                    else:
                        return "Food isn't added! (´。＿。｀)"
        elif(CleanQuery[1].lower()=="delete"or CleanQuery[1].lower()=="remove" or CleanQuery[1].lower()=="reject" or CleanQuery[1].lower()=="approve" or CleanQuery[1].lower()=="a"):
            #this is query-> !myfood delete <fuid>
            #this deletes the fuid food
            # I have provided validation to make sure only right user deletes the food
            QueryName=CleanQuery[1].lower()
            if(QueryName=="delete" or QueryName=="remove"):
                if(self.IsFuidValid(CleanQuery[2])==True):
                    IsDeleted=True
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    curr=conn.cursor()
                    try:
                        Query="""select * from fuid_user_ign where (userid=%s and fuid=%s) """
                        curr.execute(Query,(self.USER_ID,CleanQuery[2],))
                        FuidList=curr.fetchone()
                        if not FuidList:
                            IsDeleted=False
                            return "Don't Try to delete others food! ಠ_ಠ "
                        else:
                            Query="""delete from fuid_user_ign where fuid=%s"""
                            curr.execute(Query,(CleanQuery[2],))
                    except psycopg2.Error as e:
                        IsDeleted=False
                        return "Error While deleting"+e.pgerror+e.diag.message_detail
                    finally:
                        if IsDeleted==True:
                            conn.commit()
                        curr.close()
                        conn.close()
                    if(IsDeleted==True):
                        return "Food Deleted!(hope that was intentional) ( •_•)>⌐■-■ "
                    else:
                        return "Food Deletion failed successfullly!(That wasn't intentional) (•_•)"
                else:
                    return "Fuid not in databse! (>_<)"
            elif(QueryName=="approve" and self.VerifyAdminId(self.USER_ID)==True):
                #app.logger.info("WE ARE IN THIS LOOp")
                if(self.IsFuidValidInApprovalList(CleanQuery[2])==True):
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    curr=conn.cursor()
                    IsApproved=True
                    try:
                        Query="""select * from fuid_approval_table where fuid=%s"""
                        curr.execute(Query,(CleanQuery[2],))
                        FuidList=curr.fetchone()
                        if not FuidList:
                            return "Maybe Recheck FUID （*゜ー゜*） "
                        else:

                            Query="""INSERT INTO fuid_user_ign(fuid, userid, ign) VALUES (%s, %s, %s)"""
                            curr.execute(Query,(FuidList[0],FuidList[1],FuidList[2],))

                            Query="""INSERT INTO fuid_fooddata(fk_fuid, food_name, foodlvl, foodvalue) VALUES (%s, %s, %s, %s)"""
                            Strlvl=str(FuidList[4])
                            Strval=str(FuidList[5])
                            #app.logger.info("Stringlvl:"+Strlvl)
                            #app.logger.info("Stringval:"+Strval)
                            curr.execute(Query,(FuidList[0],FuidList[3],Strlvl,Strval,))

                            Query="""DELETE FROM fuid_approval_table where fuid=%s"""
                            curr.execute(Query,(FuidList[0],))
                            IsApproved=True
                    except Exception as e:
                        IsApproved=False
                        return "Error While Approving!"
                    finally:
                        if(IsApproved==True):
                            conn.commit()
                        curr.close()
                        conn.close()
                    if(IsApproved):
                        return "Food has been approved! (⌐■_■)"
                    else:
                        return "Food has been not approved(unintentional)! ( •_•)>⌐■-■"
                else:
                    return "Fuid not in approval list! (>_<)"
            elif(QueryName=="reject" and self.VerifyAdminId(self.USER_ID)==True):
                if(self.IsFuidValidInApprovalList(CleanQuery[2])==True):
                    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                    curr=conn.cursor()
                    IsRejected=True
                    try:
                        Query="""select * from fuid_approval_table where fuid=%s"""
                        curr.execute(Query,(CleanQuery[2],))
                        FuidList=curr.fetchone()
                        if not FuidList:
                            return "Maybe Recheck FUID （*゜ー゜*） "
                        else:
                            Query="""DELETE FROM fuid_approval_table where fuid=%s"""
                            curr.execute(Query,(FuidList[0],))
                            IsRejected=True
                    except Exception as e:
                        IsRejected=False
                        return "Error While Rejecting an Approval!"
                    finally:
                        if(IsRejected==True):
                            conn.commit()
                        curr.close()
                        conn.close()
                    if(IsRejected):
                        return "Food has been Rejected! (⌐■_■)"
                    else:
                        return "Food has been not Rejected (unintentional)! ( •_•)>⌐■-■ "
                else:
                    return "Fuid not in approval list! (>_<)"

            else:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                curr=conn.cursor()
                try:
                    #Query = "select * from food_Data where food_name like %s limit 5"
                    Query="""select * from fuid_approval_table"""
                    curr.execute(Query,())
                    result=curr.fetchall()
                    if not result:
                        return "Nothing for approval! ヾ(⌐■_■)ノ♪ "
                    else:
                        text="Approval Pending List \n================"
                        for row in result:
                            text+="\n"+"FUID: "+row[0]+"\n"+"IGN: "+row[2]+"\n"+"Food Name: "+row[3]+"\n"+"Food Level: "+str(row[4])+"\n--------------\n"
                        #text+="IGN:"+row[0]+"\n"
                        return text
                except psycopg2.Error as e:
                        return "Error While searching approval list"
                finally:
                    curr.close()
                    conn.close()
        else:
            return "Wrong query format. Type !help for commands final"



    def MyfoodValidator(self,text):
        if(text[0]=="!myfood"):
            length=len(text)
            if(length==1):
                return True
            elif(text[1].isdigit()==True):
                self.CURRENT_ERRORS.append("🔻 Not a valid !myfood command.\n")
                return False
            elif(text[1].lower()=="add"):
                if(length==5):
                    #length is right for query
                    if(self.ValidFoodNameChecker(text[3].upper())):
                        #foodname is valid
                        if(text[4].isdigit() and int(text[4])<=10 and int(text[4])>0):
                            #all valid
                            return True
                        else:
                            self.CURRENT_ERRORS.append(" ⚠ Level is not right it must be in between 1-10\n")
                    else:
                        #doing all errors at once rather than one at a time
                        if(not(text[4].isdigit() and int(text[4])<=10 and int(text[4])>0)):
                            self.CURRENT_ERRORS.append("⚠ Level is not right it must be in between 1-10\n")
                        self.CURRENT_ERRORS.append("\n ⚠ Food Name is not valid! type !help to see food name\n")
                elif(length>5):
                    self.CURRENT_ERRORS.append("⚠  There are some 👉extra fields in your command! Proper query is  ▶ !myfood add <youringamename> <foodname> <lvl> ◀\n")
                else:
                    self.CURRENT_ERRORS.append("⚠ There are some 👉missing  fields in your command! Proper query is  ▶ !myfood add <youringamename> <foodname> <lvl> ◀\n")
                return False
            elif(text[1].lower()=="delete" or text[1].lower()=="remove" or text[1].lower()=="reject" or text[1].lower()=="approve" or text[1].lower()=="a"):
                if(length==3):
                    LCQueryText=text[1].lower()
                    if(LCQueryText=="delete" or LCQueryText=="remove"):
                        #Delete query should be !myfood delete <NUMBER>
                        if(text[2].isdigit()==True):
                            #Fuid follows standard
                            return True
                        else:
                            self.CURRENT_ERRORS.append("⚠ FUID must be a number! Proper query is : ▶ !myfood delete <fuid> ◀\n")
                            return False
                    elif(LCQueryText=="reject" or LCQueryText=="approve"):
                        if(text[2].isdigit()==True):
                            #Fuid follows standard
                            return True
                        else:
                            self.CURRENT_ERRORS.append("⚠ FUID must be a number! Proper query is : ▶ !myfood reject/approve <fuid> ◀\n")
                            return False
                    elif(LCQueryText=="a" ):
                        if(text[2].lower()=="list"):
                            return True
                        else:
                            self.CURRENT_ERRORS.append("⚠ Command is ▶ !myfood a list ◀ \n")
                            return False
                elif(length>3):
                    self.CURRENT_ERRORS.append("⚠  There are some 👉extra fields in your command! Proper query is  ▶ !myfood delete <fuid> ◀ or  ▶ !myfood accept/reject <fuid> ◀ or  ▶ !myfood a list> ◀\n")
                else:
                    self.CURRENT_ERRORS.append("⚠ There are some 👉missing  fields in your command! Proper query is  ▶ !myfood delete <fuid> ◀ or  ▶ !myfood accept/reject <fuid> ◀ or  ▶ !myfood a list> ◀\n") 
            elif(text[1].lower()=="update"):
                if(length==4):
                    if(text[2].isdigit()):
                        #fuid is number
                        if(text[3].isdigit() and int(text[3])>0 and  int(text[3])<10):
                            #lvl is number and valid
                            return True
                        else:
                            self.CURRENT_ERRORS.append(" ⚠ Level is not right it must be in between 1-10\n")
                    else:
                        self.CURRENT_ERRORS.append("⚠ FUID must be a number! Proper query is : ▶ !myfood update <fuid> <newlevel> ◀\n")
                        if(not (text[3].isdigit() and int(text[3])>0 and  int(text[3])<10)):
                            self.CURRENT_ERRORS.append(" ⚠ Level is not right it must be in between 1-10\n")
                elif(length>4):
                    self.CURRENT_ERRORS.append("⚠  There are some 👉extra fields in your command! Proper query is  ▶ !myfood update <fuid> <newlevel> ◀\n")
                else:
                    self.CURRENT_ERRORS.append("⚠ There are some 👉missing  fields in your command! Proper query is  ▶ !myfood update <fuid> <newlevel> ◀\n")    
                return False
            else:
                self.CURRENT_ERRORS.append("🔻 Not a valid !myfood command.\n")
                return False
                
    def MyFoodQueryManager(self,text):
        CleanQuery=self.QueryCleaner(text)
        #app.logger.info(CleanQuery)
        if self.MyfoodValidator(CleanQuery):
            text=self.MyFoodQueryHandler(CleanQuery)
            return text
        else:
            ErrorText=""
            for errors in self.CURRENT_ERRORS:
                ErrorText+=errors
            return ErrorText



    def GetGuideData(self,guide_id):
        #For some reason I couldn't get it to work on %s parameter if someone can work around that I would be happy
        #It will just add extra if else and try catch blocks.
        text=""
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        if guide_id=="STATTING_GUIDE":
            try:
                Query = "select * from \"toram_data\" where \"ID\" = 'STATTING_GUIDE'"
                curr.execute(Query)
                result=curr.fetchall()
                if not result:
                    return "Guide not found! :( " +Query
                else:
                    for row in result:
                        text+=str(row[1])
                    return text
            except psycopg2.Error as e:
                return "ERROR_INVALID_QUERY_GUIDE"
            finally:
                curr.close()
                conn.close()
        elif guide_id=="REFINE_GUIDE":
            try:
                Query = "select * from \"toram_data\" where \"ID\" = 'REFINE_GUIDE'"
                curr.execute(Query)
                result=curr.fetchall()
                if not result:
                    return "Guide not found! :( " +Query
                else:
                    for row in result:
                        text+=str(row[1])
                    return text
            except psycopg2.Error as e:
                return "ERROR_INVALID_QUERY_GUIDE"
            finally:
                curr.close()
                conn.close()
        else:
            curr.close()
            conn.close()

    def GuideQueryManager(self,SearchInquiry):
        SplitSearchInquiry=self.QueryCleaner(SearchInquiry)
        if(len(SplitSearchInquiry)>1):
            text="ERROR_INVALID_QUERY_GUIDE"
            return text
        elif(SplitSearchInquiry[0]=="!statting" or SplitSearchInquiry[0]=="!Statting"):
            text=self.GetGuideData("STATTING_GUIDE") #ACTUAL PRIMARY KEY IN DB
            return text
        elif(SplitSearchInquiry[0]=="!refining" or SplitSearchInquiry[0]=="!Refining"):
            text=self.GetGuideData("REFINE_GUIDE") #ACTUAL PRIMARY KEY IN DB
            return text
        else:
            text="ERROR_INVALID_QUERY_GUIDE"
            return text

    fieldnames=['in_game_name','food_name','food_lvl','food_value']

    def VerifyClientGroupId(self,id):
        if(id in APPROVED_GROUP_ID):
            return True
        else:
            return False

    def VerifyAdminId(self,id):
        if(id in APPROVED_ADMIN_ID):
            return True
        else:
            return False

    def QueryCleaner(self,text):
        ReplacedWhitespacetext=re.sub("\s+"," ",text)
        ReplacedWhitespacetext.strip()
        SplitReplacedWhitespacetext="".join(ReplacedWhitespacetext).split()
        return SplitReplacedWhitespacetext

    def Deleteleaveuser(self,id):
        app.logger.info("in func:"+id)
        IsDeleted=True
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        curr=conn.cursor()
        try:
            Query="""select * from fuid_user_ign where userid=%s """
            curr.execute(Query,(id,))
            FuidList=curr.fetchone()
            if not FuidList:
                app.logger.info("No user food registered")
            else:
                Query="""delete from fuid_user_ign where userid=%s """
                curr.execute(Query,(id,))
        except psycopg2.Error as e:
            IsDeleted=False
            #app.logger.info("deletetion aerror")
        finally:
            if IsDeleted==True:
                conn.commit()
            curr.close()
            conn.close()

Bubblegum = bubblegum()
@app.route("/callback", methods=['POST'])
def callback():
    NouserID=True
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    body2 = request.get_json()
    app.logger.info("Request body: " + body) #It shows request body enable debug= true at start of the program. Enabled by default

    if(str(body2['events'][0]['type'])=="memberLeft"):
        #To manage LeaveEvent
        '''for some reason the LeaveEvent present in line message api doesnt return 
            userid after user leaves the group So don't use the leaveevent. If 
            you want to do operations on certain user ,add your code below.
        '''
        leavingUserID=str(body2['events'][0]['left']['members'][0]['userId'])
        Bubblegum.Deleteleaveuser(leavingUserID)
    elif(str(body2['events'][0]['type'])=="memberJoined"):
        #if player joins the group greet him with this.
        app.logger.info("New Member Joined")
        ReplyToken=body2['events'][0]['replyToken']
        NewUserMessage="Thank you for joining AA . I am bot for BubbleGum . I track food buffs and provide additional help . Check my commands using !help"
        line_bot_api.reply_message(ReplyToken,TextSendMessage(text=NewUserMessage)
                    )
        
    else:
        try:   
            Bubblegum.GROUP_ID=str(body2['events'][0]['source']['groupId'])
        except KeyError:
            app.logger.info("KEYERROR groupid")
            #use is messaging the bot rather than typing message.
        try:
            Bubblegum.USER_ID=str(body2['events'][0]['source']['userId'])
        except KeyError:
            NouserID=False
            MsgText=str(body2['events'][0]['message']['text'])
            for text in Bubblegum.commands:
                if(text in MsgText):
                    Bubblegum.InformBotFix(str(body2['events'][0]['replyToken']))
                    break
        #app.logger.info("Keyerror userid")
        #app.logger.info("!done")
    #Get the group id for verification
    # #app.logger.info(body2['events'][0]['source']['groupId'])
    # Handle webhook body
    try:
        if NouserID==True:
            handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK' 


@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    if Bubblegum.VerifyClientGroupId(Bubblegum.GROUP_ID)==True:
        msg =(event.message.text).lower()
        if "!help" in msg:
            NewText=Bubblegum.QueryCleaner(msg)
            if(len(NewText)==1 and NewText[0]=="!help"):
                content="COMMANDS\n"
                admincontent="ADMIN COMMANDS\n"
                for items in Bubblegum.Commands1:
                    content+=str(items)
                content+="\n"+Bubblegum.commandfoodname
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
                #admin content below
                '''for items in Bubblegum.commands2:
                    admincontent+=str(items)
                line_bot_api.push_message(Bubblegum.GROUP_ID,TextSendMessage(text=admincontent),)'''
            Bubblegum.CURRENT_ERRORS.clear()
        elif "!lvlyt" in msg:
            content=Bubblegum.PopularLevellingManager(msg)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            Bubblegum.CURRENT_ERRORS.clear()

        elif "!lvl" in msg:
            stringvalue=Bubblegum.GetLevelValue(msg)
            if(stringvalue!="ERROR_LEVELLING_DATA"):
                content=Bubblegum.CorynDataColletor_level(int(stringvalue))
                if(content !="ERROR_LEVELLING_DATA"):
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            Bubblegum.CURRENT_ERRORS.clear()
        elif "!myfood" in msg:
            content=Bubblegum.MyFoodQueryManager(msg)
            if(content!="ERROR_INVALID_COMMAND"):
                line_bot_api.reply_message(
                        event.reply_token,TextSendMessage(text=content)
                    )
            Bubblegum.CURRENT_ERRORS.clear()
        elif "!fs" in msg:
            content = Bubblegum.SearchQueryManager(msg)
            if content != "ERROR_INVALID_QUERY":
                line_bot_api.reply_message(
                    event.reply_token,TextSendMessage(text=content)
                )
            Bubblegum.CURRENT_ERRORS.clear()
        elif "!mats" in msg:
            content=Bubblegum.MaterialQueryManager(msg)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
            Bubblegum.CURRENT_ERRORS.clear()
        elif "!statting" or "!refining" in msg:
            content=Bubblegum.GuideQueryManager(msg)
            if content!="ERROR_INVALID_QUERY_GUIDE":
                line_bot_api.reply_message(
                    event.reply_token,TextSendMessage(text=content)
                )
            Bubblegum.CURRENT_ERRORS.clear()
        
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
