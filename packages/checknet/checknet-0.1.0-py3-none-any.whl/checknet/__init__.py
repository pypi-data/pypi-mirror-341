import socket

def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Testa a conectividade com a internet via socket TCP.
    
    Args:
        host (str): Endereço IP para testar (padrão: 8.8.8.8)
        port (int): Porta TCP (padrão: 53)
        timeout (int): Tempo limite da conexão em segundos

    Returns:
        bool: True se a conexão for bem-sucedida, False caso contrário
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
