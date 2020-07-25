# imports
import telegram as tel

from ..globalimports import *


# main func
def main(msg):
    bot = tel.Bot(token=BOTTOKEN)

    for receiverid in RECEIVERIDS:
        feedback = bot.send_message(
            chat_id=receiverid,
            text=msg,
            parse_mode=tel.ParseMode.HTML
        )
    print(feedback)


# testing
if __name__ == '__main__':

    msg = \
    '''<pre>
ELN id   :
event    : KI
KO Factor:
KI Factor:
S Factor :

|B|Code | OP    | CP    | %   |
|-|-----|-------|-------|-----|
|{:1}|{:5}|{:6.4f}|{:6.4f}|{:4.1f}|

B : Bought
OP: Original Price
CP: Closing  Price
    </pre>
    '''.format(
        '', 'RDS', 25.97488, 25.974,  100,

    )
    main(msg)
