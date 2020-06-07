from termcolor import colored


def print_error(message):
    print(colored(message, 'red'))


def print_success(message):
    print(colored(message, 'green'))


def print_status(message):
    print(colored(message, 'blue', attrs=['blink']), end='\r')