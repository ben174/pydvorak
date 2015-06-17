from string import ascii_uppercase


class ScoreCard(dict):
    def __init__(self):
        for c in ascii_uppercase:
            self[c] = CharacterScore(c)
        self[' '] = CharacterScore(' ')

    def consume_prompt(self, prompt):
        for pc in prompt.characters:
            self[pc.character].prompt_characters.append(pc)


class CharacterScore:
    def __init__(self, char):
        self.character = char
        self.prompt_characters = []

    def get_total_errors(self):
        ret = 0
        for pc in self.prompt_characters:
            ret += pc.error_count
        return ret

    def get_error_rate(self):
        return self.get_total_errors() / len(self.prompt_characters)

    def get_average_speed(self):
        return sum([pc.get_timed_time().microseconds for pc in self.prompt_characters]) / len(self.prompt_characters)

    def __str__(self):
        return self.character

    def __repr__(self):
        return self.character
