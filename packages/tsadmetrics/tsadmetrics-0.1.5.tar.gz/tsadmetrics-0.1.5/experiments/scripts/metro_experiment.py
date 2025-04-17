import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tsadmetrics as tm
import time
from sklearn.metrics import f1_score

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


df_analog  = pd.read_csv('../preprocessed_data/MetroPT3_analogic.csv')
df_analog = pd.DataFrame(df_analog).set_index('timestamp')

# Separar las características (X) y la variable objetivo (y)
X = df_analog.drop(columns='anomaly')  # Características
y = df_analog['anomaly']  # Variable objetivo

# Normalizar las características entre [0, 1]
scaler = MinMaxScaler(feature_range=(0, 1))
X_normalized = scaler.fit_transform(X)

# Convertir el resultado normalizado de nuevo a un DataFrame
X_normalized = pd.DataFrame(X_normalized, columns=X.columns, index=X.index)

# Dividir el conjunto de datos normalizado en entrenamiento y prueba
train_df_analog, test_df_analog = train_test_split(
    X_normalized.join(y),  # Unir las características normalizadas con la variable objetivo
    test_size=0.4,
    random_state=42
)

X_train_analog = train_df_analog.drop(columns='anomaly')
y_train_analog = train_df_analog['anomaly']
X_test_analog = test_df_analog.drop(columns='anomaly')
y_test_analog = test_df_analog['anomaly']


#Modelos basados en distancia
from pyod.models.lof import LOF
from pyod.models.cblof import CBLOF
from pyod.models.knn import KNN
from pyod.models.abod import ABOD

modelos_distancia = [
    LOF(n_neighbors=35, contamination=np.sum(y_train_analog)/len(y_train_analog), n_jobs=-1),
    #COF(contamination=np.sum(y_train_analog)/len(y_train_analog),method='memory'),
    CBLOF(contamination=np.sum(y_train_analog)/len(y_train_analog),n_jobs=-1),
    KNN(n_neighbors=35, contamination=np.sum(y_train_analog)/len(y_train_analog),n_jobs=-1),
    ABOD(contamination=np.sum(y_train_analog)/len(y_train_analog))
]

#Modelos basados en árboles de aislamiento
from pyod.models.iforest import IForest
modelos_arboles = [
    IForest(contamination=np.sum(y_train_analog)/len(y_train_analog),n_jobs=-1, random_state=42)
]

#Modelos basados en Reconstrucción
from pyod.models.ae1svm import AE1SVM
from pyod.models.alad import ALAD
from pyod.models.auto_encoder import AutoEncoder

modelos_reconstruccion = [
    AE1SVM(contamination=np.sum(y_train_analog)/len(y_train_analog)),
    ALAD(contamination=np.sum(y_train_analog)/len(y_train_analog)),
    AutoEncoder(contamination=np.sum(y_train_analog)/len(y_train_analog))
]



#ejecucion de los modelos

distancia_results = pd.DataFrame(columns=['nombre_modelo', 'f1_score', 'segment_wise_f_score', 'tiempo_entrenamiento'])
for modelo in modelos_distancia:

    nombre_modelo = modelo.__class__.__name__

    inicio = time.time()
    try:
        modelo.fit(X_train_analog)
        t = time.time() - inicio  
        y_pred = modelo.predict(X_test_analog)
        f1 = f1_score(y_test_analog, y_pred)
        sw_f1 = tm.segment_wise_f_score(y_test_analog, y_pred)
        print(f'Modelo: {nombre_modelo} - F1: {f1} - Segment-wise F1: {sw_f1} - Tiempo: {t}')
    except Exception as e:
            print(f'Error en el modelo {nombre_modelo}: {e}')
    # Añadir los resultados al DataFrame
    distancia_results.loc[len(distancia_results)] = [nombre_modelo, f1, sw_f1, t] 

distancia_results.to_csv('../results/distancia_results.csv')

arbol_results = pd.DataFrame(columns=['nombre_modelo', 'f1_score', 'segment_wise_f_score', 'tiempo_entrenamiento'])
for modelo in modelos_arboles:

    nombre_modelo = modelo.__class__.__name__

    inicio = time.time()
    try:
        modelo.fit(X_train_analog)
        t = time.time() - inicio  
        y_pred = modelo.predict(X_test_analog)
        f1 = f1_score(y_test_analog, y_pred)
        sw_f1 = tm.segment_wise_f_score(y_test_analog, y_pred)
        print(f'Modelo: {nombre_modelo} - F1: {f1} - Segment-wise F1: {sw_f1} - Tiempo: {t}')
    except Exception as e:
            print(f'Error en el modelo {nombre_modelo}: {e}')
    # Añadir los resultados al DataFrame
    arbol_results.loc[len(arbol_results)] = [nombre_modelo, f1, sw_f1, t]

arbol_results.to_csv('../results/arbol_results.csv')

reconstruccion_results = pd.DataFrame(columns=['nombre_modelo', 'f1_score', 'segment_wise_f_score', 'tiempo_entrenamiento'])
for modelo in modelos_reconstruccion:

    nombre_modelo = modelo.__class__.__name__

    inicio = time.time()
    try:
        modelo.fit(X_train_analog[y_train_analog == 0])
        t = time.time() - inicio  
        y_pred = modelo.predict(X_test_analog)
        f1 = f1_score(y_test_analog, y_pred)
        sw_f1 = tm.segment_wise_f_score(y_test_analog, y_pred)
        print(f'Modelo: {nombre_modelo} - F1: {f1} - Segment-wise F1: {sw_f1} - Tiempo: {t}')
    except Exception as e:
            print(f'Error en el modelo {nombre_modelo}: {e}')
    # Añadir los resultados al DataFrame
    reconstruccion_results.loc[len(reconstruccion_results)] = [nombre_modelo, f1, sw_f1, t]

reconstruccion_results.to_csv('../results/reconstruccion_results.csv')