BUBBLEGUM
=========
Toram info bot by SNAW/LEMONGRASSHAT

NEW FEATURES ARE COMING SOON
---------

___
Documentation: https://github.com/lemongrasshat/ToramBot/wiki  
Releases: https://github.com/lemongrasshat/ToramBot/releases
___
Features:
---------
* Decent help menu (I guess)
* Food Buff tracker which allows user to add , edit their own foods and auto removal if they leave that group
* Monster Levelling search which uses coryn.club as references
* Guides related to Refining and Statting in toram.
* Admin system to allow more than one food buff(Toram allows 2 for now ) this is to make sure user can't add more than allowed.


Current Bugs:
------------
These are the only ones that I have encountered but there might be more.Just Raise an issue on github.
* There is bug(feature?) where a Line user might not have his userID I have prevented them from using any command
and I have also added simple message to inform fixing steps. You just have to add bot as your friend and message it something to get
a popup and allow it and then bot will work fine.
* Don't use LeaveEvent to do operations on user leaving the line group because for some reason LeaveEvent doesn't provide userID. I have provided
other method in app.route which you can change it to your preference for user leaving.
* Sometimes you might see some name errors or keyerrors but don't worry it's just because I haven't handled all exceptions(yet!).

Setting up the bot: 
=========== 
If you haven't done this before you will require in between 20-40 minutes to set all this up. If you encounter an error , just message me on line or github.Don't worry you will get stuck but hey you gotta learn someway or another!  
Line ID: @snaw.gg
----------

Steps:
---
___
1. Download The source code from repository and install [git](https://git-scm.com/downloads) on your system.
___
2. Register on [Heroku](https://signup.heroku.com/) for hosting and verify your account.
___
3. Once you are in you apps dashboard go to deploy and install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
![Dashboard](https://imgur.com/L8XvJ61.png)  
___
4. Goto resources and search for PostGres in addons search and add **Heroku Postgres** to your app.  
![HerokuPostgres](https://imgur.com/nHOc3Mw.png)
___
5. Open Heroku Postgres dashboard from Resources menu and navigate to Settings > View Credentials. **Copy host,database,user,uri,password in notepad , keep it handy.**
![DB Credentials](https://imgur.com/rPLqsTB.png)
![DB Credentials](https://imgur.com/u8R86Fc.png)  
___
6. Heroku part is done! Now open Line Developers console [Line Developers console](https://developers.line.biz/console/) , if you don't have line account make one. After that log in using that account.
  
___
7. Create a provider for your bot.
![alt](https://imgur.com/NfMyEPp.png)
  
___
8. Create an **Messaging API chanel** for your your provider , you have to fill out some information , most of it can be changed later though also leave the optional part.
It should look something like this doesnt have to be similiar.
![Messageing api](https://imgur.com/EfatsI1.png)
  
___
9. Navigate to Messaging API tab and scroll down a bit further to **Line Official Account Features.**
* You want to **ALLOW** Bot to join group chat .
* **Disable**  Auto-reply Messages and **enable** webhook as below:

* **Disable** Greetings messages.  
![Disable](https://imgur.com/a9aveTt.png)
Final settings should look like this:
![FInalsettings](https://imgur.com/BGsGndU.png)
  
___
10. Navigate again to messaging api tab and scroll down bit further after Line Official Account Features and you  find a **Channel Access Token** . **Issue it and copy it in notepad** with previous Postgres details we need it later for bot to function.
  
___
11. Navigate to Basic Settings now go and scroll down further bit and copy **Channel Secret** into notepad.
  
___
12. Now we are done with all signups(however keep heroku and line developer console  tabs open) and time to setup postgres and webhook for app.
  
___
13. Download pgAdmin 4 from this [link](https://www.pgadmin.org/download/). It is graphical interface for managing postgres databases. You can use Command line interface also if you comfortable with it but for beginners this is the easy way.
  
___
14. After Installation open pgAdmin 4 from start menu. It should look like this.
![Pgadmin](https://imgur.com/0iAMq9V.png)
  
___
15. Right click on Servers under Browser Tab and **Create> Server**.
* Type whatever name you prefer in name field in general tab and **disable connect now**.
* Navigate to Connection tab . **Fill Host Name/ Address with Host we copied from heroku postgres dashboard** ( One that ends with amazonaws.com).  
*  **For Maintenance Database field copy Database field from Heroku Postgres dashboard or notepad.**
* **For Username field copy user field from Heroku Postgres dashboard or notepad.**
* We are done with connection now navigate to  SSL TAB change SSL mode from **prefer to REQUIRE.**
* After that navigate to Advanced and **find the field DB restriction and Fill it with Database from notepad or Heroku Postgres dashboard.**
* That's it make sure everything is right. Check pictures for reference below and click save.
![Maintenance Database](https://imgur.com/7bntflD.png)
![Maintenance Database](https://imgur.com/cfQaJJ0.png)
![Maintenance Database](https://imgur.com/VntnzCo.png)
![Maintenance Database](https://imgur.com/oDGsX9m.png)
  
___
16. Now you should see a new server in your Browser of pgadmin. Right click on it and connect. It will ask for password copy paste password from notepad or Heroku postgres Dashboard. If it fails that means you have input something wrong check for extra spaces and such redo step 15.  
  
___

17. After successful connection , You should see database structure.  Go to tree under database , it should have a named databased assigned to you .  It should look like this.
![iamgeafterconneciton](https://imgur.com/k66WFWs.png)
  
___

18. Now download [this](https://drive.google.com/file/d/1o26MkfPiKKxWmAai_JCxpmIzjO4hewlV/view?usp=sharing) file. It contains the SQL schema for postgres database.
  
___
19. Now right click on your **database name > Restore**
![restoreiamge](https://imgur.com/cMOmpcu.png)
  
___
20. Set format to Custom or Tar , for filename click on three dots and navigate to file you downloaded in step 18 and  **GOTO Restore Options and change Owner,priviliges to yes from do not save TAB and restore.**
![TarRestore](https://imgur.com/AVpCNUh.png)
  
___
21. If you encountered and error in step 20 make sure to check logs of that in pgadmin if it shows " role <somethingrandom> doesnt not exist" or something. Go to Database > Schemas>Public > Tables. If you are able to see **5 tables** then it's fine to move on to next step. **You can view data of all tables by right clicking and just make sure data in fuid_manager , lastfuid field is 1000** .
  
___
22. We are done with Postgres setup now final step is to setup webhook and adding connection to bot.
  
___
23. Locate the source file you downloaded in step 1 . Extract it if its in .zip format.
open the extracted folder and press shift and while *holding shift press right click on your mouse* and choose open powershell window here(or cmd) and make sure you are in extracted folder not outside of it.
![rightlick](https://imgur.com/qHQSeP2.png)
  
___
24. Now type following commands in Powershell window.(**You MUST HAVE HEROKU CLI INSTALLED OTHERWISE THIS WILL NOT WORK**) You can find all these commands in deploy tab of your app.
* > *heroku login*    
--> It will say press any key to open a browser window which should automatically open a browser window for you when after you press anything. Then log on to that page using heroku it will tell you to go back to Command Line interface aka Powershell . It should show you are logged in. 
* Type dir command to make sure you are in same directory as this picture below. Your path would be different but structure should be same as mine. Now type following commands.
![Directory](https://imgur.com/bCk5o2f.png)
* Now type follwowing command to initialize git directory:
>*git innit*  
* Now type following command  
> *heroku git:remote -a YOURAPPNAME*  
--> Your app name can be found in your [heroku app dashboard](https://dashboard.heroku.com/apps/) such as mine is bubblegumbottest so I will type " *heroku git:remote -a bubblegumbottest* ".
* Perform first push on your remote git by using commands below:
> *git add .*  
> *git commit -am "first bot push"*  
> *git push heroku master*   
  
___
* Wait for it to finish installing python and all the dependancies after that you should see that it has been deployed successfully if it shows error please check your app name .
command flow:
![commandflow](https://imgur.com/ViniBoq.png)
* Copy this url  from the powershell menu or you can just guess it by adding your appname.herokuapp.com , save it in the notepad.
![Shellpart](https://imgur.com/RCwl5EE.png)
  
___
25. Open app.py using notepad or any text editing tool. I am using Visual studio code.
* Enter **database uri** we copied earlier from heroku postgres dashboard on *ENTER YOUR POSTGRES URL HERE*
* Copy your Line **CHANNEL ACCESS TOKEN** in *ENTER YOUR CHANNEL ACCESS TOKEN HERE*
* Copy your Line **CHANNEL SECRET** in *ENTER CHANNEL SECRET HERE*
* LEAVE APPROVED GROUP ID and APPROVED ADMIN ID AS IT IS  
It should look like this:    
[Before](https://imgur.com/MN75ZOu.png)  
[After](https://imgur.com/zuXlsNu.png)
  
___
26. Now open the powershell(which you hopefully haven't closed if you have closed it then open it again in the same directory as we opened in step 23). type these commands:
> *git commit -am "Refreshing remote code after changes"*  
> *git push heroku master*  
 
These commands are used to upload/update changes to your bot on heroku.  
___

27. ONLY AFTER SUCCEEDING PREVIOUS STEP DO THIS :  
Now goto  Line developer console. Go to your Provider >Choose your messaging api
go to Messaging api tab. and scroll down till you find **Webhook settings** and click on edit.
![webhook](https://imgur.com/WvW6Krp.png)
  
___
28. Remember the url we copied from powershell that looked like this *https://bubblegumbottest.herokuapp.com* copy it and add callback after end of the url and paste it in the field
like this: *https://bubblegumbottest.herokuapp.com/callback*
now after saving you should see an extra option of verify and use webhook in webhook settings menu like [this.](https://imgur.com/en96Eg2.png)
  
___
29. Enable Use Webhook , you can clock verify it will show some error message like *this webhook returned some other error code* ignore it .
after step 29 webhook settings look like [this](https://imgur.com/ZNdmZFy).
  
___
30. We are 95% DONE . Nice job pulling through! Now it's time to make a group and add bot to group. You can add bot to group using QR code or Line ID like [this](https://imgur.com/eE6IaDL). Add bot as friend  and then add it into your [group](https://imgur.com/QW0cE6t). I am using PC version of LINE if you confused with layout , mobile shouldn't be any different.
  
___
31. Now go back to powershell and type: 
> *heroku logs --tail*  
This command will be used for debugging purpose if debugging is enabled(I have enabled it in code.)
  
___
32. Now send a random text message in the group chat and watch the output of powershell window. You should see something similiar to as below: 
![alt](https://imgur.com/aLA76Zn.png)
![request body](https://imgur.com/NO7KLV9.png) , take a better [look](https://imgur.com/NO7KLV9.png).
  
___
33. Copy userID field and groupID into our app.py program such as:
* APPROVED_GROUP_ID is replaced by groupID from powershell
* APPROVED_ADMIN_ID is replaced by from powershell.
* Final [app.py](https://imgur.com/m8CsBdY)
  
___
34. Now to update changes to remote bot on heroku type:
> *git commit -am "Final push "*  
> *git push heroku master* 
  
___
35. Wait for it to complete. And hurray we are done! You deserve a pat on back!
  
___
36. Type !help get command now . Remember to ignore <> as they are placeholders.

[IT WORKS!!](https://imgur.com/a/79JSKHs)
  
___
Documentation:
===========
Commands:

*FUID: FOOD UNIQUE IDENTIFIER* , It is required to make changes to your food using myfood commands.

1. > **!help**  
Description: Shows commands and format along with available food names.  
Usage: !help  
Output:  
___
2. > **!fs [options]**  
    Usage:  
    > * **!fs all**  
    Description : Shows all available food buff types.  
    Usage: !fs all  
    Output: 
    ___
    > * **!fs [FoodName]**  
    Description:Searches for food buffs having that certain food names  
    Usage: !fs int   
    Output:
___
3. > **!myfood [option1] [option2] [option3] [option4]**  
    Description: All users foodbuff will be managed by these commands. Some of the commands may not require to input all the options.  
    Usage:  
    > * **!myfood**  
    Description : Shows food assigned to you along with FUID.  
    Usage: !myfood    
    Output:
    ___
    
    > * **!myfood add [In_Game_Name] [Foodname] [Level]**  
    Description: Assigns a food to you. Allows multiple foods   
    Usage: !myfood add testname dex 8   
    Output:
    ___
    > * **!myfood update [FUID] [New_Level]**  
    Description : Updates your food using fuid with new level ,Level value is automatically calculated.    
    Usage: !myfood update 1999 8   
    Output:
    ___
    > * **!myfood delete [FUID]**  
    Description: Deletes your food using fuid forever.     
    Usage: !myfood delete 9999   
    Output: 
    ___
    ADMIN ONLY !myfood commands
    ---
    > * **!myfood a list**  
    Description: Shows list of food that yet to be approved.   
    Usage: !myfood a list   
    ___
    > * **!myfood accept [FUID]**  
    Description : Accept that food and automatically pushes it into database.    
    Usage: !myfood accept 9999   

    ___
    > * **!myfood reject [FUID]**  
    Description : Reject that food and automatically pushes it into database.    
    Usage: !myfood reject 9999 
___
    
4. Misc commands
    -----------
    > * **!refining**  
    Description : Shows resources related to refining.    
    Usage: !refining
    ___
    > * **!statting**  
    Description : Shows resources related to statting.    
    Usage: !statting 
    ___
    > * **!lvling [level]**  
    Description : Searches for bosses to level up from coryn.club  
    Usage: !lvling 200
    ___ 
___

Thank you!
===
Have a a good day
