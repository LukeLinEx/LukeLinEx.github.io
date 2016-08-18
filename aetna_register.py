import pandas as pd
import random
from sys import argv


class Aetna_register(object):
    def __init__(self, df = None, *argv):
        self.__df = df

    def __combine_first_last(self):
        self.__df['Name'] = map(lambda x, y: ' '.join([x,y]), self.__df['First'], self.__df['Last'])
        self.__df.drop(['First', 'Last'], axis=1, inplace=True)
        
    def __lower_email(self):
        self.__df['Email'] = map(lambda x: x.lower(), self.__df['Email'])

    @classmethod
    def create_with_csv(cls, csv_file):
        df_temp = pd.read_csv(csv_file)
        return cls(df_temp)

    def __create_password(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 8
        password = []
        for j in range(self.__df.shape[0]):
            mypw = ""
            for i in range(pw_length):
                next_index = random.randrange(len(alphabet))
                mypw = mypw + alphabet[next_index]
            password.append(mypw)
        
        self.__df['Password'] = password
            
    def auto_process(self, _file):
        self.__df = pd.read_csv(_file, index_col=None)
        self.__lower_email()
        self.__combine_first_last()
        self.__create_password()
        return Aetna_register(self.__df)
        
    def show_table(self):
        return self.__df


if __name__ == '__main__':
    pass










