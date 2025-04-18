import pyfcg as fcg

class Agent():
    """
    The class for representing agents.
    """

    def __init__(self, name="agent"):
        self.name = name
        self.id = fcg.gensym(name)
        self.grammar = fcg.Grammar(fcg.gensym(name + "-grammar"))

    def __repr__(self):
        """String representation for printing construction objects."""
        return "<Agent: " + self.name + " (id: " + self.id + ") ~ " + str(self.grammar_size()) + " constructions>"

    def load_grammar_from_file(self, file_name):
        """Load an FCG grammar spec in JSON format from a file."""
        self.grammar.load_grammar_from_file(file_name)


    def load_grammar_spec(self, grammar_spec):
        """Load an FCG grammar spec."""
        self.grammar.load_grammar_spec(grammar_spec)


    def formulate(self, meaning):
        """
        Formulate meaning through agent's grammar.
        """
        return self.grammar.formulate(meaning)


    def formulate_all(self, meaning):
        """
        Formulate meaning through agent's grammar, returning all solutions.
        """
        return self.grammar.formulate_all(meaning)


    def comprehend(self, utterance):
        """
        Comprehend an utterance through agent's grammar'.
        """
        return self.grammar.comprehend(utterance)


    def comprehend_all(self, utterance):
        """
        Comprehend an utterance through agent's grammar, returning all solutions.
        """
        return self.grammar.comprehend_all(utterance)


    def add_cxn(self, cxn):
        self.grammar.add_cxn(cxn)


    def delete_cxn(self, cxn):
        self.grammar.delete_cxn(cxn)


    def grammar_size(self):
        return self.grammar.size()


    def clear_cxns(self):
        self.grammar.clear_cxns()


    def find_cxn_by_name (self, cxn_name):
        return self.grammar.find_cxn_by_name(cxn_name)

    def add_category (self, category):
        self.grammar.add_category(category)

    def add_link (self, category_1, category_2):
        self.grammar.add_link(category_1, category_2)




