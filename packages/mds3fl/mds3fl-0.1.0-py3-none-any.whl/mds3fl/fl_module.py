import os
import numpy as np
import pandas as pd
import tensorflow as tf
import time
import pickle
import socket
from tensorflow.keras import layers


class MDS3FL:
    def __init__(self, is_server: bool, path1: str, path2: str, path3: str, path4: str, wr2: str,
                 client_num: int, server_ip: str, port: int, input_shape, num_conv, num_nodes,
                 use_batchnorm, use_dropout, use_reg, LR):
        self.server_status = is_server
        self.data_path = path1
        self.pathTrain1 = path2
        self.pathTrain2 = path3
        self.pathTrain3 = path4
        self.wr2 = wr2
        self.clients_count = client_num
        self.server_ip = server_ip
        self.port = port
        self.input_shape = input_shape
        self.num_conv = num_conv
        self.num_nodes = num_nodes
        self.use_batchnorm = use_batchnorm
        self.use_dropout = use_dropout
        self.use_reg = use_reg
        self.LR = LR

        (self.pb1_image_paths, self.pb2_image_paths, self.pb3_image_paths,
         self.wr2_image_paths, self.pb1_label, self.pb2_label, self.pb3_label,
         self.wr2_label) = self.retrieveData()

        self.model = self.dynamic_cnn_model()

    def retrieveData(self):
        xl_file = pd.ExcelFile(self.data_path)
        dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}
        beta = dfs['Beta Fraction']

        WR2 = beta.iloc[:, [0, 5]].iloc[6:1107]
        PB1 = beta.iloc[:, [7, 12]].iloc[6:1062]
        PB2 = beta.iloc[:, [14, 19]].iloc[6:1103]
        PB3 = beta.iloc[:, [21, 26]].iloc[6:861]

        pb1_label = list(PB1['Unnamed: 12'])
        pb2_label = list(PB2['Unnamed: 19'])
        pb3_label = list(PB3['Unnamed: 26'])
        wr2_label = list(WR2['Unnamed: 5'])

        def collect_image_paths(base_path, slice_range):
            paths = []
            for root, dirs, files in os.walk(base_path, topdown=False):
                for i in files:
                    paths.append(os.path.join(root, i))
            paths.sort()
            return paths[slice_range[0]:slice_range[1]]

        pb1_image_paths = collect_image_paths(self.pathTrain1, (2, -21))
        pb2_image_paths = collect_image_paths(self.pathTrain2, (4, -2))
        pb3_image_paths = collect_image_paths(self.pathTrain3, (2, -4))
        wr2_image_paths = collect_image_paths(self.wr2, (2, None))

        return (pb1_image_paths, pb2_image_paths, pb3_image_paths, wr2_image_paths,
                pb1_label, pb2_label, pb3_label, wr2_label)

    def dynamic_cnn_model(self):
        inputs = tf.keras.layers.Input(shape=self.input_shape)
        x = inputs

        if self.use_reg == 1:
            reg = tf.keras.regularizers.l1(0.01)
        elif self.use_reg == 2:
            reg = tf.keras.regularizers.l2(0.01)
        elif self.use_reg == 3:
            reg = tf.keras.regularizers.l1_l2(l1=0.01, l2=0.01)
        else:
            reg = None

        for i in range(self.num_conv):
            filters = 2 ** (i + 4) if self.num_conv <= 5 else 2 ** (int((i - 0.1) / 4) + 3)
            x = layers.Conv2D(filters, (3, 3), activation='relu', activity_regularizer=reg)(x)
            if self.use_batchnorm:
                x = layers.BatchNormalization()(x)
            x = layers.MaxPooling2D((2, 2))(x)

        x = layers.Flatten()(x)
        for nodes in self.num_nodes:
            x = layers.Dense(nodes, activation=layers.LeakyReLU(alpha=0.005), activity_regularizer=reg)(x)
            if self.use_dropout:
                x = layers.Dropout(0.5)(x)

        outputs = layers.Dense(1)(x)
        return tf.keras.Model(inputs, outputs)

    def path_label_generator(self, img_paths, labels):
        for img_path, label in zip(img_paths, labels):
            yield (img_path, label)

    def load_image(self, file_path, label):
        img = np.load(file_path.numpy().decode('utf-8'))
        img = img[:, :, None]
        img = tf.convert_to_tensor(img, dtype=tf.float32)
        label = tf.convert_to_tensor(label, dtype=tf.float32)
        return img, label

    def load_image_wrapper(self, file_path, label):
        return tf.py_function(self.load_image, [file_path, label], [tf.float32, tf.float32])

    def prepare_data(self, client_id: int, batch_size=8):
        cluster2_x = self.pb1_image_paths[800:] + self.pb2_image_paths[800:] + self.wr2_image_paths[800:]
        cluster2_Y = self.pb1_label[800:] + self.pb2_label[800:] + self.wr2_label[800:]
        idx = np.random.permutation(len(cluster2_Y))
        cluster2_x = np.array(cluster2_x)[idx]
        cluster2_Y = np.array(cluster2_Y)[idx]

        ds = tf.data.Dataset.from_generator(
            self.path_label_generator,
            args=(cluster2_x, cluster2_Y),
            output_signature=(tf.TensorSpec(shape=(), dtype=tf.string),
                              tf.TensorSpec(shape=(), dtype=tf.float32))
        ).map(self.load_image_wrapper, num_parallel_calls=tf.data.AUTOTUNE)

        sampling = 100
        client_ds = ds.skip(client_id * sampling).take(sampling).batch(batch_size)
        return client_ds

    def federated_avg(self, weights, client_sizes):
        total_size = np.sum(client_sizes)
        avg_weights = [np.zeros_like(w) for w in weights[0]]
        for weight, size in zip(weights, client_sizes):
            for i in range(len(weight)):
                avg_weights[i] += weight[i] * (size / total_size)
        return avg_weights

    def train_client_model(self, dataset, initial_weights, num_epochs=1):
        model = self.dynamic_cnn_model()
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.LR),
                      loss='mse', run_eagerly=True)
        model.set_weights(initial_weights)
        model.fit(dataset, epochs=num_epochs)
        return model.get_weights()

    def send_data(self, sock, data):
        data_bytes = pickle.dumps(data)
        sock.sendall(data_bytes)

    def recv_data(self, sock):
        chunks = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
        return pickle.loads(b''.join(chunks))

    def train(self, num_rounds=10):
        if self.server_status:
            # Server setup
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('0.0.0.0', self.port))
            server_socket.listen(self.clients_count)
            client_sockets = [server_socket.accept()[0] for _ in range(self.clients_count)]
            print(f"Connected {len(client_sockets)} clients")

            client_sizes = [len(list(self.prepare_data(i))) for i in range(self.clients_count)]
            global_weights = self.model.get_weights()

            for rnd in range(num_rounds):
                print(f"Round {rnd + 1}")
                client_weights = []
                for sock in client_sockets:
                    self.send_data(sock, global_weights)
                for sock in client_sockets:
                    client_weights.append(self.recv_data(sock))
                global_weights = self.federated_avg(client_weights, client_sizes)
            print("Training complete.")

        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server_ip, self.port))
            dataset = self.prepare_data(1)
            for rnd in range(num_rounds):
                print(f"[Client] Round {rnd + 1}")
                global_weights = self.recv_data(sock)
                updated_weights = self.train_client_model(dataset, global_weights)
                self.send_data(sock, updated_weights)