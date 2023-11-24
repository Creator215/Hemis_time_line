from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from bot_params import bot_token, guruh_nomi, admin_login, admin_parol
from threading import Thread
import sqlite3
from Hemis import Hemis
from Get_time import Uzb_time_zona


class Hemis_bot:
    def __init__(self):
        self.bot_config = ApplicationBuilder().token(bot_token).build()
        self.users_db = sqlite3.connect("Users.db")
        self.cursors = self.users_db.cursor()
        self.all_buttons = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[["Bugun"], ["Ertaga"]])
        self.remove_but = ReplyKeyboardRemove()
        self.is_progresing = False
        self.create_formula = """CREATE TABLE user_data(
            user_full_name DATATYPE,
            user_id DATATYPE
        )"""

        self.select_formula = """SELECT * FROM user_data """

        try:
            self.cursors.execute(self.create_formula)
            print("Jadval yaratildi")
        except:

            print("yaratib bo'lingan")

        self.bot_config.add_handler(CommandHandler("start", self.start))
        self.bot_config.add_handler(CommandHandler("add_me", self.add_me))
        self.bot_config.add_handler(CommandHandler("show_user", self.show_user))
        self.bot_config.add_handler(CommandHandler("remove_me",self.remove_me))
        self.bot_config.add_handler(CommandHandler("help",self.help))
        self.bot_config.add_handler(MessageHandler(filters=filters.TEXT, callback=self.user_messages))

        self.bot_config.run_polling()

    async def help(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.my_help = """<b>1.</b>/add_me Ro'yxatga olinishingiz uchun kerak bo'ladigan buyruq\n\n<b>2.</b>/remove_me O'zingizni ro'yxatdan o'chirib yuborishingiz uchun kerak bo'ladigan buyruq\n\n<b>3. Bugun</b> kalit so'zi aynan bugungi dars jadvalni ko'rsatadi.\n\n<b>4. Ertaga</b> kalit so'zi ertangi kunning dars jadvalini ko'rishingiz mumkin """

        await update.message.reply_html(self.my_help)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        id_ = update.effective_user.id
        all_datas = self.cursors.execute(self.select_formula).fetchall()
        print(id_)

        ins = 0
        for i in all_datas:
            if (str(i[1]) == str(id_)):
                ins = 1
                await update.message.reply_text(f"{guruh_nomi} Dars jadvaliga xush kelibsiz",
                                                reply_markup=self.all_buttons)
                break
                
            else:
                ins = 0
        if (ins == 0):
            await update.message.reply_html(
                f"Salom 👋.Mening asosiy vazifam sizga darsingiz qachon 🕔 va qayerda 🚪 bo'lishi haqida xabar berishdir.Va bu ma'lumotlarning bari <b>{guruh_nomi}</b> ning ma'lumotlaridir")
            await update.message.reply_text(
                f"Sizga to'laqonli xizmat ko'rsatishim uchun sizni ro'yxatga olishim kerak.Buning uchun menga /add_me buyrug'ini yuborsangiz yetarli. 😉\nBatafsil ma'lumot uchun /help ni yuboring")
        else:
            pass

    async def remove_me(self,update: Update, context: ContextTypes.DEFAULT_TYPE):

        id_ = update.effective_user.id
        all_datas = self.cursors.execute(self.select_formula).fetchall()
        delete_formula = f"""DELETE FROM user_data WHERE user_id="{id_}" """

        ins = 0
        for i in all_datas:
            if (str(i[1]) == str(id_)):

                self.cursors.execute(delete_formula)
                self.users_db.commit()
                await update.message.reply_text(
                    "Siz ro'yxatdan o'chirildingiz ✅.Ro'yxatdan o'tish uchun menga /add_me buyrug'ini yuboring",reply_markup=ReplyKeyboardRemove())
                ins = 1
                break
            else:
                ins = 0
        if (ins == 0):
            self.cursors.execute(delete_formula)
            await update.message.reply_text(
                "Siz ro'yxatdan o'tmagansiz ⚠️.Ro'yxatdan o'tish uchun menga /add_me buyrug'ini yuboring")

    async def add_me(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        self.first_name = update.effective_user.first_name
        self.last_name = update.effective_user.last_name
        self.user_id = update.effective_user.id
        self.all_datas = self.cursors.execute(self.select_formula).fetchall()
        self.demo_name = f"{self.first_name} {self.last_name}"
        self.insert_formula = f"""INSERT INTO user_data VALUES ("{self.first_name} {self.last_name}", "{self.user_id}")"""

        if (self.all_datas == []):
            self.cursors.execute(self.insert_formula)
            await update.message.reply_text(
                f"Tabriklaymiz! {self.demo_name} siz muvofaqiyatli ro'yxatga olindingiz ✅.Endi bemalol dars jadvalidan xabardor bo'lib turishingiz mumkin 😉",
                reply_markup=self.all_buttons)
            self.users_db.commit()
        else:
            ips = 0
            for i in self.all_datas:
                if (i[1] == self.user_id):
                    await update.message.reply_text("Siz ro'yxatdan o'tgansiz ⚠️")
                    ips = 0
                    break
                else:
                    ips = 1
            if (ips == 1):
                self.cursors.execute(self.insert_formula)
                self.users_db.commit()
                await update.message.reply_text(
                    f"Tabriklaymiz! {self.demo_name} siz muvofaqiyatli ro'yxatga olindingiz ✅.Endi bemalol dars jadvalidan xabardor bo'lib turishingiz mumkin 😉",
                    reply_markup=self.all_buttons)

    async def show_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.strs = ""
        self.ddata = self.cursors.execute(self.select_formula).fetchall()
        index = 1
        for i in self.ddata:
            self.strs += f"{index}.{i[0]}\n"
            index += 1
        if(self.strs == ""):
            await update.message.reply_text("hali hech kim ro'yxatdan o'tmadi")
        else:
            await update.message.reply_text(f"Foydalanuvchilarimiz\n\n{self.strs}")

    async def user_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text

        if (user_text == "Bugun"):
            th = Thread(target=await self.bugun(update, context))
            th.start()

        elif (user_text == "Ertaga"):
            th = Thread(target=await self.ertaga(update, context))
            th.start()

        else:
            th = Thread(target=await self.all_messages(update, context))
            th.start()

    async def bugun(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        user_id = update.effective_user.id

        all_datas = self.cursors.execute(self.select_formula).fetchall()
        indx = 0
        for i in all_datas:
            if (str(i[1]) == str(user_id)):

                indx = 1
                await update.message.reply_text("Kutib turing...", reply_markup=ReplyKeyboardRemove())
                try:
                    data = ""
                    z = Uzb_time_zona()
                    try:
                        h = Hemis(admin_login, admin_parol, z.sana("kun"), z.sana("oy"))

                        index = 1
                        for i in h.get_time_table_data_json()[z.hafta()]:
                            data += f"<b>{index}</b>) {i[2]} | {i[1]} | <b>{i[3]}</b> | {i[4]} | {i[0]}\n\n"
                            index += 1

                        await update.message.reply_html("<b>Bugun</b>\n\n" + data, reply_markup=self.all_buttons)
                    except KeyError:
                        await update.message.reply_text("Bugun hech qanday darslar yo'q.Mazza qilib dam oling 😊",
                                                        reply_markup=self.all_buttons)
                    break
                except:
                    await update.message.reply_text("Xatolik yuz berdi.qaytadan urunib ko'ring ❌",
                                                    reply_markup=self.all_buttons)
                    break

            else:
                indx = 0
        if (indx == 0):
            await update.message.reply_text(
                "Siz ro'yxatdan o'tmagansiz ⚠️.Ro'yxatdan o'tish uchun menda /add_me buyrug'ini yuboring")

    async def ertaga(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id

        all_datas = self.cursors.execute(self.select_formula).fetchall()
        indx = 0
        for i in all_datas:
            if (str(i[1]) == str(user_id)):
                indx = 1
                await update.message.reply_text("Kutib turing...", reply_markup=ReplyKeyboardRemove())
                try:
                    data = ""
                    z = Uzb_time_zona()
                    try:
                        h = Hemis(admin_login, admin_parol, z.sana("kun"), z.sana("oy"))
                        index = 1
                        for i in h.get_time_table_data_json()[z.hafta2()]:
                            data += f"<b>{index}</b>) {i[2]} | {i[1]} | <b>{i[3]}</b> | {i[4]} | {i[0]}\n\n"
                            index += 1

                        await update.message.reply_html("<b>Ertaga</b>\n\n" + data, reply_markup=self.all_buttons)
                    except KeyError:
                        await update.message.reply_text("Ertaga hech qanday darslar yo'q.Mazza qilib dam oling 😊",
                                                        reply_markup=self.all_buttons)

                except:
                    await update.message.reply_text("Xatolik yuz berdi.qaytadan urunib ko'ring ❌",
                                                    reply_markup=self.all_buttons)

                break
            else:
                indx = 1
        if (indx == 0):
            await update.message.reply_text(
                "Siz ro'yxatdan o'tmagansiz ⚠️.Ro'yxatdan o'tish uchun menga /add_me buyrug'ini yuboring")

    async def all_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Bunday buyruq mavjud emas ⛔️")


if __name__ == "__main__":
    Hemis_bot()