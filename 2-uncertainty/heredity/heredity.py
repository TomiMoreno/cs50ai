import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    p = 1

    for person in people:
        gene_probability = calculate_gene_probabilities(people, person, one_gene, two_genes)
        trait_probability = calculate_trait_probabilities(one_gene, two_genes, person, have_trait)
        p *= gene_probability * trait_probability

        


    return p



def calculate_gene_probabilities(people, person, one_gene, two_genes):
    """
        Calculate the probability of a person having a gene based on the gene's inheritance
        If the person has no parents, the probability is PROBS["gene"]
        If the person has parents, the probability is based on the probability of the parents having the gene
        each parent will pass one of their two genes on to their child randomly, and there is a PROBS["mutation"] chance that it mutates
    """

    if(people[person] == None):
        return PROBS["gene"]

    if(people[person]["mother"] == None and people[person]["father"] == None):
        return PROBS["gene"]
    else:
        mother = people[person]["mother"]
        father = people[person]["father"]
        
        person_num_of_genes = 1 if person in one_gene else 2 if person in two_genes else 0
        father_num_of_genes = 1 if father in one_gene else 2 if father in two_genes else 0
        mother_num_of_genes = 1 if mother in one_gene else 2 if mother in two_genes else 0
        p = calculateGeneBasedOnParents(father_num_of_genes, mother_num_of_genes, person_num_of_genes)

        return p

        
def calculateGeneBasedOnParents(father_copies, mother_copies, child_expected_genes):
    """
        Calculate the probability of a child having a gene based on the number of genes the parents have
        father_copies: the number of genes the father has
        mother_copies: the number of genes the mother has
        child_expected_genes: the expected number of genes the child will have
    """ 
    all_combinations = [(True, False), (True, True), (False, False), (False, True)]
    mutation_prob = PROBS["mutation"]
    valid_combinations = [x for x in all_combinations if sum(x) == child_expected_genes]
    p = 0
    for (fatherShouldPassGene, motherShouldPassGene) in valid_combinations:
        no_mutation_prob = 1- mutation_prob
        father_passes_gene_prob = father_copies / 2 * (no_mutation_prob) + (2 - father_copies) / 2 * mutation_prob
        mother_passes_gene_prob = mother_copies / 2 * (no_mutation_prob) + (2 - mother_copies) / 2 * mutation_prob

        father_prob = father_passes_gene_prob if fatherShouldPassGene else 1 - father_passes_gene_prob
        mother_prob = mother_passes_gene_prob if motherShouldPassGene else 1 - mother_passes_gene_prob
        no_mutation_prob = father_prob * mother_prob

        p += no_mutation_prob
    return p

def calculate_trait_probabilities(one_gene, two_genes, person, have_trait):
    return PROBS["trait"][2 if person in two_genes else 1 if person in one_gene else 0][person in have_trait]

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gene = 2 if person in two_genes else 1 if person in one_gene else 0
        trait = person in have_trait
        probabilities[person]["gene"][gene] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for field in probabilities[person]:
            total = sum(probabilities[person][field].values())
            for value in probabilities[person][field]:
                probabilities[person][field][value] /= total


if __name__ == "__main__":
    main()
