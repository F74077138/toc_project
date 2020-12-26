from transitions.extensions import GraphMachine

from utils import *

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_greeting(self, event):
        text = event.message.text
        text = text.replace(" ", "")
        return text.lower() == "hi"

    def is_going_to_options(self, event):
        text = event.message.text
        text = text.replace(" ", "")
        return text.lower() == "help"

    def is_going_to_list(self, event):
        text = event.message.text
        text = text.replace(" ", "")
        return text.lower() == "top"

    def is_going_to_genre(self, event):
        text = event.message.text
        text = text.replace(" ", "")
        return text.lower() == "search"

    def is_going_to_new(self, event):
        text = event.message.text
        text = text.replace(" ", "")
        return text.lower() == "new"

    def is_going_to_about(self, event):
        text = event.message.text
        text = text.replace(" ", "")
        return text.lower() == "about"

    def is_going_to_cartoon(self, event):
        return True

    def is_going_to_showgenre(self, event):
        return True

    def is_going_to_cancel(self, event):
        text = event.message.text
        text = text.replace(" ", "")
        return text.lower() == "cancel"

    def on_enter_greeting(self, event):
        print("I'm entering greeting")
        userid = event.source.user_id
        reply_token = event.reply_token
        send_text_message(reply_token, "Hallo, potato head. \nIf you need my help, please type [help].")
        #push_message1(userid, "Hallo, potato head. \nIf you need my help, please type [help].")
        send_sticker(userid, '11539', '52114114')


    def on_enter_options(self, event):
        print("I'm entering options")
        userid = event.source.user_id
        url1 = 'https://static.wikia.nocookie.net/webarebears/images/c/c6/We_Bare_Bears_The_Movie_%281602%29.png/revision/latest?cb=20201011230241'
        title = 'How can I help?'
        uptext = 'Please choose one of the options'
        labels = ['Show my favorites', 'Show genres', 'Check new', 'About this line bot']
        texts = ['top', 'search', 'new', 'about']
        send_button_message(userid, url1, title, uptext, labels, texts)


    def on_enter_list(self, event):
        print("I'm entering list")
        #reply_token = event.reply_token
        userid = event.source.user_id

        daria = 'https://www.aerogrammestudio.com/wp-content/uploads/2014/09/A-Daria-Morgendorffer-Reading-List.jpeg'
        hilda = 'https://kidscreen.com/wp/wp-content/uploads/2019/09/Hilda-1.jpg'
        gravity = 'https://filmschoolrejects.com/wp-content/uploads/2019/06/Gravity-Falls-Feature-Image-2.jpg'
        train = 'https://pyxis.nymag.com/v1/imgs/8f6/7bb/59fc103fbd292590ba644a916e8f110f8e-20-infinity-train.rsquare.w1200.png'
        urls = [daria, hilda, gravity, train]
        labels = ['Check one', 'Check two', 'Check three', 'Check four']
        texts = ['Daria', 'Hilda', 'Gravity Falls', 'Infinity train']

        send_image_carousel(userid, urls, labels, texts)

        msg = "Press on the button above or type a cartoon name."
        push_message1(userid, msg)

        '''
        print("I'm entering list")
        userid = event.source.user_id

        url1 = 'https://tvseriesfinale.com/wp-content/uploads/2020/02/harley-quinn-dc.jpg'
        title = 'My favorite cartoons'
        uptext = 'Please choose one of the options'
        labels = ['Daria', 'Hilda', 'Infinity Train', 'Gravity Falls']
        texts = ['Daria', 'Hilda', 'Infinity train', 'Gravity Falls']
        send_button_message(userid, url1, title, uptext, labels, texts)

    '''

    def on_enter_new(self, event):
        print("I'm entering new")
        #reply_token = event.reply_token
        userid = event.source.user_id
        shownew(userid)
        push_message1(userid, "Please type [help] to go back.")
        #send_text_message(reply_token, "Please type [help] to go back.")


    def on_enter_cartoon(self, event):
        print("I'm entering cartoon")
        userid = event.source.user_id
        #reply_token = event.reply_token
        cartoonname = event.message.text
        try:
            searchcartoon(userid, cartoonname)
            #img = 'https://64.media.tumblr.com/f358be42b95e40f5e20ae05de23e01f1/e3d9524d6c10f26b-1e/s640x960/b846e42178b6c44823a677bd531df1885c1608ef.jpg'
            title = 'View more?'
            uptext = 'View more?'
            labels = ['Yes', 'No']
            texts = ["top", "cancel"]
            send_confirm_message(userid, title, uptext, labels, texts)
            #send_button_message(userid, img, title, uptext, labels, texts)
        except:
            push_message1(userid, "Oops! You did smth wrong((")
            send_sticker(userid, '11538', '51626519')
            self.go_back(event)

    def on_enter_genre(self, event):
        print("I'm entering genre")
        userid = event.source.user_id
        url1 = 'https://www.sheknows.com/wp-content/uploads/2018/08/do2dznjm9d0qa03dfkcs.jpeg'
        title = 'What genre do you like?'
        uptext = 'Please choose one of the options'
        labels = ['Comedy', 'Adventure', 'Drama']
        texts = ['Comedy', 'Adventure', 'Drama']
        send_button_message(userid, url1, title, uptext, labels, texts)

    def on_enter_showgenre(self, event):
        print("I'm entering showgenre")
        userid = event.source.user_id
        #reply_token = event.reply_token
        genre = event.message.text
        try:
            searchnewcartoon(userid, genre)
            title = 'View more?'
            uptext = 'View more?'
            labels = ['Yes', 'No']
            texts = ["search", "cancel"]
            send_confirm_message(userid, title, uptext, labels, texts)
        except:
            push_message1(userid, "Oops! You did smth wrong((")
            send_sticker(userid, '11538', '51626519')
            self.go_back(event)


    def on_enter_cancel(self, event):
        print("I'm entering cancel")
        #reply_token = event.reply_token
        userid = event.source.user_id
        #send_text_message(reply_token, "Please type [help] if you need my help.")
        push_message1(userid, "Please type [help] if you need my help.")
        self.go_back()

    def on_enter_about(self, event):
        print("I'm entering help")
        #reply_token = event.reply_token
        userid = event.source.user_id
        push_message1(userid, "This chatbot is designed to help you choose a cartoon to watch. You can "
                                       "choose one of my favorites or find a cartoon by genre. Also, you can check "
                                       "new cartoons in the [check new] option.\n\n\nList of the commands:\n\n[hi] start "
                                       "communication\n[help] see options\n[top] see my favorite "
                                       "cartoons\n[search] find a cartoon by genre\n[new] check new "
                                       "cartoons\n[about] about chatbot")
        self.go_back()
