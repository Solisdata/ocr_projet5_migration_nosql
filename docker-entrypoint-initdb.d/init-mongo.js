// init-mongo.js

// Base de ton application
db = db.getSiblingDB("ma_bd");

// --- 1. Utilisateur Lecture Seule (READER) ---
db.createUser({
  user: "reader",
  pwd: "Jozrjn87sd!",
  roles: [ { role: "read", db: "ma_bd" } ]
});


// --- 2. Utilisateur Lecture/Écriture (WRITER) ---
db.createUser({
  user: "writer",
  pwd: "Hiskdsoa98!",
  roles: [ { role: "readWrite", db: "ma_bd" } ]
});

//  Utilisateur admin 
db.createUser({
  user: "admin",
  pwd: "Massyhfkd2", 
  roles: [ { role: "dbAdmin", db: "ma_bd" } ]
});