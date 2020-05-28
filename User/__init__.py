import kcnn
from collections import deque

cnn = kcnn.kconvuph(10, 3)
cnn.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
cnn.load_weights('cnnmodel/uphrcnn12cp')
labQ = deque(maxlen=5)
prelabel = deque([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
