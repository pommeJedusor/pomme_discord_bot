class CommandNotFoundException(Exception):
    pass


def get_command_description(command_name: str) -> str:
    match command_name:
        case "help":
            return "c'est la commande que vous venez de faire ;)\nelle permet de voir la liste des commandes\net une déscription pour chacune d'entre elles"

    error_message = "désolé la commande n'as pas été trouvée\npeut être une faute de frappe ou d'orthographe?"
    raise CommandNotFoundException(error_message)
