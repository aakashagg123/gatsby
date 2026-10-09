"""A tiny neural network (2 inputs, one hidden layer, 1 output) with backpropagation written by hand.

Forward:  h = tanh(W1 x + b1)      p = sigmoid(W2 h + b2)
Loss:     average log loss.
Backward: the chain rule, applied from the output back to the input. That is all backpropagation is.
"""
import math
import random


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))


class TinyNet:
    def __init__(self, n_in=2, n_hidden=6, seed=0):
        rng = random.Random(seed)
        self.w1 = [[rng.gauss(0, 0.8) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.w2 = [rng.gauss(0, 0.8) for _ in range(n_hidden)]
        self.b2 = 0.0

    def forward(self, x):
        h = [math.tanh(sum(w * v for w, v in zip(row, x)) + b) for row, b in zip(self.w1, self.b1)]
        p = sigmoid(sum(w * a for w, a in zip(self.w2, h)) + self.b2)
        return h, p

    def loss(self, rows, labels):
        total = 0.0
        for x, y in zip(rows, labels):
            p = min(max(self.forward(x)[1], 1e-9), 1 - 1e-9)
            total += -(y * math.log(p) + (1 - y) * math.log(1 - p))
        return total / len(rows)

    def gradients(self, rows, labels):
        """Return gradients of the average loss for every weight, in the same shapes."""
        n = len(rows)
        g_w1 = [[0.0] * len(self.w1[0]) for _ in self.w1]
        g_b1 = [0.0] * len(self.b1)
        g_w2 = [0.0] * len(self.w2)
        g_b2 = 0.0
        for x, y in zip(rows, labels):
            h, p = self.forward(x)
            d_out = p - y                                          # slope of the loss at the output
            for j, a in enumerate(h):
                g_w2[j] += d_out * a / n                           # output weights
                d_hidden = d_out * self.w2[j] * (1 - a * a)        # pass the slope back through tanh
                g_b1[j] += d_hidden / n
                for i, v in enumerate(x):
                    g_w1[j][i] += d_hidden * v / n                 # hidden weights
            g_b2 += d_out / n
        return g_w1, g_b1, g_w2, g_b2

    def step(self, grads, lr):
        g_w1, g_b1, g_w2, g_b2 = grads
        for j in range(len(self.w1)):
            for i in range(len(self.w1[j])):
                self.w1[j][i] -= lr * g_w1[j][i]
            self.b1[j] -= lr * g_b1[j]
            self.w2[j] -= lr * g_w2[j]
        self.b2 -= lr * g_b2

    def train(self, rows, labels, lr=0.8, epochs=800):
        curve = []
        for _ in range(epochs):
            self.step(self.gradients(rows, labels), lr)
            curve.append(self.loss(rows, labels))
        return curve

    def predict(self, rows):
        return [self.forward(x)[1] for x in rows]
