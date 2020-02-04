# -*- coding: utf-8 -*-
#/usr/bin/python2
'''
By kyubyong park. kbpark.linguist@gmail.com. 
https://www.github.com/kyubyong/tacotron
'''
class Hyperparams:
    '''Hyper parameters'''

    def __init__(self, lang):

        self.prepro = True  # if True, run `python prepro.py` first before running `python train.py`.
    
        # ␀: Padding ␃: End of Sentence
        if lang == 'fr':
            vocab = u'''␀␃ !"',-.:;?AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzàâæçèéêëîïôùûœ–’'''
        if lang == 'it':
            vocab = u'''␀␃ !',-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÈàèéìíîïòôù'''
        if lang == 'nl':
            vocab = u'''␀␃ !',-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'''
        if lang == 'el':
            vocab = u'''␀␃ !',-.:;ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyzΆΈΉΊΌΎΏΐΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩάέήίαβγδεζηθικλμνξοπρςστυφχψωϊϋόύώ'''
        if lang == 'de':
            vocab = u'''␀␃ !',-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÄÖÜßàäéöü–'''
        if lang == 'es':
            vocab = u'''␀␃ !',-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz¡¿ÁÅÉÍÓÚáæèéëíîñóöúü—'''
        if lang == 'fi':
            vocab = u'''␀␃ !',-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÄÖäéö'''
        if lang == 'ru':
            vocab = u'''␀␃ !',-.:;?êАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяё—'''
        if lang == 'zh':
            vocab = u'''␀␃ abcdefghijklmnopqrstuvwxyz·àáèéìíòóùúüāēěīōūǎǐǒǔǚǜ—、。！，－：；？'''
        if lang == 'jp':
            vocab = u'''␀␃ '-abcdefghijkmnoprstuvwxyz―、。々？'''

        self.vocab = vocab
        self.lang = lang
    
        self.data = "data/public/rw/speech/{}".format(lang)
        self.test_data = 'data/MOS/sents/{}.txt'.format(lang)
        self.max_duration = 20.0

        # signal processing
        self.sr = 22050 # Sample rate.
        self.n_fft = 2048 # fft points (samples)
        self.frame_shift = 0.0125 # seconds
        self.frame_length = 0.05 # seconds
        self.hop_length = int(self.sr*self.frame_shift) # samples.
        self.win_length = int(self.sr*self.frame_length) # samples.
        self.n_mels = 80 # Number of Mel banks to generate
        self.power = 1.2 # Exponent for amplifying the predicted magnitude
        self.n_iter = 100 # Number of inversion iterations
        self.preemphasis = .97 # or None
        self.max_db = 100
        self.ref_db = 20

        # model
        self.embed_size = 256 # alias = E
        self.encoder_num_banks = 16
        self.decoder_num_banks = 8
        self.num_highwaynet_blocks = 4
        self.r = 5 # Reduction factor. Paper => 2, 3, 5
        self.dropout_rate = .5

        # training scheme
        self.lr = 0.001 # Initial learning rate.
        self.logdir = "data/{}/logdir".format(lang)
        self.sampledir = 'data/{}/samples'.format(lang)
        self.batch_size = 32
        self.num_iterations = 400000

        self.syn_logdir = "data/{}/logdir".format(lang)
        self.EOS_char = '␃'

_H=Hyperparams('ru')

class CurrentHyperparams:

    def __init__(self):
        pass

    def __getattr__(self, name):
        return getattr(_H, name)

hyperparams = CurrentHyperparams()

