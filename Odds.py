
# Odds from Match A
odds_match_a = [12.00, 7.80, 9.20, 16.00, 40.00, 11.00, 6.20, 7.80, 14.00, 30.00,
                17.00, 11.00, 12.00, 22.00, 50.00, 45.00, 26.00, 30.00, 50.00, 101.00,
                101.00, 80.00, 100.00, 101.00, 101.00, 20.00]

# Odds from Match B
odds_match_b = [7.60, 11.00, 35.00, 101.00, 101.00, 4.50, 6.80, 20.00, 90.00, 101.00,
                5.20, 7.80, 23.00, 101.00, 101.00, 8.60, 13.00, 40.00, 101.00, 101.00,
                19.00, 30.00, 90.00, 101.00, 101.00, 21.00]

# Odds from Match C
odds_match_c = [34.8, 78.8, 45.9, 34.6, 67.8, 90.5, 45, 23, 56, 12, 34, 34, 78, 90, 34, 78, 78, 12, 78, 32, 38, 78, 22, 43, 21, 7.3]

# Define the target range
target_range = (276, 296)

# Explore all combinations
for odds_a in odds_match_a:
    for odds_b in odds_match_b:
        for odds_c in odds_match_c:
            product = odds_a * odds_b * odds_c
            if target_range[0] <= product <= target_range[1]:
                print(f"Match A Odds: {odds_a}, Match B Odds: {odds_b}, Match C Odds: {odds_c}, Product: {product}")
