dic_sample = {" ": " | ", "A": "_", "B": "_", "C": "_", "D": "_", "E": "_", "F": "_", "G": "_", "H": "_", "I": "_", "J": "_", "K": "_", "L": "_", "M": "_",
              "N": "_", "O": "_", "P": "_", "Q": "_", "R": "_", "S": "_", "T": "_", "U": "_", "V": "_", "W": "_", "X": "_", "Y": "_", "Z": "_"}


class Vigenere_Transformer:
    def __init__(self, cypher):
        self.cypher = self.Sentence_Checker(cypher)
        self.letters = "abcdefghijklmnopqrstuvwxyz"
        self.check_ic_num = 7

    def Sentence_Checker(self, sentence: str, have_space: bool = True) -> str:
        sentence = sentence.upper()
        for i in sentence:
            if i not in dic_sample:
                sentence = sentence.replace(i, "")
        if not have_space:
            sentence = sentence.replace(" ", "")
        return sentence

    def Decoder(self, input_sentence: str, key: str = "") -> str:
        if key != "":
            key = list(key.upper())
            for i in range(len(key)):
                key[i] = ord(key[i])-64
            print(key)
        else:
            key = self.Coincidence_Get_Key()
        sentence = self.Sentence_Checker(input_sentence)
        res = []
        for index, letter in enumerate(sentence):
            if letter == " ":
                continue
            res.append(chr((ord(letter)-65-key[index % len(key)]) % 26+65))
        return "".join(res)

    def Grouping_Sentence(self, num: int) -> list:
        res = [[] for i in range(num)]
        sentence = self.cypher.replace(" ", "")
        for index, letter in enumerate(sentence):
            res[index % num].append(letter)
        for i in range(num):
            res[i] = "".join(res[i])
        return res

    def Get_Letter_NUM(self, sentence: str) -> dict:
        cypher = self.Sentence_Checker(sentence, False)
        cypher = sorted(list(cypher))
        first = cypher[0]
        index = -1
        letter_num = {}
        for i, letter in enumerate(cypher):
            if letter != first:
                first = letter
                index = i-1
            letter_num[letter] = i-index
        return letter_num

    def Coincidence_Index_Calculate(self, sentence) -> float:
        letter_dict = self.Get_Letter_NUM(sentence)
        CoincidenceIndex = 0
        sentence_length = len(sentence)
        for i in letter_dict:
            CoincidenceIndex += letter_dict[i]*(letter_dict[i]-1)/(sentence_length*(sentence_length-1))
        return CoincidenceIndex

    def Get_IC_List(self, max_num: int) -> dict:
        res = {}
        for i in range(1, max_num+1):
            sentence_list = self.Grouping_Sentence(i)
            num_IC = [self.Coincidence_Index_Calculate(sentence) for sentence in sentence_list]
            res[i] = sum(num_IC)/len(num_IC)
        res = sorted(res.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        return res

    def Chi_Calculate(self, sentence_freq: list) -> float:
        expected_freq = {"A": 0.08167, "B": 0.01492, "C": 0.02782, "D": 0.04253, "E": 0.12702,
                         "F": 0.02228, "G": 0.02015, "H": 0.06094, "I": 0.06966, "J": 0.00153,
                         "K": 0.00772, "L": 0.04025, "M": 0.02406, "N": 0.06749, "O": 0.07507,
                         "P": 0.01929, "Q": 0.00095, "R": 0.05987, "S": 0.06327, "T": 0.09056,
                         "U": 0.02758, "V": 0.00978, "W": 0.02360, "X": 0.00150, "Y": 0.01974,
                         "Z": 0.00074}
        chi = 0
        freq_num = list(expected_freq.values())
        for i in range(26):
            chi += sentence_freq[i]*freq_num[i]
        return chi

    def Correlation_Calculate(self, sentence) -> int:
        letter_num = self.Get_Letter_NUM(sentence)
        sentence_length = len(sentence)
        letter_freq = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0,
                       "F": 0, "G": 0, "H": 0, "I": 0, "J": 0,
                       "K": 0, "L": 0, "M": 0, "N": 0, "O": 0,
                       "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0,
                       "U": 0, "V": 0, "W": 0, "X": 0, "Y": 0,
                       "Z": 0}
        for i in letter_num:
            letter_freq[i] = letter_num[i]/sentence_length
        freq_num = list(letter_freq.values())
        res = []
        for i in range(26):
            res.append(self.Chi_Calculate(freq_num))
            freq_num.insert(len(freq_num), freq_num[0])
            freq_num.remove(freq_num[0])
        return res.index(max(res))

    def Coincidence_Get_Key(self) -> list:
        m = self.Get_IC_List(self.check_ic_num)[0][0]
        sentence_list = self.Grouping_Sentence(m)
        res = []
        for sentence in sentence_list:
            self.Correlation_Calculate(sentence)
            res.append(self.Correlation_Calculate(sentence))
        return res


if __name__ == "__main__":
    sentence = "LAFLUIWOYWPADUFHSNBVSWVNDZQDUFRBPLUYQPLWLPHZRLUEDUBSYMIPRDIJHTYQUCUZYLKFRSKHZBUHULUEKPQFOYLYSSAMWOCWHZOLGDTDDPPOFDDTGOPYUDGWOYOSDRYKVVDVLAULRZYGWPLJZYQKYPTWVLJIAFHHSWOMUVDDAPLMJLUEPVLRNPDWFXWMQAFHZSEQCFAGQDFLJFLHLDSWCLMQLFXUBULBDUBVPVWFQHWYUHRHJGSOCUZZXAGFVLILQVAFDARKPQLZCQAGULJBUCZAMPL"
    # sentence = "DVCMUAXZKPSAL"
    cypher = Vigenere_Transformer(sentence)
    decoder = cypher.Decoder(cypher.cypher, key="")
    print(decoder)
