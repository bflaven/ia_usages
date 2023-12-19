# Define the fractions of members in different age categories
minor_members = 0.75
adult_members = 0.33
elderly_members = 0.00

# Calculate the fraction of elderly members over 25 years old
elderly_over_25 = elderly_members / adult_members * 100

# Check if one in six members is between 18 and 25 years old
sixth = 1 / 6
between_18_and_25 = (minor_members - 0.33) / 0.75 * sixth

# Print the result
if between_18_and_25 > 0:
    print("Yes, one in six members is between 18 and 25 years old.")
else:
    print("No, we cannot say that one in six members is between 18 and 25 years old.")