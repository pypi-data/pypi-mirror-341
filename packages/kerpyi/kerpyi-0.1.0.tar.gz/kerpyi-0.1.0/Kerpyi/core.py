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