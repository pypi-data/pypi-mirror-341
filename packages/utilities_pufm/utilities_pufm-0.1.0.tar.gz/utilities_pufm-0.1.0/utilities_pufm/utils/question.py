def question(question, options = ["y", "Y", "n", "N"]):
    while True:
        
        response = input(question)

        if response.strip() not in options:
            print(f"Escolha uma das opções: {options}")
        else:
            return response