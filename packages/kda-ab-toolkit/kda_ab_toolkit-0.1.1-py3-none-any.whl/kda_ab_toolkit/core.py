import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest
from itertools import combinations
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportions_ztest
from itertools import combinations
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import warnings
warnings.filterwarnings("ignore")

def clean_outliers(data, method='percentile', lower=0.05, upper=0.95, contamination=0.05, eps=0.5, min_samples=5):
    if method == 'percentile':
        low = data.quantile(lower)
        high = data.quantile(upper)
        return data[(data >= low) & (data <= high)]
    elif method == 'iqr':
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        return data[(data >= Q1 - 1.5 * IQR) & (data <= Q3 + 1.5 * IQR)]
    elif method == 'winsor':
        low = data.quantile(lower)
        high = data.quantile(upper)
        return data.clip(lower=low, upper=high)
    elif method == 'isolation_forest':
        scaled = StandardScaler().fit_transform(data.values.reshape(-1, 1))
        clf = IsolationForest(contamination=contamination, random_state=42)
        preds = clf.fit_predict(scaled)
        return data[preds == 1]
    elif method == 'dbscan':
        scaled = StandardScaler().fit_transform(data.values.reshape(-1, 1))
        db = DBSCAN(eps=eps, min_samples=min_samples)
        labels = db.fit_predict(scaled)
        return data[labels != -1]
    else:
        return data

def determine_distribution(data, alpha=0.05):
    stat, p_value = stats.normaltest(data)
    return p_value > alpha, p_value

def bootstrap_test(sample1, sample2, n_iter=1000, func=np.median, alpha=0.05):
    observed_diff = func(sample2) - func(sample1)
    boot_diffs = []
    for _ in range(n_iter):
        resample1 = np.random.choice(sample1, size=len(sample1), replace=True)
        resample2 = np.random.choice(sample2, size=len(sample2), replace=True)
        boot_diffs.append(func(resample2) - func(resample1))
    ci_lower = np.percentile(boot_diffs, 100 * alpha / 2)
    ci_upper = np.percentile(boot_diffs, 100 * (1 - alpha / 2))
    is_significant = not (ci_lower <= 0 <= ci_upper)
    return {
        'test': 'bootstrap_CI',
        'observed_diff': observed_diff,
        'ci': (ci_lower, ci_upper),
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'is_significant': is_significant,
        'p_value': None,
        'p_value_corrected': None,
        'significant': is_significant
    }

def relative_ttest(control, test, alpha=0.05):
    mean_control = np.mean(control)
    var_mean_control = np.var(control) / len(control)

    difference_mean = np.mean(test) - mean_control
    difference_mean_var = np.var(test) / len(test) + var_mean_control

    covariance = -var_mean_control  # Допущение как в изначальной реализации

    relative_mu = difference_mean / mean_control
    relative_var = (
        difference_mean_var / (mean_control ** 2)
        + var_mean_control * (difference_mean ** 2) / (mean_control ** 4)
        - 2 * (difference_mean / (mean_control ** 3)) * covariance
    )
    relative_distribution = stats.norm(loc=relative_mu, scale=np.sqrt(relative_var))
    left_bound, right_bound = relative_distribution.ppf([alpha / 2, 1 - alpha / 2])

    ci_length = (right_bound - left_bound)
    pvalue = 2 * min(relative_distribution.cdf(0), relative_distribution.sf(0))
    effect = relative_mu

    return {
        'test': 'delta_method_ratio',
        'observed_diff': effect,
        'ci_lower': left_bound,
        'ci_upper': right_bound,
        'ci': (left_bound, right_bound),
        'p_value': pvalue,
        'p_value_corrected': None,
        'significant': not (left_bound <= 0 <= right_bound)
    }

def perform_stat_test(data, metric_type='mean', test_type=None, equal_var=True, n_bootstrap=1000, alpha=0.05):
    groups = data['group'].unique()
    comparisons = {}

    group_data = {g: data[data['group'] == g]['metric'].values for g in groups}

    if metric_type == 'ratio':
        for g1, g2 in combinations(groups, 2):
            if g1 > g2:
                g1, g2 = g2, g1
            control = group_data[g1]
            test = group_data[g2]
            result = relative_ttest(control, test, alpha=alpha)
            comparisons[(g1, g2)] = result
        return comparisons

    if metric_type == 'mean':
        func = np.mean
    elif metric_type == 'median':
        func = np.median
    else:
        func = np.mean

    if test_type is None or test_type == 'auto':
        if metric_type == 'mean':
            normal_flags = [determine_distribution(vals)[0] for vals in group_data.values()]
            chosen_test = 't-test' if all(normal_flags) else 'mannwhitney'
        elif metric_type == 'conversion':
            all_binary = all(set(np.unique(vals)).issubset({0, 1}) for vals in group_data.values())
            chosen_test = 'z-test' if all_binary else 't-test'
        elif metric_type == 'median':
            chosen_test = 'bootstrap'
        else:
            chosen_test = 't-test'
    else:
        chosen_test = test_type

    for g1, g2 in combinations(groups, 2):
        if g1 > g2:
            g1, g2 = g2, g1
        x1 = group_data[g1]
        x2 = group_data[g2]
        mean1 = np.mean(x1)
        mean2 = np.mean(x2)
        diff = (mean2 - mean1) / mean1 if mean1 != 0 else np.nan

        if chosen_test == 't-test':
            stat_val, p = stats.ttest_ind(x1, x2, equal_var=equal_var)
            comparisons[(g1, g2)] = {
                'test': 't-test', 'statistic': stat_val, 'p_value': p,
                'observed_diff': diff, 'significant': p < alpha
            }
        elif chosen_test == 'mannwhitney':
            stat_val, p = stats.mannwhitneyu(x1, x2)
            comparisons[(g1, g2)] = {
                'test': 'mannwhitney', 'statistic': stat_val, 'p_value': p,
                'observed_diff': diff, 'significant': p < alpha
            }
        elif chosen_test == 'z-test':
            successes = [x1.sum(), x2.sum()]
            nobs = [len(x1), len(x2)]
            stat_val, p = proportions_ztest(successes, nobs)
            comparisons[(g1, g2)] = {
                'test': 'z-test', 'statistic': stat_val, 'p_value': p,
                'observed_diff': diff, 'significant': p < alpha
            }
        elif chosen_test == 'bootstrap':
            result = bootstrap_test(x1, x2, n_iter=n_bootstrap, func=func, alpha=alpha)
            result['observed_diff'] = diff
            comparisons[(g1, g2)] = result

    return comparisons

def adjust_multiple_comparisons(p_value_dict, alpha=0.05, method='bonferroni'):
    pairs = [pair for pair in p_value_dict if 'p_value' in p_value_dict[pair]]
    if len(pairs) <= 1:
        return p_value_dict
    raw_pvals = [p_value_dict[p]['p_value'] for p in pairs]
    reject, pvals_corr, _, _ = multipletests(raw_pvals, alpha=alpha, method=method)
    for i, pair in enumerate(pairs):
        p_value_dict[pair]['p_value_corrected'] = pvals_corr[i]
        p_value_dict[pair]['significant'] = reject[i]
    return p_value_dict

def stratified_test(data, strat_col, metric_col, metric_type='mean', test_method='auto',
                    n_bootstrap=1000, external_weights=None, alpha=0.05):
    data = data.copy()

    # Сначала получить веса
    if external_weights is None:
        external_weights = data[strat_col].value_counts(normalize=True).sort_index()
    else:
        external_weights = external_weights.sort_index()

    # Затем переименовать колонки
    data.rename(columns={strat_col: 'strat', metric_col: 'metric'}, inplace=True)
    groups = data['group'].unique()

    group_metrics = {}
    for g in groups:
        subset = data[data['group'] == g]
        strat_stats = subset.groupby('strat')['metric'].agg(['mean', 'var', 'count'])
        strat_stats['var'] = strat_stats['var'].fillna(0)
        common_strats = strat_stats.index.intersection(external_weights.index)
        if len(common_strats) == 0:
            raise ValueError("Нет общих страт между данными и внешними весами.")
        weights = external_weights.loc[common_strats]
        strat_stats = strat_stats.loc[common_strats]
        weighted_mean = (strat_stats['mean'] * weights).sum()
        weighted_var = (weights * strat_stats['var']).sum() / subset.shape[0]
        total_n = subset.shape[0]
        group_metrics[g] = {'weighted_mean': weighted_mean, 'weighted_var': weighted_var, 'n': total_n}

    if test_method == 'auto':
        normal_flags = []
        for g in groups:
            group_data = data[data['group'] == g]['metric']
            stat, p = stats.normaltest(group_data)
            normal_flags.append(p > alpha)
        all_normal = all(normal_flags)
        min_n = min(data[data['group'] == g].shape[0] for g in groups)
        if all_normal or min_n > 5000:
            chosen_method = 't-test'
            if not all_normal:
                print("⚠️ Предупреждение: выбраны ненормальные данные, но используется t-test из-за большого размера выборки")
        else:
            chosen_method = 'bootstrap'
    else:
        chosen_method = test_method

    comparisons = {}
    p_values = []
    pairs = []

    for g1, g2 in combinations(groups, 2):
        # всегда считаем как g2 - g1, относительная разница
        m1 = group_metrics[g1]['weighted_mean']
        m2 = group_metrics[g2]['weighted_mean']
        rel_diff = (m2 - m1) / m1 if m1 != 0 else np.nan
        result = {}

        if chosen_method == 't-test':
            se = np.sqrt(group_metrics[g1]['weighted_var'] / group_metrics[g1]['n'] +
                         group_metrics[g2]['weighted_var'] / group_metrics[g2]['n'])
            t_stat = rel_diff / (se / m1) if se != 0 else np.nan
            p_val = 2 * (1 - stats.norm.cdf(abs(t_stat))) if not np.isnan(t_stat) else np.nan
            result = {'test': 'strat_t-test', 't_stat': t_stat, 'p_value': p_val, 'observed_diff': rel_diff,
                      'mean1': m1, 'mean2': m2}
        elif chosen_method == 'bootstrap':
            boot_diffs = []
            for _ in range(n_bootstrap):
                boot_means = {}
                for g in [g1, g2]:
                    sub = data[data['group'] == g]
                    boot_strat_means = {}
                    for s, grp in sub.groupby('strat'):
                        vals = grp['metric'].values
                        if len(vals) > 0:
                            boot_sample = np.random.choice(vals, size=len(vals), replace=True)
                            boot_strat_means[s] = np.mean(boot_sample)
                    boot_strat_means = pd.Series(boot_strat_means)
                    common = boot_strat_means.index.intersection(external_weights.index)
                    boot_means[g] = (boot_strat_means.loc[common] * external_weights.loc[common]).sum() if len(common) > 0 else np.nan
                rel_boot = (boot_means[g2] - boot_means[g1]) / boot_means[g1] if boot_means[g1] != 0 else np.nan
                boot_diffs.append(rel_boot)
            boot_diffs = np.array(boot_diffs)
            ci_lower = np.percentile(boot_diffs, 100 * alpha / 2)
            ci_upper = np.percentile(boot_diffs, 100 * (1 - alpha / 2))
            is_significant = not (ci_lower <= 0 <= ci_upper)
            result = {
                'test': 'strat_bootstrap_CI',
                'observed_diff': rel_diff,
                'ci': (ci_lower, ci_upper),
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'significant': is_significant,
                'mean1': m1, 'mean2': m2
            }
        else:
            raise ValueError("Неизвестный метод теста для стратифицированного анализа")

        comparisons[(g1, g2)] = result
        pairs.append((g1, g2))
        if 'p_value' in result:
            p_values.append(result['p_value'])

    if (len(pairs) > 1) and (len(p_values) == len(pairs)):
        comparisons = adjust_multiple_comparisons(comparisons, alpha=alpha, method='bonferroni')

    return comparisons

def perform_cuped(data_exp, data_pre, user_col='user_id', group_col='group', metric_col='metric', min_corr=0.1):
    merged = data_exp.merge(
        data_pre[[user_col, group_col, metric_col]],
        on=[user_col, group_col],
        suffixes=('', '_pre')
    )
    adjusted_rows = []
    cuped_usage, correlations = {}, {}

    for group, group_data in merged.groupby(group_col):
        x_pre, x_exp = group_data[f'{metric_col}_pre'], group_data[metric_col]
        corr = np.corrcoef(x_pre, x_exp)[0, 1]
        correlations[group] = corr
        if abs(corr) >= min_corr:
            theta = np.cov(x_pre, x_exp)[0, 1] / np.var(x_pre)
            x_adj = x_exp - theta * (x_pre - np.mean(x_pre))
            cuped_usage[group] = True
        else:
            x_adj = x_exp
            cuped_usage[group] = False
        adj = group_data.copy()
        adj[metric_col] = x_adj
        adjusted_rows.append(adj.drop(columns=f'{metric_col}_pre'))

    return pd.concat(adjusted_rows), cuped_usage, correlations

def build_analysis_report(results_dict, original_data, metric_type='mean', alpha=0.05):
    group_summary = (
        original_data.groupby('group')['metric']
        .agg(['count', 'mean', 'median', 'std'])
        .rename(columns={'count': 'n_users'}).reset_index()
    )

    strat_used = 'stratified_test' in results_dict
    cuped_used = 'CUPED' in results_dict and isinstance(results_dict['CUPED'], dict)

    def is_multiple_comparisons_applied(results):
        if isinstance(results, dict):
            return any(
                isinstance(v, dict) and 'p_value_corrected' in v and v['p_value_corrected'] is not None
                for v in results.values()
            )
        return False

    mc_used = any(
        is_multiple_comparisons_applied(results_dict.get(key))
        for key in ['non_stratified_test', 'stratified_test']
    )

    flags = {
        'Stratification used': strat_used,
        'CUPED applied': cuped_used,
        'Multiple comparisons used': mc_used
    }

    pairwise_rows = []

    def extract_rows(results, label=None):
        if not isinstance(results, dict):
            return
        for (g1, g2), r in results.items():
            row = {
                'group_1': g1,
                'group_2': g2,
                'test': r.get('test'),
                'observed_diff': r.get('observed_diff') or r.get('diff'),
                'p_value': r.get('p_value'),
                'p_value_corrected': r.get('p_value_corrected'),
                'ci_lower': r.get('ci_lower'),
                'ci_upper': r.get('ci_upper'),
                'significant': r.get('significant') if 'significant' in r else (
                    (r.get('p_value_corrected') < alpha) if r.get('p_value_corrected') is not None else
                    (r.get('p_value') < alpha) if r.get('p_value') is not None else None
                )
            }
            if label:
                row['label'] = label
            pairwise_rows.append(row)

    extract_rows(results_dict.get('non_stratified_test'), label='non_stratified')
    extract_rows(results_dict.get('stratified_test'), label='stratified')
    if 'CUPED' in results_dict and isinstance(results_dict['CUPED'], dict):
        extract_rows(results_dict['CUPED'].get('non_stratified'), label='cuped_non_stratified')
        extract_rows(results_dict['CUPED'].get('stratified'), label='cuped_stratified')

    pairwise_df = pd.DataFrame(pairwise_rows)

    return {
        'group_summary': group_summary,
        'analysis_flags': flags,
        'pairwise_comparisons': pairwise_df,
        'original_data': original_data.copy()
    }

import plotly.graph_objects as go

def print_analysis_summary(report):
    """
    Выводит интерактивный отчет о результатах A/B теста, включая групповой summary, настройки анализа,
    результаты попарных сравнений и график распределения метрики.
    """
    if 'group_summary' not in report:
        print("Нет данных для отчета.")
        return

    group_summary = report['group_summary']

    print("📊 GROUP SUMMARY")
    display(report['group_summary'])

    print("\n📈 ANALYSIS SETTINGS")
    for k, v in report['analysis_flags'].items():
        print(f"{k:<30}: {v}")

    print("\n🧪 PAIRWISE COMPARISONS")
    display(report['pairwise_comparisons'])

    # ===== ГРАФИК РАСПРЕДЕЛЕНИЯ =====
    if 'original_data' in report:
        data = report['original_data']
        if 'group' in data.columns and 'metric' in data.columns:
            fig = go.Figure()
            groups = data['group'].unique()
            colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
            for i, group_val in enumerate(groups):
                group_data = data[data['group'] == group_val]['metric']
                fig.add_trace(go.Histogram(
                    x=group_data,
                    name=str(group_val),
                    opacity=0.6,
                    marker_color=colors[i % len(colors)],
                    nbinsx=50
                ))
            fig.update_layout(
                barmode='group',
                title='Распределение метрики по группам',
                xaxis_title='Значение метрики',
                yaxis_title='Количество пользователей',
                legend_title='Группа',
                template='plotly_white'
            )
            fig.show()

def run_ab_analysis(data, metric_type='mean',
                    stratification_column=None,
                    cleaning_method='none', alpha=0.05,
                    test_type=None, cuped_flag=True,
                    n_bootstrap=1000, external_weights=None,
                    mc_method='bonferroni'):

    """
    Если cleaning_method='auto', запускается перебор различных способов очистки
    (только для t-test и mannwhitney, без CUPED и стратификации)
    """
    result = {}
    data = data.copy()

    if cleaning_method == 'auto':
        if metric_type not in ['mean', 'median']:
            raise ValueError("cleaning_method='auto' работает только с metric_type='mean' или 'median'")
        if test_type == 'bootstrap':
            raise ValueError("cleaning_method='auto' не поддерживает bootstrap. Используйте 'ttest' или 'mannwhitney'")
        if stratification_column is not None:
            raise ValueError("cleaning_method='auto' не поддерживает стратификацию")
        if cuped_flag and 'metric_predperiod' in data.columns:
            raise ValueError("cleaning_method='auto' не совместим с CUPED")

        test_choice = test_type
        if test_choice is None or test_choice == 'auto':
            normal_flags = [determine_distribution(vals)[0] for vals in [data[data['group'] == g]['metric'] for g in data['group'].unique()]]
            test_choice = 't-test' if all(normal_flags) else 'mannwhitney'

        methods = [
            ('none', {}),
            ('percentile', {'lower': 0.01, 'upper': 0.99}),
            ('percentile', {'lower': 0.05, 'upper': 0.95}),
            ('iqr', {}),
            ('winsor', {'lower': 0.01, 'upper': 0.99}),
            ('winsor', {'lower': 0.05, 'upper': 0.95}),
            ('isolation_forest', {'contamination': 0.01}),
            ('isolation_forest', {'contamination': 0.05}),
            ('isolation_forest', {'contamination': 0.1}),
            ('dbscan', {'eps': 0.3, 'min_samples': 3}),
            ('dbscan', {'eps': 0.5, 'min_samples': 5}),
            ('dbscan', {'eps': 0.7, 'min_samples': 7}),
        ]

        best_p = 1.0
        best_result = None
        best_method = None
        cleaning_log = []

        for m, params in methods:
            try:
                temp_data = data.copy()
                temp_data['metric'] = clean_outliers(temp_data['metric'], method=m, **params)
                temp_data = temp_data.dropna(subset=['metric'])

                if temp_data['metric'].dropna().nunique() <= 1 or temp_data.shape[0] < 10:
                    raise ValueError("Too few valid observations after cleaning")

                r = perform_stat_test(temp_data, metric_type=metric_type, test_type=test_choice, alpha=alpha)

                for (g1, g2), v in r.items():
                    pval = v.get('p_value')
                    if pval is not None:
                        cleaning_log.append({
                            'method': m, 'params': params, 'test': test_choice,
                            'groups': f"{g1} vs {g2}", 'p_value': pval, 'error': None
                        })
                        if pval < best_p:
                            best_p = pval
                            best_result = r
                            best_method = (m, params)
            except Exception as e:
                cleaning_log.append({
                    'method': m, 'params': params, 'test': test_choice,
                    'groups': None, 'p_value': None, 'error': str(e)
                })
                continue

        if best_result is not None:
            result['non_stratified_test'] = best_result
            result['auto_selected_cleaning'] = best_method
            result['auto_cleaning_log'] = pd.DataFrame(cleaning_log)
            print(f"✅ Автоматически выбран метод очистки: {best_method[0]}, параметры: {best_method[1]}")
        else:
            raise RuntimeError("Не удалось найти ни одну подходящую конфигурацию очистки")

    else:
        if cleaning_method != 'none':
            data['metric'] = clean_outliers(data['metric'], method=cleaning_method)

        base_result = perform_stat_test(data, metric_type, test_type, n_bootstrap=n_bootstrap, alpha=alpha)
        if any('p_value' in r for r in base_result.values()) and len(data['group'].unique()) > 2:
            base_result = adjust_multiple_comparisons(base_result, alpha=alpha, method=mc_method)
        result['non_stratified_test'] = base_result

        if cuped_flag and 'metric_predperiod' in data.columns:
            data_exp = data[['user_id', 'group', 'metric']].copy()
            data_pre = data[['user_id', 'group', 'metric_predperiod']].copy().rename(columns={'metric_predperiod':'metric'})
            if 'user_id' in data.columns:
                data_cuped, cuped_usage, correlations = perform_cuped(data_exp, data_pre)
                cuped_result = perform_stat_test(data_cuped, metric_type, test_type, n_bootstrap=n_bootstrap, alpha=alpha)
                if any('p_value' in r for r in cuped_result.values()) and len(data_cuped['group'].unique()) > 2:
                    cuped_result = adjust_multiple_comparisons(cuped_result, alpha=alpha, method=mc_method)

                result['CUPED'] = {
                    'non_stratified': cuped_result,
                    'cuped_usage_by_group': cuped_usage,
                    'correlations': correlations
                }

    result['report'] = build_analysis_report(result, data, metric_type, alpha)
    print_analysis_summary(result['report'])
    return result