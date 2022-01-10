class Cryptography:
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&;*1234567890"

    def Encrypt(self, plain_text, key) -> str:
        key_index = self.get_index(key)
        plain_text_index = self.get_index(plain_text)
        cipher_index = self.shift_values(plain_text_index, key_index)
        cipher_index = self.balance(cipher_index)

        cipher_text = ""
        for i in range(len(cipher_index)):
            cipher_text += self.characters[cipher_index[i]]

        return cipher_text

    def Decrypt(self, cipher_text, key) -> str:
        key_index = self.get_index(key)
        cipher_text_index = self.get_index(cipher_text)

        plain_text_index = self.shift_values(cipher_text_index, key_index, "backward")
        plain_text_index = self.balance(plain_text_index)

        plain_text = ''
        for i in range(len(plain_text_index)):
            plain_text += self.characters[plain_text_index[i]]

        return plain_text

    def shift_values(self, text_index, key_index, way="forward") -> list:
        key_limit = 0
        for i in range(len(text_index)):
            if key_limit >= len(key_index):
                key_limit = 0
            if way == "backward":
                text_index[i] = text_index[i] - key_index[key_limit]
            else:
                text_index[i] = text_index[i] + key_index[key_limit]
            key_limit += 1

        return text_index

    def balance(self, indexs):
        for i in range(len(indexs)):
            if indexs[i] > 69:
                indexs[i] = indexs[i] - 71
            elif indexs[i] < 0:
                indexs[i] = indexs[i] + 71

        return indexs

    def get_index(self, string) -> list:
        index = []
        for i in range(len(string)):
            for j in range(len(self.characters)):
                if string[i] == self.characters[j]:
                    index.append(j)

        return index
if __name__ == "__main__":
    crypto = Cryptography()
    result = crypto.Encrypt("BantuPostgres69Go", "1d576")
    print(result)
    print(crypto.Decrypt(result, "1d576"))
