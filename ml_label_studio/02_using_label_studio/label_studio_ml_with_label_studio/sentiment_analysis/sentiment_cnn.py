# SentimentCNN class based on Sentiment Analysis tutorial by Ben Trevett
# https://github.com/bentrevett/pytorch-sentiment-analysis

import torch
import torch.nn as nn
import torchtext
 
class SentimentCNN(nn.Module):
    def __init__(self, state_dict=None, vocab=None, tokenizer='basic_english'):
        super().__init__()

        # tokenizer setup
        self.tokenizer = torchtext.data.utils.get_tokenizer(tokenizer)
        self.state_dict_name = state_dict

        if vocab:
            self.load_vocab(vocab)

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def _setup_model(self):
        # cnn parameters
        n_filters=100
        filter_sizes=[3,5,7]
        dropout_rate=0.25
        self.min_length = max(filter_sizes)

        # language space parameters
        embedding_dim=300
        output_dim=2

        # model setup
        self.embedding = nn.Embedding(
               len(self.vocab),
               embedding_dim,
               padding_idx=self.pad_index)
        self.convs = nn.ModuleList([nn.Conv1d(embedding_dim, 
                                              n_filters, 
                                              filter_size) 
                                    for filter_size in filter_sizes])
        self.fc = nn.Linear(len(filter_sizes) * n_filters, output_dim)
        self.dropout = nn.Dropout(dropout_rate)

        if self.state_dict_name:
            self.load_state_dict(torch.load(self.state_dict_name))

    def load_vocab(self, vocab):
        # vocabulary parameters
        self.vocab = torch.load(vocab)
        self.pad_index = self.vocab['<pad>']
        self._setup_model()
        
    def forward(self, ids):
        embedded = self.dropout(self.embedding(ids))
        embedded = embedded.permute(0,2,1)
        conved = [torch.relu(conv(embedded)) for conv in self.convs]
        pooled = [conv.max(dim=-1).values for conv in conved]
        cat = self.dropout(torch.cat(pooled, dim=-1))
        prediction = self.fc(cat)
        return prediction

    def predict_sentiment(self, text):
        tokens = self.tokenizer(text)
        ids = [self.vocab[t] for t in tokens]
        if len(ids) < self.min_length:
            ids += [self.pad_index] * (self.min_length - len(ids))
        tensor = torch.LongTensor(ids).unsqueeze(dim=0).to(self.device)
        prediction = self(tensor).squeeze(dim=0)
        probability = torch.softmax(prediction, dim=-1)
        predicted_class = prediction.argmax(dim=-1).item()
        predicted_probability = probability[predicted_class].item()

        return predicted_class, predicted_probability
