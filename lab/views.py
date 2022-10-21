from lab import app


@app.route("/")
def main():
    return "Hello, viewer!"
