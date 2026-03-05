# 🔐 SAE4_Equipe_16

L'objectif principal de ce projet est de **comprendre et implémenter les concepts mathématiques de l'ECC (Elliptic Curve Cryptography)** et de les appliquer à un **protocole cryptographique**.

---

## 📦 Technologies utilisées

Ce projet est implémenté en **Python 3.12** et utilise les bibliothèques suivantes (à installer si besoin via `pip install nom_de_la_bibliothèque`) :

- **random** : Génération de points aléatoires  
- **numpy** : Manipulation efficace de tableaux numériques  
- **matplotlib** : Visualisation et tracé de courbes  
- **os / sys** : Navigation et gestion des fichiers système  
- **hashlib / base58** : Hachage et encodage des adresses **Bitcoin**  
- **cryptography** : Benchmark des algorithmes de chiffrement **RSA** et **ECDH**  
- **pytest** : Tests unitaires des fonctions (addition, multiplication scalaire, etc.)

---

## 🧪 Tests unitaires

Pour exécuter les tests avec `pytest`, assurez-vous d'abord d'utiliser un environnement virtuel. Voici les étapes recommandées :

```bash
# Activer l'environnement virtuel
source myvenv/bin/activate

# Installer les dépendances nécessaires
pip install -r requirements.txt

# Lancer les tests sur un fichier spécifique
pytest chemin/vers/le_fichier_test.py
```

**💡 Note :**  
Si `pytest` n’est pas reconnu, ajoute ce chemin à ta variable d’environnement :

```bash
export PATH=$PATH:/mnt/netta/users/{votre_user}/.local/bin
```

---

## 🚀 Utilisation

Voici les principaux scripts disponibles dans le projet :

- `Crypto/TestCrypto.py`  
  ➤ Démontre la génération de clés jusqu'à la génération de la **clé secrète via ECDH**, en utilisant **notre propre courbe elliptique implémentée**.

- `Crypto/Benchmark/main.py`  
  ➤ Compare les performances entre **RSA (3076 bits)** et **ECDH (256 bits)** à l’aide de graphiques.  
  Cette comparaison repose sur des librairies standard pour garantir l'équité du benchmark.

- `Bitcoin/SECP256k1Demonstration.py`  
  ➤ Montre la **génération d'adresses Bitcoin**, ainsi que la **signature** et la **vérification** d'une **transaction fictive** sur la courbe **SECP256k1**.

- Tous les fichiers de tests
  ➤ Permettent de valider les opérations fondamentales sur les courbes elliptiques : **addition de points, multiplication scalaire**, etc.

---

## ✅ Pré-requis

Avant d'exécuter les fichiers du projet, assurez-vous d’avoir installé toutes les dépendances sur l'environnement virtuel ( principalement pour les tests ):

```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n'existe pas encore, vous pouvez le générer avec :

```bash
pip freeze > requirements.txt
```
