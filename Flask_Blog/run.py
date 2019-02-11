from flaskblog import create_app
app = create_app()
# when you run run.py it will load the init.py file first
if __name__ == "__main__":
    app.run(debug=True)