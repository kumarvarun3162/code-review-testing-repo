const express = require("express");
const mongoose = require("mongoose");
const axios = require("axios");
const fs = require("fs");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");

const app = express();

app.use(express.json());

// VULNERABILITY: Hardcoded Secret
const JWT_SECRET = "my-super-secret-key";

// Demo User Schema
const User = mongoose.model(
  "User",
  new mongoose.Schema({
    username: String,
    password: String, // store hash
  })
);

User.schema.pre("save", async function (next) {
  if (!this.isModified("password")) return next();
  const salt = await bcrypt.genSalt(12);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});

// --------------------------------------------------
// NoSQL Injection
// --------------------------------------------------
app.post("/login", async (req, res) => {
  const { username, password } = req.body;

  // VULNERABILITY: Unsanitized query object
  const user = await User.findOne({
    username: username,
  });

  if (!user || !(await bcrypt.compare(password, user.password))) {
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
app.get("/config", async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return res.status(403).send("Forbidden");
  }
  const token = authHeader.split(" ")[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    if (decoded.username !== "admin") {
      return res.status(403).send("Forbidden");
    }
    res.json({
      database: process.env.MONGO_URI || "mongodb://localhost:27017/test",
    });
  } catch {
    res.status(403).send("Forbidden");
  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});