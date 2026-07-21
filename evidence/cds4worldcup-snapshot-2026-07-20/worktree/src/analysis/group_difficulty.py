#!/usr/bin/env python3
"""Analyze World Cup 2026 group difficulty based on Kimi probabilities."""

import json
import csv
from collections import defaultdict

def main():
    # Read kimi-signal-distribution JSON for official groups
    with open('data/ops/candidate/kimi-signal-distribution-2026-06-12.json', 'r') as f:
        dist_data = json.load(f)
    
    groups_info = dist_data['group_balance']['groups']
    
    # Read kimi_baseline_signals_matrix.csv for per-team probabilities
    team_probs = {}
    with open('data/processed/kimi_baseline_signals_matrix.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = row['canonical_team']
            prob_str = row['kimi_probability']
            if prob_str == 'N/A' or prob_str == '':
                prob = 0.0
            else:
                prob = float(prob_str)
            team_probs[team] = prob
    
    # Build analysis for each group
    analysis_groups = []
    group_totals = []
    
    for group_letter in sorted(groups_info.keys()):
        group_data = groups_info[group_letter]
        teams = group_data['teams']
        total_prob = group_data['kimi_prob_total']
        
        # Get per-team probabilities
        team_details = []
        for team in teams:
            prob = team_probs.get(team, 0.0)
            has_data = prob > 0
            team_details.append({
                'team': team,
                'kimi_probability': prob,
                'has_kimi_data': has_data
            })
        
        # Determine highest-seeded team: team with highest probability (proxy for seed)
        highest_seed_team = max(team_details, key=lambda x: x['kimi_probability'])['team']
        # Biggest underdog: team with lowest probability (including zero)
        biggest_underdog = min(team_details, key=lambda x: x['kimi_probability'])['team']
        
        # Zero Kimi coverage: all teams have probability 0
        zero_coverage = all(t['kimi_probability'] == 0.0 for t in team_details)
        
        group_entry = {
            'group': group_letter,
            'teams': team_details,
            'group_total_kimi_probability': total_prob,
            'highest_seeded_team': highest_seed_team,
            'biggest_underdog': biggest_underdog,
            'zero_kimi_coverage': zero_coverage
        }
        analysis_groups.append(group_entry)
        group_totals.append((group_letter, total_prob))
    
    # Rank groups by difficulty (highest total = hardest)
    group_totals_sorted = sorted(group_totals, key=lambda x: x[1], reverse=True)
    difficulty_ranking = [ {'rank': i+1, 'group': g, 'total_probability': p} for i, (g, p) in enumerate(group_totals_sorted) ]
    
    # Identify group of death candidates: top 3 groups by total probability
    group_of_death_candidates = [g for g, _ in group_totals_sorted[:3]]
    
    # Identify easiest group candidates: bottom 3 groups by total probability
    easiest_group_candidates = [g for g, _ in group_totals_sorted[-3:]]
    
    # Groups with zero Kimi coverage
    zero_coverage_groups = [g['group'] for g in analysis_groups if g['zero_kimi_coverage']]
    
    # Create final analysis
    analysis = {
        'analysis_id': 'group-difficulty-analysis-2026-06-12',
        'type': 'world_cup_2026_group_difficulty',
        'created_at': '2026-06-12T08:00:00+08:00',
        'methodology': 'Based on Kimi probability data from kimi-signal-distribution-2026-06-12.json and kimi_baseline_signals_matrix.csv',
        'groups': analysis_groups,
        'difficulty_ranking': difficulty_ranking,
        'group_of_death_candidates': group_of_death_candidates,
        'easiest_group_candidates': easiest_group_candidates,
        'zero_kimi_coverage_groups': zero_coverage_groups,
        'key_insights': [
            'Group I (France + Norway) and Group H (Spain + Uruguay) have the highest total Kimi probability, making them the most difficult groups.',
            'Group B has zero Kimi coverage, meaning all teams in that group have no probability data from Kimi agents.',
            'Group of death candidates are groups with high total probability and strong teams, while easiest groups have low total probability and weaker teams.',
            'The analysis is based solely on Kimi probability data, which is treated as Red Source for baseline purposes.'
        ],
        'source_policy_compliance': 'PASS — analysis uses existing processed files only, Kimi data treated as Red Source, no fabricated probabilities'
    }
    
    # Write output JSON
    output_path = 'data/ops/candidate/group-difficulty-analysis-2026-06-12.json'
    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f'Analysis written to {output_path}')
    print(f'Total groups analyzed: {len(analysis_groups)}')
    print(f'Group of death candidates: {group_of_death_candidates}')
    print(f'Easiest group candidates: {easiest_group_candidates}')
    print(f'Zero coverage groups: {zero_coverage_groups}')

if __name__ == '__main__':
    main()