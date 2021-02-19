import json
import sys
from NPClassifier.Classifier import fingerprint_handler
from NPClassifier.Classifier import prediction_voting
import tensorflow as tf
import numpy as np

ontology_dictionary = json.loads(open("NPClassifier/Classifier/dict/index_v1.json").read())

sup_model = tf.keras.models.load_model('NPClassifier/Classifier/models_folder/models/SUPERCLASS/000001/NP_classifier_superclass_V1.tf')
class_model = tf.keras.models.load_model('NPClassifier/Classifier/models_folder/models/CLASS/000001/NP_classifier_class_V1.tf')
path_model = tf.keras.models.load_model('NPClassifier/Classifier/models_folder/models/PATHWAY/000001/NP_classifier_pathway_V1.tf')

def classify_structure(smiles):
    isglycoside = fingerprint_handler._isglycoside(smiles)

    fp = fingerprint_handler.calculate_fingerprint(smiles, 2)

    fp1 = fp[0].tolist()[0]
    fp2 = fp[1].tolist()[0]

    inp = [np.array(fp1).reshape(1,-1), np.array(fp2).reshape(1,-1)]

    # Handling SUPERCLASS
    pred_super = sup_model.predict(inp).squeeze()
    n_super = list(np.where(pred_super>=0.3)[0])

    path_from_superclass = []
    for j in n_super:
        path_from_superclass += ontology_dictionary['Super_hierarchy'][str(j)]['Pathway']
    path_from_superclass = list(set(path_from_superclass))

    # Handling CLASS
    pred_class = class_model.predict(inp).squeeze()
    n_class = list(np.where(pred_class>=0.1)[0])

    path_from_class = []
    for j in n_class:
        path_from_class += ontology_dictionary['Class_hierarchy'][str(j)]['Pathway']
    path_from_class = list(set(path_from_class))

    # Handling PATHWAY
    pred_path = path_model.predict(inp).squeeze()
    n_path = list(np.where(pred_path>=0.5)[0])

    class_result = []
    superclass_result = []
    pathway_result = []

    # Voting on Answer
    pathway_result, superclass_result, class_result, isglycoside = prediction_voting.vote_classification(n_path,
                                                                                                        n_class,
                                                                                                        n_super,
                                                                                                        pred_class,
                                                                                                        pred_super,
                                                                                                        path_from_class,
                                                                                                        path_from_superclass,
                                                                                                        isglycoside,
                                                                                                        ontology_dictionary)

    return isglycoside, class_result, superclass_result, pathway_result, path_from_class, path_from_superclass, n_path, fp1, fp2

if __name__=='__main__':
    isglycoside, class_results, superclass_results, pathway_results, path_from_class, path_from_superclass, n_path, fp1, fp2 = classify_structure(sys.argv[1])

    respond_dict = {}
    respond_dict["class_results"] = class_results
    respond_dict["superclass_results"] = superclass_results
    respond_dict["pathway_results"] = pathway_results
    respond_dict["isglycoside"] = isglycoside
    print(respond_dict)

