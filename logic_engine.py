class KnowledgeBase:
    def __init__(self):
        self.facts = set()      # Store unique facts
        self.rules = []         # Store rules as (premises, conclusion)

    def tell_fact(self, fact_string):
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        self.rules.append((premise_list, conclusion_string))

    def clear_facts(self):
        self.facts.clear()

    def forward_chain(self):
        new_facts_added = True

        while new_facts_added:
            new_facts_added = False

            for premises, conclusion in self.rules:

                # If conclusion not already known
                if conclusion not in self.facts:

                    # Modus Ponens Check
                    if all(premise in self.facts for premise in premises):
                        self.facts.add(conclusion)
                        new_facts_added = True