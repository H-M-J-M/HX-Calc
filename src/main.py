
from src.runner_kern import run_kern_method

def entry_point():
    print("Choose a heat exchanger estimation method:")
    print("a. Kern's")
    print("b. Bell-Delaware")
    print("c. Stream Analysis")
    
    estimation_method = input("Enter your choice: ")
    
    match estimation_method:
        case "a":
            run_kern_method()
        case "b":
            print("Bell-Delaware method placeholder")
        case "c":
            print("Stream Analysis placeholder")
        case _:
            print("Invalid choice")

if __name__ == "__main__":
    entry_point()