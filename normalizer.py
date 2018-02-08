from io import open
from subprocess import PIPE, Popen

class Normalizer(object):
    def file_save(self, text):
        norm_file = open("./temp/file.txt", mode="w", encoding="utf-8")
        norm_file.write(text.decode('utf-8'))
        norm_file.close()

    def tokenizer(self, text):
        #print ("Aplicando o tokenizador...")
        echo = Popen(['echo', text], stdout=PIPE)
        process = Popen(['./ugc_norm/tokenizer/webtok'], stdin=echo.stdout, stdout=PIPE)
        output = process.communicate()[0]
        return output

    def speller(self, text):
        tokens = self.tokenizer(text)
        #print ("Aplicando o speller...")
        self.file_save(tokens)
        actual_direcory = Popen('pwd', shell=False, stdout=PIPE)
        previous_path = actual_direcory.communicate()[0]
        command = 'perl ./ugc_norm/speller/spell.pl -stat ./ugc_norm/speller/lexicos/regra+cb_freq.txt -f ' + previous_path[:-1] + '/temp/file.txt'
        process = Popen(command.split(), shell=False, stdout=PIPE)
        output = process.communicate()[0]
        return output

    def acronym_searcher(self, text):
        checked_text = self.speller(text)
        #print ("Normalizando siglas...")
        self.file_save(checked_text)
        process = Popen('perl ./ugc_norm/siglas_map.pl ./ugc_norm/resources/lexico_siglas.txt ./temp/file.txt'.split(), shell=False, stdout=PIPE)
        output = process.communicate()[0]
        return output
        
    def untextese(self, text):
        text_with_acronyms = self.acronym_searcher(text)
        #print ("Normalizando internetes...")
        self.file_save(text_with_acronyms)
        process = Popen('perl ./ugc_norm/internetes_map.pl ./ugc_norm/resources/lexico_internetes.txt ./ugc_norm/resources/lexico_internetes_sigl_abrv.txt ./temp/file.txt'.split(), shell=False, stdout=PIPE)
        output = process.communicate()[0]
        return output

    def proper_noun_normalizer(self, text):
        without_textese = self.untextese(text)
        #print ("Normalizando nomes proprios...")
        self.file_save(without_textese)
        process = Popen('perl ./ugc_norm/np_map.pl ./ugc_norm/resources/lexico_nome_proprio.txt ./temp/file.txt'.split(), shell=False, stdout=PIPE)
        output = process.communicate()[0]
        return output
