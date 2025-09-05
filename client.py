import socket
import time
import datetime
import random


HOST = '127.0.0.1'  
PORT = 65432        

# --- Simulação de Relógio Local ---
# Vamos simular um relógio dessincronizado adicionando um offset em nanossegundos.
# Um valor positivo adianta o relógio, um negativo atrasa.
# Ex: 10 segundos * 1e9 = 10,000,000,000 ns
OFFSET_INICIAL_NS = int(random.uniform(-10, 10) * 1e9) 

def get_logical_time_nanoseconds():
    """Retorna o tempo do sistema + o nosso offset para simular o relógio local."""
    return time.time_ns() + OFFSET_INICIAL_NS

def format_time(nanoseconds):
    """Formata nanossegundos para uma string legível de data e hora."""
    return datetime.datetime.fromtimestamp(nanoseconds / 1e9).strftime('%Y-%m-%d %H:%M:%S.%f')

def main():
    global OFFSET_INICIAL_NS
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print(f"[CONEXÃO] Conectado ao servidor em {HOST}:{PORT}")
            print(f"[RELÓGIO LOCAL] Offset inicial: {OFFSET_INICIAL_NS / 1e9:.2f} segundos.")
            print(f"[RELÓGIO LOCAL] Hora inicial: {format_time(get_logical_time_nanoseconds())}\n")
        except ConnectionRefusedError:
            print("[ERRO] Não foi possível conectar ao servidor.")
            return

        try:
            while True:
                tempo_servidor_str = s.recv(1024).decode()
                if not tempo_servidor_str:
                    break
                
                tempo_servidor_ns = int(tempo_servidor_str)
                tempo_cliente_ns = get_logical_time_nanoseconds()

                diferenca_ns = tempo_cliente_ns - tempo_servidor_ns
                s.sendall(str(diferenca_ns).encode())

                print(f"--- Ciclo de Sincronização ---")
                print(f"Recebi tempo de referência do servidor: {format_time(tempo_servidor_ns)}")
                print(f"Minha hora local no momento era:       {format_time(tempo_cliente_ns)}")
                print(f"Enviei a minha diferença de {diferenca_ns / 1e6:.2f} ms")

                ajuste_str = s.recv(1024).decode()
                if not ajuste_str:
                    break
                
                ajuste_ns = int(ajuste_str)
                
                OFFSET_INICIAL_NS += ajuste_ns
                
                print(f"Recebi instrução para ajustar meu relógio em {ajuste_ns / 1e6:.2f} ms")
                print(f"Minha nova hora sincronizada é: {format_time(get_logical_time_nanoseconds())}\n")

        except (ConnectionResetError, BrokenPipeError):
            print("[ERRO] Conexão com o servidor foi perdida.")
        finally:
            print("Encerrando cliente.")


if __name__ == "__main__":
    main()