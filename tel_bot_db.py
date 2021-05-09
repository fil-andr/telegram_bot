import telebot
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

engine = sa.create_engine('postgresql://postgres:pswd_123@192.168.1.5:5432/postgres')

base = declarative_base()


class Company(base):
    __tablename__ = 'company'
    id = sa.Column(sa.Integer,primary_key=True)
    name = sa.Column(sa.String)
    age = sa.Column(sa.Integer)
    address = sa.Column(sa.String)
    salary = sa.Column(sa.Integer)

    def __repr__(self):
        return f'Company name={self.name}'

def db_select(id_num):
    session_postg = sessionmaker(bind=engine)()
    try:
        d = session_postg.query(Company).filter_by(id=id_num).one()
    except sa.exc.NoResultFound:
        return f'no row with id: {id_num}'
    return f'name: {d.name}, salary: {d.salary}'


bot = telebot.TeleBot('<token>')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    int_mes = ''
    try:
        int_mes = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, "Value error, please send id number as digit, letters don/'t support")
    if message.text == "/start":
        bot.send_message(message.from_user.id, "please send id number, send /help for help ")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "please send id number as digit, and you will get name and salary from DB")
    if isinstance(int_mes, int):
        d = db_select(int_mes)
        bot.send_message(message.from_user.id, d)

bot.polling(none_stop=True, interval=0)

