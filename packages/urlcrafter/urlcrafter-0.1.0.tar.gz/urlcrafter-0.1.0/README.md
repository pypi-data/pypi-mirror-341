# URLCrafter

A human-friendly Python library for building and manipulating URLs with a chainable API.

Created by Madhav Panchal (2025)
- GitHub: [Madhav1716](https://github.com/Madhav1716)
- LinkedIn: [in/madhav1716](https://linkedin.com/in/madhav1716)

## Why URLCrafter?

Python's built-in URL handling modules like `urllib`, `urlparse`, or even `requests` can be verbose and unintuitive for building or modifying URLs dynamically. Developers often have to manually concatenate strings, encode parameters, and worry about formatting — which is error-prone and time-consuming.

URLCrafter solves this by offering an intuitive, chainable syntax to create and edit URLs in a clean and readable way.

## Installation

```bash
pip install urlcrafter
```

## Features

- 🔗 Chain-friendly API for building and manipulating URLs
- 🔄 Add/remove/update query parameters
- 🛣️ Append path segments easily
- 🔒 Automatic URL encoding/decoding
- 🔤 Slugify support (turn "React Course @ 2024" into "react-course-2024")
- 📊 Set URL fragments like #section
- 🧩 Easy parsing and manipulation of existing URLs
- 📚 Batch URL creation for pagination, filters, etc.

## Simple Examples

### Basic URL Building

```python
from urlcrafter import URL

# Build a simple URL
url = URL("https://example.com").add_path("products").add_param("page", 2).build()
print(url)  # https://example.com/products?page=2

# Create a URL from scratch
url = URL().set_scheme("https").set_netloc("api.example.com").set_path("/v1/users").build()
print(url)  # https://api.example.com/v1/users

# Parse an existing URL and modify it
url = URL.parse("https://shop.example.com/products?category=electronics")
url.add_path("laptops").add_param("brand", "apple").remove_param("category")
print(url.build())  # https://shop.example.com/products/laptops?brand=apple
```

### Using Slugify

```python
from urlcrafter import URL

# Create a slug from text
article_title = "10 Python Tips & Tricks for 2025!"
url = URL("https://blog.example.com").add_path("articles").add_slugified_path(article_title).build()
print(url)  # https://blog.example.com/articles/10-python-tips-tricks-for-2025
```

### Working with Query Parameters

```python
from urlcrafter import URL

# Adding multiple parameters at once
params = {
    "sort": "price",
    "order": "asc",
    "limit": 20
}
url = URL("https://api.example.com/products").add_params(params).build()
print(url)  # https://api.example.com/products?sort=price&order=asc&limit=20

# Update a parameter
url = URL(url).add_param("sort", "rating").build()
print(url)  # https://api.example.com/products?sort=rating&order=asc&limit=20
```

### Using Fragments

```python
from urlcrafter import URL

# Add a fragment (hash)
url = URL("https://docs.example.com/guide").set_fragment("installation").build()
print(url)  # https://docs.example.com/guide#installation
```

## Advanced Usage

### Building URLs for REST APIs

```python
from urlcrafter import URL

base_api = URL("https://api.example.com/v1")

# GET /users
users_endpoint = base_api.add_path("users").build()
print(users_endpoint)  # https://api.example.com/v1/users

# GET /users/123
user_detail = base_api.add_path("users").add_path("123").build()
print(user_detail)  # https://api.example.com/v1/users/123

# GET /users/123/posts?status=published
user_posts = base_api.add_path("users").add_path("123").add_path("posts").add_param("status", "published").build()
print(user_posts)  # https://api.example.com/v1/users/123/posts?status=published
```

### Pagination Helper

```python
from urlcrafter import URL

def generate_paginated_urls(base_url, total_pages):
    """Generate a list of paginated URLs."""
    return [URL(base_url).add_param("page", i).build() for i in range(1, total_pages + 1)]

pagination_urls = generate_paginated_urls("https://blog.example.com/articles", 5)
print(pagination_urls)
# ['https://blog.example.com/articles?page=1', 'https://blog.example.com/articles?page=2', ...]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
