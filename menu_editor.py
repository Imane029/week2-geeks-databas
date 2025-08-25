from menu_item import MenuItem
from menu_manager import MenuManager
import sys

def show_user_menu():

    while True:
        print("\n--- Gestionnaire de Menu du Restaurant ---")
        print("Visualiser un article (V)")
        print("Ajouter un article (A)")
        print("Supprimer un article (D)")
        print("Mettre à jour un article (U)")
        print("Afficher le menu (S)")
        print("Quitter (Q)")
        
        choice = input("Entrez votre choix : ").upper()
        
        if choice == 'V':
            view_item()
        elif choice == 'A':
            add_item_to_menu()
        elif choice == 'D':
            remove_item_from_menu()
        elif choice == 'U':
            update_item_from_menu()
        elif choice == 'S':
            show_restaurant_menu()
        elif choice == 'Q':
            print("Fermeture du programme.")
            show_restaurant_menu()
            sys.exit()
        else:
            print("Choix invalide. Veuillez réessayer.")

def view_item():
    
    item_name = input("Entrez le nom de l'article à visualiser : ")
    item = MenuManager.get_by_name(item_name)
    if item:
        print(f"Article trouvé : Nom - {item.item_name}, Prix - {item.item_price} $")
    else:
        print(f"Aucun article trouvé avec le nom '{item_name}'.")

def add_item_to_menu():
    item_name = input("Entrez le nom du nouvel article : ")
    try:
        item_price = int(input("Entrez le prix du nouvel article : "))
        new_item = MenuItem(item_name, item_price)
        if new_item.save():
            print(f"'{item_name}' a été ajouté avec succès.")
        else:
            print(f"Une erreur s'est produite lors de l'ajout de '{item_name}'.")
    except ValueError:
        print("Prix invalide. Veuillez entrer un nombre entier.")

def remove_item_from_menu():
    
    item_name = input("Entrez le nom de l'article à supprimer : ")
    item_to_delete = MenuItem(item_name, 0)
    if item_to_delete.delete():
        print(f"'{item_name}' a été supprimé avec succès.")
    else:
        print("Une erreur s'est produite lors de la suppression de l'article. Il se peut qu'il n'existe pas.")

def update_item_from_menu():
    
    old_name = input("Entrez le nom de l'article à mettre à jour : ")
    new_name = input("Entrez le nouveau nom de l'article : ")
    try:
        new_price = int(input("Entrez le nouveau prix de l'article : "))
        item_to_update = MenuItem(old_name, 0)
        if item_to_update.update(new_name, new_price):
            print(f"'{old_name}' a été mis à jour avec succès en '{new_name}'.")
        else:
            print("Une erreur s'est produite lors de la mise à jour de l'article. Il se peut que l'article n'existe pas.")
    except ValueError:
        print("Prix invalide. Veuillez entrer un nombre entier.")

def show_restaurant_menu():
    
    items = MenuManager.all_items()
    if items:
        print("\n--- Menu du Restaurant ---")
        for item in items:
            print(f"{item.item_name} - {item.item_price} $")
    else:
        print("\nLe menu est actuellement vide.")

if __name__ == "__main__":
    show_user_menu()