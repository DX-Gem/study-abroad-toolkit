import json, os

def make_phrases(code, name, phrases_list):
    data = {
        "categories": [{
            "id": f"essential_{code}",
            "name": f"\U0001f4cb {name}应急短语",
            "icon": "\U0001f4cb",
            "phrases": phrases_list
        }]
    }
    # Save JSON
    fname = f"phrases_{code}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Save embed JS
    js = "const PHRASES_DATA = " + json.dumps(data, ensure_ascii=False) + ";"
    with open(f"phrases_{code}.js", "w", encoding="utf-8") as f:
        f.write(js)
    return len(phrases_list)

results = {}

# English
results['en'] = make_phrases("en", "英语", [
    {"id":"en_hello","ru":"Hello / Hi","kk":"Hello / Hi","pronunciation":"哈喽 / 嗨","zh":"你好","context":"通用问候","tags":["问候"]},
    {"id":"en_thanks","ru":"Thank you","kk":"Thank you","pronunciation":"三克油","zh":"谢谢","context":"道谢","tags":["道谢"]},
    {"id":"en_please","ru":"Please / Excuse me","kk":"Please / Excuse me","pronunciation":"普利兹 / 伊克斯Q兹密","zh":"请 / 打扰一下","context":"请求","tags":["礼貌"]},
    {"id":"en_help","ru":"Help! Emergency!","kk":"Help! Emergency!","pronunciation":"嗨欧普 / 伊莫真西","zh":"救命！紧急！","context":"紧急求助","tags":["紧急","救命"]},
    {"id":"en_where","ru":"Where is ...?","kk":"Where is ...?","pronunciation":"威尔 伊兹","zh":"...在哪？","context":"问路","tags":["问路"]},
    {"id":"en_how_much","ru":"How much?","kk":"How much?","pronunciation":"好 马奇","zh":"多少钱？","context":"购物","tags":["价格"]},
    {"id":"en_doctor","ru":"I need a doctor","kk":"I need a doctor","pronunciation":"爱 尼的 额 刀克特","zh":"我需要医生","context":"医疗","tags":["医疗","紧急"]},
    {"id":"en_police","ru":"Call the police!","kk":"Call the police!","pronunciation":"靠 则 普利斯","zh":"叫警察！","context":"报警","tags":["紧急","报警"]},
    {"id":"en_water","ru":"Water, please","kk":"Water, please","pronunciation":"沃特 普利兹","zh":"请给我水","context":"餐厅","tags":["饮品"]},
    {"id":"en_bill","ru":"Check, please","kk":"Check, please","pronunciation":"柴克 普利兹","zh":"买单","context":"结账","tags":["结账"]},
    {"id":"en_dont_understand","ru":"I don't understand","kk":"I don't understand","pronunciation":"爱 东特 安德斯单","zh":"我听不懂","context":"沟通","tags":["沟通"]},
    {"id":"en_sorry","ru":"Sorry","kk":"Sorry","pronunciation":"骚瑞","zh":"对不起","context":"道歉","tags":["道歉"]},
    {"id":"en_goodbye","ru":"Goodbye / Bye","kk":"Goodbye / Bye","pronunciation":"古德拜 / 拜","zh":"再见","context":"道别","tags":["告别"]},
    {"id":"en_chinese","ru":"Do you speak Chinese?","kk":"Do you speak Chinese?","pronunciation":"度 优 斯皮克 拆尼兹","zh":"你会说中文吗？","context":"沟通","tags":["翻译"]},
])

# Japanese
results['ja'] = make_phrases("ja", "日语", [
    {"id":"ja_hello","ru":"こんにちは","kk":"こんにちは","pronunciation":"空尼奇瓦","zh":"你好","context":"通用问候","tags":["问候"]},
    {"id":"ja_thanks","ru":"ありがとうございます","kk":"ありがとうございます","pronunciation":"阿里嘎多 够咋依马斯","zh":"谢谢","context":"道谢","tags":["道谢"]},
    {"id":"ja_please","ru":"お願いします","kk":"お願いします","pronunciation":"哦内盖 西马斯","zh":"请 / 拜托了","context":"请求","tags":["礼貌"]},
    {"id":"ja_help","ru":"助けて！","kk":"助けて！","pronunciation":"塔苏克忒","zh":"救命！","context":"紧急求助","tags":["紧急","救命"]},
    {"id":"ja_where","ru":"...はどこですか？","kk":"...はどこですか？","pronunciation":"...瓦 多科 得斯嘎","zh":"...在哪？","context":"问路","tags":["问路"]},
    {"id":"ja_how_much","ru":"いくらですか？","kk":"いくらですか？","pronunciation":"依库拉 得斯嘎","zh":"多少钱？","context":"购物","tags":["价格"]},
    {"id":"ja_doctor","ru":"医者を呼んでください","kk":"医者を呼んでください","pronunciation":"依夏 哦 永得 库达赛","zh":"请叫医生","context":"医疗","tags":["医疗"]},
    {"id":"ja_police","ru":"警察を呼んで！","kk":"警察を呼んで！","pronunciation":"凯撒茨 哦 永得","zh":"叫警察！","context":"报警","tags":["紧急","报警"]},
    {"id":"ja_water","ru":"お水をください","kk":"お水をください","pronunciation":"哦米租 哦 库达赛","zh":"请给我水","context":"餐厅","tags":["饮品"]},
    {"id":"ja_bill","ru":"お会計お願いします","kk":"お会計お願いします","pronunciation":"哦凯凯 哦内盖西马斯","zh":"买单","context":"结账","tags":["结账"]},
    {"id":"ja_dont_understand","ru":"わかりません","kk":"わかりません","pronunciation":"瓦卡里马森","zh":"我不懂","context":"沟通","tags":["沟通"]},
    {"id":"ja_sorry","ru":"すみません","kk":"すみません","pronunciation":"苏米马森","zh":"对不起","context":"道歉/搭话","tags":["道歉"]},
    {"id":"ja_goodbye","ru":"さようなら","kk":"さようなら","pronunciation":"撒哟那拉","zh":"再见","context":"道别","tags":["告别"]},
    {"id":"ja_train","ru":"駅はどこですか？","kk":"駅はどこですか？","pronunciation":"诶ki 瓦 多科得斯嘎","zh":"车站在哪？","context":"交通","tags":["问路","交通"]},
])

# Korean
results['ko'] = make_phrases("ko", "韩语", [
    {"id":"ko_hello","ru":"안녕하세요","kk":"안녕하세요","pronunciation":"安宁哈塞哟","zh":"你好","context":"通用问候","tags":["问候"]},
    {"id":"ko_thanks","ru":"감사합니다","kk":"감사합니다","pronunciation":"卡姆萨哈米达","zh":"谢谢","context":"道谢","tags":["道谢"]},
    {"id":"ko_please","ru":"부탁합니다","kk":"부탁합니다","pronunciation":"普塔卡米达","zh":"请 / 拜托","context":"请求","tags":["礼貌"]},
    {"id":"ko_help","ru":"살려주세요!","kk":"살려주세요!","pronunciation":"萨里奥 组塞哟","zh":"救命！","context":"紧急求助","tags":["紧急","救命"]},
    {"id":"ko_where","ru":"... 어디예요?","kk":"... 어디예요?","pronunciation":"... 哦滴耶哟","zh":"...在哪？","context":"问路","tags":["问路"]},
    {"id":"ko_how_much","ru":"얼마예요?","kk":"얼마예요?","pronunciation":"哦马耶哟","zh":"多少钱？","context":"购物","tags":["价格"]},
    {"id":"ko_doctor","ru":"의사가 필요해요","kk":"의사가 필요해요","pronunciation":"依萨嘎 皮留嘿哟","zh":"我需要医生","context":"医疗","tags":["医疗"]},
    {"id":"ko_police","ru":"경찰 불러주세요!","kk":"경찰 불러주세요!","pronunciation":"gyong查尔 布鲁组塞哟","zh":"叫警察！","context":"报警","tags":["紧急","报警"]},
    {"id":"ko_water","ru":"물 주세요","kk":"물 주세요","pronunciation":"木尔 组塞哟","zh":"请给我水","context":"餐厅","tags":["饮品"]},
    {"id":"ko_bill","ru":"계산해 주세요","kk":"계산해 주세요","pronunciation":"给三嘿 组塞哟","zh":"买单","context":"结账","tags":["结账"]},
    {"id":"ko_dont_understand","ru":"이해 못 해요","kk":"이해 못 해요","pronunciation":"依嘿 莫 忒哟","zh":"我听不懂","context":"沟通","tags":["沟通"]},
    {"id":"ko_sorry","ru":"죄송합니다","kk":"죄송합니다","pronunciation":"崔松哈米达","zh":"对不起","context":"道歉","tags":["道歉"]},
    {"id":"ko_goodbye","ru":"안녕히 계세요","kk":"안녕히 계세요","pronunciation":"安宁hi 给塞哟","zh":"再见","context":"道别","tags":["告别"]},
])

# German
results['de'] = make_phrases("de", "德语", [
    {"id":"de_hello","ru":"Hallo / Guten Tag","kk":"Hallo / Guten Tag","pronunciation":"哈喽 / 古腾 塔克","zh":"你好","context":"通用问候","tags":["问候"]},
    {"id":"de_thanks","ru":"Danke schoen","kk":"Danke schoen","pronunciation":"当克 勋","zh":"非常感谢","context":"道谢","tags":["道谢"]},
    {"id":"de_please","ru":"Bitte","kk":"Bitte","pronunciation":"比特","zh":"请 / 不客气","context":"请求/应答","tags":["礼貌"]},
    {"id":"de_help","ru":"Hilfe!","kk":"Hilfe!","pronunciation":"希欧非","zh":"救命！","context":"紧急求助","tags":["紧急","救命"]},
    {"id":"de_where","ru":"Wo ist ...?","kk":"Wo ist ...?","pronunciation":"沃 伊斯特","zh":"...在哪？","context":"问路","tags":["问路"]},
    {"id":"de_how_much","ru":"Wie viel kostet das?","kk":"Wie viel kostet das?","pronunciation":"维 非欧 科斯特 达斯","zh":"多少钱？","context":"购物","tags":["价格"]},
    {"id":"de_doctor","ru":"Ich brauche einen Arzt","kk":"Ich brauche einen Arzt","pronunciation":"依西 布劳赫 艾嫩 阿茨特","zh":"我需要医生","context":"医疗","tags":["医疗","紧急"]},
    {"id":"de_police","ru":"Rufen Sie die Polizei!","kk":"Rufen Sie die Polizei!","pronunciation":"鲁fen 贼 滴 珀利菜","zh":"叫警察！","context":"报警","tags":["紧急","报警"]},
    {"id":"de_water","ru":"Wasser, bitte","kk":"Wasser, bitte","pronunciation":"瓦瑟 比特","zh":"请给我水","context":"餐厅","tags":["饮品"]},
    {"id":"de_bill","ru":"Die Rechnung, bitte","kk":"Die Rechnung, bitte","pronunciation":"滴 赖西弄 比特","zh":"买单","context":"结账","tags":["结账"]},
    {"id":"de_dont_understand","ru":"Ich verstehe nicht","kk":"Ich verstehe nicht","pronunciation":"依西 费尔施特额 尼西特","zh":"我听不懂","context":"沟通","tags":["沟通"]},
    {"id":"de_sorry","ru":"Entschuldigung","kk":"Entschuldigung","pronunciation":"恩特书迪贡","zh":"对不起","context":"道歉","tags":["道歉"]},
    {"id":"de_goodbye","ru":"Auf Wiedersehen","kk":"Auf Wiedersehen","pronunciation":"奥夫 维德贼恩","zh":"再见","context":"道别","tags":["告别"]},
])

# French
results['fr'] = make_phrases("fr", "法语", [
    {"id":"fr_hello","ru":"Bonjour / Salut","kk":"Bonjour / Salut","pronunciation":"邦如 / 萨吕","zh":"你好","context":"通用问候","tags":["问候"]},
    {"id":"fr_thanks","ru":"Merci beaucoup","kk":"Merci beaucoup","pronunciation":"梅西 博库","zh":"非常感谢","context":"道谢","tags":["道谢"]},
    {"id":"fr_please","ru":"S'il vous plait","kk":"S'il vous plait","pronunciation":"西欧 乌 普莱","zh":"请","context":"请求","tags":["礼貌"]},
    {"id":"fr_help","ru":"Au secours!","kk":"Au secours!","pronunciation":"欧 瑟库","zh":"救命！","context":"紧急求助","tags":["紧急","救命"]},
    {"id":"fr_where","ru":"Ou est ...?","kk":"Ou est ...?","pronunciation":"乌 埃","zh":"...在哪？","context":"问路","tags":["问路"]},
    {"id":"fr_how_much","ru":"Combien ca coute?","kk":"Combien ca coute?","pronunciation":"宫比安 萨 库特","zh":"多少钱？","context":"购物","tags":["价格"]},
    {"id":"fr_doctor","ru":"J'ai besoin d'un medecin","kk":"J'ai besoin d'un medecin","pronunciation":"热 波兹万 单 梅德桑","zh":"我需要医生","context":"医疗","tags":["医疗","紧急"]},
    {"id":"fr_police","ru":"Appelez la police!","kk":"Appelez la police!","pronunciation":"阿普莱 拉 珀利斯","zh":"叫警察！","context":"报警","tags":["紧急","报警"]},
    {"id":"fr_water","ru":"De l'eau, s'il vous plait","kk":"De l'eau, s'il vous plait","pronunciation":"德 洛 西欧乌普莱","zh":"请给我水","context":"餐厅","tags":["饮品"]},
    {"id":"fr_bill","ru":"L'addition, s'il vous plait","kk":"L'addition, s'il vous plait","pronunciation":"拉迪雄 西欧乌普莱","zh":"买单","context":"结账","tags":["结账"]},
    {"id":"fr_dont_understand","ru":"Je ne comprends pas","kk":"Je ne comprends pas","pronunciation":"热 呢 宫pong 帕","zh":"我听不懂","context":"沟通","tags":["沟通"]},
    {"id":"fr_sorry","ru":"Pardon / Desole","kk":"Pardon / Desole","pronunciation":"帕东 / 得祖类","zh":"对不起","context":"道歉","tags":["道歉"]},
    {"id":"fr_goodbye","ru":"Au revoir","kk":"Au revoir","pronunciation":"欧 喝瓦","zh":"再见","context":"道别","tags":["告别"]},
])

# Malay
results['ms'] = make_phrases("ms", "马来语", [
    {"id":"ms_hello","ru":"Hello / Hai","kk":"Hello / Hai","pronunciation":"哈喽 / 嗨","zh":"你好","context":"通用问候","tags":["问候"]},
    {"id":"ms_thanks","ru":"Terima kasih","kk":"Terima kasih","pronunciation":"特立马 卡西","zh":"谢谢","context":"道谢","tags":["道谢"]},
    {"id":"ms_please","ru":"Tolong / Sila","kk":"Tolong / Sila","pronunciation":"多long / 西拉","zh":"请 / 麻烦","context":"请求","tags":["礼貌"]},
    {"id":"ms_help","ru":"Tolong! Bantuan!","kk":"Tolong! Bantuan!","pronunciation":"多long / 班图安","zh":"救命！帮帮忙！","context":"紧急求助","tags":["紧急","救命"]},
    {"id":"ms_where","ru":"Di mana ...?","kk":"Di mana ...?","pronunciation":"滴 马那","zh":"...在哪？","context":"问路","tags":["问路"]},
    {"id":"ms_how_much","ru":"Berapa harga?","kk":"Berapa harga?","pronunciation":"波拉帕 哈嘎","zh":"多少钱？","context":"购物","tags":["价格"]},
    {"id":"ms_doctor","ru":"Saya perlu doktor","kk":"Saya perlu doktor","pronunciation":"萨亚 普鲁 多克多","zh":"我需要医生","context":"医疗","tags":["医疗"]},
    {"id":"ms_police","ru":"Panggil polis!","kk":"Panggil polis!","pronunciation":"邦gi欧 珀利斯","zh":"叫警察！","context":"报警","tags":["紧急","报警"]},
    {"id":"ms_water","ru":"Air, tolong","kk":"Air, tolong","pronunciation":"阿依 多long","zh":"请给我水","context":"餐厅","tags":["饮品"]},
    {"id":"ms_bill","ru":"Bil, tolong","kk":"Bil, tolong","pronunciation":"比欧 多long","zh":"买单","context":"结账","tags":["结账"]},
    {"id":"ms_dont_understand","ru":"Saya tak faham","kk":"Saya tak faham","pronunciation":"萨亚 达 法汉","zh":"我听不懂","context":"沟通","tags":["沟通"]},
    {"id":"ms_sorry","ru":"Maaf","kk":"Maaf","pronunciation":"马阿夫","zh":"对不起","context":"道歉","tags":["道歉"]},
    {"id":"ms_goodbye","ru":"Selamat tinggal","kk":"Selamat tinggal","pronunciation":"色拉马 丁嘎","zh":"再见","context":"道别","tags":["告别"]},
])

for code, count in results.items():
    print(f"  {code}: {count} phrases")
print(f"Done! {sum(results.values())} total phrases across {len(results)} languages")
