"""
    Proje Adı: BDO TOOLS Discord

"""


class Help():
    texts = []
    dizi = []
    mesaj = ""

    def __init__(self):
        self.ekle("Tüm Komutlar '!' ile başlar;\n")
        self.ekle("!help: komutu ile kullanabileceğiniz komutların listesini görürsünüz.\n")
        self.ekle("!clear {sayı}: komutu ile yazılı kanalda mesajlarınızı silebilirsiniz.\n")
        self.ekle("!item 'item_adi': Kayıtlı itemi aramak için bu komutu kullanabilirsiniz.\n")
        self.ekle("!add 'item_adi', 'resim_url': Yeni item kaydetmek için bu komutu kullanabilirsiniz.\n")
        self.stringadd()
        self.Mesaj()

    def ekle(self, str):
        self.texts.append(str)

    def stringadd(self):

        self.dizi.append("```css\n")

        for text in self.texts:
            self.dizi.append(text)
        self.dizi.append("```")

    def Mesaj(self):

        for text in self.dizi:
            self.mesaj += text
