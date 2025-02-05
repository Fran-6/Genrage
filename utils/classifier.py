import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import streamlit as st


# paramètres:

allowed_characters = "abcdefghijklmnopqrstuvwxyz '-àâçèéêëîïñôöûü"
n_letters = len(allowed_characters)
alldata_labels_uniq = ['fs', 'ms']
n_hidden = 128//2
candidats = ["ure", "érafe", "intère", "harise", "harisse", "mec", "mecton", "crunarde", "sépale"]

# fonctions

# def set_cuda():
#     # Check if CUDA is available
#     device = torch.device('cpu')
#     if torch.cuda.is_available():
#         device = torch.device('cuda')

#     torch.set_default_device(device)
#     return torch.get_default_device()

# %
class CharRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(CharRNN, self).__init__()

        self.rnn = nn.RNN(input_size, hidden_size) # done
        self.h2o = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)
    
    def forward(self, line_tensor):
        rnn_out, hidden = self.rnn(line_tensor)
        output = self.h2o(hidden[0])
        output = self.softmax(output)

        return output

# %
# todo : transformer en dcitionnaire
# Find letter index from all_letters, e.g. "a" = 0
def letterToIndex(letter):
    return allowed_characters.find(letter)

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor

# %
def label_from_output(output, output_labels):
    top_n, top_i = output.topk(1)
    label_i = top_i[0].item()
    return output_labels[label_i], label_i

@st.cache_resource
def set_classifier():
    # set_cuda()
    rnn = CharRNN(n_letters, n_hidden, len(alldata_labels_uniq))
    import os
    rnn.load_state_dict(torch.load('./utils/rnn_model.pth', weights_only=True)) # charge les paramètres du modèle à partir du fichier.
    return rnn

def evaluation(lexeme, rnn):
    lexeme = lexeme.lower()
    rnn.eval() #set to eval mode    
    classes=alldata_labels_uniq
    with torch.no_grad(): # do not record the gradients during eval phase
        text_tensor = lineToTensor(lexeme)
        output = rnn(text_tensor)   
        guess, guess_i = label_from_output(output, classes)

    sortie = output.numpy()[0]
    sortie = np.exp(sortie)

    return guess_i, sortie[guess_i]

def check_input_text(saisie):
    saisie = saisie.lower().replace(chr(10), ";") # enlève les sauts de ligne
    s = set(saisie) - (set(allowed_characters) | set(";"))
    lexemes = []
    lexemes = saisie.split(";")
    lexemes = [l.strip() for l in lexemes if (l != "" and not l.isspace())]
    # les chaînes vides ou faites d'espaces font planter le RNN
    nb_words = len(lexemes)
    nb_limite_de_mots = 20
    if not lexemes:
        max_word = ""
        max_len = 0
    else:
        max_word = max(lexemes, key=len)
        max_len = len(max_word)

    answer = None

    if nb_words == 0 or saisie == "":
        answer = '### Veuillez saisir un mot ou des mots séparés par ":red[;]" '
    elif len(s)!=0:
        answer = '### Caractère(s) non autorisé(s): ' + " ".join(sorted(s))
    elif len(saisie) > 30 * 10:
        answer = f'### Nombre de caratères  saisis {len(saisie)} contre {30*10} maximum autorisés'
    elif nb_words > nb_limite_de_mots:
        answer = f'### Trop de mots saisis "{nb_words}" contre {nb_limite_de_mots} maximum autorisés)'
    elif max_len > 30:  
         answer = f'### Mot saisi "{max_word}" trop long, {max_len} caractères contre 30 maximum autorisés)'
    else:
        pass
    

    return answer, lexemes
    

