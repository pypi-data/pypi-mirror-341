import argparse
from mscnltk import question, code

def main():
    parser = argparse.ArgumentParser(prog="tricknlp-cli")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand to show all questions
    help_parser = subparsers.add_parser("help", help="Show all available questions")
    
    # Subcommand to get the code for a specific question number
    code_parser = subparsers.add_parser("code", help="Get the code for a specific question number")
    code_parser.add_argument("question_number", type=int, help="Question number to fetch code for")

    args = parser.parse_args()

    if args.command == "help":
        print(question())  # Show all questions
    elif args.command == "code":
        print(code(args.question_number))  # Show code for specific question
    else:
        print("Invalid option. Use 'tricknlp-cli help' to see available options.")
