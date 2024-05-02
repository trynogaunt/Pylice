import toml

class Language():
    def __init__(self) -> None:
        with open("app/language.toml") as l:
            with open('app/language.toml','r', encoding="utf8") as l:
                self.language_data = toml.load(l)
    
    def interface(self, langue : str , module) -> dict:
        dict = {}
        module = module.split(".")[1].lower()
        print(self.language_data)
        for sentence , values in self.language_data[langue][module].items():
            dict[sentence] = values
        return dict