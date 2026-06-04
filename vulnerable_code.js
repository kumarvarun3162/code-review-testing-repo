const express = require("express");
const mongoose = require("mongoose");
const axios = require("axios");
const fs = require("fs");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");

const app = express();

app.use(express.json());

// Secure Secret
const JWT_SECRET = process.env.JWT_SECRET;

// Demo User Schema
const User = mongoose.model(
  "User",
  new mongoose.Schema({
    username: String,
    password: String,
  })
);

// Hash password before saving
const hashPassword = async (password) => {
  const salt = await bcrypt.genSalt(10);
  return await bcrypt.hash(password, salt);
};

// Compare password with hashed password
const comparePassword = async (password, hashedPassword) => {
  return await bcrypt.compare(password, hashedPassword);
};

// --------------------------------------------------
// NoSQL Injection
// --------------------------------------------------
app.post("/register", async (req, res) => {
  const { username, password } = req.body;

  const hashedPassword = await hashPassword(password);

  const user = new User({
    username: username,
    password: hashedPassword,
  });

  try {
    await user.save();
    res.send("User created successfully");
  } catch (err) {
    res.status(400).send(err);
  }
});

app.post("/login", async (req, res) => {
  const { username, password } = req.body;

  const user = await User.findOne({ username: username });

  if (!user) {
    return res.status(401).send("Invalid credentials");
  }

  const isValidPassword = await comparePassword(password, user.password);

  if (!isValidPassword) {
    return res.status(401).send("Invalid credentials");
  }

  const token = jwt.sign(
    { username: user.username },
    JWT_SECRET,
    { expiresIn: "1h" }
  );

  res.json({ token });
});

// --------------------------------------------------
// SSRF
// --------------------------------------------------
const trustedUrls = ["https://example.com", "https://example.org"];

app.get("/fetch", async (req, res) => {
  const url = req.query.url;

  if (!trustedUrls.includes(url)) {
    return res.status(403).send("Forbidden");
  }

  try {
    const response = await axios.get(url);
    res.send(response.data);
  } catch (err) {
    res.status(500).send(err);
  }
});

// --------------------------------------------------
// Path Traversal
// --------------------------------------------------
const fileDirectory = "./files";

app.get("/file", (req, res) => {
  const filename = req.query.name;

  if (!filename) {
    return res.status(400).send("Filename is required");
  }

  const filePath = `${fileDirectory}/${filename}`;

  if (!filePath.startsWith(fileDirectory)) {
    return res.status(403).send("Forbidden");
  }

  try {
    const content = fs.readFileSync(filePath, "utf8");
    res.send(content);
  } catch (err) {
    res.status(404).send("File not found");
  }
});

// --------------------------------------------------
// Insecure JWT Verification
// --------------------------------------------------
app.get("/profile", (req, res) => {
  const token = req.headers.authorization;

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    res.json(decoded);
  } catch {
    res.status(401).send("Unauthorized");
  }
});

// Remove /config endpoint to prevent information disclosure
// app.get("/config", (req, res) => {
//   res.json({
//     database: "mongodb://localhost:27017/test",
//     jwtSecret: JWT_SECRET,
//   });
// });

app.listen(3000, () => {
  console.log("Server running on port 3000");
});