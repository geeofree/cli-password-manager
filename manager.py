if __name__ == '__main__':
    from locker import Locker
    from cmd import print_options, ask_option_number

    pw_manager = Locker()
    data = pw_manager.get_locker_data()

    print_options()
    selected_option = ask_option_number()

    while selected_option != 0:
        if selected_option == 1:
            pw_manager.print_data()
        elif selected_option == 5:
            print_options()


        selected_option = ask_option_number()
