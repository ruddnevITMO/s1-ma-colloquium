from urllib.parse import quote
import os

if __name__ == '__main__':
    writeToReadme = True
    header = "Материалы для подготовки к коллоквиуму по математическому анализу"
    githubName = "ruddnevITMO"
    repoName = "s1-ma-colloquium"

    with open("cardsList.txt", encoding="utf-8") as namesFile:
        cards = ["0"] + [i.rstrip() for i in namesFile]

    if writeToReadme:
        readme = open("../README.md", "w", encoding='utf-8')

    def printWrite(*args):
        line = ' '.join([str(arg) for arg in args])
        if writeToReadme:
            readme.write(line + '\n')
        print(line)

    def quoteConvert(text):
        return text.lower().replace(" ", "-").replace(".", "").replace(",", "").replace("(", "").replace(")", "")

    replacements = [["о", "o"], ["М", "M"], ["е", "e"],
                    ["а", "a"], ["р", "p"], ["Т", "T"],
                    ["В", "B"], ["К", "K"], ["с", "c"]]

    imageLinkTemplate = "https://raw.githubusercontent.com/" + githubName + "/" + repoName + "/main/cards/"
    linkTemplate = "https://" + githubName + ".github.io/" + repoName + "/#"
    linkToTop = linkTemplate + quote(quoteConvert(header))

    alts = [int(i[:-4]) for i in os.listdir("../altCards")]
    altsLink = "https://raw.githubusercontent.com/" + githubName + "/" + repoName + "/main/altCards/"

    # Заголовок
    printWrite("# " + header)

    # Формируем содержание
    howManyCards = len(cards) - 1
    for n in range(1, howManyCards + 1):
        name = cards[n]
        original = name
        for placing in replacements:
            name = name.replace(placing[0], placing[1]).replace(placing[0].upper(), placing[1].upper())

        outputLine = "[" + name + "](" + linkTemplate + quote(quoteConvert(original) + "-" + str(n) + "-наверх") + ")"
        if n != howManyCards:  # на последней главе содержания не нужен перенос строки
            outputLine += "\\"

        printWrite(outputLine)

    # Формируем сами билеты
    for n in range(1, howManyCards + 1):
        printWrite("##", cards[n], "[" + str(n) + "] [наверх](" + linkToTop + ")")
        printWrite("!["+cards[n]+"]("+imageLinkTemplate+str(n)+".jpg)")
        if n in alts:
            printWrite("### Альтернативный билет для ", cards[n], "[" + str(n) + "] [наверх](" + linkToTop + ")")
            printWrite("!["+cards[n]+"]("+altsLink+str(n)+".png)")
        printWrite("---")
