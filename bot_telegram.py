import telebot
import json

Chave_api = '7231613204:AAFlP7X8VAYE1jFRMrVHlzsxcPVxQ-dh-_Q'
Vip_group_Id = -1002246389545
bot = telebot.TeleBot(Chave_api)



def save_users(user):
    file = 'Usuarios_Vip.json'
    try:
        with open(file, 'r') as usu_obj:
            data = json.load(usu_obj)
        
        if not any(i['User_Id'] == user['User_Id'] for i in data):
            data.append(user)

            with open(file, 'w') as usu_obj:
                json.dump(data, usu_obj, indent=4)

    except (FileNotFoundError, json.JSONDecodeError):
        data = [user]
        with open(file, 'w') as usu_obj:
            json.dump(data, usu_obj, indent=4)



def is_user_in_group(user):
    file = 'Usuarios_Vip.json'
    try:
        with open(file, 'r') as usu_obj:
            data = json.load(usu_obj)
                
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    
    try:
        member = bot.get_chat_member(Vip_group_Id, user)
        is_in_group = member.status in ['member', 'administrator', 'creator']

    except telebot.apihelper.ApiException:
        is_in_group = False

    is_in_file = any(i["User_Id"] == user for i in data)

    if is_in_group and not is_in_file:

        user = {
            'User_Id': user,
            'First_Name': bot.get_chat(user).first_name,
            'Username': bot.get_chat(user).username
        }
        data.append(user)
        with open(file, 'w') as usu_obj:
            json.dump(data, usu_obj, indent=4)
    
    elif not is_in_group and is_in_file:
        data = [i for i in data if i['User_Id'] != user]
        with open(file, 'w') as usu_obj:
            json.dump(data, usu_obj, indent=4)

    return is_in_group




@bot.message_handler(commands=['opcao1'])
def opcao1(mensagem):
    link = ''
    bot.send_message(mensagem.chat.id, f"Entre no nosso grupo gratuito {link}")
    


@bot.message_handler(commands=['opcao2'])
def opcao2(mensagem):
    user_id = mensagem.chat.id
    if not is_user_in_group(user_id):

        user = {
            'User_Id': mensagem.chat.id,
            'First_Name': mensagem.from_user.first_name,
            'Username': mensagem.from_user.username
        }
        save_users(user)

        link_grupo = 't.me/+bFQ36Dt9PiE4MjUx'
        link_pag = '@Pagmente_bot'
        bot.send_message(mensagem.chat.id, f"Pague para poder entrar no grupo Vip {link_pag}")
    else:
        bot.send_message(mensagem.chat.id, "você já participa do nosso grupo Vip")
    


@bot.message_handler(commands=['opcao3'])
def opcao3(mensagem):
    print(mensagem.chat.id)
    id_adm = '5874786456'
    bot.send_message(mensagem.chat.id, f'Olá, {mensagem.from_user.first_name} enviamos a sua mensagem para um dos Adms, aguarde retorno da mensagem')
    bot.send_message(id_adm, f'Um usuário solicitou contato, informações:')
    bot.send_message(id_adm, f'{mensagem.chat.id}, {mensagem.from_user.first_name}')







def verificar(mensagem):
    return True
    
@bot.message_handler(func= verificar)
def responder(mensagem):

    texto = '''
Escolha uma opção para continuar (Clique no item):
/opcao1 Entrar no grupo gratis
/opcao2 Entrar no grupo Vip
/opcao3 Falar com Adm

Responder qualquer outra coisa não ira funcionar, Clique em uma das opções.'''

    bot.send_message(mensagem.chat.id, f"Olá {mensagem.from_user.first_name}")
    bot.send_message(mensagem.chat.id, texto)


bot.polling()