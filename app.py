from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "my-blog-secret-key"

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    print("ERROR: MONGO_URI is not found in .env file")
else:
    print("MONGO_URI found")

client = MongoClient(mongo_uri)

# Database
db = client["blog_platform"]
posts_collection = db["posts"]


# Test connection
try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")
except Exception as e:
    print("MongoDB connection failed:", e)


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        users = db["users"]

        users.insert_one({
            "username": username,
            "email": email,
            "password": password
        })

        return "Registration successful!"

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = db["users"].find_one({
            "email": email,
            "password": password
        })

        if user:
            session["user_id"] = str(user["_id"])
            session["email"] = user["email"]
            return redirect(url_for("dashboard"))

        return "Invalid email or password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    posts = db["posts"].find().sort("_id", -1)

    return render_template("dashboard.html", posts=posts)

@app.route("/create-post", methods=["GET", "POST"])
def create_post():

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        posts = db["posts"]

        posts.insert_one({
            "title": title,
            "content": content
        })

        return "Post published successfully!"

    return render_template("create_post.html")
from bson.objectid import ObjectId

@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):

    posts = db["posts"]

    post = posts.find_one({
        "_id": ObjectId(post_id)
    })

    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")

        posts.update_one(
            {"_id": ObjectId(post_id)},
            {
                "$set": {
                    "title": title,
                    "content": content
                }
            }
        )

        return "Post updated successfully!"

    return render_template("edit_post.html", post=post)
@app.route("/delete-post/<post_id>", methods=["POST"])
def delete_post(post_id):

    posts = db["posts"]

    posts.delete_one({
        "_id": ObjectId(post_id)
    })

    return "Post deleted successfully!"
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/post")
def post():
    posts = list(posts_collection.find())
    return render_template("post.html", posts=posts)


@app.route("/add_post", methods=["POST"])
def add_post():
    title = request.form["title"]
    content = request.form["content"]

    posts_collection.insert_one({
        "title": title,
        "content": content
    })

    return redirect("/post")







if __name__ == "__main__":
    app.run(debug=True)