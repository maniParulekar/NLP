{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "Created on Tue Aug  8 20:54:15 2017\n",
    "@author: DIP\n",
    "@Copyright: Dipanjan Sarkar\n",
    "\"\"\"\n",
    "\n",
    "import numpy as np\n",
    "\n",
    "\n",
    "# prints components of all the topics \n",
    "# obtained from topic modeling\n",
    "def print_topics_udf(topics, total_topics=1,\n",
    "                     weight_threshold=0.0001,\n",
    "                     display_weights=False,\n",
    "                     num_terms=None):\n",
    "    \n",
    "    for index in range(total_topics):\n",
    "        topic = topics[index]\n",
    "        topic = [(term, float(wt))\n",
    "                 for term, wt in topic]\n",
    "        topic = [(word, round(wt,2)) \n",
    "                 for word, wt in topic \n",
    "                 if abs(wt) >= weight_threshold]\n",
    "                     \n",
    "        if display_weights:\n",
    "            print('Topic #'+str(index+1)+' with weights')\n",
    "            print(topic[:num_terms]) if num_terms else topic\n",
    "        else:\n",
    "            print('Topic #'+str(index+1)+' without weights')\n",
    "            tw = [term for term, wt in topic]\n",
    "            print(tw[:num_terms]) if num_terms else tw\n",
    "        print()\n",
    "        \n",
    "\n",
    "# extracts topics with their terms and weights\n",
    "# format is Topic N: [(term1, weight1), ..., (termn, weightn)]        \n",
    "def get_topics_terms_weights(weights, feature_names):\n",
    "    feature_names = np.array(feature_names)\n",
    "    sorted_indices = np.array([list(row[::-1]) \n",
    "                           for row \n",
    "                           in np.argsort(np.abs(weights))])\n",
    "    sorted_weights = np.array([list(wt[index]) \n",
    "                               for wt, index \n",
    "                               in zip(weights,sorted_indices)])\n",
    "    sorted_terms = np.array([list(feature_names[row]) \n",
    "                             for row \n",
    "                             in sorted_indices])\n",
    "    \n",
    "    topics = [np.vstack((terms.T, \n",
    "                     term_weights.T)).T \n",
    "              for terms, term_weights \n",
    "              in zip(sorted_terms, sorted_weights)]     \n",
    "    \n",
    "    return topics         \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "projNlp",
   "language": "python",
   "name": "projnlp"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
