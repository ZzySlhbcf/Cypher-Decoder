dic_sample = {" ": " | ", "A": "_", "B": "_", "C": "_", "D": "_", "E": "_", "F": "_", "G": "_", "H": "_", "I": "_", "J": "_", "K": "_", "L": "_", "M": "_",
              "N": "_", "O": "_", "P": "_", "Q": "_", "R": "_", "S": "_", "T": "_", "U": "_", "V": "_", "W": "_", "X": "_", "Y": "_", "Z": "_"}


class Scrambler:
    def __init__(self, scrambler: str, move):
        self.scrambler = list(scrambler)
        self.can_move = False
        if type(move) == int:
            self.orign_move = move
        else:
            self.orign_move = 0
        self.Move_Scrambler(move)
        self.flag = 0  # 转动次数

    def Move_Scrambler(self, move) -> list:
        if type(move) == int:
            for i in range(move):
                self.scrambler.insert(len(self.scrambler), self.scrambler[0])
                self.scrambler.remove(self.scrambler[0])
            if self.can_move and move != 0:
                self.flag = (self.flag+1) % 26
        elif type(move) == str:
            for i in range(ord(move)-ord("A")):
                self.scrambler.insert(len(self.scrambler), self.scrambler[0])
                self.scrambler.remove(self.scrambler[0])
                self.orign_move += 1

    def Check_Round(self) -> int:
        if self.flag == 26 or not self.can_move:
            self.flag = 0
            self.can_move = False
            return 0
        return 1

    def Get_Up_Index(self, up_index: int) -> int:
        char_move = (self.flag+self.orign_move) % 26
        char_letter = self.scrambler[up_index]
        output_index = (26-char_move+ord(char_letter)-65) % 26
        return output_index

    def Get_Down_Index(self, down_index: int) -> int:
        char_move = (self.flag+self.orign_move) % 26
        char_letter = chr((down_index+char_move) % 26+65)
        output_index = self.scrambler.index(char_letter)
        return output_index


class ENIGMA_Transformer:
    def __init__(self, scrambler_list: list, reflextor: str, sentence: str, plugboard: dict = {}):
        self.scrambler_list = scrambler_list
        self.reflextor = list(self.Sentence_Checker(reflextor, have_space=False))
        self.cypher = self.Sentence_Checker(sentence)
        self.plugboard = plugboard
        for i in list(plugboard.keys()):
            self.plugboard[plugboard[i]] = i

    def Sentence_Checker(self, sentence: str, have_space: bool = True) -> str:
        sentence = sentence.upper()
        for i in sentence:
            if i not in dic_sample:
                sentence = sentence.replace(i, "")
        if not have_space:
            sentence = sentence.replace(" ", "")
        return sentence

    def Decoder(self):
        scrambler_move_index = 0
        res = []
        for letter in self.cypher:
            if letter in self.plugboard:
                letter = self.plugboard[letter]
            if letter == " ":
                res.append(" ")
                continue
            down_index = ord(letter)-65
            for index, scrambler in enumerate(self.scrambler_list):
                if index == scrambler_move_index:  # 检查转盘状态
                    scrambler.can_move = True  # 激活转盘
                    move_num = scrambler.Check_Round()
                    if not move_num:  # 如果已经转满一圈
                        scrambler_move_index = (scrambler_move_index+1) % len(self.scrambler_list)  # 转盘转动标记后移
                    scrambler.Move_Scrambler(move_num)  # 转盘转动
                down_index = scrambler.Get_Down_Index(down_index)
            reflextor_letter = self.reflextor[down_index]
            up_index = ord(reflextor_letter)-65
            for scrambler in self.scrambler_list[::-1]:
                up_index = scrambler.Get_Up_Index(up_index)
            res_letter = chr(up_index+65)
            if res_letter in self.plugboard:
                res_letter = self.plugboard[res_letter]
            res.append(res_letter)
        return res


if __name__ == "__main__":
    Scrambler_1 = Scrambler("UWYGADFPVZBECKMTHXSLRINQOJ", "E")
    Scrambler_2 = Scrambler("AJPCZWRLFBDKOTYUQGENHXMIVS", "A")
    Scrambler_3 = Scrambler("TAGBPCSDQEUFVNZHYIXJWLRKOM", "B")
    Reflextor = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    Sentence = "GYHRVFLRXY"
    Plugboard = {"A": "B", "S": "Z", "U": "Y", "G": "H", "L": "Q", "E": "N"}
    print(Sentence)
    Scrambler_list = [Scrambler_2, Scrambler_1, Scrambler_3]
    cyter = ENIGMA_Transformer(Scrambler_list, Reflextor, Sentence, Plugboard)
    decode = cyter.Decoder()
    print("".join(decode))
