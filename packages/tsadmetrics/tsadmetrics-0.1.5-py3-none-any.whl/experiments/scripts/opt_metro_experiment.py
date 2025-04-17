import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tsadmetrics as tm
import time
from sklearn.metrics import f1_score, recall_score, precision_score
import optuna
from optuna.samplers import TPESampler
from functools import partial
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os
import json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import classification_report

def simplify_dataset(
    data: pd.DataFrame,
    window_size: int = 2,
    time_col: str = None,
    anomaly_col: str = 'anomaly',
    agg_func: str = 'mean'
) -> pd.DataFrame:
    """
    Reduce un dataset aplicando agregación en ventanas temporales.
    """
    simplified_data = data.rolling(window_size, step=window_size).mean()
    simplified_data = simplified_data.dropna()
    simplified_data[anomaly_col] = (simplified_data[anomaly_col] > 0.1).astype(int)
    return simplified_data.reset_index(drop=True)

# Configuración inicial para PyTorch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

def guardar_prediccion(modelo_nombre, y_true, y_pred_binario, y_pred_continuo=None, timestamps=None):
    """
    Guarda las predicciones ordenadas por timestamp.
    """
    os.makedirs('../results/predictions', exist_ok=True)
    
    resultados = pd.DataFrame({
        'timestamp': timestamps if timestamps is not None else np.arange(len(y_true)),
        'ground_truth': np.array(y_true).flatten(),
        'prediction_binary': np.array(y_pred_binario).flatten()
    })
    
    if y_pred_continuo is not None:
        resultados['prediction_continuous'] = np.array(y_pred_continuo).flatten()
    
    if 'timestamp' in resultados.columns:
        resultados = resultados.sort_values('timestamp')
    
    nombre_archivo = f'../results/predictions/{modelo_nombre}_pred.csv'
    resultados.to_csv(nombre_archivo, index=False)
    return nombre_archivo

# -------------------------------
# Cargar y preparar datos
df_analog = pd.read_csv('../preprocessed_data/MetroPT3_analogic.csv')
df_analog = pd.DataFrame(df_analog).set_index('timestamp')
df_analog = df_analog.sort_index()

# Reducción de tamaño
print('Tamaño inicial del dataset:', df_analog.shape)
print(f'Proporción de anomalías: {df_analog["anomaly"].mean():.2f}')
df_analog = simplify_dataset(df_analog, window_size=10, time_col='timestamp')
print('Tamaño del dataset:', df_analog.shape)
print(f'Proporción de anomalías: {df_analog["anomaly"].mean():.2f}')

# Separar y normalizar datos
X = df_analog.drop(columns='anomaly')
y = df_analog['anomaly']
scaler = MinMaxScaler(feature_range=(0, 1))
X_normalized = scaler.fit_transform(X)
X_normalized = pd.DataFrame(X_normalized, columns=X.columns, index=X.index)

# -------------------------------
# DIVISIÓN DE DATOS
# 1. Para modelos no-LSTM (shuffle=True)
train_df_shuf, test_df_shuf = train_test_split(
    X_normalized.join(y),
    test_size=0.4,
    random_state=42,
    shuffle=True
)

# 2. Para LSTM (shuffle=False para mantener orden temporal)
train_df_noshuf, test_df_noshuf = train_test_split(
    X_normalized.join(y),
    test_size=0.4,
    random_state=42,
    shuffle=False
)

# Preparar datos para modelos no-LSTM
X_train_shuf = train_df_shuf.drop(columns='anomaly')
y_train_shuf = train_df_shuf['anomaly']
X_test_shuf = test_df_shuf.drop(columns='anomaly')
y_test_shuf = test_df_shuf['anomaly']

# Preparar datos para LSTM
X_train_noshuf = train_df_noshuf.drop(columns='anomaly')
y_train_noshuf = train_df_noshuf['anomaly']
X_test_noshuf = test_df_noshuf.drop(columns='anomaly')
y_test_noshuf = test_df_noshuf['anomaly']

contamination = np.sum(y_train_shuf)/len(y_train_shuf)

# -------------------------------
# Definición del modelo LSTM
class AnomalyLSTM(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super(AnomalyLSTM, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_time_step = lstm_out[:, -1, :]
        output = self.fc(last_time_step)
        return self.sigmoid(output)

def train_lstm(X_train, y_train, X_test, y_test, timestamps_test, sequence_length=10, epochs=20, batch_size=16):
    # Preparar datos secuenciales
    def create_sequences(data, targets, seq_length):
        xs, ys = [], []
        for i in range(len(data)-seq_length):
            xs.append(data[i:(i+seq_length)])
            ys.append(targets[i+seq_length])
        return np.array(xs), np.array(ys)
    
    X_train_seq, y_train_seq = create_sequences(X_train.values, y_train.values, sequence_length)
    X_test_seq, y_test_seq = create_sequences(X_test.values, y_test.values, sequence_length)
    
    # Convertir a tensores PyTorch
    train_data = TensorDataset(
        torch.FloatTensor(X_train_seq), 
        torch.FloatTensor(y_train_seq).unsqueeze(1)
    )
    test_data = TensorDataset(
        torch.FloatTensor(X_test_seq), 
        torch.FloatTensor(y_test_seq).unsqueeze(1)
    )
    
    # IMPORTANTE: shuffle=False para DataLoader
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)
    
    # Inicializar modelo
    model = AnomalyLSTM(input_size=X_train.shape[1]).to(device)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # Entrenamiento
    train_start = time.time()
    for epoch in range(epochs):
        model.train()
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
    
    # Evaluación
    model.eval()
    test_preds, test_true, test_scores = [], [], []
    with torch.no_grad():
        for batch_x, batch_y in test_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            outputs = model(batch_x)
            predicted = (outputs > 0.5).float()
            test_preds.extend(predicted.cpu().numpy())
            test_scores.extend(outputs.cpu().numpy())
            test_true.extend(batch_y.cpu().numpy())
    
    train_time = time.time() - train_start
    
    # Ajustar predicciones al tamaño original y ordenar por timestamp
    full_preds = np.concatenate([np.zeros(sequence_length), np.array(test_preds).flatten()])
    full_scores = np.concatenate([np.zeros(sequence_length), np.array(test_scores).flatten()])
    full_preds = full_preds[:len(y_test)]
    full_scores = full_scores[:len(y_test)]
    
    # Crear DataFrame con timestamps para ordenar
    pred_df = pd.DataFrame({
        'timestamp': timestamps_test[-len(full_preds):],
        'y_true': y_test[-len(full_preds):],
        'y_pred': full_preds,
        'y_scores': full_scores
    }).sort_values('timestamp')
    
    # Calcular métricas ordenadas
    f1 = f1_score(pred_df['y_true'], pred_df['y_pred'])
    sw_f1 = tm.segment_wise_f_score(pred_df['y_true'], pred_df['y_pred'])
    
    guardar_prediccion("LSTM", pred_df['y_true'], pred_df['y_pred'], pred_df['y_scores'], pred_df['timestamp'])
    
    return model, f1, sw_f1, train_time, pred_df['y_pred']

# [Resto de las funciones (objective, optimize_model, evaluate_models) permanecen iguales...]

# -------------------------------
# Modelos
from pyod.models.lof import LOF
from pyod.models.cblof import CBLOF
from pyod.models.knn import KNN
from pyod.models.iforest import IForest
from pyod.models.ae1svm import AE1SVM
from pyod.models.auto_encoder import AutoEncoder

modelos_distancia = [LOF, CBLOF, KNN]
modelos_arboles = [IForest]
modelos_machine_learning = []
modelos_reconstruccion = [AE1SVM, AutoEncoder]

# -------------------------------
# Función evaluate_models modificada
# -------------------------------
# Función evaluate_models modificada para ordenar todas las predicciones
def evaluate_models(model_classes, best_params_dict, results_filename, include_lstm=False):
    results_df = pd.DataFrame(columns=[
        'nombre_modelo', 'f1_score', 'segment_wise_f_score', 'tiempo_entrenamiento', 'best_params'
    ])
    
    # Evaluar modelos no-LSTM (usando datos con shuffle)
    for model_class in model_classes:
        nombre_modelo = model_class.__name__
        params = best_params_dict.get(nombre_modelo, {})
        params['contamination'] = contamination
        
        if model_class.__name__ in ['LOF', 'CBLOF', 'KNN', 'IForest']:
            params['n_jobs'] = -1
        
        inicio = time.time()
        try:
            model = model_class(**params)
            
            if nombre_modelo in ['AutoEncoder', 'AE1SVM']:
                model.fit(X_train_shuf[y_train_shuf == 0])
            else:
                model.fit(X_train_shuf)
                
            t = time.time() - inicio
            y_pred = model.predict(X_test_shuf)
            y_scores = model.decision_function(X_test_shuf) if hasattr(model, 'decision_function') else None
            
            # Crear DataFrame temporal con timestamps para ordenar
            pred_df = pd.DataFrame({
                'timestamp': X_test_shuf.index,
                'y_true': y_test_shuf,
                'y_pred': y_pred,
                'y_scores': y_scores if y_scores is not None else np.nan
            }).sort_values('timestamp')
            
            # Calcular métricas sobre datos ordenados
            f1 = f1_score(pred_df['y_true'], pred_df['y_pred'])
            sw_f1 = tm.segment_wise_f_score(pred_df['y_true'], pred_df['y_pred'])
            
            # Guardar predicciones ordenadas
            guardar_prediccion(
                nombre_modelo, 
                pred_df['y_true'], 
                pred_df['y_pred'], 
                pred_df['y_scores'] if 'y_scores' in pred_df.columns else None,
                pred_df['timestamp']
            )
            
            print(f'Modelo: {nombre_modelo} - F1: {f1:.4f} - Segment-wise F1: {sw_f1:.4f} - Tiempo: {t:.2f}s')
            
            results_df.loc[len(results_df)] = [
                nombre_modelo, f1, sw_f1, t, json.dumps(params, ensure_ascii=False)
            ]
        except Exception as e:
            print(f'Error en el modelo {nombre_modelo}: {e}')
    
    # Evaluar LSTM (usando datos sin shuffle)
    if include_lstm:
        inicio_lstm = time.time()
        print("\nEntrenando modelo LSTM (sin shuffle)...")
        
        lstm_model, lstm_f1, lstm_sw_f1, lstm_time, lstm_preds = train_lstm(
            X_train_noshuf, y_train_noshuf, 
            X_test_noshuf, y_test_noshuf,
            timestamps_test=X_test_noshuf.index
        )
        
        print(f'Modelo: LSTM - F1: {lstm_f1:.4f} - Segment-wise F1: {lstm_sw_f1:.4f} - Tiempo: {lstm_time:.2f}s')
        
        results_df.loc[len(results_df)] = [
            "LSTM", lstm_f1, lstm_sw_f1, lstm_time,
            json.dumps({
                "sequence_length": 10,
                "epochs": 20,
                "batch_size": 16,
                "hidden_size": 64,
                "num_layers": 2,
                "dropout": 0.2
            }, ensure_ascii=False)
        ]
    
    # Guardar resultados
    os.makedirs('../results', exist_ok=True)
    results_df.to_csv(f'../results/{results_filename}', index=False)
    print(f'Resultados guardados en {results_filename}')
    return results_df

# -------------------------------
# Parámetros y ejecución
best_params = {
    'LOF': {"n_neighbors": 62, "metric":"minkowski", "contamination":contamination, "n_jobs":-1},
    'CBLOF': {"n_clusters": 8, "alpha": 0.87571, "beta": 6, "contamination":contamination, "n_jobs":-1},
    'KNN': {"n_neighbors": 5, "method":"mean", "contamination":contamination, "n_jobs":-1},
    'IForest': {'n_jobs':-1, "contamination":contamination},
    'AutoEncoder': {},
    'AE1SVM': {}
}

print("\nEvaluando modelos basados en distancia...")
distancia_results = evaluate_models(modelos_distancia, best_params, 'distancia_results.csv')

print("\nEvaluando modelos basados en árboles...")
arbol_results = evaluate_models(modelos_arboles, best_params, 'arbol_results.csv')

print("\nEvaluando modelos de reconstrucción...")
reconstruccion_results = evaluate_models(modelos_reconstruccion, best_params, 'reconstruccion_results.csv')

print("\nEvaluando LSTM...")
ml_results = evaluate_models(modelos_machine_learning, best_params, 'ml_results.csv', include_lstm=True)