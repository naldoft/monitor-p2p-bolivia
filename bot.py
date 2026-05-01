import requests
import json
import csv
from datetime import datetime
import pytz
import os

def obtener_precios():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fiat": "BOB", "page": 1, "rows": 1, "asset": "USDT", "publisherType": None, "payTypes": []
    }

    # Consulta Compra
    payload["tradeType"] = "BUY"
    res_c = requests.post(url, json=payload, headers=headers).json()
    precio_c = res_c['data'][0]['adv']['price']

    # Consulta Venta
    payload["tradeType"] = "SELL"
    res_v = requests.post(url, json=payload, headers=headers).json()
    precio_v = res_v['data'][0]['adv']['price']

    return precio_c, precio_v

def actualizar_csv():
    p_compra, p_venta = obtener_precios()
    
    # Hora de Bolivia (GMT-4)
    tz = pytz.timezone('America/La_Paz')
    fecha = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")
    
    # Formateo idéntico a tu imagen: "15,24"
    def fmt(n): return str(n).replace(".", ",")
    
    nueva_fila = [fecha, fmt(6.86), fmt(6.96), fmt(p_compra), fmt(p_venta)]
    
    with open('data.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(nueva_fila)

if __name__ == "__main__":
    actualizar_csv()
