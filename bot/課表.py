import telebot


bot = telebot.TeleBot("6697126624:AAFL4s3pa6yqgzcqbwvgFnqQri-flJyTVVg", parse_mode=None)

curriculum = [[]]
for i in range(6):
    curriculum.append([])


def pretty_curriculum_table() -> str:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    table = ["| Day       | Time   | Class Name       |"]
    table.append("|-----------|--------|------------------|")

    for i in range(7):
        if len(curriculum[i]) == 0:
            table.append(f"| {days[i]:<9} | {' ':<6} | {'No classes':<16} |")
        else:
            for time, class_name in curriculum[i]:
                table.append(f"| {days[i]:<9} | {time:<6} | {class_name:<16} |")

    message = "<pre>"
    message += '\n'.join(table)
    message += "</pre>"
    return message


@bot.message_handler(commands=['add_class'])
def send_welcome(message):
    command_text = message.text.split(' ')
    if len(command_text) < 2:
        bot.reply_to(message, "Please enter the class name")
        return

    weekday = int(command_text[1])
    if weekday < 0 or weekday > 6:
        bot.reply_to(message, "Invalid weekday(expecting 0-6)")
        return

    if len(command_text) < 3:
        bot.reply_to(message, "Please enter the class time")
        return

    time = command_text[2]
    if len(time) != 4:
        bot.reply_to(message, "Invalid time format(expecting HHMM)")
        return

    if len(command_text) < 4:
        bot.reply_to(message, "Please enter the class name")
        return

    class_name = command_text[3]
    curriculum[weekday].append((time, class_name))
    bot.reply_to(message, "Class added successfully")
    bot.reply_to(message, f"Current classes for {weekday}: {curriculum[weekday]}")


@bot.message_handler(commands=['show_curriculum'])
def show_curriculum(message):
    bot.reply_to(message, pretty_curriculum_table(), parse_mode='HTML')


@bot.message_handler(commands=['remove_class'])
def remove_class(message):
    command_text = message.text.split(' ')
    if len(command_text) < 2:
        bot.reply_to(message, "Please enter the class name")
        return

    weekday = int(command_text[1])
    if weekday < 0 or weekday > 6:
        bot.reply_to(message, "Invalid weekday(expecting 0-6)")
        return

    if len(command_text) < 3:
        bot.reply_to(message, "Please enter the class time")
        return

    time = command_text[2]
    if len(time) != 4:
        bot.reply_to(message, "Invalid time format(expecting HHMM)")
        return

    if len(command_text) < 4:
        bot.reply_to(message, "Please enter the class name")
        return

    class_name = command_text[3]
    for i in range(len(curriculum[weekday])):
        if curriculum[weekday][i][0] == time and curriculum[weekday][i][1] == class_name:
            curriculum[weekday].pop(i)
            bot.reply_to(message, "Class removed successfully")
            bot.reply_to(message, f"Current classes for {weekday}: {curriculum[weekday]}")
            return
    bot.reply_to(message, "Class not found")


@bot.message_handler(commands=['curriculum'])
def show_help(message):
    bot.reply_to(message, "Commands:\n/add_class <weekday> <time> <class_name>\n/remove_class <weekday> <time> <class_name>\n/show_curriculum")

@bot.message_handler(command=['aaa'])
def callback_choice(message):
    bot.send_message(message.chat.id, text = '4')

bot.infinity_polling()