# 🎯 URLCrafter

<div align="center">
  <img src="https://raw.githubusercontent.com/Madhav1716/URLCrafter/main/assets/logo.png" alt="URLCrafter Logo" width="200"/>
  
  [![PyPI version](https://badge.fury.io/py/urlcrafter.svg)](https://badge.fury.io/py/urlcrafter)
  [![Python Versions](https://img.shields.io/pypi/pyversions/urlcrafter.svg)](https://pypi.org/project/urlcrafter/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

## 🎨 URL Crafting Made Fun!

Tired of wrestling with URL strings? Say goodbye to messy concatenation and hello to URLCrafter! 🎉

URLCrafter is your friendly neighborhood URL wizard 🧙‍♂️, turning URL manipulation from a chore into a breeze. With its chainable API, you'll be crafting URLs like a pro in no time!

Created by Madhav Panchal (2025)
- GitHub: [Madhav1716](https://github.com/Madhav1716)
- LinkedIn: [in/madhav1716](https://linkedin.com/in/madhav1716)

## 🎯 Why Choose URLCrafter?

Python's built-in URL handling can feel like trying to solve a Rubik's cube blindfolded 🤪. URLCrafter swoops in like a superhero 🦸‍♂️ to save the day with:

- No more string concatenation nightmares
- Say goodbye to manual URL encoding
- Wave farewell to parameter management headaches
- Welcome to clean, readable, and fun URL manipulation!

## 🚀 Installation

```bash
pip install urlcrafter
```

## 🎮 Features

| Feature | Description |
|---------|-------------|
| 🔗 Chainable API | Build URLs with style and grace |
| 🔄 Query Management | Add, remove, update parameters like a boss |
| 🛣️ Path Handling | Navigate paths with ease |
| 🔒 URL Encoding | Let URLCrafter handle the encoding magic |
| 🔤 Slugify | Turn "My Awesome Post!" into "my-awesome-post" |
| 📊 Fragment Support | Add those fancy #hashtags |
| 🧩 URL Parsing | Break down and rebuild URLs like a pro |

## 🎪 Let's Play!

### Basic URL Building

```python
from urlcrafter import URL

# Build a simple URL
url = URL("https://example.com").add_path("products").add_param("page", 2).build()
print(url)  # https://example.com/products?page=2

# Create a URL from scratch
url = URL().set_scheme("https").set_netloc("api.example.com").set_path("/v1/users").build()
print(url)  # https://api.example.com/v1/users

# Parse and modify an existing URL
url = URL.parse("https://shop.example.com/products?category=electronics")
url.add_path("laptops").add_param("brand", "apple").remove_param("category")
print(url.build())  # https://shop.example.com/products/laptops?brand=apple
```

### 🎭 Fun with Slugify

```python
from urlcrafter import URL

# Turn any text into a URL-friendly slug
article_title = "10 Python Tips & Tricks for 2025!"
url = URL("https://blog.example.com").add_path("articles").add_slugified_path(article_title).build()
print(url)  # https://blog.example.com/articles/10-python-tips-tricks-for-2025
```

### 🎯 REST API Magic

```python
from urlcrafter import URL

# Build REST API endpoints with ease
base_api = URL("https://api.example.com/v1")

# GET /users
users_endpoint = base_api.add_path("users").build()
print(users_endpoint)  # https://api.example.com/v1/users

# GET /users/123/posts?status=published
user_posts = base_api.add_path("users").add_path("123").add_path("posts").add_param("status", "published").build()
print(user_posts)  # https://api.example.com/v1/users/123/posts?status=published
```

## 🤝 Join the Party!

Contributions are welcome! Let's make URL manipulation even more awesome together! 🎉

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<div align="center">
  <sub>Built with ❤️ by the URLCrafter team</sub>
</div>
