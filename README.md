# CKY-Parser
* Constituency parser trained by the ATIS portion of Penn Treebank
* Probabilistic_CFG.py learns a probabilistic CFG from trees, and stores it in "NP -> DT NN # 0.5" format. 
* CKY_Parser.py takes the grammar and a sentence as input, and outputs the highest-probability parse.
* All words that occurred only once, are replaced with <unk>.
* To avoid underflow, log-probabilities are used. 
