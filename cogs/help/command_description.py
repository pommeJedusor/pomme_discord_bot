class CommandNotFoundException(Exception):
    pass


def get_command_description(command_name: str) -> str:
    match command_name:
        case "help":
            return "c'est la commande que vous venez de faire ;)\nelle permet de voir la liste des commandes\net une déscription pour chacune d'entre elles"
        case "epicgames_set_channel":
            return "permet de spécifier le channel dans lequel envoyer les notifs des nouveaux jeux gratuits epic games\n1 seul channel max par serveur discord"
        case "epicgames_set_role":
            return "permet de spécifier le rôle qui seras mentionné lorsque des nouveaux jeux gratuits epic games sont disponibles\nils ne seront pas mentionnés si le jeux a déjà été gratuis depuis l'ajout du bot au serveur\n1 seul channel max par serveur discord"

    error_message = "désolé la commande n'as pas été trouvée\npeut être une faute de frappe ou d'orthographe?"
    raise CommandNotFoundException(error_message)
