import openai
import pickle
import os

def cut_message(message,turns):
    return message[max(0,len(message)-turns*2+1):]

def add_assistant_message_latest(message):
    if message[0]["role"] == "assistant":
        message_assistant = message.pop(0)
        message.insert(len(message)-1,message_assistant)
    return message

def preprocess(message,turns,support):
    if support:
        message = add_assistant_message_latest(message)
    message = cut_message(message,turns)
    return message

print("タイトルを入力してください")
title = input()
print("保存する対話ターン数を指定してください。指定しない場合は5です。")
turns = input()
if turns == "":
    turns = 5
else:
    turns = int(turns)
if os.path.isfile("history/pic/{}.pic".format(title)):
    with open("history/pic/{}.pic".format(title), 'rb') as f:
        dialogue_message = pickle.load(f)
    print("前回の対話です。")
    for line in dialogue_message:
        print("role:{} context:{}".format(line["role"],line["content"]))
else:
    dialogue_message = []
    print("ChatGPTに設定を入力してください。不要の場合はenterを押してください")
    system_setting = input()
    if system_setting != "":
        dialogue_message.append({"role": "system","content": system_setting})
    print("エージェントへの支持を直前に持っていきますか？(yes/no)、指定しない場合はnoです。")
    support = input()
    if support == "yes":
        support = True
    else:
        support = False

flag=True

while flag:
    print("モデルを選択してください。3.5を入力するとGPT-3.5,4を入力するとGPT-4を使用します。")
    input_model = input()
    if input_model == "3.5":
        model = "gpt-3.5-turbo"
        flag=False
    elif input_model == "4":
        model = "gpt-4"
        flag=False

flag=True
print("質問を入力してください")
while flag:
    text = input()
    if text == "exit":
        exit()
    else:
        dialogue_message.append({"role": "user","content": text})

    send_text_data = preprocess(dialogue_message,turns,support)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=send_text_data
        )
    print(response["choices"][0]["message"]["content"])
    dialogue_message.append({"role": "assistant","content": response["choices"][0]["message"]["content"]})
    # オブジェクト保存
    with open("history/pic/{}.pic".format(title),"wb") as f:
        pickle.dump(dialogue_message,f)
    # textファイル用
    text_data = ""
    for line in dialogue_message:
        text_data += "role:{}\ncontext:{}\n".format(line["role"],line["content"])
    with open("history/text/{}.txt".format(title),"w",encoding="utf-8") as f:
        f.write(text_data)
