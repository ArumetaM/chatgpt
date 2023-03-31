import openai
import pickle
import os

print("タイトルを入力してください")
title = input()
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
flag=True
print("質問を入力してください")
while flag:
    text = input()
    if text == "exit":
        exit()
    else:
        dialogue_message.append({"role": "user","content": text})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=dialogue_message
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

