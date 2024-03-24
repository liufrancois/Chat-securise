Mon projet consiste en une messagerie sécurisée en Python qui permet à deux clients de communiquer en passant par un serveur.

Client.py :

Le programme commence par générer une clé RSA avec la classe Demande, puis demande le nom à l'utilisateur. 
Il envoie ensuite au serveur le nom et la clé publique RSA chiffrée avec un chiffrement par bloc. 
En retour, il reçoit le nom et la clé publique de l’autre utilisateur, les déchiffre, 
puis appelle le constructeur de la classe thread qui permet d'envoyer et de recevoir des messages chiffrés.
Les messages sont d'abord chiffrés avec la clé secrète, puis avec la clé publique de l’autre utilisateur.
L’affichage est réalisé avec la bibliothèque Tkinter.


serveur.py :

Le programme commence par attendre que les deux personnes se connectent. 
Pour chacune d'entre elles, le serveur reçoit le nom et sa clé publique chiffrés, 
puis envoie le nom et sa clé publique à l'autre utilisateur. 
Il utilise la fonction run de la classe ClientThread pour recevoir un message et l’envoyer à l'autre utilisateur.