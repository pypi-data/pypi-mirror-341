import pandas as pd
import numpy as np
import time
import os
from tsadmetrics import *

def cargar_prediccion(modelo_nombre):
    """
    Carga las predicciones guardadas previamente.
    """
    nombre_archivo = f'../results/predictions/{modelo_nombre}_pred.csv'
    resultados = pd.read_csv(nombre_archivo)
    
    y_true = resultados['ground_truth'].values
    y_pred_binary = resultados['prediction_binary'].values
    y_pred_continuous = resultados['prediction_continuous'].values
    return y_true, y_pred_binary, y_pred_continuous

# Lista de modelos y métricas
nombre_modelos = ['CBLOF', 'IForest', 'KNN', 'LOF','AE1SVM','AutoEncoder','LSTM']
metrics = [
    ('point_wise_f_score', point_wise_f_score),
    ('point_adjusted_f_score', point_adjusted_f_score),
    ('delay_th_point_adjusted_f_score', delay_th_point_adjusted_f_score),
    ('point_adjusted_at_k_f_score', point_adjusted_at_k_f_score),
    ('latency_sparsity_aw_f_score', latency_sparsity_aw_f_score),
    ('segment_wise_f_score', segment_wise_f_score),
    ('composite_f_score', composite_f_score),
    ('time_tolerant_f_score', time_tolerant_f_score),
    ('range_based_f_score',range_based_f_score),
    ('ts_aware_f_score',ts_aware_f_score),
    ('enhanced_ts_aware_f_score', enhanced_ts_aware_f_score),
    ('affiliation_based_f_score', affiliation_based_f_score),
    ('nab_score', nab_score),
    ('temporal_distance', temporal_distance),
    ('average_detection_count', average_detection_count),
    ('absolute_detection_distance',absolute_detection_distance),
    ('total_detected_in_range',total_detected_in_range),
    ('detection_accuracy_in_range',detection_accuracy_in_range),
    ('weighted_detection_difference',weighted_detection_difference),
    ('binary_pate', binary_pate),
    ('mean_time_to_detect', mean_time_to_detect),
]

metrics_params = {
    'delay_th_point_adjusted_f_score': {'k': 10},
    'point_adjusted_at_k_f_score': {'k': 0.7},
    'latency_sparsity_aw_f_score': {'ni': 2},
    'time_tolerant_f_score': {'t': 30},
    'range_based_f_score': {'p_alpha': 0, 'r_alpha':0},
    'ts_aware_f_score': {'theta': 0.5, 'alpha':0.5, 'delta': 0, 'beta':1},
    'enhanced_ts_aware_f_score': {'beta':1,'theta_p': 0.5, 'theta_r':0.1},
    'total_detected_in_range': {'k': 30},
    'detection_accuracy_in_range': {'k': 30},
    'weighted_detection_difference':{'k': 30},
    'binary_pate': {'early': 20, 'delay': 20}
}

# Crear directorio si no existe
os.makedirs('../results/computed_metrics', exist_ok=True)

# Rutas de los archivos
results_path = '../results/computed_metrics/resultados.csv'
times_path = '../results/computed_metrics/tiempos.csv'

# Intentar cargar resultados existentes o crear nuevos DataFrames
try:
    all_results_df = pd.read_csv(results_path)
    all_times_df = pd.read_csv(times_path)
    print("Cargados resultados previos encontrados.")
except:
    all_results_df = pd.DataFrame(columns=['modelo'] + [m[0] for m in metrics])
    all_times_df = pd.DataFrame(columns=['modelo', 'metrica', 'tiempo'])
    print("No se encontraron resultados previos, comenzando desde cero.")

# Función para guardar el progreso
def guardar_progreso():
    all_results_df.to_csv(results_path, index=False)
    all_times_df.to_csv(times_path, index=False)
    print(f"\nProgreso guardado a las {time.strftime('%H:%M:%S')}")

# Tiempo de inicio y última vez que se guardó
start_time = time.time()
last_save_time = start_time

# Bucle principal de cálculo
for modelo in nombre_modelos:
    # Verificar si el modelo ya está completo en los resultados
    if modelo in all_results_df['modelo'].values:
        print(f"\nModelo {modelo} ya calculado, saltando...")
        continue
    
    print(f"\nComenzando cálculo para modelo: {modelo}")
    
    try:
        # Cargar predicciones
        y_true, y_pred, _ = cargar_prediccion(modelo)
        
        # Diccionario para almacenar resultados del modelo actual
        model_results = {'modelo': modelo}
        model_times = []
        
        for metric_name, metric_func in metrics:
            # Verificar si esta métrica ya está calculada para este modelo
            if not all_results_df.empty and modelo in all_results_df['modelo'].values:
                existing_row = all_results_df[all_results_df['modelo'] == modelo].iloc[0]
                if not pd.isna(existing_row[metric_name]):
                    print(f"Métrica {metric_name} ya calculada para {modelo}, saltando...")
                    continue
            
            print(f"Calculando métrica: {metric_name}, modelo: {modelo}...")
            
            try:
                # Calcular métrica y tiempo de ejecución
                start_metric_time = time.time()
                
                if metric_name in metrics_params:
                    params = metrics_params[metric_name]
                    metric_value = metric_func(y_true, y_pred, **params)
                else:
                    metric_value = metric_func(y_true, y_pred)
                
                computation_time = time.time() - start_metric_time
                
                # Actualizar resultados
                model_results[metric_name] = metric_value
                model_times.append({
                    'modelo': modelo,
                    'metrica': metric_name,
                    'tiempo': computation_time
                })
                
                print(f"Valor: {metric_value:.4f}, tiempo: {computation_time:.4f}s")
                
                # Guardar progreso cada hora
                current_time = time.time()
                if current_time - last_save_time > 3600:  # 3600 segundos = 1 hora
                    # Añadir resultados parciales
                    if modelo not in all_results_df['modelo'].values:
                        all_results_df = pd.concat([all_results_df, pd.DataFrame([model_results])], ignore_index=True)
                    else:
                        idx = all_results_df.index[all_results_df['modelo'] == modelo][0]
                        all_results_df.loc[idx, metric_name] = metric_value
                    
                    all_times_df = pd.concat([all_times_df, pd.DataFrame(model_times)], ignore_index=True)
                    model_times = []  # Resetear tiempos para no duplicar
                    
                    guardar_progreso()
                    last_save_time = current_time
                
            except Exception as e:
                print(f"Error calculando {metric_name} para {modelo}: {str(e)}")
                model_results[metric_name] = np.nan
                model_times.append({
                    'modelo': modelo,
                    'metrica': metric_name,
                    'tiempo': np.nan
                })
        
        # Añadir resultados completos del modelo a los DataFrames principales
        if modelo not in all_results_df['modelo'].values:
            all_results_df = pd.concat([all_results_df, pd.DataFrame([model_results])], ignore_index=True)
        else:
            # Actualizar fila existente
            idx = all_results_df.index[all_results_df['modelo'] == modelo][0]
            for metric_name in model_results:
                if metric_name != 'modelo':
                    all_results_df.loc[idx, metric_name] = model_results[metric_name]
        
        all_times_df = pd.concat([all_times_df, pd.DataFrame(model_times)], ignore_index=True)
        
        # Guardar después de completar cada modelo
        guardar_progreso()
        last_save_time = time.time()
    
    except Exception as e:
        print(f"Error procesando modelo {modelo}: {str(e)}")
        # Añadir filas con NaN para este modelo
        model_results = {'modelo': modelo}
        for m in metrics:
            model_results[m[0]] = np.nan
        all_results_df = pd.concat([all_results_df, pd.DataFrame([model_results])], ignore_index=True)
        guardar_progreso()

# Guardar resultados finales
guardar_progreso()
print("\nProceso completado. Resultados finales guardados.")