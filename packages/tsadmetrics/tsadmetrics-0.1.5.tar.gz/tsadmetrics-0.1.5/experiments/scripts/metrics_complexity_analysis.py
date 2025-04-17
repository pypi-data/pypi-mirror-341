import pandas as pd
import numpy as np
import time
import os
from tsadmetrics import *

# Lista de modelos y métricas
binary_metrics = [
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
binary_metrics_params ={
    'delay_th_point_adjusted_f_score': {'k': 10},
    'point_adjusted_at_k_f_score': {'k': 0.7},
    'latency_sparsity_aw_f_score': {'ni': 2},
    'time_tolerant_f_score': {'t': 30},
    'range_based_f_score': {'p_alpha': 0, 'r_alpha':0}, #Valor por defecto
    'ts_aware_f_score': {'theta': 0.5, 'alpha':0.5, 'delta': 0, 'beta':1}, #Valor por defecto
    'enhanced_ts_aware_f_score': {'beta':1,'theta_p': 0.5, 'theta_r':0.1}, #Valor por defecto
    'total_detected_in_range': {'k': 30},
    'detection_accuracy_in_range': {'k': 30},
    'weighted_detection_difference':{'k': 3},
    'binary_pate': {'early': 20, 'delay': 20}

}

continuous_metrics = [
    ('precision_at_k', precision_at_k),
    ('auc_roc_pw', auc_roc_pw),
    ('auc_pr_pw', auc_pr_pw),
    ('auc_pr_pa', auc_pr_pa),
    ('auc_pr_sw', auc_pr_sw),
    ('vus_roc', vus_roc),
    ('vus_pr', vus_pr),
    ('real_pate', real_pate)]

continuous_metrics_params ={
    'vus_roc': {'window': 4},
    'vus_pr': {'window': 4},
    'real_pate': {'early': 3, 'delay': 3},

}
SIZE = 1000
# Cargar predicciones
y_true, y_pred = np.random.choice([0, 1], size=SIZE), np.random.choice([0, 1], size=SIZE)

Binary_mode = 1

if Binary_mode == 0:
    for metric_name, metric_func in binary_metrics:
        
            # Calcular métrica y tiempo de ejecución
            

            start_time = time.time()
            if metric_name in binary_metrics_params:
                params = binary_metrics_params[metric_name]
                metric_value = metric_func(y_true, y_pred, **params)
            else:
                metric_value = metric_func(y_true, y_pred)
            computation_time = time.time() - start_time
            

            
            print(f"Métrica: {metric_name} - Valor: {metric_value:.4f} - Tiempo: {computation_time:.4f}s")
                
else:                
    y_true = np.random.choice([0, 1], size=SIZE)
    y_pred = np.random.rand(SIZE)  # Predicciones continuas
        
            # Calcular métrica y tiempo de ejecución
            
    for metric_name, metric_func in continuous_metrics:

        start_time = time.time()
        if metric_name in continuous_metrics_params:
            params = continuous_metrics_params[metric_name]
            metric_value = metric_func(y_true, y_pred, **params)
        else:
            metric_value = metric_func(y_true, y_pred)
        computation_time = time.time() - start_time
        

        
        print(f"Métrica: {metric_name} - Valor: {metric_value:.4f} - Tiempo: {computation_time:.4f}s")
                
                
            
        
