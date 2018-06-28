"""
    Proje Adı: msobot Discord Botu

"""


class Help():
    texts = []
    dizi = []
    mesaj = ""

    def __init__(self):
        self.ekle("Tüm Komutlar '!' ile başlar;\n")
        self.ekle("!help: komutu ile kullanabileceğiniz komutların listesini görürsünüz.\n")
        self.ekle("!clear {sayı}: komutu ile yazılı kanalda mesajlarınızı silebilirsiniz.\n")
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
