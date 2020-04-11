This bot was made on fsATC: https://discord.gg/XdymmEj
DM peeeeeta#4718 on discord for questions and suggestions

Make sure you edit the config.py to suit your server or else it wont work. The way the bot works is when you DM it will create a ticket in the category you set up in config.py. The ticket creator cannot see that channel but anything sent in that channel will be sent to the user. After the user created the ticket anything sent in the users dms to the bot will be sent to that channel. Make sure you set permissions for the category. For example if you only want staff to see the channel in the category perms set @everyone to denied for read messages and see channels and allow staff to see it. The reason the bot DMs back and forth is so that users who can see the ticket for example staff can make comments that the ticket creator cannot see. Comments are used by %%message. Once the ticket is closed by .solve or .close the user can create a ticket again by messaging the bot. 

PM means private message (PM For Support Bot)

Also when setting the ranks to true make sure you edit the rele names by ctrl + f on the bot.py file and searching role to find where the roles are held to change. The default ones include, Admin, Moderator...