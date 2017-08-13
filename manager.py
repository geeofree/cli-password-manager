if __name__ == '__main__':
    from locker import Locker

    pw_manager = Locker()
    data = pw_manager.get_locker_data()

    pw_manager.print_options()
    selected_option = pw_manager.ask_option_number()

    while selected_option != 0:
        if selected_option == 1:
            pw_manager.print_data()
        elif selected_option == 2:
            pw_manager.add_password()
        elif selected_option == 5:
            pw_manager.print_options()

        selected_option = pw_manager.ask_option_number()
