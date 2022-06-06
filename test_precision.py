from keras.models import load_model
import pickle
import pandas as pd


with open('data_to_be_used_final_2022', 'rb') as file:
    my_unpickler = pickle.Unpickler(file)
    data_test_2015 = my_unpickler.load()


model_year = 2021
model = load_model('prediction_model.h5')
print(data_test_2015[0][0])


columns = []
for i in range(41):
    columns += ['x_%i' % (i+1)]
print(columns)
test_x_2013 = pd.DataFrame(data_test_2015[0], columns=columns+['p_1', 'p_2'])
test_y_2013 = pd.DataFrame(data_test_2015[1], columns=['y_1', 'y_2'])

print(test_x_2013.head())
print(test_y_2013.head())

total_test_2013 = pd.concat([test_x_2013, test_y_2013], axis=1)
total_test_2013 = total_test_2013.dropna()
total_test_2013 = total_test_2013.sample(frac=1).reset_index(drop=True)

test_x_2013 = total_test_2013.ix[:, columns]
test_y_2013 = total_test_2013.ix[:, ['y_1', 'y_2']]

print(test_y_2013)

nb = 0

for i in range(2890):
    pred = model.predict(test_x_2013.values[i].reshape(1,41))
    truth = test_y_2013.values[i]

    if pred[0][0] > 0.5 and truth[0] > 0.5:
        nb += 1
    elif pred[0][0] < 0.5 and truth[0] < 0.5:
        nb += 1
    else:
        print(pred, truth)

print(nb)
print(nb/2890)
