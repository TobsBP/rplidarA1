'''
Anotações de Testes
1) A referencia de ângulo do Lidar é constante, significa que se eu rodar ele duas vezes seguidas
as posições dos objetos corresponderão à mesma faixa de ângulo
2) O motor do Lidar aponta para a direção/sentido de 180 graus. E isso é sempre constante
3) O angulo aumenta no sentido horário
'''
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar

def initialize_lidar(port='/dev/ttyUSB0'):
    """Inicializa o Lidar."""
    lidar = RPLidar(port)
    return lidar

def check_lidar_health(lidar):
    """Verifica e imprime a saúde do Lidar."""
    health = lidar.get_health()
    if health[0] == 'Good':
        print("Lidar está em bom estado.")
    else:
        print(f"Problema com o Lidar: {health}")
    return health

def collect_scan_data(lidar, num_scans=10):
    """Coleta dados de varredura do Lidar."""
    scan_data = []
    for i, scan in enumerate(lidar.iter_scans()):
        if i >= num_scans:
            break
        scan_data = scan
    return scan_data

def extract_angle_distance(scan_data):
    """Extrai ângulos e distâncias dos dados de varredura."""
    angles = [measurement[1] for measurement in scan_data]
    distances = [measurement[2] for measurement in scan_data]
    return angles, distances

def plot_polar_coordinates(angles, distances):
    """Plota os dados em coordenadas polares."""
    angles_radians = np.deg2rad(angles)
    plt.figure()
    ax = plt.subplot(111, polar=True)
    ax.plot(angles_radians, distances)
    ax.set_title('Coordenadas polares')
    ax.grid(True)
    plt.show()

def main():
    """Função principal"""
    lidar = initialize_lidar()
    check_lidar_health(lidar) 
    scan_data = collect_scan_data(lidar)
    angles, distances = extract_angle_distance(scan_data)
    
    for angle, distance in zip(angles, distances):
        print(f'Angulo: {angle} Distância: {distance}')  # Distância em mm
    
    plot_polar_coordinates(angles, distances)
    
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

if __name__ == '__main__':
    main()