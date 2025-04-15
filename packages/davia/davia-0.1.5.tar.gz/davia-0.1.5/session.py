from davia import Davia, run_server

app = Davia()


@app.task
def my_task():
    return "Hello, World!"


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    run_server(app, browser=False)
