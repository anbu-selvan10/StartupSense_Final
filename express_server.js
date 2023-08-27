const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const passport = require("passport");
const morgan = require("morgan");
const app = express();
const port = 4000;
const cors = require("cors");
app.use(cors());

app.use(morgan("tiny"));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(passport.initialize());
const jwt = require("jsonwebtoken");

mongoose
  .connect(
    "mongodb+srv://Anbu:tQ5wNYbZjfk4rEuT@cluster0.6bzyp56.mongodb.net/StartupSense",
    {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    }
  )
  .then(() => console.log("MongoDB connected"))
  .catch((err) => console.log(err));

app.listen(port, () => console.log(`Server is running on port ${port}`));

const userSchema = new mongoose.Schema({
  username: String,
  email: String,
  password: String,
  bio: String
});

const User = mongoose.model('User', userSchema);

const createToken = (userId) => {
    const expiresIn = 60 * 60 * 24 * 3;
    const payload = { userId: userId };
  
    const token = jwt.sign(payload, "Q$r2K6W8n!jCW%Zk", { expiresIn });
  
    return token;
  };

  app.post("/register", (req, res) => {
    console.log(req.body);
    const {
    username,
    email,
    password,
    confirm_password,
    bio 
    } = req.body;
    
    if (password !== confirm_password) {
        res.status(400).json({ message: "Password incorrect" });
    }

    
    const newUser = new User({
      username,
      email,
      password,
      bio
    });
    console.log(newUser);
    newUser
      .save()
      .then((user) => {
        res.status(200).json({ message: "User registered successfully" });
      })
      .catch((err) => {
        console.log("error in saving the user", err);
        res.status(500).json({ message: err });
      });
  });

app.post("/login", (req, res) => {
    const { username, password } = req.body;
  
    User.findOne({ username })
      .then((user) => {
        if (!user) {
          res.status(400).json({ message: "User not found" });
        }
  
        if (user.password !== password) {
          res.status(400).json({ message: "Password incorrect" });
        }
  
        const token = createToken(user._id);
        res.status(200).json({ token });
      })
      .catch((err) => {
        console.log("error in finding the user", err);
        res.status(400).json({ message: err });
      });
  });

app.get("/userprofile", async(req, res) => {
  const authHeader = req.headers.authorization;

  if(!authHeader){
    console.log("Nothing");
    return res.status(401).json({error: 'No token'});
  }

  const token = authHeader.split(" ")[1];

  jwt.verify(token, "Q$r2K6W8n!jCW%Zk", async(err, decoded) => {
    if(err){
      console.log("Error: ", err);
      return res.status(401).json({error: 'Invalid token'});
    }

    console.log("Decoded: ", decoded);

    try{
      const user = await User.findById(decoded.userId);

      if(!user){
        return res.status(404).json({error: 'Invalid user'});
      }

      res.status(200).json({
        username: user.username,
        email: user.email,
        bio: user.bio
    });

    }catch (error) {
      console.error("Error fetching user:", error);
      return res.status(500).json({ error: 'Server error while retrieving user' });
  }

  } )
})
