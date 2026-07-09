# Dans les pas d’Al-Kindi

Un petit outil de cryptanalyse, écrit en Python, pour jouer avec le chiffre de César
et redécouvrir une idée vieille de plus de mille ans : casser un code sans en connaître la clé.

---

## 🧩 Pourquoi ce projet ?

Parce que jongler avec des messages secrets, c’est bien plus marrant qu’un cours de crypto.
Ce projet est né d’un stage où on voulait comprendre, manipuler et surtout s’amuser
avec le chiffrement classique. Rien de sorcier, juste des lettres qui se décalent
et un brin de statistiques.

Le clin d’œil historique : au IXe siècle, **Al-Kindi** remarque que dans une langue,
certaines lettres reviennent plus souvent que d’autres.
En comptant les lettres d’un texte chiffré, on peut deviner le message original.
Son idée toute simple est le cœur de notre outil.

---

## 🚀 Ce que fait l’outil

Une fois lancé, le programme permet de :

- **Chiffrer** un texte avec un décalage à la César.
- **Déchiffrer** quand on connaît la clé.
- **Craquer automatiquement** un message chiffré sans la clé, grâce à l’analyse de fréquence.
- *(bonus)* Visualiser les fréquences des lettres avec un petit graphique.

Le tout en ligne de commande (pour l’instant), avec un code clair et commenté en français.

---

## 🛠️ Technologies utilisées

- Python 3 (rien que du standard)
- Le module `collections` (Counter) pour compter les lettres
- En option : `matplotlib` pour les graphiques, `tkinter` pour une éventuelle interface

---

## 📦 Installation

git clone https://github.com/ton-compte/dans-les-pas-dalkindi.git
cd dans-les-pas-dalkindi