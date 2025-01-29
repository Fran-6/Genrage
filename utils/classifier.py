import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


# paramètres:

allowed_characters = "abcdefghijklmnopqrstuvwxyz '-àâçèéêëîïñôöûü"
n_letters = len(allowed_characters)
alldata_labels_uniq = ['fs', 'ms']
n_hidden = 128//2
candidats = ["ure", "érafe", "intère", "harise", "harisse", "mec", "mecton", "crunarde", "sépale"]

# fonctions

def set_cuda():
    # Check if CUDA is available
    device = torch.device('cpu')
    if torch.cuda.is_available():
        device = torch.device('cuda')

    torch.set_default_device(device)
    return torch.get_default_device()

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


def set_classifier():
    set_cuda()
    rnn = CharRNN(n_letters, n_hidden, len(alldata_labels_uniq))
    rnn.load_state_dict(torch.load('./utils/rnn_model.pth', weights_only=True)) # charge les paramètres du modèle à partir du fichier.
    return rnn

def evaluation(lexeme, rnn):

    rnn.eval() #set to eval mode    
    classes=alldata_labels_uniq
    with torch.no_grad(): # do not record the gradients during eval phase
        text_tensor = lineToTensor(lexeme)
        output = rnn(text_tensor)   
        guess, guess_i = label_from_output(output, classes)

    sortie = output.numpy()[0]
    sortie = np.exp(sortie)

    return guess_i, sortie[guess_i]

