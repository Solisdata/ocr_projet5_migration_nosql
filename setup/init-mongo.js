// init-mongo.js

// Récupération des variables d'environnement
const dbName = process.env.DB_NAME;
const readerUser = process.env.READER_USER;
const readerPass = process.env.READER_PASS;
const writerUser = process.env.WRITER_USER;
const writerPass = process.env.WRITER_PASS;
const rootUser = process.env.MONGO_ROOT_USER;
const rootPass = process.env.MONGO_ROOT_PASS;

// Sélection de la base
const db = db.getSiblingDB(dbName);

// --- 1. Utilisateur Lecture Seule ---
db.createUser({
  user: readerUser,
  pwd: readerPass,
  roles: [ { role: "read", db: dbName } ]
});

// --- 2. Utilisateur Lecture/Écriture ---
db.createUser({
  user: writerUser,
  pwd: writerPass,
  roles: [ { role: "readWrite", db: dbName } ]
});

// --- 3. Utilisateur Admin ---
db.createUser({
  user: rootUser,
  pwd: rootPass,
  roles: [ { role: "dbAdmin", db: dbName } ]
});