const express = require("express");
const mongoose = require("mongoose");
const axios = require("axios");
const fs = require("fs");
const jwt = require("jsonwebtoken");

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
    password: password,
  });

  if (!user) {
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
  const response = await axios.get(url);

  res.send(response.data);
});

// --------------------------------------------------
// Path Traversal
// --------------------------------------------------
app.get("/file", (req, res) => {
  const filename = req.query.name;

  // VULNERABILITY: Arbitrary file read
  const content = fs.readFileSync(filename, "utf8");

  res.send(content);
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
  res.json({
    database: "mongodb://localhost:27017/test",
    jwtSecret: JWT_SECRET,
  });
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
