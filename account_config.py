'''
Created on 16 Nov 2016

@author: mozat
'''
raw_accounts =  '''
https://www.instagram.com/wendyslookbook/
https://www.instagram.com/thesartorialist/
https://www.instagram.com/solsolstreet/
https://www.instagram.com/asianstreetfashion/
https://www.instagram.com/majorstreetstyle/
https://www.instagram.com/ootd.indonesiaa/
https://www.instagram.com/streetmag/
https://www.instagram.com/street_style_paris/
https://www.instagram.com/tsangtastic
https://www.instagram.com/hapatime
https://www.instagram.com/alexcloset
https://www.instagram.com/thestreetograph
https://www.instagram.com/tlnique
https://www.instagram.com/ashleighdmello
https://www.instagram.com/petiteflowerpresents
https://www.instagram.com/poppy_shmy
https://www.instagram.com/streetstyled/
https://www.instagram.com/streetper/
https://www.instagram.com/songofstyle
https://www.instagram.com/chrisellelim
https://www.instagram.com/imjennim
https://www.instagram.com/alealimay
https://www.instagram.com/chiaraferragni/
https://www.instagram.com/queenhorsfall
https://www.instagram.com/yunastyle
https://www.instagram.com/halopeoplekr
https://www.instagram.com/jdinkoreasince2012
https://www.instagram.com/realstreet1
https://www.instagram.com/beeswonderland
https://www.instagram.com/daphnemodeandthecity
https://www.instagram.com/rumineely
https://www.instagram.com/littleblackboots
https://www.instagram.com/streetstyle
https://www.instagram.com/yoyokulala
https://www.instagram.com/evangelineyan
https://www.instagram.com/cherriemun_
https://www.instagram.com/songdani
https://www.instagram.com/emilythemermaid
https://www.instagram.com/chrisaliescorners
https://www.instagram.com/rchlwngxx
https://www.instagram.com/karenngkarenng
https://www.instagram.com/savoirsam
https://www.instagram.com/audreyxaudrey
https://www.instagram.com/skinnyspy
https://www.instagram.com/olivialazuardy
https://www.instagram.com/forevervanny
https://www.instagram.com/violettedaily
https://www.instagram.com/itsfranxcesca
https://www.instagram.com/jenniferwhwang
https://www.instagram.com/dreachong
https://www.instagram.com/anazsiantar
https://www.instagram.com/kaillling
https://www.instagram.com/cindytanjaya
https://www.instagram.com/thehautepursuit
https://www.instagram.com/ootdsubmit/
https://www.instagram.com/ootdmagazine/
'''



# instogram_accounts = [
#     'https://www.instagram.com/wendyslookbook/',
#     'https://www.instagram.com/thesartorialist/',
#     'https://www.instagram.com/solsolstreet/',
#     'https://www.instagram.com/asianstreetfashion/'    
#     ]

instogram_accounts = raw_accounts.split()
# instogram_accounts.reverse()

if __name__ == '__main__':
#     print raw_accounts
    accounts = raw_accounts.split()
    print len(accounts)
    for idx, account in enumerate(accounts):
        print idx, account