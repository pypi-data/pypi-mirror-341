# -*- coding: utf-8 -*-
"""
@File    :   _rank_ifs_groups_update.py
@Time    :   2024/12/23
@Author  :   Dawn
@Version :   1.0
@Desc    :   DIF for scCyclone
"""


import numpy as np
import pandas as pd
import anndata as ad
from joblib import Parallel, delayed
from typing import Union
import scanpy as sc

from . import _utils


import warnings
warnings.filterwarnings('ignore')



def _compute_dif(e, data_a, data_b, valid_cells, n_bins, random_seed=22):
    """
    Compute dpsi values for a given event.

    Parameters
    ----------
    
    e (list): Iso identifier.
    data_a (pd.DataFrame): Data frame for group A.
    data_b (pd.DataFrame): Data frame for group B.
    min_cell_valid (int):The minimum number of effective cells.
    n_bins (int): Number of expression level bins for sampling.
    random_seed (int): Seed for the random number generator.

    Returns
    -------
    dict
        Dictionary containing the event, shuffled dpsi values, and observed dpsi value.
    """

    sub_a = data_a[[e]].dropna()
    sub_b = data_b[[e]].dropna()
    rpr_value=sub_a[e].gt(0).sum()/data_a.shape[0]
    tpr_value=sub_b[e].gt(0).sum()/data_b.shape[0]
    dpr_value=tpr_value-rpr_value
    rif_value=np.round(sub_a.mean().values[0],3)
    tif_value=np.round(sub_b.mean().values[0],3)
    
    min_shape = min(sub_a.shape[0], sub_b.shape[0])
    dif_observed = np.round((sub_b.mean() - sub_a.mean()).values[0], 3)
    
    if min_shape >= valid_cells:
        sub_data = pd.concat([sub_a, sub_b])
        label_list = np.array(["ref"] * sub_a.shape[0] + ["target"] * sub_b.shape[0])
        
        dif_list = []
        for _ in range(n_bins):
            if random_seed is not None:
                np.random.seed(random_seed)  # 设置随机数种子
            np.random.shuffle(label_list)
            shuffle_a = sub_data[label_list == "ref"]
            shuffle_b = sub_data[label_list == "target"]
            
            dif = np.round((shuffle_b.mean() - shuffle_a.mean()).values[0], 3)
            dif_list.append(dif)
    else:
        dif_list = [None]
    
    return {
        "iso": e,
        "dif_shuffle": dif_list,
        "dif_observed": dif_observed,
        "rif_value":rif_value,
        "tif_value":tif_value,
        "rpr_value":rpr_value,
        "tpr_value":tpr_value,
        "dpr_value":dpr_value,
        
        
    }
    
    

def _compute_pvalue(
    dif_shuffle, 
    dif_observed
    ):
    """
    Compute p-value based on observed and shuffled dpsi values.

    Parameters
    ----------
    
    dif_shuffle (np.ndarray): An array containing shuffled dif values.
    dif_observed (float): The observed dif value.

    Returns
    -------
    float or None
        Computed p-value.
    """
    if len(set(dif_shuffle)) > 1:
        # 使用 NumPy 的广播特性来比较 observed 值与 shuffle 值
        greater = np.array(dif_shuffle) > dif_observed
        less = np.array(dif_shuffle) < dif_observed

        count_greater = np.sum(greater)
        count_less = np.sum(less)

        # 如果 observed 值是正数，则计算大于 observed 的比例
        # 如果 observed 值是负数，则计算小于 observed 的比例
        # 如果 observed 值是零，则计算绝对值大于 shuffle 值的比例
        if dif_observed > 0:
            pvalue = count_greater / len(dif_shuffle)
        elif dif_observed < 0:
            pvalue = count_less / len(dif_shuffle)
        else:
            pvalue = (count_greater + count_less) / len(dif_shuffle)
    else:
        pvalue = 1  # 或者 None，取决于您如何处理这种情况

    return pvalue




def rank_ifs_groups(
    adata: ad.AnnData,
    groupby: str,
    groups: Union[str, list]="all",
    reference: str = "rest",
    key_added: Union[str, None] = None,
    valid_cells: int = 50,
    n_bins: int = 100,
    random_seed: int = 22,
    var_name: str ="gene_name"
    ):
    """
    Rank ifs for characterizing groups.

    Parameters
    ----------
    
    adata (ad.Anndata): Annotated data matrix.
    groupby (str) :The key of the observations grouping to consider.
    groups ([str, list]): Subset of groups, e.g. ['g1', 'g2', 'g3'], to which comparison shall be restricted, or 'all' (default), for all groups.
    reference (str): If 'rest', compare each group to the union of the rest of the group. If a group identifier, compare with respect to this group.
    key_added ([str, None]): The key in adata.uns information is saved to.
    percent (float): The minimum percentage of cells in which a event must be expressed to be kept (default is 0.1).
    valid_cells (int): The minimum number of effective cells.
    n_bins (int): Number of expression level bins for sampling.
    random_seed (int): Seed for the random number generator.

    Returns
    -------
    ad.AnnData
        Annotated data matrix with rank information stored in adata.uns[key_added].
    """

    groups_order = _utils.check_groups(adata,groupby,groups,reference)
    print(groups_order)
    
    iso_list = list(adata.var.index)
    
    # Initialize adata.uns[key_added]
    
    if key_added is None:
        key_added = "rank_ifs_groups"
    adata.uns[key_added] = {}
    adata.uns[key_added]["params"] = {"groupby": groupby, "reference": reference}

    # Initialize empty dictionaries for storing results
    data_iso_dict = {}
    data_dif_observed_dict = {}
    data_pval_dict = {}
    data_pval_adj_dict = {}
    data_dpr_dict = {}
    data_rpr_dict ={}
    data_tpr_dict ={}
    data_rif_dict = {}
    data_tif_dict = {}
    var_name_dict = {}
    

    # Iterate over groups
    for i in groups_order:
        if i != reference:
            print("Group {} start!".format(i))
            iso_data_list = []
            adata_target = adata[adata.obs[groupby] == i]
            adata_ref = adata[adata.obs[groupby] != i] if reference == "rest" else adata[adata.obs[groupby].isin([reference])]
            data_target = adata_target.to_df()
            data_ref = adata_ref.to_df()

            # Parallel computation of dpsi
            print("Compute dif...")
            rs = Parallel(n_jobs=-1)(delayed(_compute_dif)(e, data_ref, data_target, valid_cells, n_bins, random_seed) for e in adata.var.index)
            iso_data_list.extend(rs)
            result = pd.DataFrame(iso_data_list)

            # Compute p-values and sort results
            print("Compute pvalue...")

            result['pvals'] = result.apply(lambda row: _compute_pvalue(row['dif_shuffle'], row['dif_observed']), axis=1)
            result = result.sort_values(by=['dif_observed', 'pvals'], ascending=[False, True])

            # Store results in dictionaries
            data_iso_dict[i] = result['iso'].to_list()
            data_dif_observed_dict[i] = result['dif_observed'].to_list()
            data_rif_dict[i] = result['rif_value'].to_list()
            data_tif_dict[i] = result['tif_value'].to_list()
            data_pval_dict[i] = result['pvals'].to_list()
            data_dpr_dict[i] = result['dpr_value'].to_list()
            data_rpr_dict[i] = result['rpr_value'].to_list()
            data_tpr_dict[i] = result['tpr_value'].to_list()
            data_pval_adj_dict[i] = _utils.compute_pvalue_bonferroni(result['pvals'].to_list())
            var_name_dict[i] = adata_target[:,result['iso'].to_list()].var[var_name].to_list()

            print("Group {} complete!".format(i))
            print("-----------------------------------------")


    # Convert dictionaries to structured arrays
    name_data = pd.DataFrame(data_iso_dict).to_records(index=False)
    dif_data = pd.DataFrame(data_dif_observed_dict).to_records(index=False)
    pval_data = pd.DataFrame(data_pval_dict).to_records(index=False)
    pval_adj_data = pd.DataFrame(data_pval_adj_dict).to_records(index=False)
    dpr_data = pd.DataFrame(data_dpr_dict).to_records(index=False)
    rpr_data = pd.DataFrame(data_rpr_dict).to_records(index=False)
    tpr_data = pd.DataFrame(data_tpr_dict).to_records(index=False)
    tif_data = pd.DataFrame(data_tif_dict).to_records(index=False)
    rif_data = pd.DataFrame(data_rif_dict).to_records(index=False)
    var_name_data = pd.DataFrame(var_name_dict).to_records(index=False)
    
    

    # Store results in adata.uns
    adata.uns[key_added]['names'] = name_data
    adata.uns[key_added]['dif'] = dif_data
    adata.uns[key_added]['pvals'] = pval_data
    adata.uns[key_added]['pvals_adj'] = pval_adj_data
    adata.uns[key_added]['dpr'] = dpr_data
    adata.uns[key_added]['rpr'] = rpr_data
    adata.uns[key_added]['tpr'] = tpr_data
    adata.uns[key_added]['rif'] = rif_data
    adata.uns[key_added]['tif'] = tif_data
    adata.uns[key_added]['gene_name'] = var_name_data

    return adata


