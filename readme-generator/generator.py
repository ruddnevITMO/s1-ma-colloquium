from urllib.parse import quote
import os
import sys
import re

if __name__ == '__main__':

    if len(sys.argv) == 1:
        # НАЧАЛО ЧАСТИ, КОТОРУЮ НУЖНО ИЗМЕНИТЬ

        githubName = "ваш github ник"
        repoName = "название вашего репозитория"
        header = "заголовок вашего сайта"
        fileExtension = ".jpg"

        # КОНЕЦ ЧАСТИ, КОТОРУЮ НУЖНО ИЗМЕНИТЬ
    elif len(sys.argv) == 5:
        githubName = sys.argv[1]
        repoName = sys.argv[2]
        header = sys.argv[3]
        fileExtension = sys.argv[4]
    else:
        print("Неверное количество аргументов")
        sys.exit()

    altFileExtension = fileExtension
    obfuscateContents = True
    writeToReadme = True
    printing = False

    cards = ["0"]
    with open("../cardsList.txt", encoding="utf-8") as namesFile:
        for line in namesFile:
            if line.strip() == "":
                print("Нашел пустую строку в cardsList.txt")
            else:
                cards.append(line.rstrip())

    if re.search(r'^[0-9]+\.', cards[1]):
        if cards[1][0] != "1":
            print("Неправильный список билетов в cardsList.txt! Уберите нумерацию")

    for i in range(1, len(cards)):
        if re.search(r'^[0-9]+\.', cards[i]):
            cards[i] = re.search(r"(?<=\. ).*", cards[i]).group()

    if writeToReadme:
        readme = open("../README.md", "w", encoding='utf-8')


    def printWrite(*args):
        line = ' '.join([str(arg) for arg in args])
        if writeToReadme:
            readme.write(line + '\n')
        if printing:
            print(line)


    def quoteConvert(text):
        return text.lower().replace(" ", "-").replace(".", "").replace(",", "").replace("(", "").replace(")", "")


    replacements = [["о", "o"], ["М", "M"], ["е", "e"],
                    ["а", "a"], ["р", "p"], ["Т", "T"],
                    ["В", "B"], ["К", "K"], ["с", "c"],
                    ["у", "y"]]

    imageLinkTemplate = "https://raw.githubusercontent.com/" + githubName + "/" + repoName + "/main/cards/"
    linkTemplate = "https://" + githubName + ".github.io/" + repoName + "/#"
    linkToTop = linkTemplate + quote(quoteConvert(header))

    alts = []

    altsDir = os.listdir("../altCards")
    for file in altsDir:
        if re.search(r"[0-9]+\.(jpg|png|jpeg)", file):
            alts.append(int(re.match(r"[0-9]+(?=\.(jpg|png|jpeg))", file).group()))

    altsLink = "https://raw.githubusercontent.com/" + githubName + "/" + repoName + "/main/altCards/"

    # Заголовок
    printWrite("# " + header)

    # Формируем содержание
    howManyCards = len(cards) - 1
    for n in range(1, howManyCards + 1):
        name = cards[n]
        original = name

        if obfuscateContents:
            for placing in replacements:
                name = name.replace(placing[0], placing[1]).replace(placing[0].upper(), placing[1].upper())

        outputLine = "[" + name + "](" + linkTemplate + quote(quoteConvert(original) + "-" + str(n) + "-наверх") + ")"
        if n != howManyCards:  # на последней главе содержания не нужен перенос строки
            outputLine += "\\"

        printWrite(outputLine)

    # Формируем сами билеты
    for n in range(1, howManyCards + 1):
        printWrite("##", cards[n], "[" + str(n) + "] [наверх](" + linkToTop + ")")
        printWrite("![" + cards[n] + "](" + imageLinkTemplate + str(n) + fileExtension + ")")
        if n in alts:
            printWrite("### Альтернативный билет для ", cards[n], "[" + str(n) + "] [наверх](" + linkToTop + ")")
            printWrite("![" + cards[n] + "](" + altsLink + str(n) + altFileExtension + ")")
        printWrite("---")

