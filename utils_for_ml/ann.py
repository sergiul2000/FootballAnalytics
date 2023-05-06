import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# load the data
data = pd.read_csv("utils_for_ml\\unified_players.csv")

# separate the target variable from the input features
X = data.drop(
    columns={
        "rating",
        "rating_mls_formula",
        "team",
        "league",
        "position",
        "name",
        "mapped_position",
        "player_number",
        "year_start",
        "year_end",
        # "number"
    },
    axis=1,
)
y = data["rating"]

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# standardize the input features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# define the model
model = tf.keras.Sequential(
    [
        tf.keras.layers.Input(shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1),
    ]
)


# compile the model
model.compile(optimizer="adam", loss="mse")


# model.compile(optimizer="adam", loss="binary_crossentropy")


# train the model
history = model.fit(X_train, y_train, epochs=100, batch_size=32)


# evaluate the model on test data
train_loss = model.evaluate(X_train, y_train)


# predictions = model.predict(X_train)

# accuracy.update_state(y_train, predictions)


# accuracy.reset_states()

print(f"Train loss: {train_loss}")
# print(f"Train accuracy: {acc}")

# print(history)

# predictions = model.predict(x_batch)
# accuracy.update_state(y_batch, predictions)

# accuracy.reset_states()


# Predicting the Test set results
y_pred = model.predict(X_test)
y_pred = y_pred > 0.5

print("*" * 20)
score = model.evaluate(X_test, y_test, batch_size=32)
print("Test score:", score)
