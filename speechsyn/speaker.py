from __future__ import print_function
from speechsyn import hyperparams
from speechsyn.hyperparams import hyperparams as hp
import tqdm
from speechsyn.data_load import load_from_lines, load_vocab
import tensorflow as tf
from speechsyn.train import Graph
from speechsyn.utils import spectrogram2wav, plot_test_alignment
from scipy.io.wavfile import write
import os
import numpy as np
import sys
import matplotlib

matplotlib.use('pdf')
import matplotlib.pyplot as plt

SEC_PER_CHAR = float(10) / 180  # [sec/char]
SEC_PER_ITER = float(12) / 200  # [sec/iter]


def get_EOS_index(text):
    # Load vocab
    char2idx, idx2char = load_vocab()

    _text = np.array([idx2char[t] for t in text])
    return np.argmax(_text == hp.EOS_char)


def get_EOS_fire(alignment, text):
    EOS_index = get_EOS_index(text)
    text_max_indicies = np.argmax(alignment, axis=0)
    r = []
    for i, max_index in enumerate(text_max_indicies):
        if max_index == EOS_index:
            r.append(i)
    if not len(r) == 0:
        return max(r)
    return None


def synthesize(phrases):
    if not os.path.exists(hp.sampledir): os.mkdir(hp.sampledir)

    # Load graph
    g = Graph(mode="synthesize");
    print("Graph loaded")

    # Load data
    if phrases is str:
        texts, max_len = load_from_lines([phrases])
    else:
        texts, max_len = load_from_lines([phrases])

    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess, tf.train.latest_checkpoint(hp.syn_logdir));
        print("Restored!")

        # Feed Forward
        ## mel
        size = 10
        y_hat = np.zeros((texts.shape[0], size, hp.n_mels * hp.r), np.float32)
        for j in tqdm.tqdm(range(size)):
            _y_hat = sess.run(g.y_hat, {g.x: texts, g.y: y_hat})
            y_hat[:, j, :] = _y_hat[:, j, :]

        ## alignments
        alignments = sess.run([g.alignments], {g.x: texts, g.y: y_hat})[0]
        ## mag
        mags = sess.run(g.z_hat, {g.y_hat: y_hat})
        print('Len of mags', len(mags))
        for i, mag in enumerate(mags):
            print("File {}.wav is being generated ...".format(i + 1))
            text, alignment = texts[i], alignments[i]
            print(alignment.shape)
            print("len text", float(len(text)))
            min_sample_sec = float(get_EOS_index(text)) * SEC_PER_CHAR
            print("min sec ", min_sample_sec)
            al_EOS_index = get_EOS_fire(alignment, text)
            al_EOS_index = None

            if not al_EOS_index == None:
                # trim the audio
                audio = spectrogram2wav(mag[:al_EOS_index * hp.r, :])
            else:
                audio = spectrogram2wav(mag, min_sample_sec)
            audio_path = os.path.join(hp.sampledir, '{}.wav'.format(i + 1))
            write(audio_path, hp.sr, audio)
            print(audio_path)
            return audio_path


if __name__ == '__main__':
    args = sys.argv[1:]
    lang = args[0]
    hyperparams._H =hyperparams.Hyperparams(lang) 
    text = args[1]
    synthesize(text)
    print("Done")