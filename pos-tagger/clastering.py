# coding: utf-8

import pandas
import codecs
import re
import itertools
from features_extractor import feat_extract
from sklearn.cluster import KMeans, MiniBatchKMeans, AgglomerativeClustering
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_selection import VarianceThreshold

# function: opening tables
def opening_data_target(feat_name, m, n):
	# getting features
	data = pandas.read_csv(feat_name, header=None, sep=';')
	features = data.iloc[m:n, 1:]
	words = data.iloc[:, 0]

	# getting targets
	data_target = pandas.read_csv('.\\test_data\\test_ml.csv', header=None, sep=';')
	target = data_target.iloc[:, 1]

	return features, target, words

# function: features selection
def feature_selection(features):
	sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
	features = sel.fit_transform(features)
	return features

# function: finding the best values of tags
def validate_with_mappings(preds, target, dataset):
	arr = []
	map_preds = []
	permutations = itertools.permutations([1, 2, 3, 4, 5, 6, 7, 0])
	for a, b, c, d, e, f, g, h in permutations:
		mapping = {7: a, 6: b, 5: c, 4: d, 3: e, 2: f, 1: g, 0: h}
		mapped_preds = [mapping[pred] for pred in preds]
		map_preds.append(mapped_preds)
		arr.append(float(sum(mapped_preds != target)) / len(target))
	return map_preds[arr.index(min(arr))]

# function: k-means clustering algorithm
def K_means(feat_name, m, n):
	features, target, words = opening_data_target(feat_name, m, n)
	km = KMeans(n_clusters=8, random_state=242)
	km_preds = km.fit_predict(features)

	# getting k-mans tags
	km_tags = validate_with_mappings(km_preds, target, features)

	# K-means results
	''''
	print 'Accuracy ', accuracy_score(target, km_tags)
	print 'Precision ', precision_score(target, km_tags)
	print 'Recall ', recall_score(target, km_tags)
	print 'F1 ', f1_score(target, km_tags)
	'''

# function: aglomerative clustering algorithm
def Aglomerative_cl(feat_name, m, n):
	features, target, words = opening_data_target(feat_name, m, n)
	ac = AgglomerativeClustering(n_clusters=8, linkage='average', affinity='cosine')
	ac_preds = ac.fit_predict(features)

	# getting aglomerative tags
	# need only for evaluation
	# ac_tags = validate_with_mappings(ac_preds, target, features)

	# Aglomerative results
	'''
	print 'Accuracy ', accuracy_score(target, ac_tags)
	print 'Precision ', precision_score(target, ac_tags)
	print 'Recall ', recall_score(target, ac_tags)
	print 'F1 ', f1_score(target, ac_tags)
	'''
	return ac_preds, words

#K_means('.\\test_data\\features.csv')
#Aglomerative_cl('.\\test_data\\features.csv')
