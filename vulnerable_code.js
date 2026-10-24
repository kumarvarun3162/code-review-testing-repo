const express = require("express");
const mongoose = require("mongoose");
const axios = require("axios");
const fs = require("fs");
const jwt = require("jsonwebtoken");
const bcrypt = require('bcrypt');
const path = require('path');
const { URL } = require('url');

const app = express();

app.use(express.json());

// VULNERABILITY: Hardcoded Secret
const JWT_SECRET = "my-super-secret-key";

// Demo User Schema
const User = mongoose.model(
  "User",
  new mongoose.Schema({
    username: String,
    password: String,
  })
);
// --------------------------------------------------
// NoSQL Injection
// --------------------------------------------------
app.post("/login", async (req, res) => {
  const { username, password } = req.body;

  // VULNERABILITY: Unsanitized query object
  const user = await User.findOne({
    username: username,
  });

  if (!user) {
    return res.status(401).send("Invalid credentials");
  }

  const match = await bcrypt.compare(password, user.password);
  if (!match) {
    return res.status(401).send("Invalid credentials");
  }

  const token = jwt.sign(
    { username: user.username },
    JWT_SECRET
  );

  res.json({ token });
});

// --------------------------------------------------
// SSRF
// --------------------------------------------------
app.get("/fetch", async (req, res) => {
  const url = req.query.url;

  // VULNERABILITY: User-controlled URL request
  try {
    const parsedUrl = new URL(url);
    if (!['http:', 'https:'].includes(parsedUrl.protocol)) throw new Error('Invalid protocol');
    const response = await axios.get(parsedUrl.toString());
    res.send(response.data);
  } catch (err) {
    res.status(400).send('Invalid URL');
  }
});

// --------------------------------------------------
// Path Traversal
// --------------------------------------------------
const BASE_DIR = path.resolve(__dirname, 'public');
app.get("/file", (req, res) => {
  const filename = req.query.name;

  // VULNERABILITY: Arbitrary file read
  const normalized = path.normalize(filename);
  const filePath = path.join(BASE_DIR, normalized);
  if (!filePath.startsWith(BASE_DIR)) return res.status(400).send('Invalid path');
  try {
    const content = fs.readFileSync(filePath, "utf8");
    res.send(content);
  } catch (err) {
    res.status(404).send('File not found');
  }
});

// --------------------------------------------------
// Insecure JWT Verification
// --------------------------------------------------
app.get("/profile", (req, res) => {
  const token = req.headers.authorization;

  try {
    // VULNERABILITY: Weak secret
    const decoded = jwt.verify(token, JWT_SECRET);

    res.json(decoded);
  } catch {
    res.status(401).send("Unauthorized");
  }
});

// --------------------------------------------------
// Information Disclosure
// --------------------------------------------------
app.get("/config", (req, res) => {
  res.status(403).send('Forbidden');
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});