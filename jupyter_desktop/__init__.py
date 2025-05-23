import os
import shlex
from shutil import which
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

def setup_desktop():
    # Detecta a resoluÃ§Ã£o da tela automaticamente ou usa o padrÃ£o
    width = os.getenv("SCREEN_WIDTH", "1100")
    height = os.getenv("SCREEN_HEIGHT", "520")
    resolution = f"{width}x{height}"

    # Cria um diretÃ³rio temporÃ¡rio para os sockets
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')

    # Verifica se o comando 'vncserver' estÃ¡ disponÃ­vel
    vncserver = which('vncserver')
    if vncserver:
        vnc_args = [vncserver]
        socket_args = []
    else:
        # Usa o TigerVNC embutido se nÃ£o encontrar o comando 'vncserver'
        vnc_args = [
            os.path.join(HERE, 'share/tigervnc/bin/vncserver'),
            '-rfbunixpath', sockets_path,
        ]
        socket_args = ['--unix-target', sockets_path]

    # Monta o comando do VNC com a resoluÃ§Ã£o definida
    vnc_command = ' '.join(shlex.quote(p) for p in (vnc_args + [
        '-verbose',
        '-xstartup', os.path.join(HERE, 'share/xstartup'),
        '-geometry', resolution,
        '-SecurityTypes', 'None',
        '-fg',
        ':1',
    ]))

    # Retorna a configuraÃ§Ã£o completa do servidor
    return {
        'command': [
            'websockify', '-v',
            '--web', os.path.join(HERE, 'share/web/noVNC-1.6.0'),
            '--heartbeat', '10',  # heartbeat ajustado para 10 segundos
            '5901',
        ] + socket_args + [
            '--',
            '/bin/sh', '-c',
            f'cd {os.getcwd()} && {vnc_command}'
        ],
        'port': 5901,
        'timeout': 300,  # timeout aumentado para 300 segundos
        'mappath': {'/': '/vnc.html'},
        'new_browser_window': True  # abre automaticamente em uma nova janela
    }

# Teste de execuÃ§Ã£o
if __name__ == "__main__":
    config = setup_desktop()
    print("ConfiguraÃ§Ã£o gerada com sucesso!")
    print(config)
    
