import nltk
import requests

GIST = '''
https://gist.githubusercontent.com/nzhukov/b66c831ea88b4e5c4a044c952fb3e1ae/raw/7935e52297e2e85933e41d1fd16ed529f1e689f5/A%2520Brief%2520History%2520of%2520the%2520Web.txt
'''


class PartOfSpeechTagging:
    POS_TAGS_TRANSLATION = {
        'NN': 'noun, singular',
        'IN': 'preposition/subordinating conjunction',
        'DT': 'determiner',
        'NNP': 'proper noun, singular',
        'JJ': 'adjective',
    }

    def __init__(self, sentence: str) -> None:
        self._sentence = sentence

    @property
    def count_part_of_speech(self) -> dict:
        counts = dict()

        for _, pos in self.tagged:
            c = counts.get(pos, 0) + 1
            counts[pos] = c

        return counts

    @property
    def tagged(self) -> list:
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

        tokens = nltk.word_tokenize(self._sentence)

        return nltk.pos_tag(tokens)

    @property
    def top_5(self) -> list:
        return sorted(
            self.count_part_of_speech.items(),
            key=lambda kv: kv[1]
        )[:-6:-1]


def main():
    uri = GIST.strip()
    r = requests.get(uri)
    r.raise_for_status()

    p = PartOfSpeechTagging(r.text)
    pprint_top_5(p.top_5)


def pprint_top_5(counts: list):
    print('Top 5')
    for pos, count in counts:
        print(f'{PartOfSpeechTagging.POS_TAGS_TRANSLATION[pos.strip()]} - {count}')


if __name__ == '__main__':
    main()
