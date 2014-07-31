class Model:
    def __init__(self, model_type, model_path=None):
        self.model_type = model_type
        self.similarity = {}
        if model_path is not None:
            self.load_model(model_path)

    def load_model(self, path):
        for line in open(path, 'r'):
            en_1, en_2, sim = line.split('\t')
            # print en_1, en_2, sim
            self.similarity.setdefault(en_1, {})
            self.similarity[en_1][en_2] = sim.strip()

    def get_similarity(self, en_1, en_2):
        try:
            return self.similarity[en_1][en_2]
        except KeyError:
            return self.similarity[en_2][en_1]
