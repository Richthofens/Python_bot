import telebot
from telebot.types import LabeledPrice, ShippingOption, PreCheckoutQuery
import json
# import requests


chave_bot = '6818276113:AAFLGI2Lfa52pPHRPkYSCJR9LBZtvV6yECA'

bot = telebot.TeleBot(chave_bot)
provider_ = ''
Vip_group_Id = -1002246389545

@bot.message_handler(commands= ['start'])
def inicio_pag(mensagem):
    bot.reply_to(mensagem, f'Olá, {mensagem.from_user.first_name}')

    prices = [LabeledPrice(label= "Acesso ao grupo vip", amount= 1000)]
    bot.send_invoice(chat_id= mensagem.chat.id, title = "Acesso ao grupo Vip",description= "Pagamento para acessar o grupo Vip",
                     invoice_payload= "Acesso-vip",provider_token= provider_, currency= "USD", prices= prices,
                     start_parameter= "Access-group-vip", is_flexible= False)
    
@bot.pre_checkout_query_handler(func= lambda query: True)
def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    if pre_checkout_query.invoice_payload != "Acesso_VIP":

        bot.answer_pre_checkout_query(pre_checkout_query.id, ok= False, error_message= "Algo deu errado...!")
    else:
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok= True)

@bot.message_handler(content_types= ["successful_payment"])
def pag_concluido(mensagem):
    bot.reply_to(mensagem, "Pagamento recebido! Adicionaremoss você ao grupo VIP..")

    bot.add_chat_member(Vip_group_Id, mensagem.from_user.id)
    



bot.polling()