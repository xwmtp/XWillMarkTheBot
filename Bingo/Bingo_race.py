class Bingo_race:

    def __init__(self, date, time, url, comment, player):
        self.date = date
        self.time = time
        self.url = url
        self.seed = extract_seed(url)
        self.type = extract_type(url, date)
        self.player = player
        self.comment = comment
        self.row = regex_to_row(extract_row(comment))

    def isBingo(self):
        return "bingo" in self.url


    def print_race(self, url = False):
        print_list = [str(self.date), str(self.time), self.type, self.seed, self.row, self.comment,]
        if url:
            print_list.append(self.url)
        print("\t".join(print_list))