def andgate():
    """
    import numpy as np 

    def step_function(x):
        return 1 if x>= 0 else 0

    def perceptron_learning(X, y, learning_rate= 0.1, epochs = 10):
        weights = np.zeros(X.shape[1])
        bias = 0
        
        for epoch in range(epochs):
            for i in range(len(X)):
                linear_output = np.dot(X[i], weights) +bias
                prediction = step_function(linear_output)
                error = y[i] - prediction
                weights += learning_rate * error* X[i]
                bias += learning_rate *error
                
        return weights, bias


    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1])

    weights, bias = perceptron_learning(X, y)

    def predict(X, weights, bias):
        linear_output = np.dot(X, weights) + bias
        return step_function(linear_output)

    for x in X:
        print(x, predict(x, weights, bias))
        
        """
        
def titanic():
    """
    import re
    import seaborn as sns

    def match(data, pattern, column):
        return [value for value in data[column].dropna() if re.match(str(value), pattern)]
    titanic = sns.load_dataset('titanic')
    print("choose form the columns", titanic.columns)
    column = input("enter the column    ")
    pattern = input("enter the pattern  ")

    matches = match(titanic, pattern, column)

    print(f'found {len(matches)} matches in the column {column} for the pattern {pattern}')

    
    """
    
def mahalanobis():
    """
    import numpy as np
    from scipy.spatial.distance import mahalanobis
    
    def compute_mahalanobis_distance_between_polygons(polygon1, polygon2):
        poly1_array, poly2_array = np.array(polygon1), np.array(polygon2)
        centroid1, centroid2 = np.mean(poly1_array, axis=0), np.mean(poly2_array, axis=0)
        inv_cov_matrix = np.linalg.inv(np.cov(np.vstack((poly1_array, poly2_array)).T))
        return mahalanobis(centroid1, centroid2, inv_cov_matrix)

    if __name__ == "__main__":
        def get_polygon_input(polygon_num):
            print(f"Enter the coordinates of Polygon {polygon_num} (e.g., x1 y1, x2 y2, ...):")
            points = input("Coordinates: ").strip().split(",")
            polygon = [tuple(map(float, point.strip().split())) for point in points]
            return polygon
    
        polygon1 = get_polygon_input(1)
        polygon2 = get_polygon_input(2)
        distance = compute_mahalanobis_distance_between_polygons(polygon1, polygon2)
        print(f"Mahalanobis Distance between the polygons: {distance}")


    
    
    """
    
def shannon():
    """
    
    import seaborn as sns
    import numpy as np

    df = sns.load_dataset('titanic')

    # Choose a column
    column = input('enter column name')

    # Get value counts and convert to probabilities
    value_counts = df[column].value_counts(normalize=True)

    # Compute Shannon entropy manually
    probabilities = value_counts.values
    shannon_entropy = -np.sum(probabilities * np.log2(probabilities))

    print(f"Shannon Entropy of column '{column}': {shannon_entropy:.4f}")


    """
    
def unsupervised():
    
    """
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    from sklearn.cluster import KMeans
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from tensorflow.keras.utils import to_categorical
    from sklearn.decomposition import PCA

    # Load dataset
    digits = load_digits()
    X = digits.images / 16.0  # Normalize
    y = digits.target
    X = np.expand_dims(X, axis=-1)  # Add channel dimension

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    y_train_cat = to_categorical(y_train, num_classes=10)
    y_test_cat = to_categorical(y_test, num_classes=10)

    # Supervised Learning: Build CNN Model
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(8, 8, 1)),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train model
    model.fit(X_train, y_train_cat, epochs=10, validation_data=(X_test, y_test_cat), batch_size=32)

    # Evaluate model
    test_acc = model.evaluate(X_test, y_test_cat, verbose=0)[1]
    print(f"Test Accuracy: {test_acc:.2f}")

    # Unsupervised Learning: Apply K-Means Clustering
    X_flattened = X.reshape(X.shape[0], -1)
    kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_flattened)

    # Reduce dimensions for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_flattened)

    # Plot clustered images
    fig, axes = plt.subplots(1, 5, figsize=(10, 5))
    for i, ax in enumerate(axes):
        ax.imshow(X[i].squeeze(), cmap='gray')
        ax.set_title(f"Cluster {labels[i]}")
        ax.axis('off')
    plt.show()

    # Plot PCA visualization
    plt.figure(figsize=(8, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis', alpha=0.6)
    plt.colorbar(label="Cluster Label")
    plt.title("PCA Visualization of Clusters")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.show()

    
    
    
    """
    
def bayesian():
    
    """
    
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.datasets import load_iris
    
    # Load dataset
    data = load_iris()
    X = data.data  # Features
    y = data.target  # Target labels
    
    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train the Bayesian classifier
    model = GaussianNB()
    model.fit(X_train, y_train)
    
    # Predict on test data
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=data.target_names)
    
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

    
    """
    
def hopfield():
    """
    
    import numpy as np 
    def train_hopfield(patterns): 
        num_neurons = len(patterns[0]) 
        weight_matrix = np.zeros((num_neurons, num_neurons)) 
        for pattern in patterns: 
            pattern = np.array(pattern).reshape(-1, 1) 
            weight_matrix += pattern @ pattern.T 
        np.fill_diagonal(weight_matrix, 0)  # No self-connections 
        return weight_matrix 
    def recall_pattern(weight_matrix, input_pattern, max_iterations=10): 
        output_pattern = np.array(input_pattern) 
        for _ in range(max_iterations): 
            for i in range(len(output_pattern)): 
                net_input = np.dot(weight_matrix[i], output_pattern) 
                output_pattern[i] = 1 if net_input >= 0 else -1 
        return output_pattern 
    # Original pattern 
    original_pattern = [-1, 1, -1, -1, -1, -1, -1, 1, -1, 1] 
    # Train the Hopfield network 
    weight_matrix = train_hopfield([original_pattern]) 
    # Noisy pattern to recover 
    noisy_pattern = [-1, -1, -1, 1, -1, -1, -1, 1, -1, -1] 
    # Recovered pattern 
    recovered_pattern = recall_pattern(weight_matrix, noisy_pattern) 
    print("Original Pattern:", original_pattern) 
    print("Noisy Pattern:", noisy_pattern) 
    print("Recovered Pattern:", recovered_pattern) 
    
    
    """
    
def fuzzy():
    
    """
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import StandardScaler
    from fcmeans import FCM
    from sklearn.datasets import load_wine
    
    # Load publicly available dataset (Wine dataset)
    wine = load_wine()
    X = wine.data[:, :2]  # Taking only the first two features for visualization
    
    # Standardizing the dataset
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply Fuzzy C-Means
    fcm = FCM(n_clusters=3, m=2.0, max_iter=150, error=1e-5, random_state=42)
    fcm.fit(X_scaled)
    
    # Get cluster centers and labels
    centers = fcm.centers
    labels = fcm.predict(X_scaled)
    
    # Plot results
    plt.figure(figsize=(8, 6))
    for i in range(3):
        plt.scatter(X_scaled[labels == i, 0], X_scaled[labels == i, 1], label=f'Cluster {i+1}')
    plt.scatter(centers[:, 0], centers[:, 1], marker='x', color='black', s=200, label='Centers')
    plt.show()

    
    
    
    
    """
    
def male():
    """
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Flatten, InputLayer
    import matplotlib.pyplot as plt

    data = './Training'
    img_size = (64, 64)

    datagen = ImageDataGenerator(rescale=1. / 255, validation_split=0.2)

    train = datagen.flow_from_directory(data, target_size=img_size, batch_size=32, class_mode='binary',
                                        subset='training')
    val = datagen.flow_from_directory(data, target_size=img_size, batch_size=32, class_mode='binary',
                                    subset='validation')

    model = Sequential([
        InputLayer(input_shape=(*img_size, 3)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    h = model.fit(
        train,
        validation_data=val,
        epochs=10
    )

    plt.plot(h.history['accuracy'], label='Train Acc')
    plt.plot(h.history['val_accuracy'], label='Val Acc')
    plt.plot(h.history['loss'], label='Train Loss')
    plt.plot(h.history['val_loss'], label='Val Loss')
    plt.xlabel("Epochs"), plt.ylabel("Loss/Accuracy")
    plt.legend(), plt.show()

    print(f"\nTest Accuracy: {model.evaluate(val, verbose=0)[1]:.2f}")

    
    
    
    """

def handwritten():
    
    """
    
    import tensorflow as tf
    from tensorflow.keras import datasets, layers, models, utils

    # Load and preprocess data
    (x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()
    x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255
    x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255

    y_train = utils.to_categorical(y_train, 10)
    y_test = utils.to_categorical(y_test, 10)

    # Build the CNN model
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])

    # Compile and train
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_test, y_test))

    # Evaluate
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print(f"Test accuracy: {test_acc:.4f}")

    
    
    
    """
    
def fuzz_real():
    
    
    """
    import cv2 
    import numpy as np
    import skfuzzy as fuzz
    import skfuzzy.control as ctrl

    brightness = ctrl.Antecedent(np.arange(0, 256, 1), 'brightness')
    edge_intensity = ctrl.Antecedent(np.arange(0, 256, 1), 'edge_intensity') 
    classification = ctrl.Consequent(np.arange(0, 101, 1), 'classification')

    brightness['dark'] = fuzz.trimf(brightness.universe, [0, 50, 100]) 
    brightness['normal'] = fuzz.trimf(brightness.universe, [50, 127, 200])
    brightness['bright'] = fuzz.trimf(brightness.universe, [150, 200, 255]
                                    )
    edge_intensity['low'] = fuzz.trimf(edge_intensity.universe, [0, 50, 100]) 
    edge_intensity['medium'] = fuzz.trimf(edge_intensity.universe, [50, 127, 200]) 
    edge_intensity['high'] = fuzz.trimf(edge_intensity.universe, [150, 200, 255])

    classification['low'] = fuzz.trimf(classification.universe, [0, 25, 50]) 
    classification['medium'] = fuzz.trimf(classification.universe, [25, 50, 75]) 
    classification['high'] = fuzz.trimf(classification.universe, [50, 75, 100])

    rule1 = ctrl.Rule(brightness['dark'] | edge_intensity['low'], classification['low']) 
    rule2 = ctrl.Rule(brightness['normal'] | edge_intensity['medium'], classification['medium']) 
    rule3 = ctrl.Rule(brightness['bright'] | edge_intensity['high'], classification['high'])

    classification_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    classifier = ctrl.ControlSystemSimulation(classification_ctrl)
    def real_time_image_classification(): 
        cap = cv2.VideoCapture(0) 
        while True: 
            ret, frame = cap.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness_value = np.mean(gray)
            edges = cv2.Canny(gray, 100, 200)
            edge_intensity_value = np.mean(edges)
            
            classifier.input['brightness'] = brightness_value
            classifier.input['edge_intensity'] = edge_intensity_value
            classifier.compute()
            
            classification_result = classifier.output['classification']
            cv2.putText(frame, f'Classification: {classification_result:.2f}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow('Real-Time Classification', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            cap.release()
            cv2.destroyAllWindows()
        
    if __name__ == "__main__": 
        real_time_image_classification()

        
        
        
    
    
    """
    
def kmeans():
    """
    
    import cv2 
    import numpy as np
    cap = cv2.VideoCapture(0)
    k = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    attempts = 10
    while True: 
        ret, frame = cap.read() 
        if not ret: break
        resized_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

        pixel_data = resized_frame.reshape((-1, 3))
        pixel_data = np.float32(pixel_data)
        

        _, labels, centers = cv2.kmeans(pixel_data, k, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)

        centers = np.uint8(centers)
        segmented_data = centers[labels.flatten()]
        segmented_image = segmented_data.reshape(resized_frame.shape)

        cv2.imshow('Real-Time K-Means Clustering', segmented_image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    """
    


def activation():
    
    """
    import numpy as np

class Neuron:
    def __init__(self, features):
        self.weights = np.random.rand(features)
        self.bias = np.random.rand()

    def activate(self, x):
        return 1 / (1 + np.exp(-np.dot(x, self.weights) - self.bias))

    def train(self, inputs, targets, lr=0.01, num_iters=10000):
        for _ in range(num_iters):
            idx = np.random.randint(len(inputs))
            error = targets[idx] - self.activate(inputs[idx])
            self.weights += lr * error * inputs[idx]
            self.bias += lr * error

neuron = Neuron(3)
x_train = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
y_train = np.array([0, 1, 1, 1])
neuron.train(x_train, y_train)

for x, y in zip(x_train, y_train):
    print(f"Input: {x}, Prediction: {neuron.activate(x):.4f}, Actual: {y}")

    
    
    
    
    """
    
def error():
    """
    import torch

x_train = torch.tensor([[1, 2], [2, 3], [3, 4], [4, 5]], dtype=torch.float32)
y_train = torch.tensor([0, 0, 1, 1], dtype=torch.int64)
x_test = torch.tensor([[5, 6], [0, 1]], dtype=torch.float32)

# Simple KNN using PyTorch
k = 3
y_pred = []

for x in x_test:
    distances = torch.norm(x_train - x, dim=1)
    nearest_labels = y_train[torch.topk(distances, k, largest=False).indices]
    y_pred.append(torch.mode(nearest_labels).values.item())

print("Predictions:", y_pred)
"""


def hebbian():
    """
    import numpy as np
class Neuron:
    def __init__(self, num_inputs):
        self.weights = np.random.rand(num_inputs)
    
    def activate(self, inputs):
        weighted_sum = np.dot(inputs, self.weights)
        return weighted_sum
    
    def learn_hebbian(self, inputs, learning_rate):
        activation = self.activate(inputs)
        
        self.weights += learning_rate * activation * inputs
        

if __name__ == "__main__":
    num_inputs = 3
    neuron = Neuron(num_inputs)
    
    inputs = np.array([0.5, 0.3, 0.2])
    learning_rate = 0.1
    num_iterations = 1000
    
    for i in range(num_iterations):
        neuron.learn_hebbian(inputs, learning_rate)
    print(neuron.weights)
    
    
    
    """
    
    
def gates():
    """
    
    
import numpy as np
import matplotlib.pyplot as plt

def gaussian(v, w):
    return np.exp(-np.linalg.norm(v - w) ** 2)

inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
outputs = np.array([0, 1, 1, 0])
w1, w2 = np.array([1, 1]), np.array([0, 0])

f1 = [gaussian(i, w1) for i in inputs]
f2 = [gaussian(i, w2) for i in inputs]

# Visualization
plt.figure(figsize=(4, 4))
for i in range(len(inputs)):
    marker = 'x' if outputs[i] == 0 else 'o'
    plt.scatter(f1[i], f2[i], marker=marker, label=f"Class {outputs[i]}" if plt.gca().get_legend_handles_labels()[1].count(f"Class {outputs[i]}") == 0 else "")

x = np.linspace(0, 1, 10)
plt.plot(x, -x + 1, label="y = -x + 1")

plt.xlabel("Hidden Function 1")
plt.ylabel("Hidden Function 2")
plt.xlim(-0.1, 1)
plt.ylim(-0.1, 1)
plt.legend()
plt.grid()
plt.show()

    """
    
def xor():
    """
    
    
    import tensorflow as tf
import numpy as np

x = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

model = tf.keras.Sequential([
    tf.keras.layers.Dense(2, activation='sigmoid'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='mse')
model.fit(x, y, epochs=500, verbose=0)

for i in x:
    prediction = model.predict(i.reshape(1, -1), verbose=0)[0][0]
    print(f"Input: {i}, Predicted: {prediction:.2f}")

    """
    
def xor_rbf():
    
    """
    import numpy as np
import matplotlib.pyplot as plt

def gaussian(v, w):
    return np.exp(-np.linalg.norm(v - w) ** 2)

inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
outputs = np.array([0, 1, 1, 0])
w1, w2 = np.array([1, 1]), np.array([0, 0])

f1 = [gaussian(i, w1) for i in inputs]
f2 = [gaussian(i, w2) for i in inputs]

# Visualization
plt.figure(figsize=(5, 5))
for i in range(len(inputs)):
    marker = 'x' if outputs[i] == 0 else 'o'
    plt.scatter(f1[i], f2[i], marker=marker)

x = np.linspace(0, 1, 10)
plt.plot(x, -x + 1)

plt.show()

    
    
    
    
    """

def hebbian_pca():
    """
    import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Generate data
data = np.random.multivariate_normal([0, 0], [[3, 2], [2, 2]], 1000)

# Hebbian learning
weights = np.random.randn(2)
for x in data:
    weights += 0.01 * np.dot(weights, x) * x
weights /= np.linalg.norm(weights)

# PCA
pca_direction = PCA(n_components=1).fit(data).components_[0]

# Plot
plt.scatter(data[:, 0], data[:, 1], alpha=0.3)
plt.quiver(0, 0, weights[0], weights[1], color='r', scale=3)
plt.quiver(0, 0, pca_direction[0], pca_direction[1], color ='g', scale=3)
plt.axis('equal')
plt.show()

    
    
    
    
    """

def som():
    """
    # Implement the features used in Self organizing maps using competitive learning algorithm. 
import numpy as np
import matplotlib.pyplot as plt

class SOM:
    def _init_(self, grid_size, input_dim, learning_rate=0.5, sigma=1.0, iterations=1000):
        self.grid_size = grid_size
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.sigma = sigma
        self.iterations = iterations
        
        # Initialize weights randomly
        self.weights = np.random.rand(grid_size, grid_size, input_dim)
        
        # Create grid of neuron coordinates
        self.neuron_positions = np.array([[np.array([i, j]) for j in range(grid_size)] for i in range(grid_size)])

    def find_bmu(self, sample): #BMU = best matching unit
        distances = np.linalg.norm(self.weights - sample, axis=2)
        return np.unravel_index(np.argmin(distances), distances.shape)
    
    def update_weights(self, sample, bmu, iteration):
        learning_rate = self.learning_rate * (1 - iteration / self.iterations)
        sigma = self.sigma * (1 - iteration / self.iterations)
        
        # Compute distance from BMU
        distance_to_bmu = np.linalg.norm(self.neuron_positions - np.array(bmu), axis=2)
        
        # Compute neighborhood function (Gaussian)
        neighborhood = np.exp(-distance_to_bmu*2 / (2 * (sigma*2)))
        
        # Update weights
        self.weights += learning_rate * neighborhood[:, :, np.newaxis] * (sample - self.weights)
    
    def train(self, data):
        for i in range(self.iterations):
            sample = data[np.random.randint(0, len(data))]  # Pick a random sample
            bmu = self.find_bmu(sample)
            self.update_weights(sample, bmu, i)
    
    def plot_weights(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = self.weights[i, j]  # Extract RGB color from weight vector
                ax.add_patch(plt.Rectangle((j, self.grid_size - i - 1), 1, 1, color=color, ec='black'))
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, self.grid_size)
        ax.set_ylim(0, self.grid_size)
        plt.show()

# Generate synthetic data
np.random.seed(42)
data = np.random.rand(1000, 3)  # 1000 samples with 3 features (RGB colors)

# Train SOM
som = SOM(grid_size=10, input_dim=3, iterations=5000)
som.train(data)

# Plot the SOM weight map
som.plot_weights()
    
    
    """
    
def backprop():
    """
    import tensorflow as tf

# Define model
input_size, hidden_size, output_size = 3, 5, 1
inputs = tf.keras.Input(shape=(None, input_size))
x = tf.keras.layers.SimpleRNN(hidden_size)(inputs)
outputs = tf.keras.layers.Dense(output_size)(x)
model = tf.keras.Model(inputs, outputs)

# Compile and train
model.compile(optimizer="adam", loss="mse") 
data = tf.random.normal((2, 4, input_size))
targets = tf.random.normal((2, output_size))
model.fit(data, targets, epochs=10,verbose=2)


    
    """



def neural():
    """
    import numpy as np 
import matplotlib.pyplot as plt 
from tensorflow import keras 
from tensorflow.keras.datasets import mnist 
from tensorflow.keras.utils import to_categorical 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout 
#Load the dataset 
(X_train, y_train), (X_test, y_test) = mnist.load_data() 
# Pre-process the data 
X_train = X_train.astype(np.float32) / 255.0 
X_test = X_test.astype(np.float32) / 255.0 
# Reshape the data to add a channel dimension 
X_train = np.expand_dims(X_train, axis=-1) 
X_test = np.expand_dims(X_test, axis=-1) 
# One-hot encode the labels 
y_train = to_categorical(y_train, num_classes=10) 
y_test = to_categorical(y_test, num_classes=10) 
model = Sequential() 
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1))) 
model.add(MaxPooling2D(pool_size=(2, 2))) 
model.add(Dropout(0.25)) 
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu')) 
model.add(MaxPooling2D(pool_size=(2, 2))) 
model.add(Dropout(0.25)) 
model.add(Flatten()) 
model.add(Dense(128, activation='relu')) 
model.add(Dense(10, activation='softmax')) 
# Compile the model 
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']) 
# Train the model 
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, 
y_test)) 
# Evaluate the model 
loss, accuracy = model.evaluate(X_test, y_test) 
print("Loss: ", loss) 
print("Accuracy: ", accuracy) 
#Extract the accuracy history 
acc = history.history['accuracy'] 
val_acc = history.history['val_accuracy'] 
# Plot the accuracy history 
plt.plot(acc) 
plt.plot(val_acc) 
plt.title('Model Accuracy') 
plt.ylabel('Accuracy') 
plt.xlabel('Epoch') 
plt.legend(['Train', 'Test'], loc='upper left') 
plt.show() 
    
    
    """
    
def optimisation():
    """
    import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Load and preprocess data
def get_data():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return (x_train, y_train), (x_test, y_test)

# Define model
def build_model():
    model = keras.Sequential([
        layers.Flatten(input_shape=(28, 28)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(10)
    ])
    return model

# Train and evaluate with different optimizers
def train_and_evaluate(optimizer):
    model = build_model()
    model.compile(optimizer=optimizer, loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
    (x_train, y_train), (x_test, y_test) = get_data()
    model.fit(x_train, y_train, epochs=5, batch_size=64, verbose=1)
    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Accuracy with {optimizer}: {accuracy:.2%}")

optimizers = ['Adagrad', 'RMSprop', 'Adam']
for opt in optimizers:
    train_and_evaluate(opt)

    
    
    
    """
    
def cnn1():
    """
    import torch 
import torch.nn as nn 
import torch.optim as optim 
import torchvision 
import torchvision.transforms as transforms 
from torch.utils.data import DataLoader 
import matplotlib.pyplot as plt 
import numpy as np 
 
# Load MNIST dataset 
def get_data(): 
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), 
(0.5,))]) 
    trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, 
transform=transform) 
    testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, 
transform=transform) 
    trainloader = DataLoader(trainset, batch_size=64, shuffle=True) 
    testloader = DataLoader(testset, batch_size=1000, shuffle=False) 
    return trainloader, testloader 
 
# Define CNN Architectures 
class LeNet(nn.Module): 
    def __init__(self): 
        super(LeNet, self).__init__() 
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5) 
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5) 
        self.fc1 = nn.Linear(16*4*4, 120) 
        self.fc2 = nn.Linear(120, 84) 
        self.fc3 = nn.Linear(84, 10) 
        self.relu = nn.ReLU() 
        self.pool = nn.MaxPool2d(2, 2) 
 
    def forward(self, x): 
        x = self.pool(self.relu(self.conv1(x))) 
        x = self.pool(self.relu(self.conv2(x))) 
        x = x.view(-1, 16*4*4) 
        x = self.relu(self.fc1(x)) 
        x = self.relu(self.fc2(x)) 
        x = self.fc3(x) 
        return x 
 
class AlexNet(nn.Module): 
    def __init__(self): 
        super(AlexNet, self).__init__() 
        self.features = nn.Sequential( 
            nn.Conv2d(1, 64, kernel_size=3, stride=1, padding=1), 
            nn.ReLU(), 
            nn.MaxPool2d(kernel_size=2, stride=2), 
            nn.Conv2d(64, 192, kernel_size=3, padding=1), 
            nn.ReLU(), 
            nn.MaxPool2d(kernel_size=2, stride=2), 
            nn.Conv2d(192, 384, kernel_size=3, padding=1), 
            nn.ReLU(), 
            nn.Conv2d(384, 256, kernel_size=3, padding=1), 
            nn.ReLU(), 
            nn.Conv2d(256, 256, kernel_size=3, padding=1), 
            nn.ReLU(), 
            nn.MaxPool2d(kernel_size=2, stride=2), 
        ) 
        self.classifier = nn.Sequential( 
            nn.Linear(256 * 3 * 3, 4096), 
            nn.ReLU(), 
            nn.Linear(4096, 4096), 
            nn.ReLU(), 
            nn.Linear(4096, 10), 
        ) 
 
    def forward(self, x): 
        x = self.features(x) 
        x = x.view(x.size(0), -1) 
        x = self.classifier(x) 
        return x 
 
# Train and evaluate model 
def train_model(model, trainloader, testloader, optimizer_type): 
    model = model() 
    criterion = nn.CrossEntropyLoss() 
    optimizer = optimizer_type(model.parameters(), lr=0.01) 
 
    for epoch in range(5): 
        model.train() 
        for images, labels in trainloader: 
            optimizer.zero_grad() 
            outputs = model(images) 
            loss = criterion(outputs, labels) 
            loss.backward() 
            optimizer.step() 
        print(f"Epoch {epoch+1} completed") 
 
    model.eval() 
    correct = 0 
    total = 0 
    with torch.no_grad(): 
        for images, labels in testloader: 
            outputs = model(images) 
            _, predicted = torch.max(outputs, 1) 
            total += labels.size(0) 
            correct += (predicted == labels).sum().item() 
 
    accuracy = 100 * correct / total 
    print(f"Accuracy with {model.__class__.__name__}: {accuracy:.2f}%") 
    return model 
 
# Visualization Function 
def visualize_filters(model): 
    with torch.no_grad(): 
        for name, param in model.named_parameters(): 
            if 'conv' in name and param.requires_grad: 
                filters = param.cpu().numpy() 
                fig, axes = plt.subplots(1, min(6, filters.shape[0])) 
                for i, ax in enumerate(axes): 
                    ax.imshow(filters[i, 0], cmap='gray') 
                    ax.axis('off') 
                plt.show() 
                break 
 
# Load data 
trainloader, testloader = get_data() 
 
# Train models 
models = [LeNet, AlexNet] 
optimizers = [optim.Adam] 
for model in models: 
    for opt in optimizers: 
        trained_model = train_model(model, trainloader, testloader, opt) 
        visualize_filters(trained_model)
    
    
    
    
    """
    
def cnn2():
    """
    import tensorflow as tf 
from tensorflow.keras.applications import VGG16 
from tensorflow.keras.models import Model 
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Input 
from tensorflow.keras.optimizers import Adam 
from tensorflow.keras.utils import to_categorical 
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.metrics import confusion_matrix, classification_report 
import seaborn as sns 
import cv2 
# Load MNIST Dataset 
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data() 
# Preprocess Data 
x_train = np.expand_dims(x_train, axis=-1) 
x_test = np.expand_dims(x_test, axis=-1) 
# Convert grayscale to 3 channels for pretrained models 
x_train = np.repeat(x_train, 3, axis=-1) 
x_test = np.repeat(x_test, 3, axis=-1) 
# Resize images to 32x32 for VGG-16 compatibility 
x_train_resized = np.array([cv2.resize(img, (32, 32)) for img in x_train]) 
x_test_resized = np.array([cv2.resize(img, (32, 32)) for img in x_test]) 
# Normalize data 
x_train_resized, x_test_resized = x_train_resized / 255.0, x_test_resized / 255.0 
x_train, x_test = x_train / 255.0, x_test / 255.0 
# Convert labels to categorical 
y_train_cat = to_categorical(y_train, 10) 
y_test_cat = to_categorical(y_test, 10) 
# Define VGG-16 Model 
base_model_vgg = VGG16(weights='imagenet', include_top=False, input_shape=(32, 32, 3)) 
for layer in base_model_vgg.layers: 
    layer.trainable = False 
x = Flatten()(base_model_vgg.output) 
x = Dense(256, activation='relu')(x) 
x = Dense(10, activation='softmax')(x) 
vgg_model = Model(inputs=base_model_vgg.input, outputs=x) 
vgg_model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy']) 
# Train VGG-16 
vgg_model.fit(x_train_resized, y_train_cat, epochs=5, batch_size=64, 
validation_data=(x_test_resized, y_test_cat)) 
 
# Define PlacesNet-like CNN 
input_layer = Input(shape=(28, 28, 3)) 
x = Conv2D(64, (3,3), activation='relu', padding='same')(input_layer) 
x = MaxPooling2D((2,2))(x) 
x = Conv2D(128, (3,3), activation='relu', padding='same')(x) 
x = MaxPooling2D((2,2))(x) 
x = Flatten()(x) 
x = Dense(256, activation='relu')(x) 
x = Dense(10, activation='softmax')(x) 
 
placesnet_model = Model(inputs=input_layer, outputs=x) 
placesnet_model.compile(optimizer=Adam(), loss='categorical_crossentropy', 
metrics=['accuracy']) 
 
# Train PlacesNet 
placesnet_model.fit(x_train, y_train_cat, epochs=5, batch_size=64, validation_data=(x_test, 
y_test_cat)) 
 
# Evaluate and Visualize Results 
def plot_confusion_matrix(model, x_test, y_test, title): 
    y_pred = np.argmax(model.predict(x_test), axis=1) 
    cm = confusion_matrix(y_test, y_pred) 
    plt.figure(figsize=(8, 6)) 
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues') 
    plt.xlabel('Predicted') 
    plt.ylabel('True') 
    plt.title(f'Confusion Matrix: {title}') 
    plt.show() 
 
# Confusion Matrices 
plot_confusion_matrix(vgg_model, x_test_resized, y_test, "VGG-16") 
plot_confusion_matrix(placesnet_model, x_test, y_test, "PlacesNet") 
 
# Display Feature Maps 
def visualize_feature_maps(model, x_sample): 
    layer_outputs = [layer.output for layer in model.layers if isinstance(layer, Conv2D)] 
    activation_model = Model(inputs=model.input, outputs=layer_outputs) 
    activations = activation_model.predict(np.expand_dims(x_sample, axis=0)) 
    for i, activation in enumerate(activations[:3]):  # Show first 3 layers 
        plt.figure(figsize=(10, 5)) 
        for j in range(min(activation.shape[-1], 6)):  # Show first 6 filters 
            plt.subplot(1, 6, j+1) 
            plt.imshow(activation[0, :, :, j], cmap='viridis') 
            plt.axis('off') 
        plt.show() 
 
# Show feature maps of first test image 
visualize_feature_maps(vgg_model, x_test_resized[0]) 
visualize_feature_maps(placesnet_model, x_test[0]) 
    
    
    
    
    """

def rnn():
    """
    import numpy as np
from numpy.random import randn, seed


def sigmoid(x): return 1 / (1 + np.exp(-x))


def rnn_cell(xt, ht, Wx, Wh, b): return np.tanh(Wx @ xt + Wh @ ht + b)


def rnn_forward(x_seq, h0, Wx, Wh, b):
    h, hs = h0, []
    for xt in x_seq:
        h = rnn_cell(xt, h, Wx, Wh, b)
        hs.append(h)
    return np.stack(hs)


def lstm_cell(xt, ht, ct, Wf, Wi, Wc, Wo, bf, bi, bc, bo):
    xh = np.vstack((ht, xt))
    ft = sigmoid(Wf @ xh + bf)
    it = sigmoid(Wi @ xh + bi)
    c̃t = np.tanh(Wc @ xh + bc)
    ct_next = ft * ct + it * c̃t
    ot = sigmoid(Wo @ xh + bo)
    ht_next = ot * np.tanh(ct_next)
    return ht_next, ct_next


# -------- Sample Test --------
seed(0)
i_size, h_size, seq_len = 2, 2, 2
x_seq = [randn(i_size, 1) for _ in range(seq_len)]
h0 = c0 = np.zeros((h_size, 1))

# RNN weights
Wx, Wh, b = [randn(*s) for s in [(h_size, i_size), (h_size, h_size), (h_size, 1)]]

# LSTM weights and biases
Wf, Wi, Wc, Wo, bf, bi, bc, bo = [randn(h_size, h_size + i_size) for _ in range(4)] + [randn(h_size, 1) for _ in
                                                                                       range(4)]

print("=== RNN Output ===")
print(np.round(rnn_forward(x_seq, h0, Wx, Wh, b).squeeze(), 3))

print("=== LSTM Output (1st step) ===")
ht, ct = lstm_cell(x_seq[0], h0, c0, Wf, Wi, Wc, Wo, bf, bi, bc, bo)
print("h:", np.round(ht.squeeze(), 3))
print("c:", np.round(ct.squeeze(), 3))

    
    
    """