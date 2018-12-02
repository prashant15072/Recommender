from __future__ import division
import numpy as np
from collections import namedtuple


def get_hits(matched_predictions, positive_feedback):
    reldata = get_relevance_data(matched_predictions, positive_feedback)
    true_pos, false_pos = reldata.tp, reldata.fp
    true_neg, false_neg = reldata.tn, reldata.fn

    true_pos_hits = true_pos.sum()
    false_pos_hits = false_pos.sum()
    true_neg_hits = true_neg.sum()
    false_neg_hits = false_neg.sum()

    hits = namedtuple('Hits', ['true_positive', 'true_negative', 'false_positive', 'false_negative'])
    hits = hits._make([true_pos_hits, true_neg_hits, false_pos_hits, false_neg_hits])
    return hits


def get_relevance_scores(matched_predictions, positive_feedback):
    users_num = matched_predictions.shape[0]
    reldata = get_relevance_data(matched_predictions, positive_feedback)
    true_pos, false_pos = reldata.tp, reldata.fp
    true_neg, false_neg = reldata.tn, reldata.fn

    # true positive rate
    precision = true_pos / (true_pos + false_pos)
    # sensitivity
    recall = true_pos / (true_pos + false_neg)
    # false positive rate
    fallout = false_pos / (false_pos + true_neg)
    # true negative rate
    specifity = true_neg / (false_pos + true_neg)
    # false negative rate
    miss_rate = false_neg / (false_neg + true_pos)

    #average over all users
    precision = np.nansum(precision) / users_num
    recall = np.nansum(recall) / users_num
    fallout = np.nansum(fallout) / users_num
    specifity = np.nansum(specifity) / users_num
    miss_rate = np.nansum(miss_rate) / users_num

    scores = namedtuple('Relevance', ['precision', 'recall', 'fallout', 'specifity', 'miss_rate'])
    scores = scores._make([precision, recall, fallout, specifity, miss_rate])
    return scores


def get_ranking_scores(matched_predictions, feedback_data, switch_positive, alternative=True):
    users_num, topk, holdout = matched_predictions.shape
    ideal_scores_idx = np.argsort(feedback_data, axis=1)[:, ::-1] #returns column index only
    ideal_scores_idx = np.ravel_multi_index((np.arange(feedback_data.shape[0])[:, None], ideal_scores_idx), dims=feedback_data.shape)

    is_positive = feedback_data >= switch_positive
    positive_feedback = np.where(is_positive, feedback_data, 0)
    negative_feedback = np.where(~is_positive, -feedback_data, 0)

    relevance_scores_pos = (matched_predictions * positive_feedback[:, None, :]).sum(axis=2)
    relevance_scores_neg = (matched_predictions * negative_feedback[:, None, :]).sum(axis=2)
    ideal_scores_pos = positive_feedback.ravel()[ideal_scores_idx]
    ideal_scores_neg = negative_feedback.ravel()[ideal_scores_idx]

    discount_num = max(holdout, topk)
    if alternative:
        discount = np.log2(np.arange(2, discount_num+2))
        relevance_scores_pos = 2**relevance_scores_pos - 1
        relevance_scores_neg =float(2)**(relevance_scores_neg)- 1
        ideal_scores_pos = 2**ideal_scores_pos - 1
        ideal_scores_neg = float(2)**ideal_scores_neg - 1
    else:
        discount = np.hstack([1, np.log(np.arange(2, discount_num+1))])

    dcg = (relevance_scores_pos / discount[:topk]).sum(axis=1)
    dcl = (relevance_scores_neg / -discount[:topk]).sum(axis=1)
    idcg = (ideal_scores_pos / discount[:holdout]).sum(axis=1)
    idcl = (ideal_scores_neg / -discount[:holdout]).sum(axis=1)
    ndcg = np.nansum(dcg / idcg) / users_num
    ndcl = np.nansum(dcl / idcl) / users_num
    ranking_score = namedtuple('Ranking', ['nDCG', 'nDCL'])._make([ndcg, ndcl])
    return ranking_score


def get_relevance_data(matched_items, positive_feedback, not_rated_penalty=0):
    negative_feedback = ~positive_feedback
    missed_items = ~matched_items

    #relevant items present both in preferences and in recommendations
    in_top_pos = (matched_items & positive_feedback[:, None, :]).any(axis=2)
    #irrelevant items present both in preferences and in recommendations
    in_top_neg = (matched_items & negative_feedback[:, None, :]).any(axis=2)
    #irrelevant items, present in preferences and not recommended by algo
    no_recom_pos = (missed_items & negative_feedback[:, None, :]).all(axis=1)
    #relevant items, present in preferences and not recommended by algo
    no_recom_neg = (missed_items & positive_feedback[:, None, :]).all(axis=1)

    true_pos = in_top_pos.sum(axis=1)
    false_pos = in_top_neg.sum(axis=1)
    true_neg = no_recom_pos.sum(axis=1)
    false_neg = no_recom_neg.sum(axis=1)

    if not_rated_penalty > 0:
        #penalize prediction of items not present in preferences (i.e. not rated yet)
        #this decreases the advantage of the tensor algorithm,
        #as it penalizes potentially relevant predictions, taking into account
        #that we are able to correctly predict highly rated items in ~95% cases
        #this option should not be turned on
        not_rated_items = missed_items.all(axis=2)
        false_pos = false_pos + not_rated_penalty * not_rated_items.sum(axis=1)

    relevance_data = namedtuple('RelevanceData', ['tp', 'fp', 'tn', 'fn'])
    relevance_data = relevance_data._make([true_pos, false_pos, true_neg, false_neg])
    return relevance_data
