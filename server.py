import socket
import threading
import datetime
import time

HOST = '127.0.0.1'  
PORT = 65432        
TEMPO_DE_SINCRONIZACAO_SEGUNDOS = 20

clientes_conectados = {}
lock = threading.Lock() 

def get_current_time_nanoseconds():
    return time.time_ns()

def format_time(nanoseconds):
    return datetime.datetime.fromtimestamp(nanoseconds / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')

def handle_client(conn, addr):
    """
    Função para lidar com cada cliente em uma thread separada.
    Por agora, apenas mantém a conexão viva. A lógica de sincronização
    é centralizada na função `sincronizar_relogios`.
    """
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    with lock:
        clientes_conectados[conn] = addr
    
    try:
        while True:
            time.sleep(1)
    except (ConnectionResetError, BrokenPipeError):
        print(f"[CONEXÃO PERDIDA] {addr} desconectou.")
    finally:
        with lock:
            if conn in clientes_conectados:
                del clientes_conectados[conn]
        conn.close()


def sincronizar_relogios():
    while True:
        time.sleep(TEMPO_DE_SINCRONIZACAO_SEGUNDOS)
        
        print("\n" + "="*50)
        print(f"[{datetime.datetime.now()}] >>> INICIANDO NOVO CICLO DE SINCRONIZAÇÃO <<<")
        print("="*50)

        with lock:
            if not clientes_conectados:
                print("[AVISO] Nenhum cliente conectado para sincronizar.")
                continue

            diferencas_de_tempo = []

            tempo_servidor_ns = get_current_time_nanoseconds()
            print(f"[SERVIDOR] Meu tempo de referência: {format_time(tempo_servidor_ns)}")
            diferencas_de_tempo.append(0)

            clientes_a_remover = []
            for conn, addr in clientes_conectados.items():
                try:
                    conn.sendall(str(tempo_servidor_ns).encode())
                    
                    diferenca_str = conn.recv(1024).decode()
                    if diferenca_str:
                        diferenca_ns = int(diferenca_str)
                        diferencas_de_tempo.append(diferenca_ns)
                        print(f"[CLIENTE {addr}] Respondeu com diferença de {diferenca_ns / 1e6:.2f} ms")
                    else:
                        raise ConnectionResetError
                except (socket.error, ValueError) as e:
                    print(f"[ERRO] Não foi possível comunicar com {addr}. Removendo. Erro: {e}")
                    clientes_a_remover.append(conn)

            for conn in clientes_a_remover:
                if conn in clientes_conectados:
                    del clientes_conectados[conn]
                    conn.close()
            
            if not diferencas_de_tempo:
                continue

            media_das_diferencas_ns = sum(diferencas_de_tempo) / len(diferencas_de_tempo)
            print(f"\n[CÁLCULO] Média das diferenças: {media_das_diferencas_ns / 1e6:.2f} ms")

            idx_diferenca = 1 # Começa em 1 porque o 0 é o servidor
            for conn, addr in list(clientes_conectados.items()):
                try:
                    diferenca_do_cliente_ns = diferencas_de_tempo[idx_diferenca]
                    ajuste_ns = int(media_das_diferencas_ns - diferenca_do_cliente_ns)
                    
                    print(f"[AJUSTE] Enviando para {addr} o ajuste de {ajuste_ns / 1e6:.2f} ms")
                    conn.sendall(str(ajuste_ns).encode())
                    idx_diferenca += 1
                except (socket.error, IndexError) as e:
                    print(f"[ERRO] Falha ao enviar ajuste para {addr}. Erro: {e}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVIDOR] Servidor iniciado em {HOST}:{PORT}. Aguardando conexões...")

        sync_thread = threading.Thread(target=sincronizar_relogios, daemon=True)
        sync_thread.start()

        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()