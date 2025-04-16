import .server

def main() -> None:
    .server.app.run(transport='stdio')
