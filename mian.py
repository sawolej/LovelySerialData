import serial
import time
import numpy as np
import matplotlib.pyplot as plt

def display_as_image(data):
    np_data = np.array(data)

    plt.imshow(np_data, cmap='gray', interpolation='nearest')
    plt.colorbar() 
    plt.show()

def process_data(data, rows, pixels):
    try:
        data_array = np.array(data, dtype=float).reshape(rows, -1)

        cluster_size = data_array.shape[1] // pixels

        processed_data = []
        for row in data_array:
            averaged_clusters = [np.mean(row[i:i+cluster_size]) for i in range(0, len(row), cluster_size)]
            processed_data.append(averaged_clusters)

        return processed_data
    except Exception as e:
        print(f"Errno: {e}")
        return []

rows = 5  
pixels = 10  

s = serial.Serial('COM5', 9600, timeout=1)

m_values = []  
p_values = []  

try:
    while True:
        s.readline().decode("utf-8")  
        data_line = s.readline().decode("utf-8").strip()

        if data_line:
            m, p = data_line.split(';')
            m_values.append(m)
            p_values.append(p)

        time.sleep(1)
except KeyboardInterrupt:
    processed_m = process_data(m_values, rows, pixels)
    processed_p = process_data(p_values, rows, pixels)

    print("magnitude:")
    for row in processed_m:
        print(row)

    print("phase:")
    for row in processed_p:
        print(row)

    display_as_image(processed_m)
    display_as_image(processed_p)
