import socket
import sys
from threading import Thread
from queue import Queue

class Game:
    """Interface unique pour tous les jeux"""
    def __init__(self, game_name="", player_count=1):
        self.game_name = game_name
        self.player_count = player_count
        self._init_network()
        
    def _init_network(self, hostprocessing="127.0.0.1", hostconsole="127.0.0.1", hostmatriceled=None):
        """Initialise toutes les connexions réseaux"""
        # Connexion Processing (obligatoire)
        self._processing = socket.socket()
        self._processing.connect((hostprocessing, 15426))
        
        # Connexion Console (pour commandes)
        self._console = socket.socket()
        self._console.connect((hostconsole, 58591))
        
        # Connexion Matrice LED (facultative)
        self._matriceled = None
        if hostmatriceled is not None:
            try:
                self._matriceled = socket.socket()
                self._matriceled.connect((hostmatriceled, 8000))
                print(f"[{self.game_name}] Connexion à la matrice LED établie")
            except Exception as e:
                print(f"[{self.game_name}] Erreur connexion matrice LED: {e}")
        
        # Système de commandes
        self._cmd_queue = Queue()
        self._running = True
        Thread(target=self._listen_commands, daemon=True).start()

    def _listen_commands(self):
        """Écoute les commandes en arrière-plan"""
        while self._running:
            try:
                cmd = self._console.recv(1024).decode().strip()
                if cmd: 
                    self._cmd_queue.put(cmd)
                    if cmd == "KILL":
                        self._running = False
            except:
                break

    def send_frame(self, frame, target="processing"):
        """
        Envoie une frame au processing ou à la matrice LED
        target: "processing" (par défaut) ou "matriceled"
        """
        try:
            if target == "processing":
                self._processing.sendall(frame.encode())
            elif target == "matriceled" and self._matriceled is not None:
                self._matriceled.sendall(frame.encode())
        except Exception as e:
            print(f"[{self.game_name}] Erreur envoi frame ({target}): {e}")

    def commands(self):
        """Générateur de commandes (non bloquant)"""
        while self._running:
            if not self._cmd_queue.empty():
                yield self._cmd_queue.get()
            else:
                yield None

    def close(self):
        """Ferme toutes les connexions"""
        self._running = False
        self._processing.close()
        self._console.close()
        if self._matriceled is not None:
            self._matriceled.close()
        print(f"[{self.game_name}] Connexions fermées")